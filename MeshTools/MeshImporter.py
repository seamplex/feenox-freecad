import FreeCAD, Mesh

def import_vtk_to_freecad(filename):
    doc = FreeCAD.ActiveDocument
    mesh_obj = doc.addObject("Mesh::Feature", "FeenoX_Mesh")
    mesh_obj.Mesh = Mesh.Mesh(filename)
    mesh_obj.ViewObject.DisplayMode = "Flat Lines"
    mesh_obj.ViewObject.ShapeColor = (0.0, 0.6, 1.0)
    FreeCAD.Gui.ActiveDocument.ActiveView.fitAll()
