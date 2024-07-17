import typer
import subprocess


app = typer.Typer()


@app.callback()
def callback():
    """
    Awesome Portal Gun
    """


@app.command()
def shoot():
    """
    Shoot the portal gun
    """
    typer.echo("Shooting portal gun!!!!")


@app.command()
def load():
    """
    Load the portal gun
    """
    typer.echo("Loading portal gun")

@app.command()
def launch(file: str):
    subprocess.run(["nvim", file])

if __name__ == '__main__':
    app()
