import marimo

__generated_with = "0.14.11"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    mo.nav_menu( { "#/": "Home",
                   "#/power_absorbtion": "Power",
                   "#/settings": "Settings",
                   "#/about": "About",
                    "Links": { "https://twitter.com/marimo_io": "Twitter", 
                               "https://github.com/marimo-team/marimo": "GitHub", }, },
                               orientation="horizontal", )
    return


@app.cell
def _(mo):
    import config as cfg
    folder_browser = mo.ui.file_browser(initial_path="",#cfg.get_initial_path(), 
                                        selection_mode='directory',
                                        label='Base folder',
                                        multiple= False)
    return (folder_browser,)


@app.cell
def _(folder_browser, mo):
    race_browser = mo.ui.file_browser(initial_path=folder_browser.path(index=0),
                                      selection_mode='directory',
                                      label='Race folder',
                                      multiple= False)
    return (race_browser,)


@app.cell
def _(folder_browser, mo, race_browser):
    mo.sidebar( [ mo.md("# Wave2D Box"), 
                  mo.vstack([folder_browser, race_browser])] )
    return


@app.cell
def _(mo):
    def render_home():
        header = mo.md("# Home. Test text")
        test = mo.md(
        r'''
        The exponential function $f(x) = e^x$ can be represented as

        \[
            f(x) = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \ldots.
        \]
        '''
        )
        return mo.vstack([header, test ])
    return (render_home,)


@app.cell
def _(mo):
    def render_power_absorbtion():
        header = mo.md("# Power Absorbtion")
        test = mo.md(
        r'''
        The exponential function $f(x) = e^x$ can be represented as

        \[
            f(x) = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \ldots.
        \]
        '''
        )
        return mo.vstack([header, test ])
    return (render_power_absorbtion,)


@app.cell
def _(mo):
    def render_settings():
        folder, set_folder = mo.state(0)
        header = mo.md("# Settings")
        def xyz(x):
            set_folder('xzcvcx')
        
        form = mo.ui.file_browser(
            initial_path="",#cfg.get_initial_path(), 
            selection_mode='directory',
            label='Select Base folder',
            multiple= False
            ).form(on_change=xyz)

        return mo.vstack([header, 
                          form,
                          mo.md(f"Has value: ")])
    return (render_settings,)


@app.cell
def _(mo):
    def render_about():
        header = mo.md("# About")
        test = mo.md(
        r'''
        The exponential function $f(x) = e^x$ can be represented as

        \[
            f(x) = 1 + x + \frac{x^2}{2!} + \frac{x^3}{3!} + \ldots.
        \]
        '''
        )
        return mo.vstack([header, test ])
    return (render_about,)


@app.cell
def _(mo, render_about, render_home, render_power_absorbtion, render_settings):
    mo.routes({ "#/": render_home,
                "#/power_absorbtion": render_power_absorbtion,            
                "#/settings": render_settings,
                "#/about": render_about, 
                mo.routes.CATCH_ALL: render_home,
              })
    return


if __name__ == "__main__":
    app.run()
