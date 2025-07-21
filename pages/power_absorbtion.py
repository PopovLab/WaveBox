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
    /// {get_hstate()} | Work: {race_name} {inp_text}
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
    return (tasks,)


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
    fig, ax = plt.subplots()
    fig.suptitle(title)
    for task1, tv in zip(done_tasks, tasks.value):
        if tv:
            #pb = read_power_balance(race_path.joinpath(task))
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
    #plt.show()


    return (ax,)


@app.cell
def _(mo, tasks):
    tasks_stack = mo.hstack([tasks, tasks.value], justify="space-between")
    return


@app.cell
def _(ax, ax_pabs, mo, params, plot_options, table, tasks):
    mo.ui.tabs({
        "Pabs table": table,
        "Pabs": mo.as_html(ax_pabs),
        "Pabs(psi)": mo.hstack([mo.as_html(ax), tasks, plot_options]),
        'Params':mo.tree(params.sections())
    })
    return


if __name__ == "__main__":
    app.run()
