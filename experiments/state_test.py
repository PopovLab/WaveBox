import marimo

__generated_with = "0.14.11"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    get_state, set_state = mo.state(20)
    # Updating the state through the slider will recreate the number (below)
    slider = mo.ui.slider(0, 100, value=get_state(), on_change=set_state)
    # Updating the state through the number will recreate the slider (above)
    number = mo.ui.number(0, 100, value=get_state(), on_change=set_state)
    # slider and number are synchronized to have the same value (try it!)

    return mo, number, slider


@app.cell
def _(number, slider):
    slider, number
    return


@app.cell
def _():
    return


@app.cell
def _(mo):
    get_counter, set_count = mo.state(0)
    return get_counter, set_count


@app.cell
def _(get_counter, mo, set_count, set_counter):
    mo.hstack([
            mo.ui.button(label = "-", on_change= set_count),
            mo.ui.text(f"count = {get_counter()}"),
            mo.ui.button(label ="+", on_change= lambda _: set_counter(lambda v: v + 1)),
    ])
    return


@app.cell
def _(get_counter):
    value = get_counter()
    return


@app.cell
def _(get_counter, mo):
    mo.md(
        f"""
    The counter's current value is **{get_counter()}**!

    This cell runs automatically on button click, even though it
    doesn't reference either button.
    """
    )
    return


@app.cell
def _(mo):
    get_x, set_x = mo.state(0)



    return get_x, set_x


@app.cell
def _(get_x, mo, set_x):
    x = mo.ui.slider(
        0, 10, value=get_x(), on_change=set_x, label="$x$:")
    x_plus_one = mo.ui.number(
        1,
        11,
        value=get_x() + 1,
        on_change=lambda v: set_x(v - 1),
        label="$x + 1$:",
    )

    return x, x_plus_one


@app.cell
def _(x, x_plus_one):
    def render():
        return [x, x_plus_one]
    return (render,)


@app.cell
def _(render):
    render()
    return


@app.cell
def _(mo, render):
    mo.routes({ "#/": render,
                mo.routes.CATCH_ALL: render,
              })
    return


if __name__ == "__main__":
    app.run()
