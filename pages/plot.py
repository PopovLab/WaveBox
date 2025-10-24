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
    

def render_eflda_fig(task_path, title):
    fig, ax = plt.subplots()
    #fig.suptitle(title)
    pcm = render_eflda_axis(task_path, ax)
    fig.colorbar(pcm, ax=ax) #, label='eflda'
    return fig

def make_eflda_pabs_fig(task_path, title):
    fig, axs = plt.subplots(1,2,  figsize=(12, 5))
    fig.suptitle(title)
    pcm = render_eflda_axis(task_path, axs[0])
    fig.colorbar(pcm, ax=axs[0]) #, label='eflda'
    render_pabs_axis(task_path, axs[1])
    return fig

def get_param_value(params, name):
    if name in params['w2grid']:
        return f"{name}={params['w2grid'][name]}"
    else:
        return f"There is no {name}"
    
def get_title(params, vars_list= None):
    title = [params['common']['name']]
    if vars_list:
        for var_name in vars_list:
            title.append(get_param_value(params, var_name))
    else:
        var_name = params['series']['var']
        title.append(get_param_value(params, var_name))
        
    return " ".join(title)