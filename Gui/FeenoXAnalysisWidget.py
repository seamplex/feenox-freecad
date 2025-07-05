from PySide2 import QtWidgets
from FeenoXBoundaryCondition import FeenoXBoundaryCondition
from Gui.BCEditorWidget import BCEditorWidget
from Gui.ResultViewerWidget import ResultViewerWidget
from MeshTools.GeoWriter import write_gmsh_geo
import FreeCAD, Mesh, os, subprocess
import FreeCADGui

class FaceSelectionObserver:
    def __init__(self, bc_obj, widget):
        self.bc = bc_obj
        self.widget = widget

    def addSelection(self, doc, obj_name, sub_name, pos):
        obj = FreeCADGui.getDocument(doc).getObject(obj_name)
        if "Face" in sub_name:
            self.bc.add_face(obj.Object, sub_name)
            self.widget.face_list.addItem(f"{obj.Object.Name}.{sub_name}")
            self.widget.update_preview()

class FeenoXAnalysisTaskPanel:
    def __init__(self, analysis_obj):
        from PySide2.QtWidgets import QWidget, QVBoxLayout
        self.widget = FeenoXAnalysisWidget(analysis_obj)
        self.form = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        self.form.setLayout(layout)

    def getStandardButtons(self):
        from PySide2.QtWidgets import QDialogButtonBox
        return QDialogButtonBox.Ok | QDialogButtonBox.Cancel

    def accept(self):
        return True

    def reject(self):
        return True


class FeenoXAnalysisWidget(QtWidgets.QWidget):
    def __init__(self, analysis_obj, parent=None):
        super().__init__(parent)
        self.analysis = analysis_obj
        self.bc_widgets = []
        self.init_ui()
        self.active_observer = None
        self.active_bc_widget = None

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        self.problem_combo = QtWidgets.QComboBox()
        self.problem_combo.addItems(["mechanical", "thermal", "fluid"])
        self.problem_combo.setCurrentText(self.analysis.problem_type)
        self.problem_combo.currentTextChanged.connect(self.update_problem_type)

        layout.addWidget(QtWidgets.QLabel("Problem Type:"))
        layout.addWidget(self.problem_combo)

        self.bc_container = QtWidgets.QVBoxLayout()
        self.bc_group_box = QtWidgets.QGroupBox("Boundary Conditions")
        self.bc_group_box.setLayout(self.bc_container)
        layout.addWidget(self.bc_group_box)

        add_bc_btn = QtWidgets.QPushButton("Add Boundary Condition")
        add_bc_btn.clicked.connect(self.add_bc_widget)
        layout.addWidget(add_bc_btn)

        update_btn = QtWidgets.QPushButton("Update Preview")
        update_btn.clicked.connect(self.update_preview)
        layout.addWidget(update_btn)

        self.preview_box = QtWidgets.QPlainTextEdit()
        self.preview_box.setReadOnly(True)
        layout.addWidget(QtWidgets.QLabel("FeenoX .fee Preview:"))
        layout.addWidget(self.preview_box)

        create_mesh_btn = QtWidgets.QPushButton("Create Mesh")
        create_mesh_btn.clicked.connect(self.create_mesh)
        layout.addWidget(create_mesh_btn)

        solve_btn = QtWidgets.QPushButton("Solve with FeenoX")
        solve_btn.clicked.connect(self.solve_feenox)
        layout.addWidget(solve_btn)

        self.result_viewer_group = QtWidgets.QGroupBox("Postprocessing: View Results")
        self.result_viewer = ResultViewerWidget("result.vtu", self.analysis.problem_type)
        viewer_layout = QtWidgets.QVBoxLayout()
        viewer_layout.addWidget(self.result_viewer)
        self.result_viewer_group.setLayout(viewer_layout)
        layout.addWidget(self.result_viewer_group)

        self.setLayout(layout)

    def update_problem_type(self, new_type):
        self.analysis.problem_type = new_type
        self.update_preview()

    # def add_bc_widget(self):
    #     bc = FeenoXBoundaryCondition(name=f"BC{len(self.analysis.boundary_conditions)+1}")
    #     self.analysis.add_boundary_condition(bc)
    #     widget = BCEditorWidget(bc)
    #     self.bc_widgets.append(widget)
    #     self.bc_container.addWidget(widget)
    #     self.update_preview()
    
    # def add_bc_widget(self):
    #     bc = FeenoXBoundaryCondition(name=f"BC{len(self.analysis.boundary_conditions)+1}")
    #     self.analysis.add_boundary_condition(bc)
    #     widget = BCEditorWidget(bc)
    #     observer = FaceSelectionObserver(bc, widget)
    #     FreeCADGui.Selection.addObserver(observer)
    # 
    #     self.bc_widgets.append(widget)
    #     self.bc_container.addWidget(widget)
    #     self.update_preview()
    
    def add_bc_widget(self):
        bc = FeenoXBoundaryCondition(name=f"BC{len(self.analysis.boundary_conditions)+1}")
        self.analysis.add_boundary_condition(bc)
        widget = BCEditorWidget(bc)
        self.bc_widgets.append(widget)
        self.bc_container.addWidget(widget)
    
        # Remove previous observer
        if self.active_observer:
            FreeCADGui.Selection.removeObserver(self.active_observer)
    
        # Attach observer only to newly added widget
        self.active_observer = FaceSelectionObserver(bc, widget)
        FreeCADGui.Selection.addObserver(self.active_observer)
        self.active_bc_widget = widget
    
        self.update_preview()
    
    

    def update_preview(self):
        fee_text = self.analysis.write_fee_file()
        self.preview_box.setPlainText(fee_text)

    def create_mesh(self):
        cad_objs = set()
        for bc in self.analysis.boundary_conditions:
            for obj, _ in bc.face_refs:
                cad_objs.add(obj)

        for obj in cad_objs:
            brep_filename = f"{obj.Name}.brep"
            obj.Shape.exportBrep(brep_filename)

        write_gmsh_geo(self.analysis, "mesh.geo")

        try:
            subprocess.run(["gmsh", "mesh.geo", "-3", "-format", "vtk", "-o", "mesh.vtk"], check=True)
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(None, "Gmsh Error", str(e))
            return

        try:
            mesh_obj = FreeCAD.ActiveDocument.addObject("Mesh::Feature", "FeenoX_Mesh")
            mesh_obj.Mesh = Mesh.Mesh("mesh.vtk")
            mesh_obj.ViewObject.DisplayMode = "Flat Lines"
            mesh_obj.ViewObject.ShapeColor = (0.0, 0.6, 1.0)
            FreeCAD.Gui.ActiveDocument.ActiveView.fitAll()
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Mesh Import Error", str(e))

    def solve_feenox(self):
        try:
            fee_text = self.analysis.write_fee_file()
            with open("input.fee", "w") as fee_file:
                fee_file.write(fee_text)

            result = subprocess.run(["feenox", "input.fee"], capture_output=True, text=True)
            if result.returncode != 0:
                QtWidgets.QMessageBox.critical(None, "FeenoX Error", result.stderr)
                return

            result_file = "result.vtu"
            if os.path.exists(result_file):
                mesh_obj = FreeCAD.ActiveDocument.addObject("Mesh::Feature", "FeenoX_Result")
                mesh_obj.Mesh = Mesh.Mesh(result_file)
                mesh_obj.ViewObject.DisplayMode = "Flat Lines"
                mesh_obj.ViewObject.ShapeColor = (0.0, 0.8, 0.3)
                FreeCAD.Gui.ActiveDocument.ActiveView.fitAll()
                self.result_viewer = ResultViewerWidget(result_file, self.analysis.problem_type)
                self.result_viewer_group.layout().addWidget(self.result_viewer)
            else:
                QtWidgets.QMessageBox.warning(None, "No Result File", f"{result_file} not found.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Solve Error", str(e))
