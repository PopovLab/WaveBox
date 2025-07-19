import marimo

__generated_with = "0.14.11"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    form = mo.ui.text_area(placeholder="...").form()
    return (form,)


@app.cell
def _(form, mo):
    mo.vstack([form, mo.md(f"Has value: {form.value}")])
    return


if __name__ == "__main__":
    app.run()
