
"""
Created on Wednesday 8 Jul, 14:00:00 2020

@author: Mark Connelly

Utility functions for EZ-mcserver.
"""
import json
from pathlib import Path
from click import UsageError
import click
import requests


def get_server_versions_info() -> dict:
    """Read server_versions.json. Contains information about versions of
    MineCraft, download URLs, and release dates.

    Returns:
        dict: dict containing server information.
    """
    path = Path(__file__).parent.joinpath('server_versions.json')
    with open(path, 'r') as fp:
        server_versions = json.load(fp)
    return server_versions


def download_from_url(url: str):
    """Downloads a file from URL in 1MB chunks with a progress bar.

    Args:
        url (str): Download URL for a file
    """
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))  # Bytes
    block_size = 1024*1024  # 1 Megabyte
    with click.progressbar(length=total_size,
                           show_pos=True,
                           show_percent=True) as progress_bar:
        with open(Path(url).name, 'wb') as f:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
