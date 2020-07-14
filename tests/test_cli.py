from click.testing import CliRunner
from click import UsageError
from pathlib import Path
import pytest

from mcserver import cli
server_jar = Path('server.jar')
eula_txt = Path('eula.txt')


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    if server_jar.exists():
        server_jar.unlink()


def test_mcserver_versions():
    """Test running `mcserver versions` command.
    """
    runner = CliRunner()
    result = runner.invoke(cli.versions, ''.split())
    assert result.exit_code == 0, 'Exit code not 0, Something went wrong.'
    assert result.output, 'Unexpected output.'


def test_mcserver_init():
    """Test running `mcserver init` command.
    """
    runner = CliRunner()
    result = runner.invoke(cli.install, '-v 1.16.1 -y'.split())
    assert result.exit_code == 0, 'Exit code not 0, Something went wrong.'
    assert eula_txt.exists(), 'Expected eula.txt file but not found'
