import os
import typer
from rich.console import Console
import subprocess
from datetime import datetime
import pickle
import atexit
import pdb
from typing_extensions import Annotated
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
def status():
    """
    Display the status of atom.
    """
    global state
    b = state['rel_base'] if state['rel_base'] else state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return
    typer.echo(f'\nNode checked out: {b.id if not b.is_base() else "base"}\n')


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

    if id == 0:
        base()
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")

    state['rel_base'] = node
    typer.echo(f'\nNode {id} is now root.\n')


@app.command()
def base():
    """
    Checkout base node.
    """
    global state
    state['rel_base'] = None
    typer.echo('\nRoot reset to base node.\n')
    

@app.command()
def add(name: str):
    """
    Adds a new node to the currently checked out node.
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
def remove(id: int):
    """
    Removes node with id and unlinks from parents/children.
    """
    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    node.remove_node()


@app.command()
def link(parent_id: int, child_id: int):
    """
    Links parent to child by id.
    """
    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    parent = b.get_by_id(parent_id)
    child = b.get_by_id(child_id)

    if parent is None:
        typer.echo("Parent node does not exist.")

    if child is None:
        typer.echo("Child node does not exist.")

    if not parent.try_link_child(child):
        print(f"Linking parent {parent_id} to child {child_id} failed.")


@app.command()
def unlink(parent_id: int, child_id: int):
    """
    Unlinks parent to child by id.
    """
    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    parent = b.get_by_id(parent_id)
    child = b.get_by_id(child_id)

    if parent is None:
        typer.echo("Parent node does not exist.")

    if child is None:
        typer.echo("Child node does not exist.")

    if not parent.try_unlink_child(child):
        print(f"Unlinking parent {parent_id} from child {child_id} failed.")


@app.command()
def complete(id: int):
    """
    Marks the current node as completed.
    """

    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    node.mark_state(datetime.now)


@app.command()
def incomplete(id: int):
    """
    Marks the current node as incomplete.
    """

    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    node.mark_state(None)


@app.command()
def tree(id: Annotated[int, typer.Option(help='ID of tree root.')] = None):
    """
    Displays a tree rooted at the node id.
    """

    if id and id <= 0:
        typer.echo('ID must be a positive integer.')
        return

    global state
    b = state['rel_base'] if state['rel_base'] else state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    #If the base node is checked out, only print the root nodes unless a nonzero id is passed in as option
    if id == 0 or b == state['abs_base'] and id == None:
        typer.echo("\nAvailable root nodes:")
        for child in state['abs_base'].children:
            console.print(get_node_display(child))
        typer.echo("")
        return


    #If id is not given, display the tree from the currently checked out node
    if id is None:
        console.print(get_tree_string(b))
        return

    #Display the tree from an arbitrary root (except 0)
    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    console.print(get_tree_string(node))


@app.command()
def rename(id: int, name: str):
    """
    Renames the node with the given id.
    """

    if len(name) == 0:
        typer.echo("String cannot be empty.")
        return

    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    node.change_name(name)


@app.command()
def alias(id: int, name: str):
    """
    Aliases the node with the given id.
    """

    if len(name) == 0:
        typer.echo("String cannot be empty.")
        return

    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    if not node.try_add_alias(name):
        typer.echo('Unable to add alias to node.')
        return


@app.command()
def unalias(id: int, name: str):
    """
    Aliases the node with the given id.
    """

    if len(name) == 0:
        typer.echo("String cannot be empty.")
        return

    global state
    b = state['abs_base']
    if b is None:
        typer.echo("No base node found.")
        return

    node = b.get_by_id(id)
    if node is None:
        typer.echo(f"Node {id} does not exist.")
        return

    if not node.try_remove_alias(name):
        typer.echo('Unable to remove alias to node.')
        return



# @app.command()
# def launch(file: str):
#     subprocess.run(["nvim", file])

if __name__ == '__main__':
    app()
