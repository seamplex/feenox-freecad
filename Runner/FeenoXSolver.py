import subprocess

def run_feenox(input_file="input.fee"):
    result = subprocess.run(["feenox", input_file], capture_output=True, text=True)
    return result
