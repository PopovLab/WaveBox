import marimo

__generated_with = "0.15.5"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    return


@app.cell
def _():
    MarginRatio=1.1
    Nr = 551
    Nr_margin=int(Nr*MarginRatio)
    return Nr, Nr_margin


@app.cell
def _():
    import pandas as pd
    df = pd.read_table('tmp/Eflda_551.dat', header=None, names=['X','Y','eflda'], sep='\\s+')
    min_eflda = df['eflda'].max()
    return df, min_eflda


@app.cell
def _(Nr, Nr_margin, df):
    N_teta = int(df.shape[0]/Nr_margin)
    Nr, Nr_margin, N_teta
    return


@app.cell
def _(df, min_eflda):
    import plotly.graph_objects as go
    import numpy as np

    fig1 = go.Figure(data=[
        go.Mesh3d(x=df['X'], y=df['Y'], z=df['eflda'], colorbar_x=1.07,
                 intensity = df['eflda']/min_eflda, intensitymode='vertex', flatshading= False,)
    ])

    fig1.update_layout(
        scene = dict(
            aspectratio=dict(x=1, y=1, z=0.45),
            xaxis = dict(nticks=4, range=[-10,10],),
            yaxis = dict(nticks=4, range=[-10,10],),
            zaxis = dict(nticks=4, range=[0,min_eflda],),),
        width=700,
        margin=dict(r=20, l=10, b=10, t=10))
    fig1.show()
    return


@app.cell
def _(df):
    df
    return


@app.cell
def _(df):
    df.shape[0]
    return


if __name__ == "__main__":
    app.run()
