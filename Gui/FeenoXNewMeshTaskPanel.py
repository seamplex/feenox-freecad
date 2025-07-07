from PySide2.QtWidgets import QWidget, QVBoxLayout
from Gui.FeenoXNewMeshPanel import FeenoXNewMeshPanel

class FeenoXNewMeshTaskPanel:
    def __init__(self, analysis_obj):
        self.widget = FeenoXNewMeshPanel(analysis_obj)
        self.form = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        self.form.setLayout(layout)

    def getStandardButtons(self):
        from PySide2.QtWidgets import QDialogButtonBox
        return QDialogButtonBox.Close

    def reject(self):
        return True