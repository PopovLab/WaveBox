import marimo

__generated_with = "0.14.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import config as cfg
    import marimo as mo
    folder_browser = mo.ui.file_browser(initial_path=cfg.get_initial_path(), 
                                        selection_mode='directory',
                                        label='Base folder',
                                        multiple= False)

    return cfg, folder_browser, mo


@app.cell
def _(folder_browser, mo):
    race_browser = mo.ui.file_browser(initial_path=folder_browser.path(index=0),
                                      selection_mode='directory',
                                      label='Race folder',
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
def _(cfg, mo, race_browser):
    race_path = race_browser.path(index=0)
    if race_path:
        if race_path.joinpath('done_tasks.txt').exists():
            #info = mo.md(f"done_tasks exists")
            cfg.set_initial_path(race_path.parent.parent.as_posix())
            info_kind = 'success'
            done_tasks = get_done_tasks(race_path)
            info = mo.md(f"{race_path.name}\n\n {done_tasks}")        
        else:
            info = mo.md(f"done_tasks not exists!")
            info_kind = 'danger'
    else:
        info = mo.md(f"Upps2")
        info_kind = 'danger'        
    return done_tasks, info, info_kind, race_path


@app.cell
def _(info, info_kind, mo):
    mo.callout(info, kind=info_kind)
    return


@app.cell
def _(mo, race_path):
    import configparser
    check_param= False
    if race_path:
        if race_path.joinpath('input.par').exists():
            check_param= True
    mo.stop(not check_param, mo.md("**Can't open input.par.**"))

    params = configparser.ConfigParser(inline_comment_prefixes=('#',))
    params.read(race_path.joinpath('input.par'))
    def print_params(params):
        for section in params.sections():
            print(f"[{section}]")

    return (params,)


@app.cell
def _(mo, params, race_path):
    input_info = mo.md(f"{race_path.name} - Name: {params['common']['name']}") 
    return (input_info,)


@app.cell
def _(race_path):
    if race_path:
        if race_path.joinpath('system_info.ini').exists():
            pass
        
    return


@app.cell
def _(info_kind, input_info, mo):
    mo.callout(input_info, kind=info_kind)
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
def _(done_tasks, info_kind, mo, race_path):
    mo.stop(info_kind == 'danger', mo.md("**Submit the form to continue.**"))
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
def _(info_kind, mo, tasks_data):
    mo.stop(info_kind == 'danger', mo.md("**Submit the form to continue.**"))
    import pandas as pd
    df = pd.DataFrame.from_dict(tasks_data)
    table = mo.ui.table(data=df)
    return df, pd, table


@app.cell
def _():
    return


@app.cell
def _(df, info_kind, mo, params):
    mo.stop(info_kind == 'danger', mo.md("**Submit the form to continue.**"))
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
def _(done_tasks, info_kind, mo, params, pd, plt, race_path):
    mo.stop(info_kind == 'danger', mo.md("**Submit the form to continue.**"))
    if params['series']['var'] == 'Nr':
        title = params['common']['name'] + ' Mmax=' + params['w2grid']['Mmax']
    else:
        title = params['common']['name'] +' Nr=' + params['w2grid']['Nr'] 
    fig, ax = plt.subplots()
    fig.suptitle(title)
    for task1 in done_tasks:
        #pb = read_power_balance(race_path.joinpath(task))
        pabs_psi = race_path.joinpath(task1).joinpath('pabs(psi).dat')
        df1 = pd.read_table(pabs_psi, header=None, names=['psi','dV','Pabs', 'PabsLD','PabsTT','PabsMX'], sep='\\s+' )
        #plt.plot( df['b'] , label='b')
        #plt.legend()
        #plt.show()
        ax.plot(df1['psi'], df1['Pabs']/df1['dV'] , label=task1)

        #print(df1.index)
    ax.legend()
    ax.set_xlim([0, 0.4])
    #ax.set_ylim([0, 0.000002])
    ax.set_yscale('log')
    ax.set_xlabel('psi')
    ax.set_ylabel('Pabs/dV');
    #plt.show()


    return (ax,)


@app.cell
def _(ax, ax_pabs, mo, params, table):
    mo.ui.tabs({
        "Pabs table": table,
        "Pabs": mo.as_html(ax_pabs),
        "Pabs(psi)": mo.as_html(ax),
        'Params':mo.tree(params.sections())

    })
    return


if __name__ == "__main__":
    app.run()
