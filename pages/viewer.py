import marimo

__generated_with = "0.17.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import ui_elements
    import plot as plot
    ui_elements.nav_menu()
    return mo, plot


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
    mo.md(
        f"""
    /// admonition | Folder : {folder_browser.path(index=0)} 
    ///
    """
    )
    return


@app.function
def get_race_list(directory_path):
    path_list= [item for item in directory_path.iterdir() if item.is_dir()]            
    return sorted([ {'name':p.name, 'path':p} for p in path_list], key=lambda item: item['name'], reverse=True)


@app.cell
def _(folder_browser, mo):
    race_table = mo.ui.table(data=get_race_list(folder_browser.path(index=0)), pagination=True, show_download = False, selection= 'single')
    return (race_table,)


@app.cell
def _(mo, race_table):
    import shutil
    delete_chkbox = mo.ui.checkbox(label='Are you sure?')
    def delete_race(x):
        if not delete_chkbox.value: return
        directory_to_remove = race_table.value[0]['path']
        if directory_to_remove.exists():
            print(f'remove {directory_to_remove}')
            try:
                # Attempt to remove the directory
                shutil.rmtree(directory_to_remove)
                with mo.redirect_stdout():
                    print(f"Directory '{directory_to_remove}' removed successfully.")
            except OSError as e:
                print(f"Error removing directory '{directory_to_remove}': {e}")
                print("Ensure the directory is empty before attempting to remove it with Path.rmdir().")
    delete_btn = mo.ui.run_button(label="Delete race data", kind='warn', on_change=delete_race)
    return delete_btn, delete_chkbox


@app.cell
def _(delete_btn, delete_chkbox, mo, race_table):

    mo.vstack([race_table, mo.hstack([delete_btn, delete_chkbox])])
    return


@app.cell
def _():
    #race_table.value[0]
    return


@app.cell
def _(folder_browser, mo):
    mo.sidebar([folder_browser])
    return


@app.cell
def _(mo, race_table):
    mo.stop((len(race_table.value) == 0) , mo.md("**Select Race Data.**"))
    return


@app.cell
def _(mo):
    get_hstate, set_hstate = mo.state('admonition')
    return get_hstate, set_hstate


@app.cell
def _(race_table, set_hstate):
    from race import Race
    race= Race(race_table.value[0]['path'])

    if race.is_good:
        set_hstate('admonition')  
    else:
        set_hstate('attention')
    return (race,)


@app.cell
def _(get_hstate, mo, race):
    mo.md(
        f"""
    /// {get_hstate()} | Race: {race.name} {race.title}
    Description: {race.description} <br>
    Tasks: {race.info_text}  <br>
    {race.sys_info} <br>
    Execution time: {race.exe_time}
    ///
    """
    )
    return


@app.cell
def _(race):
    #mo.stop(get_hstate() == 'attention', mo.md("**Submit the form to continue.**"))
    for task in race.tasks_collection:
        pb = read_power_balance(race.result_path.joinpath(task['task_name']))
        task.update(pb)
        #print(pb)
    return


@app.function
def read_power_balance(path):
    pb = {}
    if path.joinpath('power_balance.dat').exists():
        with path.joinpath('power_balance.dat').open("r") as file:
            content = [line.strip().split() for line in file.readlines()]
            for line in content:
                pb[line[0]] = float(line[2])
    return pb


@app.cell
def _(mo, race):
    #mo.stop(get_hstate() == 'attention', mo.md("**Submit the form to continue.**"))
    import pandas as pd
    df = pd.DataFrame.from_dict(race.tasks_collection)
    table = mo.ui.table(data=df, selection=None, show_column_summaries= False)
    return df, pd, table


@app.cell
def _():
    axis_style =  dict(showline=True, linewidth=1, linecolor='black', mirror=True, ticks='outside', gridcolor='grey')
    layout_style = dict(
        margin=dict(r=20, t=30, b=10),
        xaxis= axis_style,
        yaxis= axis_style,
        plot_bgcolor='white', paper_bgcolor='white',
        legend=dict(orientation="v", y=1.01, x=1.01),
        title_font_size=16,
        title_x=0.5 # Center the title
    )
    return (layout_style,)


@app.cell
def _(df, layout_style, race):
    import plotly.express as px
    px_line = px.line(x=df[race.params['series']['var']], y=df['Pabs(kW)'], title="Pabs(kW)", markers=True)
    px_line.update_layout(layout_style)
    px_line.update_yaxes(title_text='Pabs(kW)')
    px_line.update_xaxes(title_text= race.params['series']['var']);
    return px, px_line


@app.cell
def _(mo):
    psi_min = mo.ui.number(start=0.0, stop=1.0, step =0.1, label="psi min")
    psi_max = mo.ui.number(start=0.0, stop=1.0, step =0.1, value=1.0, label="psi max")
    return psi_max, psi_min


@app.cell
def _(mo):
    log_checkbox = mo.ui.checkbox(label="log scale")
    dv_norm_checkbox = mo.ui.checkbox(label="dv norm")
    return dv_norm_checkbox, log_checkbox


@app.cell
def _(log_checkbox, mo, psi_max, psi_min):
    plot_options = mo.vstack([log_checkbox, psi_min, psi_max])
    return


@app.cell
def _(mo, race):
    done_tasks = [tsk['task_name'] for tsk in race.tasks_collection]
    task_checkboxs = mo.ui.array([mo.ui.checkbox(label=task, value=True) for task in done_tasks], label="Task list")
    radio = mo.ui.radio(options=done_tasks, value=done_tasks[0])
    return done_tasks, radio, task_checkboxs


@app.cell
def _(race):
    #mo.stop(get_hstate() == 'attention', mo.md("**Submit the form to continue.**"))
    #title = plot.get_title(race.params,['Nr', 'mmax', 'nphi1'])
    title = race.get_plot_title(['Nr', 'mmax', 'nphi1'])
    title
    return (title,)


@app.cell
def _(
    done_tasks,
    dv_norm_checkbox,
    layout_style,
    log_checkbox,
    pd,
    px,
    race,
    task_checkboxs,
    title,
):
    pabs_collection = px.line(title= title, markers=True)
    for task1, check in zip(done_tasks, task_checkboxs.value):
        if check:
            pabs_psi = race.result_path.joinpath(task1).joinpath('pabs(psi).dat')
            if not pabs_psi.exists():
                continue
            df1 = pd.read_table(pabs_psi, header=None, names=['psi','dV','Pabs', 'PabsLD','PabsTT','PabsMX'], sep='\\s+' )
            if dv_norm_checkbox.value:
                pabs_collection.add_scatter(x=df1['psi'], y=df1['Pabs']/df1['dV'], name=task1)
            else:
                pabs_collection.add_scatter(x=df1['psi'], y=df1['Pabs'], name=task1)

    pabs_collection.update_layout(layout_style)
    if log_checkbox.value:
        pabs_collection.update_yaxes(type="log")
    pabs_collection.update_yaxes(title_text='Pabs(kW)')
    pabs_collection.update_xaxes(title_text= race.params['series']['var']);
    return (pabs_collection,)


@app.cell
def _(mo):
    col_names = [ 'psi','Sflux', 'dSflux/dpsi', 'dPld/dpsi', 'dPttmp/dpsi', 'dPmix/dpsi', 'dPtot/dpsi']
    dropdown = mo.ui.dropdown(
        options= col_names, value='Sflux', label="choose one"
    )
    return (dropdown,)


@app.cell
def _(layout_style, log_checkbox, pd, px, race, task_checkboxs, title):

    def flux_plot(name):
        plot = px.line(title= title, markers=True)
        for tsk, check in zip(race.tasks_collection, task_checkboxs.value):
            if check:
                task_name = tsk['task_name']
                file = race.result_path.joinpath(task_name).joinpath('flux(psi).dat')
                if not file.exists():
                    continue
                df1 = pd.read_table(file, sep='\\s+' )
                plot.add_scatter(x=df1['psi'], y=df1[name], name=task_name)

        plot.update_layout(layout_style)
        if log_checkbox.value:
            plot.update_yaxes(type="log")
        plot.update_yaxes(title_text= name)
        plot.update_xaxes(title_text= race.params['series']['var'])
        return plot
    return (flux_plot,)


@app.cell
def _(mo, task_checkboxs):
    tasks_stack = mo.hstack([task_checkboxs, task_checkboxs.value], justify="space-between")
    return


@app.cell
def _(mo, plot, race, title):
    from pathlib import Path

    from matplotlib import pyplot as plt
    def render_Pabs(task):
        if not task:
            return mo.md(text='No selected task')
        task_path = race.result_path.joinpath(task) 
        return mo.as_html(plot.render_Pabs(task_path, title))
    return Path, render_Pabs


@app.cell
def _(Path, mo, plot, race):

    def render_eflda(task):
        if not task:
            return mo.md(text='No selected task')
        task_path  =  race.result_path.joinpath(task)        
        image = task_path.joinpath('eflda_image.png')
        if not Path(image).exists():
            try:
                fig = plot.render_eflda_fig(task_path)
                fig.savefig(image, dpi=300, bbox_inches='tight', transparent=False)
            except Exception as e:
                with mo.redirect_stdout():
                    print(f"Exception: {e}")
        if Path(image).exists():                
            return mo.image(src= image, alt= 'eflda', width=600, height=500)
        else:
            return mo.md(text='No image')    
    return (render_eflda,)


@app.cell
def _(Path, mo, plot, race):
    def render_eflda_pabs(task):
        if not task:
            return mo.md(text='No selected task')
        task_path  =  race.result_path.joinpath(task)        
        image = task_path.joinpath('eflda_pabs.png')
        if not Path(image).exists():
            try:
                fig = plot.make_eflda_pabs_fig(task_path, ['Nr', 'mmax', 'nphi1'])
                fig.savefig(image, dpi=300, bbox_inches='tight', transparent=False)
            except Exception as e:
                with mo.redirect_stdout():
                    print(f"Exception: {e}")
        if Path(image).exists():                
            return mo.image(src= image, alt= 'eflda pabs', width=1100, height=500)
        else:
            return mo.md(text='No image')
    return (render_eflda_pabs,)


@app.cell
def _(mo, race):
    def create_view_item(item):
        return mo.md(f">{item[0]} = {item[1]}")

    def create_view_section(section):
        text = [f" {i[0]} = {i[1]}" for i in section]
        return mo.md('>'+'<br>'.join(text))

    #prams_ui ={f"**{s}**": mo.vstack([create_view_item(i) for i in params.items(s)]) for s in params.sections()}
    prams_ui ={f"**{s}**": create_view_section(race.params.items(s)) for s in race.params.sections()}
    return (prams_ui,)


@app.cell
def _(
    dropdown,
    dv_norm_checkbox,
    flux_plot,
    log_checkbox,
    mo,
    pabs_collection,
    prams_ui,
    px_line,
    radio,
    render_Pabs,
    render_eflda,
    table,
    task_checkboxs,
):
    mo.ui.tabs({
        "Pabs table": table,
        "Pabs": mo.ui.plotly(px_line),
        "Pabs(psi)": mo.hstack([
            mo.vstack([mo.ui.plotly(pabs_collection), mo.hstack([log_checkbox, dv_norm_checkbox])]),
            task_checkboxs]),
        "Flux(psi)": mo.hstack([
            mo.vstack([mo.ui.plotly(flux_plot(dropdown.value)), mo.hstack([log_checkbox, dropdown])]),
            task_checkboxs]),    
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
    return (task_slider,)


@app.cell
def _():
    return


@app.cell
def _(done_tasks, mo, render_eflda_pabs, task_slider):
    def get_task():
        return done_tasks[task_slider.value-1]
    mo.vstack([
        mo.hstack([task_slider,mo.md(f"Task - {get_task()}")]),
        mo.lazy(render_eflda_pabs(get_task()),show_loading_indicator=True),
    ])
    return


@app.cell
def _(Path, done_tasks, e, mo, race_path):
    def clear_image_cach(x):
        print(x)
        for task in done_tasks:
            task_path  =  Path(race_path).joinpath(task)
            for f in task_path.glob('*.png'):
                try:
                    f.unlink()
                except FileNotFoundError:
                    print(f"Error deleting file '{f}': {e}")
    mo.ui.run_button(label="Clear image cache", kind='warn', on_change=clear_image_cach)
    return


if __name__ == "__main__":
    app.run()
