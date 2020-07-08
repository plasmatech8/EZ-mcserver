
"""
Created on Wednesday 8 Jul, 14:00:00 2020

@author: Mark Connelly

CLI interface for EZ-mcserver.
"""
import pathlib
import click

# ================ Root Group ================


@click.group()
def mcserver():
    print("mcserver")


# ================ Commands ==================


@mcserver.command()
def start():
    """Start server"""
    print('start')


@mcserver.command()
def stop():
    """Stop server"""
    print('stop')


@mcserver.command()
def init():
    """Initialise a server"""
    print('init')


@mcserver.command()
def ui():
    """UI interface for managing the server"""
    print('ui')


# ============== Mods Group ==================


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


# ============== Plugins Group ================


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


if __name__ == '__main__':
    mcserver()
