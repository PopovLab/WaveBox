import pandas as pd
from matplotlib import pyplot as plt
from pathlib import Path

race_path = Path()

def render_pabs_axis(task, axis):
    pabs_psi = race_path.joinpath(task).joinpath('pabs(psi).dat')
    if pabs_psi.exists():
        df = pd.read_table(pabs_psi, header=None, names=['psi','dV','Pabs', 'PabsLD','PabsTT','PabsMX'], sep='\\s+' )
        axis.plot(df['psi'], df['Pabs'], label=task)

def render_Pabs(task, title):
    fig, ax = plt.subplots()
    fig.suptitle(title)
    if task:
        render_pabs_axis(task, ax)
    ax.legend()
    ax.set_xlabel('psi')
    ax.set_ylabel('Pabs');
    return ax

def render_eflda_axis(task_path, axis):
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
    #ax.legend()
    ax.set_aspect('equal')
    ax.set_xlabel('R(cm)')
    ax.set_ylabel('Y(cm)')
    # Save the plot to a file
    return fig
