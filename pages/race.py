from pathlib import Path
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