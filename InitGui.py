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
    # Icon = "feenox/Resources/icons/feenox.svg"
    Icon = FreeCAD.getUserAppDataDir()+ "Mod/feenox/Resources/icons/feenox.svg"

    def Initialize(self):
        import Gui.CommandFeenoXEditAnalysis
        FreeCADGui.addCommand("FeenoX_Edit_Analysis", Gui.CommandFeenoXEditAnalysis.CommandFeenoXEditAnalysis())

        self.appendToolbar("FeenoX Tools", ["FeenoX_Edit_Analysis"])
        self.appendMenu("FeenoX", ["FeenoX_Edit_Analysis"])
        
    def Initialize(self):
        import Gui.CommandFeenoXEditAnalysis
        import Gui.CommandFeenoXNewAnalysis

        FreeCADGui.addCommand("FeenoX_Edit_Analysis", Gui.CommandFeenoXEditAnalysis.CommandFeenoXEditAnalysis())
        FreeCADGui.addCommand("FeenoX_New_Analysis", Gui.CommandFeenoXNewAnalysis.CommandFeenoXNewAnalysis())

        self.appendToolbar("FeenoX Tools", ["FeenoX_New_Analysis", "FeenoX_Edit_Analysis"])
        self.appendMenu("FeenoX", ["FeenoX_New_Analysis", "FeenoX_Edit_Analysis"])
        

    def GetClassName(self):
        return "Gui::PythonWorkbench"

FreeCADGui.addWorkbench(FeenoXWorkbench())
