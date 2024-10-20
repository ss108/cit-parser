import typer

from src.invoke import tokenize

app = typer.Typer()


@app.command()
def hi():
    typer.echo("Hello World")


@app.command()
def test_tokenization():
    test_text = "heheheh hi"
    res = tokenize(test_text)
    print(res)


if __name__ == "__main__":
    app()
