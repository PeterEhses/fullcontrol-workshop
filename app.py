import marimo

__generated_with = "0.17.8"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import fullcontrol as fc
    return fc, mo


@app.cell
def _(mo):
    mo.md("""
    # FullControl Workshop - Getting Started
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Draw a Simple Square

    This example creates a square path in G-code.
    """)
    return


@app.cell
def _(fc):
    # Create a simple square
    steps = [
        fc.Point(x=0, y=0, z=0.2),
        fc.Point(x=20, y=0, z=0.2),
        fc.Point(x=20, y=20, z=0.2),
        fc.Point(x=0, y=20, z=0.2),
        fc.Point(x=0, y=0, z=0.2),
    ]

    # Convert to G-code
    gcode = fc.transform(steps, 'plot')
    print(gcode)
    return


if __name__ == "__main__":
    app.run()
