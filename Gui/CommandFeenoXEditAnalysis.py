import FreeCADGui
from FeenoXAnalysis import FeenoXAnalysis
from Gui.FeenoXAnalysisWidget import FeenoXAnalysisWidget
from Gui.FeenoXAnalysisWidget import FeenoXAnalysisTaskPanel
from PySide2 import QtWidgets

class CommandFeenoXEditAnalysis:
    def GetResources(self):
        return {'MenuText': "Edit FeenoX Analysis",
                'ToolTip': "Edit problem type and boundary conditions",
                'Pixmap': "feenox/Resources/icons/feenox.svg"}

    def Activated(self):
        sel = FreeCADGui.Selection.getSelection()
        if sel and hasattr(sel[0], "Proxy") and isinstance(sel[0].Proxy, FeenoXAnalysis):
            # widget = FeenoXAnalysisWidget(sel[0].Proxy)
            # FreeCADGui.Control.showDialog(widget)
            # widget = FeenoXAnalysisTaskPanel(sel[0].Proxy)
            # FreeCADGui.Control.showDialog(widget)            
            from Gui.FeenoXAnalysisWidget import FeenoXAnalysisTaskPanel
            panel = FeenoXAnalysisTaskPanel(sel[0].Proxy)
            FreeCADGui.Control.showDialog(panel)            
        else:
            from PySide2 import QtWidgets
            QtWidgets.QMessageBox.warning(None, "FeenoX", "Select a FeenoXAnalysis object to edit.")


    def IsActive(self):
        return True
