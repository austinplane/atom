import os
import typer
from rich.console import Console
import subprocess
import pickle
import atexit
import pdb
from .node import Node
from .display import get_node_display, get_tree_string

console = Console()
app = typer.Typer()
pickle_path = os.path.expanduser('~/code/atom/tree.pkl')

state = {
        'abs_base': None,
        'rel_base': None,
        }

def change_pickle_path(path):
    global pickle_path
    pickle_path = path

def run_at_exit():
    global state
    if state['abs_base'] is None: return

    with open(pickle_path, 'wb') as f:
        pickle.dump(state, f)

atexit.register(run_at_exit)


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context):
    """
    CLI todo app.
    """

    global state
    if not os.path.exists(pickle_path):
        state['abs_base'] = Node('base')
    else:
        with open(pickle_path, 'rb') as f:
            state = pickle.load(f)

    if ctx.invoked_subcommand is None:
        b = state['abs_base']
        typer.echo("\nAvailable root nodes:")
        if b is not None:
            for child in b.children:
                console.print(get_node_display(child))
            typer.echo("")
        else:
            typer.echo("No base node found.")

@app.command()
def checkout(id: int):
    """
    Check out a node for processing.
    """

    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")

    state['rel_base'] = node
    typer.echo(f'Node {id} is now root.')


@app.command()
def add(name: str):
    """
    Adds a new node.
    """

    global state
    b = state['rel_base'] if state['rel_base'] else state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = Node(name, b)
    result = b.try_link_child(node)
    if not result:
        print(f"Could not add node {name}")


@app.command()
def tree(id: int):
    """
    Displays a tree rooted at the node id.
    """

    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")

    console.print(get_tree_string(node))


# @app.command()
# def launch(file: str):
#     subprocess.run(["nvim", file])

if __name__ == '__main__':
    app()
