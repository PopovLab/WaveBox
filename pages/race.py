from pathlib import Path
import configparser
import tomllib
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
            self.read_input_file()                
            self.read_system_info()
        else:
            self.info_text = '**Select race folder**'  

    def read_system_info(self):
        file = self.result_path / 'system_info.ini'
        if file.exists():
            sys_info = configparser.ConfigParser(inline_comment_prefixes=('#',))
            sys_info.read(file)
            si = sys_info['system_info']
            self.sys_info = f"Host: {si['host']} OS: {si['system']}<br>CPU: {si['processor']}"
        else:
            self.sys_info = "**Can't system_info.ini.**"    
            self.is_good = False

    def read_input_file(self):
        file = self.result_path / 'input.toml'
        if file.exists():
            with open(file, "rb") as f:
                self.params = tomllib.load(f)
            self.title = f"Name: {self.params['work']['name']}"
            self.description = self.params['work']['description'] 
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
            self.done_tasks = [tsk['task_name'] for tsk in self.tasks_collection]

    def read_exe_time(self):
        f = self.result_path.joinpath('execution_time.txt')
        if f.exists():
            with self.result_path.joinpath('execution_time.txt').open("r") as file:
                line = file.readline()
        else:
            line = 'none'
        self.exe_time = line


    def get_value(self, name):
        if 'w2grid' in self.params:
            if name in self.params['w2grid']:
                return f"{name}={self.params['w2grid'][name]}"
            else:
                return f"There is no {name}"
        else:
            return f"There is no w2grid"

    def get_plot_title(self, vars_list= None):
        if 'work' in self.params:
            name = self.params['work']['name']
        else:
            name = self.params['common']['name']
        #if type(name) is list: # fix for nml name = ['FT', -15]
        #    name = "".join([str(n) for n in name])
        title = [name]
        if vars_list:
            for var_name in vars_list:
                title.append(self.get_value(var_name))
        else:
            var_name = self.params['series']['var']
            title.append(self.get_value(var_name))
            
        return " ".join(title)        