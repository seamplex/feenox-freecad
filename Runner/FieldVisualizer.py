import FreeCAD, Mesh

def apply_field_visualization(result_file, field_name, problem_type):
    doc = FreeCAD.ActiveDocument
    result_obj = doc.addObject("Mesh::Feature", f"Result_{field_name}")
    result_obj.Mesh = Mesh.Mesh(result_file)
    result_obj.ViewObject.DisplayMode = "Flat Lines"
    result_obj.ViewObject.ShapeColor = (0.8, 0.8, 0.2)

    try:
        result_obj.ViewObject.setColorByScalar(field_name)
        print(f"Visualized field: {field_name}")
    except Exception as e:
        print(f"Could not apply field visualization: {e}")
