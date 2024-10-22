import typer

from src.cit_parser.invoke import invoke
from src.cit_parser.postprocess import organize

app = typer.Typer()


@app.command()
def hi():
    typer.echo("Hello World")


@app.command()
def test():
    text = """shall do pursuant to California Civil Code Cal. Civ. Code § 1080"""
    res = invoke(text)
    print(res)

    authorities = organize(res)
    for x in authorities.all(True):
        print(x)


if __name__ == "__main__":
    app()
