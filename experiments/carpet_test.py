import marimo

__generated_with = "0.15.5"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _(df):
    MarginRatio=1.1
    Nr = 101
    Nr_margin=int(Nr*MarginRatio)
    N_teta = int(df.shape[0]/Nr_margin)
    #Nr, Nr_margin, N_teta
    return N_teta, Nr_margin


@app.cell
def _():
    import pandas as pd
    df = pd.read_table('Eflda_101.dat', header=None, names=['X','Y','eflda'], sep='\\s+')
    min_eflda = df['eflda'].max()
    return (df,)


@app.cell
def _(df):
    df.shape[0]
    return


@app.cell
def _(N_teta, Nr_margin, df):
    df['a'] =  df.index % N_teta
    df['b'] = Nr_margin - df.index // N_teta
    df
    return


@app.cell
def _(df):
    import plotly.graph_objects as go
    import numpy as np
    fig = go.Figure(go.Carpet(
        a = df['a'],
        b = df['b'],
        x = df['X'],
        y = df['Y'],
        aaxis = dict(
            #tickprefix = 'a = ',
            smoothing = 0,
            minorgridcount = 1,
            type = 'linear'
        ),
        baxis = dict(
            #tickprefix = 'b = ',
            smoothing = 0,
            minorgridcount = 1,
            type = 'linear'
        )
    ))

    fig.show()
    return (go,)


@app.cell
def _(df, go):
    Eflda = go.Figure(go.Carpet(
        a = df['a'],
        b = df['b'],
        x = df['X'],
        y = df['Y'],
        baxis = dict(
          startline = False,
          endline = False,
          showticklabels = "none",
          smoothing = 0,
          showgrid = False
        ),
        aaxis = dict(
          startlinewidth = 2,
          startline = True,
          showticklabels = "none",
          endline = True,
          showgrid = False,
          endlinewidth = 2,
          smoothing = 0
        )
    ))

    Eflda.add_trace(go.Contourcarpet(
        z = df['eflda'],
        showlegend = True,
        name = "Eflda",
        autocontour = False,
        ncontours=1024,
        line=dict(width=0),  # убираем линии контуров
        contours=dict(
            showlines=False,    # без линий
            coloring='fill',    # только заливка
            showlabels=False    # без подписей
        ),
    ))



    Eflda.show()
    return


if __name__ == "__main__":
    app.run()
