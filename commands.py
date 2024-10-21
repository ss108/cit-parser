import typer

from src.invoke import invoke

app = typer.Typer()


@app.command()
def hi():
    typer.echo("Hello World")


@app.command()
def test():
    text = "Why speculate? Brown v. Board of Education of Topeka, 347 U.S. 483 (1954)"
    res = invoke(text)
    print(res)


if __name__ == "__main__":
    app()
