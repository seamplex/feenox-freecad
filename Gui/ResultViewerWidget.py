from PySide2 import QtWidgets
import vtk
from Runner.FieldVisualizer import apply_field_visualization

class ResultViewerWidget(QtWidgets.QWidget):
    def __init__(self, result_file, problem_type, parent=None):
        super().__init__(parent)
        self.result_file = result_file
        self.problem_type = problem_type
        self.fields = []
        self.init_ui()
        self.parse_fields()

    def init_ui(self):
        layout = QtWidgets.QVBoxLayout()

        self.field_list = QtWidgets.QListWidget()
        layout.addWidget(QtWidgets.QLabel("Available Result Fields:"))
        layout.addWidget(self.field_list)

        show_btn = QtWidgets.QPushButton("Show Selected Field")
        show_btn.clicked.connect(self.visualize_field)
        layout.addWidget(show_btn)

        self.setLayout(layout)

    def parse_fields(self):
        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(self.result_file)
        reader.Update()

        data = reader.GetOutput()
        point_data = data.GetPointData()

        for i in range(point_data.GetNumberOfArrays()):
            name = point_data.GetArrayName(i)
            self.fields.append(name)
            self.field_list.addItem(name)

    def visualize_field(self):
        selected = self.field_list.currentItem()
        if selected:
            field_name = selected.text()
            apply_field_visualization(self.result_file, field_name, self.problem_type)
