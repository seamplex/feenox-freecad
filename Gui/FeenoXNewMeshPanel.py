from PySide2 import QtWidgets
import FreeCAD, os, subprocess, Mesh


class FeenoXNewMeshPanel(QtWidgets.QWidget):
    def __init__(self, solid_obj):
        super().__init__()
        self.solid_obj = solid_obj
        self.brep_exported = False
        self.init_ui()

    def export_brep(self):
        brep_filename = f"{self.solid_obj.Name}.brep"
        self.solid_obj.Shape.exportBrep(brep_filename)
        QtWidgets.QMessageBox.information(None, "Export", f"BREP exported as {brep_filename}")

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        self.geo_edit = QtWidgets.QPlainTextEdit()
        self.geo_edit.setPlaceholderText("// Custom Gmsh .geo commands here")
        layout.addWidget(QtWidgets.QLabel("Custom Gmsh .geo commands:"))
        layout.addWidget(self.geo_edit)

        self.export_btn = QtWidgets.QPushButton("Export CAD as BREP")
        self.export_btn.clicked.connect(self.export_brep)
        layout.addWidget(self.export_btn)

        self.mesh_btn = QtWidgets.QPushButton("Generate Mesh")
        self.mesh_btn.clicked.connect(self.generate_mesh)
        layout.addWidget(self.mesh_btn)

        self.close_btn = QtWidgets.QPushButton("Close")
        self.close_btn.clicked.connect(self.close_panel)
        layout.addWidget(self.close_btn)

        self.setLayout(layout)

    def export_brep(self):
        # Get the main geometry object from the analysis.
        obj = getattr(self.analysis, "geometry_object", None)
        if obj is None:
            QtWidgets.QMessageBox.warning(None, "Export", "No geometry object found in analysis.")
            return
        brep_filename = f"{obj.Name}.brep"
        obj.Shape.exportBrep(brep_filename)
        QtWidgets.QMessageBox.information(None, "Export", f"BREP exported as {brep_filename}")
        self.brep_exported = True

    def generate_mesh(self):
        if not self.brep_exported:
            self.export_brep()

        # Write .geo file
        geo_content = ""
        obj = getattr(self.analysis, "geometry_object", None)
        if obj is None:
            QtWidgets.QMessageBox.warning(None, "Export", "No geometry object found in analysis.")
            return
        brep_filename = f"{obj.Name}.brep"

        geo_content += f"Merge '{brep_filename}.brep';\n"
        geo_content += "// Physical groups (simple one-to-one, placeholder)\n"
        geo_content += "// TODO: Assign physicals for each entity as needed\n"
        geo_content += "\n// --- User custom geo ---\n"
        geo_content += self.geo_edit.toPlainText()

        with open("mesh.geo", "w") as f:
            f.write(geo_content)

        mesh_name = self.get_next_mesh_name()
        mesh_vtk = f"{mesh_name}.vtk"

        try:
            subprocess.run(["gmsh", "mesh.geo", "-3", "-format", "vtk", "-o", mesh_vtk], check=True)
        except subprocess.CalledProcessError as e:
            QtWidgets.QMessageBox.critical(None, "Gmsh Error", str(e))
            return

        try:
            mesh_obj = FreeCAD.ActiveDocument.addObject("Mesh::Feature", mesh_name)
            mesh_obj.Mesh = Mesh.Mesh(mesh_vtk)
            mesh_obj.ViewObject.DisplayMode = "Flat Lines"
            mesh_obj.ViewObject.ShapeColor = (0.0, 0.6, 1.0)
            FreeCAD.Gui.ActiveDocument.ActiveView.fitAll()
            QtWidgets.QMessageBox.information(None, "Mesh", f"Mesh '{mesh_name}' created and shown.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "Mesh Import Error", str(e))

    def get_next_mesh_name(self):
        base = "FeenoX_Mesh"
        index = 1
        doc = FreeCAD.ActiveDocument
        existing = [o.Name for o in doc.Objects]
        while f"{base}{index:03d}" in existing:
            index += 1
        return f"{base}{index:03d}"

    def close_panel(self):
        import FreeCADGui
        FreeCADGui.Control.closeDialog()
