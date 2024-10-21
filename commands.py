import typer

from src.invoke import invoke
from src.postprocess import organize

app = typer.Typer()


@app.command()
def hi():
    typer.echo("Hello World")


@app.command()
def test():
    text = "The Plaintiff contends that the Defendant’s actions constituted a breach of fiduciary duty, as set forth in Smith v. Jones, 456 F.2d 789, 792 (2d Cir. 1983). In Smith, the court held that a fiduciary is required to act with the utmost good faith and loyalty towards the party they represent. This principle has been reaffirmed in subsequent cases, including Doe v. Roe, 512 U.S. 234, 238 (Brr. 1994), where the Supreme Court emphasized that any conflict of interest must be fully disclosed to the beneficiary. Accordingly, there is no genuine issue of material fact regarding the Defendant’s failure to disclose such conflicts, and summary judgment is appropriate."
    res = invoke(text)

    authorities = organize(res)

    for x in authorities.caselaw:
        print(x.full_text)


if __name__ == "__main__":
    app()
