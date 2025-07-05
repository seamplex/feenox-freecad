class FeenoXAnalysis:
    def __init__(self, problem_type="mechanical"):
        self.problem_type = problem_type
        self.boundary_conditions = []

    def add_boundary_condition(self, bc):
        self.boundary_conditions.append(bc)

    def remove_boundary_condition(self, bc):
        if bc in self.boundary_conditions:
            self.boundary_conditions.remove(bc)

    def write_fee_file(self):
        blocks = [bc.write_fee_block() for bc in self.boundary_conditions]
        return "\n".join(blocks)
