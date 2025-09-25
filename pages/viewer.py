import marimo

__generated_with = "0.15.5"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import ui_elements
    ui_elements.nav_menu()
    return (mo,)


@app.cell
def _(mo):
    mo.md("""## Power absorbtion v2""")
    return


@app.cell
def _():
    import config as cfg
    return (cfg,)


@app.cell
def _(cfg, mo):
    folder_browser = mo.ui.file_browser(initial_path=cfg.get_initial_path(), 
                                        selection_mode='directory',
                                        label='Base folder',
                                        restrict_navigation= True,
                                        multiple= False)
    return (folder_browser,)


@app.function
def get_race_list(directory_path):
    path_list= [item for item in directory_path.iterdir() if item.is_dir()]            
    return [ {'name':p.name, 'path':p} for p in path_list]


@app.cell
def _(folder_browser, mo):
    race_table = mo.ui.table(data=get_race_list(folder_browser.path(index=0)), pagination=True, show_download = False, selection= 'single')
    race_table
    return (race_table,)


@app.cell
def _():
    #race_table.value[0]
    return


@app.cell
def _(folder_browser, mo):
    mo.sidebar([folder_browser])
    return


@app.function
def get_done_tasks(path):
    with path.joinpath('done_tasks.txt').open("r") as file:
            done_tasks = [line.strip() for line in file.readlines()]
    return done_tasks


@app.cell
def _(mo):
    get_hstate, set_hstate = mo.state('admonition')
    return get_hstate, set_hstate


@app.cell
def _(race_table, set_hstate):
    race_path = race_table.value[0]['path']
    if race_path:
        race_name = race_path.name
        if race_path.joinpath('done_tasks.txt').exists():
            done_tasks = get_done_tasks(race_path)
            info_text = ", ".join(done_tasks)
            set_hstate('admonition')
        else:
            info_text = "done_tasks not exists!"
            set_hstate('attention')
    else:
        info_text = '**Select race folder**'  
        race_name = ''
        set_hstate('attention')
    return done_tasks, info_text, race_name, race_path


@app.cell
def _(race_path, set_hstate):
    import configparser
    check_param= False
    if race_path:
        if race_path.joinpath('input.par').exists():
            check_param= True
            params = configparser.ConfigParser(inline_comment_prefixes=('#',))
            params.read(race_path.joinpath('input.par'))
            inp_text = f"Name: {params['common']['name']}"
        else:
            inp_text = "**Can't open input.par.**"
            set_hstate('attention')
    else:
            inp_text = "**Can't open input.par.**"
            set_hstate('attention')
    return configparser, inp_text, params


@app.cell
def _(configparser, race_path, set_hstate):
    if race_path:
        if race_path.joinpath('system_info.ini').exists():
            sys_info = configparser.ConfigParser(inline_comment_prefixes=('#',))
            sys_info.read(race_path.joinpath('system_info.ini'))
            si = sys_info['system_info']
            sys_text = f"Host: {si['host']} OS: {si['system']}<br>CPU: {si['processor']}"
        else:
            sys_text = "**Can't system_info.ini.**"    
            set_hstate('attention')
    else:
        sys_text = "**Can't system_info.ini.**"
        set_hstate('attention')
    return (sys_text,)


@app.cell
def _(get_hstate, info_text, inp_text, mo, race_name, sys_text):
    mo.md(
        f"""
    /// {get_hstate()} | Race: {race_name} {inp_text}
    Tasks: {info_text} <br>
    {sys_text}
    ///
    """
    )
    return


@app.function
def read_power_balance(path):
    pb = {}
    with path.joinpath('power_balance.dat').open("r") as file:
        content = [line.strip().split() for line in file.readlines()]
        for line in content:
            pb[line[0]] = float(line[2])
    return pb


@app.cell
def _(done_tasks, race_path):
    #mo.stop(get_hstate() == 'attention', mo.md("**Submit the form to continue.**"))
    tasks_data =[]
    for task in done_tasks:
        pb = read_power_balance(race_path.joinpath(task))
        pb['task'] = task
        tmp = task.split('_')
        pb[tmp[0]] = int(tmp[1])
        tasks_data.append(pb)
        #print(pb)
    return (tasks_data,)


@app.cell
def _(mo, tasks_data):
    #mo.stop(get_hstate() == 'attention', mo.md("**Submit the form to continue.**"))
    import pandas as pd
    df = pd.DataFrame.from_dict(tasks_data)
    table = mo.ui.table(data=df)
    return df, pd, table


@app.cell
def _():
    axis_style =  dict(showline=True, linewidth=1, linecolor='black', mirror=True, ticks='outside', gridcolor='grey')
    layout_style = dict(
        margin=dict(r=20, t=30, b=10),
        xaxis= axis_style,
        yaxis= axis_style,
        plot_bgcolor='white', paper_bgcolor='white',
        legend=dict(
            orientation="v",
            y=1.01,
            x=1.01
        ),
        title_font_size=16,
        title_x=0.5 # Center the title
    )
    return (layout_style,)


@app.cell
def _(df, layout_style, params):
    import plotly.express as px
    px_line = px.line(x=df[params['series']['var']], y=df['Pabs(kW)'], title="Pabs(kW)", markers=True)
    px_line.update_layout(layout_style)
    px_line.update_yaxes(title_text='Pabs(kW)')
    px_line.update_xaxes(title_text= params['series']['var']);
    return px, px_line


@app.cell
def _(mo):
    psi_min = mo.ui.number(start=0.0, stop=1.0, step =0.1, label="psi min")
    psi_max = mo.ui.number(start=0.0, stop=1.0, step =0.1, value=1.0, label="psi max")
    return psi_max, psi_min


@app.cell
def _(mo):
    log_checkbox = mo.ui.checkbox(label="log scale")
    return (log_checkbox,)


@app.cell
def _(log_checkbox, mo, psi_max, psi_min):
    plot_options = mo.vstack([log_checkbox, psi_min, psi_max])
    return


@app.cell
def _(done_tasks, mo):
    tasks = mo.ui.array([mo.ui.checkbox(label=task, value=True) for task in done_tasks], label="Task list")
    radio = mo.ui.radio(options=done_tasks, value=done_tasks[0])
    return radio, tasks


@app.cell
def _(params):
    #mo.stop(get_hstate() == 'attention', mo.md("**Submit the form to continue.**"))
    if params['series']['var'] == 'Nr':
        title = params['common']['name'] + ' Mmax=' + params['w2grid']['Mmax']
    else:
        title = params['common']['name'] +' Nr=' + params['w2grid']['Nr'] 
    return (title,)


@app.cell
def _(
    done_tasks,
    layout_style,
    log_checkbox,
    params,
    pd,
    px,
    race_path,
    tasks,
    title,
):
    pabs_collection = px.line(title= title, markers=True)
    for task1, tv in zip(done_tasks, tasks.value):
        if tv:
            pabs_psi = race_path.joinpath(task1).joinpath('pabs(psi).dat')
            df1 = pd.read_table(pabs_psi, header=None, names=['psi','dV','Pabs', 'PabsLD','PabsTT','PabsMX'], sep='\\s+' )
            pabs_collection.add_scatter(x=df1['psi'], y=df1['Pabs']/df1['dV'], name=task1)
    pabs_collection.update_layout(layout_style)
    if log_checkbox.value:
        pabs_collection.update_yaxes(type="log")
    pabs_collection.update_yaxes(title_text='Pabs(kW)')
    pabs_collection.update_xaxes(title_text= params['series']['var']);
    return (pabs_collection,)


@app.cell
def _(mo, tasks):
    tasks_stack = mo.hstack([tasks, tasks.value], justify="space-between")
    return


@app.cell
def _(mo, pd, race_path, title):
    from matplotlib import pyplot as plt
    def render_pabs_axis(task, axis):
        pabs_psi = race_path.joinpath(task).joinpath('pabs(psi).dat')
        df = pd.read_table(pabs_psi, header=None, names=['psi','dV','Pabs', 'PabsLD','PabsTT','PabsMX'], sep='\\s+' )
        return axis.plot(df['psi'], df['Pabs'], label=task)

    def render_Pabs(task):
        fig, ax = plt.subplots()
        fig.suptitle(title)
        if task:
            render_pabs_axis(task, ax)
        ax.legend()
        ax.set_xlabel('psi')
        ax.set_ylabel('Pabs');
        return mo.as_html(ax)
    return plt, render_Pabs


@app.cell
def _(mo, pd, plt, race_path, title):
    from pathlib import Path
    def render_eflda_axis(task_path, axis):
        cmhot = plt.get_cmap("plasma")
        Eflda = task_path.joinpath('Eflda.dat')
        if Path(Eflda).exists():
            df = pd.read_table(Eflda, header=None, names=['X','Y','eflda'], sep='\\s+')
            return axis.tripcolor(df['X'], df['Y'], df['eflda'], cmap="plasma", shading='flat')
        else:
            return axis.tripcolor([1, 1, -1, -1], [1, -1, 1, -1], [0, 1, 2, 3], cmap="plasma", shading='flat')

    def render_eflda(task):
        if not task:
            return mo.md(text='No selected task')
        task_path  =  Path(race_path).joinpath(task)
        eflda_plot = task_path.joinpath('eflda_plot.png')
        if not Path(eflda_plot).exists():
            fig, ax = plt.subplots()
            fig.suptitle(title)
            pcm = render_eflda_axis(task_path, ax)
            fig.colorbar(pcm, ax=ax, extend='max', label='eflda')
            #ax.legend()
            ax.set_aspect('equal')
            ax.set_xlabel('X')
            ax.set_ylabel('Y');
            # Save the plot to a file
            fig.savefig(eflda_plot, dpi=300, bbox_inches='tight', transparent=False)
        #return mo.as_html(ax)
        return mo.image(src= eflda_plot, alt= 'eflda', width=600,height=450)
    return (render_eflda,)


@app.cell
def _(mo, params):
    def create_view_item(item):
        return mo.md(f">{item[0]} = {item[1]}")

    def create_view_section(section):
        text = [f" {i[0]} = {i[1]}" for i in section]
        return mo.md('>'+'<br>'.join(text))

    #prams_ui ={f"**{s}**": mo.vstack([create_view_item(i) for i in params.items(s)]) for s in params.sections()}
    prams_ui ={f"**{s}**": create_view_section(params.items(s)) for s in params.sections()}
    return (prams_ui,)


@app.cell
def _(
    log_checkbox,
    mo,
    pabs_collection,
    prams_ui,
    px_line,
    radio,
    render_Pabs,
    render_eflda,
    table,
    tasks,
):
    mo.ui.tabs({
        "Pabs table": table,
        "Pabs": mo.ui.plotly(px_line),
        "Pabs(psi)": mo.hstack([mo.vstack([mo.ui.plotly(pabs_collection), log_checkbox]), tasks]),
        #'Params': mo.tree({s:dict(params.items(s)) for s in params.sections()}, label='input.par'),
        "Eflda": mo.hstack([ 
            mo.lazy(render_eflda(radio.value)),
            mo.lazy(render_Pabs(radio.value)), radio]),
        'Params': mo.accordion(prams_ui, multiple=True)

    })
    return


@app.cell
def _(done_tasks, mo):
    task_slider = mo.ui.slider(start=1, stop= len(done_tasks), label="Task", value=1)
    def get_task():
        return done_tasks[task_slider.value-1]
    return get_task, task_slider


@app.cell
def _(get_task, mo, render_Pabs, render_eflda, task_slider):

    mo.vstack([
        mo.hstack([task_slider,mo.md(f"Task - {get_task()}"), mo.ui.run_button(label="Clear", kind='warn')] ),
        mo.hstack([    
            mo.lazy(render_eflda(get_task())),
            mo.lazy(render_Pabs(get_task()))]),
   
    ])
    return


if __name__ == "__main__":
    app.run()
