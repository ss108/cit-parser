import typer

from src.cit_parser.invoke import invoke
from src.cit_parser.postprocess import organize

app = typer.Typer()


@app.command()
def hi():
    typer.echo("Hello World")


@app.command()
def test():
    text = """An employer's liability under FEHA for hostile environment sexual harassment committed by customers or clients prior to the effective date of the 2003 amendment to section 12940, subdivision (j) (Stats. 2003, ch. 671, § 1) is uncertain. Wrong v. Johnson, 56 F. 2d 123 (N.D. Cal. 2021)"""
    res = invoke(text)

    full = [x for x in res if x.is_full]
    print(full)

    authorities = organize(res)
    print(authorities)


if __name__ == "__main__":
    app()
