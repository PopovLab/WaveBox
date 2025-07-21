import marimo

__generated_with = "0.14.12"
app = marimo.App(width="medium", app_title="Qq")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import ui_elements
    ui_elements.nav_menu()
    return


@app.cell
def _(mo):
    mo.md("""# Settings""")
    return


@app.cell
def _():
    from config import get_initial_path
    get_initial_path()
    return (get_initial_path,)


@app.cell
def _(get_initial_path, mo):
    form = mo.ui.file_browser(initial_path= get_initial_path(), 
                                        selection_mode='directory',
                                        label='Select Base folder',
                                        multiple= False).form()
    return (form,)


@app.cell
def select_cell(form):
    form 
    return


@app.cell
def _(form, mo):
    from config import set_initial_path
    if form.value:
        set_initial_path(form.value[0].id)
        out_text= form.value[0].id
    else:
        out_text ='Select base folder'

    mo.md(out_text)    
    return


if __name__ == "__main__":
    app.run()
