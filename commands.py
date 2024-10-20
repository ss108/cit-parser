import typer

from src.invoke import get_labels, tokenize

app = typer.Typer()


@app.command()
def hi():
    typer.echo("Hello World")


# @app.command()
# def test_invoke():
#     text = "Hello World. Cororo v. Yee, 515 U.S. 70 (1995). 18 U.S.C. Sec 87"
#     res = asyncio.run(invoke(text))
#     print(res)


@app.command()
def test_tokenization():
    text = "Hello World. Cororo v. Yee, 515 U.S. 70 (1995). 18 U.S.C. Sec 87"
    res = tokenize(text)

    res = get_labels(res)
    print(res)


if __name__ == "__main__":
    app()
