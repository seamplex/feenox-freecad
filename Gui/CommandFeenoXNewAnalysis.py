import FreeCAD, FreeCADGui
from PySide2 import QtWidgets
from FeenoXAnalysis import FeenoXAnalysis
from Gui.FeenoXAnalysisWidget import FeenoXAnalysisWidget
import ViewProviderFeenoXAnalysis

class CommandFeenoXNewAnalysis:
    def GetResources(self):
        return {
            'MenuText': "New FeenoX Analysis",
            'ToolTip': "Create a new FeenoXAnalysis object",
            'Pixmap': "feenox/Resources/icons/feenox.svg"
        }

    def Activated(self):
        doc = FreeCAD.ActiveDocument
        if not doc:
            doc = FreeCAD.newDocument()

        obj = doc.addObject("App::FeaturePython", "FeenoXAnalysis")
        obj.Proxy = FeenoXAnalysis()
        ViewProviderFeenoXAnalysis.ViewProviderFeenoXAnalysis(obj)
            
        FreeCADGui.Selection.clearSelection()
        FreeCADGui.Selection.addSelection(obj)

        # 👇 Launch editor immediately
        widget = FeenoXAnalysisWidget(obj.Proxy)
        # FreeCADGui.Control.showDialog(widget)
        from Gui.FeenoXAnalysisWidget import FeenoXAnalysisTaskPanel
        # panel = FeenoXAnalysisTaskPanel(sel[0].Proxy)
        panel = FeenoXAnalysisTaskPanel(obj.Proxy)
        FreeCADGui.Control.showDialog(panel)        

    def IsActive(self):
        return True
