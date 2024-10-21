import typer

from src.invoke import invoke

app = typer.Typer()


@app.command()
def hi():
    typer.echo("Hello World")


@app.command()
def test():
    text = "Hello World. Cororo v. Yee, 515 U.S. 70 (1995). 18 U.S.C. Sec 87"
    res = invoke(text)
    print(res)


if __name__ == "__main__":
    app()
