from PySide2.QtWidgets import QWidget, QVBoxLayout
from Gui.FeenoXNewMeshPanel import FeenoXNewMeshPanel

class FeenoXNewMeshTaskPanel:
    def __init__(self, solid_obj):
        self.widget = FeenoXNewMeshPanel(solid_obj)
        self.form = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        self.form.setLayout(layout)

    def getStandardButtons(self):
        from PySide2.QtWidgets import QDialogButtonBox
        return QDialogButtonBox.Close

    def reject(self):
        return True
