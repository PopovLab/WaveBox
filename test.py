import marimo

__generated_with = "0.14.11"
app = marimo.App(width="medium", app_title="test")


@app.cell
def _(mo):
    nav_menu = mo.nav_menu(
        {
            "/about": "About",
            "/overview": "Overview",
            "/sales": f"{mo.icon('lucide:shopping-cart')} Sales",
            "/products": f"{mo.icon('lucide:package')} Products",
        }
    )
    nav_menu
    return


@app.cell
def _(mo):
    def page1():
        return mo.md("## This is page 1")
    def render_about():
        return mo.md("## This is page about")
    def render_contact():
        return mo.md("## This is page contact")        
    return page1, render_about, render_contact


@app.cell
def _(mo, page1, render_about, render_contact):
    mo.routes(
        {
            "#/": page1,
            "#/about": render_about,
            "#/contact": render_contact,
            mo.routes.CATCH_ALL: page1,
        }
    )
    return


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
