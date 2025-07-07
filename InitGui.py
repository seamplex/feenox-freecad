# import FreeCADGui
# 
# class FeenoXWorkbench(FreeCADGui.Workbench):
#     def Initialize(self):
#         import Gui.CommandFeenoXEditAnalysis
#         FreeCADGui.addCommand("FeenoX_Edit_Analysis", Gui.CommandFeenoXEditAnalysis.CommandFeenoXEditAnalysis())
# 
#     def GetClassName(self):
#         return "Gui::PythonWorkbench"
# 
#     def Activated(self):
#         pass  # Optional: code that runs when activated
# 
#     def Deactivated(self):
#         pass  # Optional: cleanup when switching away
# 
# FreeCADGui.addWorkbench(FeenoXWorkbench())

# import FreeCADGui
# 
# class FeenoXWorkbench(FreeCADGui.Workbench):
#     def Initialize(self):
#         import Gui.CommandFeenoXEditAnalysis
#         FreeCADGui.addCommand("FeenoX_Edit_Analysis", Gui.CommandFeenoXEditAnalysis.CommandFeenoXEditAnalysis())
# 
#     def GetClassName(self):
#         return "Gui::PythonWorkbench"
# 
# FreeCADGui.addWorkbench(FeenoXWorkbench())

import FreeCADGui

class FeenoXWorkbench(FreeCADGui.Workbench):
    MenuText = "FeenoX"
    ToolTip = "Finite Element Workbench powered by FeenoX"
    Icon = FreeCAD.getUserAppDataDir()+ "Mod/feenox-freecad/Resources/icons/feenox.svg"

    def Initialize(self):
        import Gui.CommandFeenoXNewAnalysis
        import Gui.CommandFeenoXNewMesh

        FreeCADGui.addCommand("FeenoX_New_Analysis", Gui.CommandFeenoXNewAnalysis.CommandFeenoXNewAnalysis())
        FreeCADGui.addCommand("FeenoX_New_Mesh", Gui.CommandFeenoXNewMesh.CommandFeenoXNewMesh())

        self.appendToolbar("FeenoX Tools", ["FeenoX_New_Analysis", "FeenoX_New_Mesh"])
        self.appendMenu("FeenoX", ["FeenoX_New_Analysis", "FeenoX_New_Mesh"])

    def GetClassName(self):
        return "Gui::PythonWorkbench"

FreeCADGui.addWorkbench(FeenoXWorkbench())
