
"""
Created on Wednesday 8 Jul, 14:00:00 2020

@author: Mark Connelly

CLI interface for EZ-mcserver.
"""
import json
from pathlib import Path
import subprocess
from click.exceptions import UsageError
import click

from . import util

# =============================== Base Group ==================================


@click.group()
def mcserver():
    pass


# ============================= Base Commands =================================


@mcserver.command()
@click.option('-v', '--version', required=False,
              help="VERSION of MineCraft Server")
@click.option('-u', '--url', required=False,
              help="URL to download the MineCraft Server")
def init(version, url):
    """Initialise a server of specified VERSION or from URL into the working
    directory."""
    # Input validation
    if version is not None and url is not None:
        raise UsageError('Use option VERSION or URL. Not both.')
    if version is None and url is None:
        raise UsageError('One option is required: VERSION or URL.')
    # URL passed
    if url is not None:
        server_info = {'url': url}
    # VERSION passed
    if version is not None:
        versions_info = util.get_server_versions_info()
        if version not in versions_info:
            raise UsageError('VERSION not found in list of versions. Try URL '
                             'or mcserver versions command to list known '
                             'versions.')
        server_info = versions_info[version]

    # Prompt message
    print(f'\nDownload and initialise MineCraft Server into {Path.cwd()}:')
    print('    version:     ', version or '-')
    print('    release date:', server_info.get('date', '-'))
    print('    download url:', server_info['url'])
    click.confirm('Do you want to continue?', default=True, abort=True)

    # Eula
    print('\nPlease read the MINECRAFT END USER LICENSE AGREEMENT:')
    print('    https://account.mojang.com/documents/minecraft_eula')
    click.confirm('Do you accept?', abort=True)

    # Download
    print('Downloading server.jar...')
    util.download_from_url(server_info['url'])

    # Run
    print('Initialising server...')
    subprocess.call(['java', '-jar', 'server.jar', '--initSettings'])
    with open('eula.txt', 'r') as f:
        eula = f.read()
    with open('eula.txt', 'w') as f:
        f.write(eula.replace('false', 'true'))

    # Ending message
    print('Server initialised!')


@mcserver.command()
def versions():
    """See possible versions"""
    print('\n          (See https://mcversions.net/ to obtain the URL for '
          'versions not shown)\n')
    print('Version', 'Release Date', 'URL', sep='  ')
    for version, info in util.get_server_versions_info().items():
        print(version.ljust(7), info['date'].ljust(12), info['url'], sep='  ')


@mcserver.command()
def start():
    """Start server in working directory."""
    print('start')


@mcserver.command()
def stop():
    """Stop server in working directory."""
    print('stop')


@mcserver.command()
def ui():
    """UI interface for managing the server"""
    print('ui')


# ============================== Mods Group ===================================


@mcserver.group()
def mods():
    """Manage mods"""
    print('mods')


@mods.command('list')
def mods_list():
    """List available mods"""
    print('mods')


@mods.command('install')
def mods_install():
    """Install a mod"""
    print('mods')


@mods.command('uninstall')
def mods_uninstall():
    """Uninstall a mod"""
    print('mods')


# ============================== Plugins Group ================================


@mcserver.group()
def plugins():
    """Install a plugin"""
    print('plugins')


@plugins.command('list')
def plugins_list():
    """List available plugins"""
    print('plugins')


@plugins.command('install')
def plugins_install():
    """Install a plugin"""
    print('plugins')


@plugins.command('uninstall')
def plugins_uninstall():
    """Uninstall a plugin"""
    print('plugins')


# =============================================================================

if __name__ == '__main__':
    mcserver()
