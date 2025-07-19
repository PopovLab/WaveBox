import marimo

__generated_with = "0.14.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    import ui_elements
    ui_elements.nav_menu()
    return


@app.cell
def _(mo):
    mo.md("# Home. Test text")
    return


@app.cell
def _(mo):
    mo.md(
        r'''
        The exponential function $f(x) = e^x$ can be represented as

        \[
            f(x) = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \ldots.
        \]
        '''
        )
    return


if __name__ == "__main__":
    app.run()
