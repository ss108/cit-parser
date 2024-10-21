import typer

from src.invoke import invoke

app = typer.Typer()


@app.command()
def hi():
    typer.echo("Hello World")


@app.command()
def test():
    text = "The Elusive Cat contended, with claws unsheathed, that the aforementioned Mischievous Dog had engaged in “continuous and unrepentant disruption of peace,” citing Paws v. Claws, 377 F.3d 82 (2019). The respondent, The Mischievous Dog, in a counter-claim, referenced Bone v. Squeaky Toy, U.S. 302 (2020), arguing that “an occasional bark falls within the scope of a canine’s natural rights.”"
    res = invoke(text)
    print(res)


if __name__ == "__main__":
    app()
