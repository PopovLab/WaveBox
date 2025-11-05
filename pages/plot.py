import pandas as pd
from matplotlib import pyplot as plt
from pathlib import Path

def render_pabs_axis(task_path: Path, axis):
    axis.set_xlabel('psi')
    axis.set_ylabel('Pabs')
    #axis.legend()
    file = task_path.joinpath('pabs(psi).dat')
    if file.exists():
        df = pd.read_table(file, header=None, names=['psi','dV','Pabs', 'PabsLD','PabsTT','PabsMX'], sep='\\s+' )
        axis.plot(df['psi'], df['Pabs'])

def render_Pabs(task_path: Path, title):
    fig, ax = plt.subplots()
    #fig.suptitle(title)
    render_pabs_axis(task_path, ax)
    return ax

def render_eflda_axis(task_path: Path, axis):
    axis.set_aspect('equal')
    axis.set_xlabel('R(cm)')
    axis.set_ylabel('Y(cm)')
    cmhot = plt.get_cmap("plasma")
    Eflda = task_path.joinpath('Eflda.dat')
    if Path(Eflda).exists():
        df = pd.read_table(Eflda, header=None, names=['X','Y','eflda'], sep='\\s+')
        return axis.tripcolor(df['X'], df['Y'], df['eflda'], cmap="plasma", shading='flat')
    else:
        return axis.tripcolor([1, 1, -1, -1], [1, -1, 1, -1], [0, 1, 2, 3], cmap="plasma", shading='flat')
    

def render_eflda_fig(task_path: Path):
    fig, ax = plt.subplots()
    #fig.suptitle(title)
    pcm = render_eflda_axis(task_path, ax)
    fig.colorbar(pcm, ax=ax) #, label='eflda'
    return fig

import configparser
import f90nml
def make_title(task_path: Path, vars_list: list):
    try:
        params = f90nml.read(task_path.joinpath('input.nml'))
        title = get_title(params, vars_list)
    except:
        title = "I can't read the parameters for the task."
    return title

def make_eflda_pabs_fig(task_path: Path, show_vars: list):
    fig, axs = plt.subplots(1,2,  figsize=(12, 5))
    titile = make_title(task_path, show_vars)
    fig.suptitle(titile)
    pcm = render_eflda_axis(task_path, axs[0])
    fig.colorbar(pcm, ax=axs[0]) #, label='eflda'
    render_pabs_axis(task_path, axs[1])
    return fig

def get_param_value(params, name):
    value = find_key(params, name)
    if value:
        return value
    else:
        return f"There is no {name}"


def find_key(data, target_key):
    """
    Рекурсивно ищет ключ `target_key` в словаре `data` (включая вложенные разделы).
    Возвращает значение ключа, если он найден, или None, если не найден.
    """
    if isinstance(data, dict):
        # Если ключ есть в текущем уровне
        if target_key in data:
            return f"{target_key}={data[target_key]}"
        # Ищем в значениях-словарях и списках
        for key, value in data.items():
            result = find_key(value, target_key)
            if result is not None:
                return result
    else:
        return None
    
def get_title(params, vars_list= None):
    if 'work' in params:
        name = params['work']['name']
    else:
        name = params['common']['name']
    if type(name) is list: # fix for nml name = ['FT', -15]
        name = "".join([str(n) for n in name])
    title = [name]
    if vars_list:
        for var_name in vars_list:
            title.append(get_param_value(params, var_name))
    else:
        var_name = params['series']['var']
        title.append(get_param_value(params, var_name))
        
    return " ".join(title)


if __name__ == "__main__":
    task_path= Path("D:\\PopovLab\\Program_wave2D\\Results\\T-15\\2025-09-26_12-54-03\\Nr_271")
    #task_path= Path("D:\\PopovLab\\Program_wave2D\\Results\\FT-2_LH_freq\\2025-11-01_22-59-08\\freq_0.90000")
    params = f90nml.read(task_path.joinpath('input.nml'))
    print(params)
    print(params['w2grid'])
    print(get_title(params,  ['Nr', 'mmax', 'nphi1', 'freq']))