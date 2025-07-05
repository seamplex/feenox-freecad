class FeenoXBoundaryCondition:
    def __init__(self, name=None):
        self.name = name or "UnnamedBC"
        self.face_refs = []           # List of tuples like (obj, "Face12")
        self.problem_type = "mechanical"
        self.tokens = {}
        self.use_group_syntax = False

    def add_face(self, obj, face_name):
        if (obj, face_name) not in self.face_refs:
            self.face_refs.append((obj, face_name))

    def remove_face(self, obj, face_name):
        if (obj, face_name) in self.face_refs:
            self.face_refs.remove((obj, face_name))

    def set_token(self, property, expression):
        self.tokens[property] = expression

    def clear_tokens(self):
        self.tokens = {}

    def format_group_name(self):
        return "_".join([f"{obj.Name}_{face}" for obj, face in self.face_refs])

    def write_fee_block(self):
        group_line = ""
        if self.use_group_syntax:
            group_list = [self.format_group_name()]
            group_line = f"bc GROUPS {' '.join(group_list)} {{"
        else:
            group_line = f"bc {self.format_group_name()} {{"

        block = group_line + "\n"
        for prop, expr in self.tokens.items():
            block += f"  {prop} = {expr}\n"
        block += "}\n"
        return block
