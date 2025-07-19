import marimo

__generated_with = "0.14.12"
app = marimo.App(width="medium", app_title="Wave2D")


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
    mo.md(
        """
    ## Wave2D Box<br>
    Это web-приложение написанное на marimo для просмотра реультатов вычисления Wave2D<br>
    Удобное и интерактивное. Каждая страница по сути это блокнот Marimo. Его можно редактировать прямо в браузере

    * **[Power](\power_absorbtion)** - раздел показывает поглощенную мощность по радиусу
    * **Settings** - очевидно настройки
    * **About** - еще не придумал о чем
    """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
    The exponential function $f(x) = e^x$ can be represented as

    \[
        f(x) = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \ldots.
    \]
    """
    )
    return


if __name__ == "__main__":
    app.run()
