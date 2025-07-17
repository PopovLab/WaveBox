import marimo

__generated_with = "0.13.6"
app = marimo.App(width="medium")


@app.cell
def _():
    import numpy as np
    import marimo as mo
    from matplotlib import pyplot as plt
    return mo, np, plt


@app.cell
def _(mo):
    omega = mo.ui.slider(1,9)
    omega
    return (omega,)


@app.cell
def _(np, omega, plt):
    x=np.linspace(0., 1., 30)
    plt.plot(x, np.sin(omega.value*x), label='sin')
    plt.legend()
    plt.show()
    return


if __name__ == "__main__":
    app.run()
