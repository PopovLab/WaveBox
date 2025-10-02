import marimo

__generated_with = "0.15.5"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(mo):
    import random


    # rowId and columnName are strings.
    def style_cell(_rowId, _columnName, value):
        # Apply inline styling to the visible individual cells.
        return {
            "backgroundColor": "gray"
            if value < 4
            else "cornflowerblue",
            "color": "white",
            "fontStyle": "italic",
        }


    table = mo.ui.table(
        data=[random.randint(0, 10) for x in range(40)],
        #style_cell=style_cell,
        #pagination = False,
        show_download = False,
        selection= 'single'
    );
    return (table,)


@app.cell
def _(mo, table):
    #mo.vstack([table, table.value])
    html = f"<h1>Hello, world!</h1> {mo.as_html(table)}"

    return


@app.cell
def _(mo):
    nav_menu = mo.nav_menu(
        {
            "/overview": "Overview",
            "Sales": {
                "/sales": "Overview",
                "/sales/invoices": {
                    "label": "Invoices",
                    "description": "View invoices",
                },
                "/sales/customers": {
                    "label": "Customers",
                    "description": "View customers",
                },
            },
        },orientation='vertical'
    )
    return (nav_menu,)


@app.cell
def _(mo, nav_menu, table):
    accordion = mo.accordion(
        {
            "Door 1": mo.vstack([table, table.value]),
            "Door 2": mo.vstack([table, table.value]),
            "Door 3": nav_menu,
        }
    )
    return (accordion,)


@app.cell
def _(accordion, mo):
    mo.sidebar([accordion])
    return


@app.cell
def _(table):
    table.value
    return


@app.cell
def _(mo):
    mo.plain([1,3,54])
    return


if __name__ == "__main__":
    app.run()
