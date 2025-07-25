import marimo

__generated_with = "0.14.12"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import ui_elements
    ui_elements.nav_menu()
    return (mo,)


@app.cell
def _(mo):
    mo.md("""## Power absorbtion""")
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


@app.cell
def _(folder_browser, mo):
    race_browser = mo.ui.file_browser(initial_path=folder_browser.path(index=0),
                                      selection_mode='directory',
                                      label='Race folder',
                                      restrict_navigation= True,
                                      multiple= False)
    return (race_browser,)


@app.cell
def _(folder_browser, mo, race_browser):
    mo.sidebar([mo.vstack([folder_browser, race_browser])])
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
def _(race_browser, set_hstate):
    race_path = race_browser.path(index=0)
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
def _(df, params):
    #mo.stop(get_hstate() == 'attention', mo.md("**Submit the form to continue.**"))
    from matplotlib import pyplot as plt
    fig_pabs, ax_pabs = plt.subplots()
    fig_pabs.suptitle('Pabs')
    ax_pabs.plot(df[params['series']['var']], df['Pabs(kW)'] , label='Pabs(kW)')
    ax_pabs.set_xlabel(params['series']['var'])
    ax_pabs.set_ylabel('Pabs(kW)');
    #ax_pabs.set_legend()
    #fig_pabs.show()

    return ax_pabs, plt


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
    return (plot_options,)


@app.cell
def _(done_tasks, mo):
    tasks = mo.ui.array([mo.ui.checkbox(label=task, value=True) for task in done_tasks], label="Task list")
    radio = mo.ui.radio(options=done_tasks, value=done_tasks[0])
    return radio, tasks


@app.cell
def _(
    done_tasks,
    log_checkbox,
    params,
    pd,
    plt,
    psi_max,
    psi_min,
    race_path,
    tasks,
):
    #mo.stop(get_hstate() == 'attention', mo.md("**Submit the form to continue.**"))
    if params['series']['var'] == 'Nr':
        title = params['common']['name'] + ' Mmax=' + params['w2grid']['Mmax']
    else:
        title = params['common']['name'] +' Nr=' + params['w2grid']['Nr'] 
    def render_pabs_collection():
        fig, ax = plt.subplots()
        fig.suptitle(title)
        for task1, tv in zip(done_tasks, tasks.value):
            if tv:
                pabs_psi = race_path.joinpath(task1).joinpath('pabs(psi).dat')
                df1 = pd.read_table(pabs_psi, header=None, names=['psi','dV','Pabs', 'PabsLD','PabsTT','PabsMX'], sep='\\s+' )
                ax.plot(df1['psi'], df1['Pabs']/df1['dV'] , label=task1)
        ax.legend()
        ax.set_xlim([psi_min.value, psi_max.value])
        #ax.set_ylim([0, 0.000002])
        if log_checkbox.value:
            ax.set_yscale('log')
        ax.set_xlabel('psi')
        ax.set_ylabel('Pabs/dV');
        ax.autoscale(enable=True, axis='y', tight= True)
        return ax
    return render_pabs_collection, title


@app.cell
def _(mo, tasks):
    tasks_stack = mo.hstack([tasks, tasks.value], justify="space-between")
    return


@app.cell
def _(mo, pd, plt, race_path, radio, title):
    def render_pabs_axis(task, axis):
        pabs_psi = race_path.joinpath(task).joinpath('pabs(psi).dat')
        df = pd.read_table(pabs_psi, header=None, names=['psi','dV','Pabs', 'PabsLD','PabsTT','PabsMX'], sep='\\s+' )
        return axis.plot(df['psi'], df['Pabs'], label=task)

    def render_Pabs():
        fig, ax = plt.subplots()
        fig.suptitle(title)
        if radio.value:
            render_pabs_axis(radio.value, ax)
        ax.legend()
        ax.set_xlabel('psi')
        ax.set_ylabel('Pabs');
        return mo.as_html(ax)
    return render_Pabs, render_pabs_axis


@app.cell
def _(mo, pd, plt, race_path, radio, title):

    def render_eflda_axis(task, axis):
        cmhot = plt.get_cmap("plasma")
        Eflda = race_path.joinpath(task).joinpath('Eflda.dat')
        df = pd.read_table(Eflda, header=None, names=['X','Y','eflda'], sep='\\s+')
        return axis.tripcolor(df['X'], df['Y'], df['eflda'], cmap="plasma", shading='flat', label=task)

    def render_eflda():
        fig, ax = plt.subplots()
        fig.suptitle(title)
        if radio.value:
            pcm = render_eflda_axis(radio.value, ax)
            fig.colorbar(pcm, ax=ax, extend='max', label='eflda')
        #ax.legend()
        ax.set_aspect('equal')
        ax.set_xlabel('X')
        ax.set_ylabel('Y');
        return mo.as_html(ax)
    return render_eflda, render_eflda_axis


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
    ax_pabs,
    mo,
    plot_options,
    prams_ui,
    radio,
    render_Pabs,
    render_eflda,
    render_pabs_collection,
    table,
    tasks,
):
    mo.ui.tabs({
        "Pabs table": table,
        "Pabs": mo.as_html(ax_pabs),
        "Pabs(psi)": mo.hstack([mo.as_html(render_pabs_collection()), tasks, plot_options]),
        #'Params': mo.tree({s:dict(params.items(s)) for s in params.sections()}, label='input.par'),
        "Eflda": mo.hstack([ mo.lazy(render_eflda, show_loading_indicator=True),mo.lazy(render_Pabs()), radio]),
        'Params': mo.accordion(prams_ui, multiple=True)

    })
    return


@app.cell
def _(race_path):
    preview_file = race_path.joinpath('preview.mp4')
    fps = 5
    dpi = 100
    preview_file
    return dpi, fps, preview_file


@app.cell
def _(mo):
    rerun = mo.ui.button(label="Rerun")
    rerun

    return (rerun,)


@app.cell
def _(mo, preview_file, rerun):
    rerun
    mo.stop(not preview_file.exists())
    mo.video(
        src=preview_file,
        controls=True,
    )
    return


@app.cell
def _(mo):
    create_animation = mo.ui.run_button(label="Create Animation", kind='warn')
    create_animation
    return (create_animation,)


@app.cell
def _(
    create_animation,
    done_tasks,
    dpi,
    fps,
    mo,
    pd,
    plt,
    preview_file,
    race_path,
    render_eflda_axis,
    render_pabs_axis,
):
    mo.stop(not create_animation.value)
    #import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    import matplotlib.animation as animation
    #fig, ax1 = plt.subplots(figsize=(7, 6))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), constrained_layout=True)
    #fig.subplots_adjust(right=0.99,wspace=0.01, hspace=0.01)
    n_frames = len(done_tasks)

    line, = render_pabs_axis(done_tasks[0], ax1)
    im1  = render_eflda_axis(done_tasks[0], ax2)
    actors= {'line': line, 'im1': im1}
    def frame_update(frame_index):
        task = done_tasks[frame_index]
        pabs_psi = race_path.joinpath(task).joinpath('pabs(psi).dat')
        df = pd.read_table(pabs_psi, header=None, names=['psi','dV','Pabs', 'PabsLD','PabsTT','PabsMX'], sep='\\s+' )
        line.set_xdata(df['psi'])
        line.set_ydata(df['Pabs'])
        ax1.set_title(f"{task} ", fontsize=14)
        ax1.relim()
        ax1.autoscale_view()
        pabs_psi = race_path.joinpath(task).joinpath('Eflda.dat')
        df = pd.read_table(pabs_psi, header=None, names=['X','Y','eflda'], sep='\\s+' )
        actors['im1'].remove()
        actors['im1']= render_eflda_axis(task, ax2)
        ax2.relim()
        ax2.autoscale_view()
        return [line, actors['im1']]

    animator = FuncAnimation(
        fig, 
        frame_update, 
        frames=range(0, n_frames, 1),
        interval=1000//fps,
        blit=True
    )
    # Set up formatting for the movie files
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=fps, metadata=dict(artist='Me'), bitrate=1800)
    with mo.status.progress_bar(total=n_frames) as bar:
        animator.save(
            preview_file,
            writer=writer,
            dpi=dpi,
            progress_callback=lambda i, n: bar.update())


    print(f"\nАнимация сохранена в {preview_file.name}")
    plt.close()  

    return


if __name__ == "__main__":
    app.run()
