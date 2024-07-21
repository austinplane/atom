import os
import pytest
from typer.testing import CliRunner
from atom.main import app, change_pickle_path

pickle_path = os.path.expanduser('~/code/atom/test_tree.pkl')

@pytest.fixture
def runner():
    if os.path.exists(pickle_path):
        os.remove(pickle_path)

    change_pickle_path(pickle_path)

    runner = CliRunner()
    return runner

def test_app_start(runner):
    result = runner.invoke(app)
    assert result.exit_code == 0
