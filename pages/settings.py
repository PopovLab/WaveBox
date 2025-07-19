import marimo

__generated_with = "0.14.11"
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
    mo.notebook_dir().parent
    return


@app.cell
def _(mo):
    mo.md("""# Settings""")
    return


@app.cell
def _():
    import config as cfg
    cfg.get_initial_path()
    return (cfg,)


@app.cell
def _(cfg, mo):
    form = mo.ui.file_browser(initial_path=cfg.get_initial_path(), 
                                        selection_mode='directory',
                                        label='Select Base folder',
                                        multiple= False).form()
    return (form,)


@app.cell
def select_cell(form, mo):
    mo.vstack([form ,mo.md(f"Has value: {form.value}")])
    return


if __name__ == "__main__":
    app.run()
