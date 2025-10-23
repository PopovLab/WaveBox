import pandas as pd
from matplotlib import pyplot as plt
from pathlib import Path

def render_pabs_axis(task_path: Path, axis):
    file = task_path.joinpath('pabs(psi).dat')
    if file.exists():
        df = pd.read_table(file, header=None, names=['psi','dV','Pabs', 'PabsLD','PabsTT','PabsMX'], sep='\\s+' )
        axis.plot(df['psi'], df['Pabs'])

def render_Pabs(task_path: Path, title):
    fig, ax = plt.subplots()
    fig.suptitle(title)
    render_pabs_axis(task_path, ax)
    #ax.legend()
    ax.set_xlabel('psi')
    ax.set_ylabel('Pabs');
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
    fig.suptitle(title)
    pcm = render_eflda_axis(task_path, ax)
    fig.colorbar(pcm, ax=ax, extend='max') #, label='eflda'
    return fig

def make_eflda_pabs_fig(task_path, title):
    fig, axs = plt.subplots(1,2,  figsize=(12, 5))
    fig.suptitle(title)
    pcm = render_eflda_axis(task_path, axs[0])
    fig.colorbar(pcm, ax=axs[0]) #, label='eflda'
    render_pabs_axis(task_path, axs[1])
    return fig