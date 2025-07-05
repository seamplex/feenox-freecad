import FreeCAD, FreeCADGui

class ViewProviderFeenoXAnalysis:
    def __init__(self, obj):
        obj.ViewObject.Proxy = self

    def doubleClicked(self, obj):
        from Gui.FeenoXAnalysisWidget import FeenoXAnalysisTaskPanel
        FreeCADGui.Control.showDialog(FeenoXAnalysisTaskPanel(obj.Object.Proxy))
        return True
