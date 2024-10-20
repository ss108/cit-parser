import asyncio

import typer

from src.invoke import invoke

app = typer.Typer()


@app.command()
def hi():
    typer.echo("Hello World")


@app.command()
def test_invoke():
    text = "Hello World. Cororo v. Yee, 515 U.S. 70 (1995)."
    res = asyncio.run(invoke(text))
    print(res)


# @app.command()
# def test_tokenization():
#     test


if __name__ == "__main__":
    app()
