import marimo

__generated_with = "0.15.5"
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
    return mo, np


@app.cell
def _(mo):
    omega = mo.ui.slider(1,19)
    omega
    return (omega,)


@app.cell
def _():
    layout_style = dict(
        margin=dict(r=20, t=30, b=10),
        plot_bgcolor='white', paper_bgcolor='white',
        legend=dict(
            orientation="v",
            y=1.01,
            x=1.01
        ),
        title_font_size=16,
        title_x=0.5 # Center the title
    )
    return (layout_style,)


@app.cell
def _(layout_style, mo, np, omega):
    import plotly.express as px
    x=np.linspace(0., 1., 130)
    fig = px.line(x=x, y=[np.sin(omega.value*x), np.cos(omega.value*x)], title="sample figure")
    fig.update_xaxes(showline=True, linewidth=1, linecolor='black', mirror=True, ticks='outside', gridcolor='grey')
    fig.update_yaxes(showline=True, linewidth=1, linecolor='black', mirror=True, ticks='outside', gridcolor='grey')
    fig.update_layout(layout_style)
    fig.update_yaxes(title_text='Y-axis')

    plot = mo.ui.plotly(fig)
    return (plot,)


@app.cell
def _(mo, omega, plot):
    mo.vstack([plot, omega.value])
    return


if __name__ == "__main__":
    app.run()
