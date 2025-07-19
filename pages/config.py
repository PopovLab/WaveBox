import marimo as mo
def get_initial_path():
    data_file = mo.notebook_dir().parent / "data" / "initial_path.txt"
    if data_file.exists():
        with data_file.open("r") as file:
            init_path = file.read().strip()
            #print(f"init_path: {init_path}")
            return init_path
    else:
        #print("No init_path file found")
        return "No init_path file found"

def set_initial_path(init_path):
    data_file = mo.notebook_dir() / "data" / "initial_path.txt"
    with data_file.open("w") as file:
       file.write(init_path)