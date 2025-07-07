import FreeCAD
import FreeCADGui
from FeenoXAnalysis import FeenoXAnalysis
from Gui.FeenoXNewMeshTaskPanel import FeenoXNewMeshTaskPanel

class CommandFeenoXNewMesh:
    def GetResources(self):
        return {
            'MenuText': "New FeenoX Mesh",
            'ToolTip': "Create a new mesh using Gmsh for FeenoX",
            'Pixmap': "feenox/Resources/icons/mesh.svg"
        }

    def Activated(self):
        doc = FreeCAD.ActiveDocument
        if not doc:
            return

        # analysis = None
        # for obj in doc.Objects:
        #     if hasattr(obj, "Proxy") and isinstance(obj.Proxy, FeenoXAnalysis):
        #         analysis = obj.Proxy
        #         break
        # if not analysis:
        #     from PySide2 import QtWidgets
        #     QtWidgets.QMessageBox.warning(None, "No FeenoXAnalysis", "Create/select a FeenoXAnalysis first.")
        #     return

        doc = FreeCAD.ActiveDocument
        # Let the user select the object to mesh (or pick the active one)
        sel = FreeCADGui.Selection.getSelection()
        if not sel:
            QtWidgets.QMessageBox.warning(None, "No Selection", "Select a solid object to mesh.")
            return
        obj = sel[0]

        # FreeCADGui.Control.showDialog(FeenoXNewMeshTaskPanel(analysis))
        FreeCADGui.Control.showDialog(FeenoXNewMeshTaskPanel(obj))

    def IsActive(self):
        return bool(FreeCAD.ActiveDocument)
