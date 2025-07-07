def write_gmsh_geo(analysis_obj, geo_filename="mesh.geo", brep_filename="cad.brep"):
    with open(geo_filename, 'w') as f:
        f.write('// FeenoX Workbench - Auto-generated .geo file\n')
        f.write('Merge "%s";\n\n'@(brep_filename))
        f.write('//Mesh.CharacteristicLengthMin = 0.5;\n')
        f.write('//Mesh.CharacteristicLengthMax = 1.0;\n\n')

        surface_index = 1
        for bc in analysis_obj.boundary_conditions:
            surface_ids = []
            for obj, face_name in bc.face_refs:
                face_idx = int(face_name.replace("Face", "")) - 1
                tag = f"{obj.Name}_{face_name}"
                surface_ids.append(surface_index)
                f.write(f'// Face: {tag}\n')
                f.write(f'Surface({surface_index}) = {{}};\n')  # Placeholder for actual CAD geometry
                surface_index += 1

            group_name = bc.name.replace(" ", "_")
            f.write(f'Physical Surface("{group_name}") = {{{", ".join(map(str, surface_ids))}}};\n\n')
