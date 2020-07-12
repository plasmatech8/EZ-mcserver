from mcserver import util
from click import UsageError
import pytest
from pathlib import Path
import time
server_jar = Path('server.jar')


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    if server_jar.exists():
        server_jar.unlink()


def test_get_server_versions_info():
    """Test obtaining server versions info from JSON file.
    """
    assert util.get_server_versions_info(), 'Unable to get server versions.'


def test_download_from_url():
    """Test download function for MineCraft server Jar.
    """
    test_url = ('https://launcher.mojang.com/v1/objects/'
                'a412fd69db1f81db3f511c1463fd304675244077/server.jar')
    util.download_from_url(test_url)
    assert server_jar.exists(), 'Download failed.'
