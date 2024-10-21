import typer

from src.invoke import invoke

app = typer.Typer()


@app.command()
def hi():
    typer.echo("Hello World")


@app.command()
def test():
    text = "Jojo, 45 F.3d at 87. Yeah, tha"
    res = invoke(text)
    print(res)


if __name__ == "__main__":
    app()
