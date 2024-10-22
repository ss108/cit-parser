import typer

from src.cit_parser.invoke import invoke
from src.cit_parser.postprocess import organize

app = typer.Typer()


@app.command()
def hi():
    typer.echo("Hello World")


@app.command()
def test():
    text = """For all the reasons explained in the briefs filed by
Mr. Singh, Mr. Mendez-Colín, and Mr. Campos-Chaves,
Section 1229(a)(2) cannot reasonably be read to be satisfied when DHS had not first filed a valid Notice to Appear in conformity with Section 1229(a)(1). Amici write
separately to highlight two points that support the
noncitizens’ reading of Section 1229(a)(2): the statutory
history and practical problems created by the government’s interpretation.
First, amici agree with the noncitizens’ position that
the statutory text is clear and thus dispositive of the
question presented. The statutory history, moreover,
bolsters the noncitizens’ interpretation and is “an important part of” the context of the text. United States v.
Hansen, 599 U.S. 762, 775-776 (2023). And also see also Scalia & Garner, Reading Law: The Interpretation of Legal Texts
256 (2012)(endorsing use of “statutory history—the statutes repealed or amended by the statute under consideration” as part of statutory interpretation)."""
    res = invoke(text)

    authorities = organize(res)
    print(authorities)


if __name__ == "__main__":
    app()
