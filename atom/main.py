import os
import typer
import subprocess
import pickle
import atexit
import pdb
from .node import Node

app = typer.Typer()
pickle_path = os.path.expanduser('~/code/atom/tree.pkl')

state = {
        'abs_base': None
        }

def change_pickle_path(path):
    global pickle_path
    pickle_path = path

def run_at_exit():
    b = state['abs_base']
    if b is None: return

    with open(pickle_path, 'wb') as f:
        pickle.dump(b, f)

atexit.register(run_at_exit)


@app.callback()
def callback():
    """
    CLI todo app.
    """
    if not os.path.exists(pickle_path):
        state['abs_base'] = Node('base')
    else:
        with open(pickle_path, 'rb') as f:
            state['abs_base'] = pickle.load(f)

@app.command()
def ping():
    """
    Check that the base node is loaded.
    """

    b = state['abs_base']
    if b is not None:
        typer.echo(b)
    else:
        typer.echo("No base node found.")

@app.command()
def add(name: str):
    """
    Adds a new node.
    """
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = Node(name, b)
    result = b.try_link_child(node)
    if not result:
        print(f"Could not add node {name}")

# @app.command()
# def launch(file: str):
#     subprocess.run(["nvim", file])

if __name__ == '__main__':
    app()
