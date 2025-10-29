from pathlib import Path
import configparser
class Race:
    """Непосредственно сам заезд-расчет"""

    def __init__(self, result_path: Path):
        self.is_good = False
        self.name = ''
        self.exe_time = ''
        self.tasks_collection = []
        self.result_path = result_path
        if result_path:
            self.name = result_path.name
            if (result_path/'done_tasks.txt').exists():
                self.read_tasks_collection()
                self.info_text = ", ".join([x['task_name'] for x in self.tasks_collection])
                self.read_exe_time()
                self.is_good = True
            else:
                self.info_text = "done_tasks not exists!"
        else:
            self.info_text = '**Select race folder**'  
        self.read_input_file()

    def read_input_file(self):
        file = self.result_path / 'input.toml'
        if file.exists():
            self.title = "**input.toml**"    
            self.description = " input.toml "      
        else:
            self.read_ini_params(self.result_path / 'input.par')



    def read_ini_params(self, file: Path):
        if file.exists():
            self.params = configparser.ConfigParser(inline_comment_prefixes=('#',))
            self.params.read(file)
            self.title = f"Name: {self.params['common']['name']}"
            self.description = self.params.get('common', 'description', fallback= 'none')
        else:
            self.title = "**Can't open input.par.**"    
            self.description = ""        
            self.is_good = False

    def read_tasks_collection(self):
        with self.result_path.joinpath('done_tasks.txt').open("r") as file:
                lines = [line.strip() for line in file.readlines()]
        for line in lines:
            x = line.split(',')
            task_name= x[0]
            item = dict(task_name= task_name)
            tmp = task_name.split('_')
            try:
                item[tmp[0]] = int(tmp[1]) # iterated var
            except ValueError as e:
                with mo.redirect_stdout():
                    print(f"Caught a ValueError: {e}")
                item[tmp[0]] = 'ValueError'
            if len(x)>1:
                item['exec_time']= x[1]
            self.tasks_collection.append(item)

    def read_exe_time(self):
        f = self.result_path.joinpath('execution_time.txt')
        if f.exists():
            with self.result_path.joinpath('execution_time.txt').open("r") as file:
                line = file.readline()
        else:
            line = 'none'
        self.exe_time = line