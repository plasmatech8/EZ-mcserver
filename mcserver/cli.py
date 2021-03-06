
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
import requests
import shutil

from . import util

# =============================== Base Group ==================================


@click.group()
def mcserver():
    pass


# ============================= Base Commands =================================


@mcserver.command()
@click.option('-v', '--version', required=False, confirmation_prompt=True,
              help="VERSION of MineCraft Server")
@click.option('-u', '--url', required=False,
              help="URL to download the MineCraft Server")
@click.option('-y', required=False, is_flag=True,
              help='Accept EULA and continue without confirmation prompt')
@click.pass_context
def install(ctx, version, url, y):
    """Download and initialise a MineCraft server with the specified VERSION
    or download URL into the working directory.
    """
    # Input validation
    if version is not None and url is not None:
        raise UsageError('Use option VERSION or URL. Not both.')
    if version is None and url is None:
        ctx.invoke(versions)
        value = click.prompt('Please enter the MineCraft Server VERSION number'
                             ' or URL to a JAR file', default='1.16.1').strip()
        if value.startswith('http:') or value.startswith('https:'):
            url = value
        else:
            version = value
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
    print(
        f'\nDownload and initialise this MineCraft Server under {Path.cwd()}:',
        f'version:      {version or "-"}',
        f'release date: {server_info.get("date", "-")}',
        f'download url: {server_info["url"]}',
        sep='\n\t'
    )
    if not y:
        click.confirm('Do you want to continue?', default=True, abort=True)

    # Eula
    print(
        '\nPlease read the MINECRAFT END USER LICENSE AGREEMENT:',
        'https://account.mojang.com/documents/minecraft_eula',
        sep='\n\t'
    )
    if not y:
        click.confirm('Do you accept?', default=True, abort=True)

    # Download
    print('\nDownloading server.jar...')
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
@click.option('-w', '--world', required=False, default='world',
              help="WORLD name to start the server with")
@click.option('-u', '--universe', required=False, default='worlds',
              help="UNIVERSE directory where worlds are stored")
def start(world, universe):
    """Start server.jar in the working directory using the command:
        java -jar server.jar --world WORLD --universe UNIVERSE

    For more flexibility, you can use the java command instead.

    java <JAVA-SETTINGS> -jar server.jar <MINECRAFT-SETTINGS>

    java -Xms512M -Xmx5G -jar server.jar --universe worlds/ --world myworld

    See `java --help` and `java -X` for flags/options Java runtime.

    See `java -jar server.jar --help` for flags/options for MineCraft.

    Important: use options `--universe worlds/ --world <WORLD-NAME>` so that
    EZ-mcserver can detect worlds (only sees worlds in worlds/ directory).
    """
    if Path('server.jar').exists():
        try:
            ip = requests.get('https://api.ipify.org').text
            print('Starting server with public IP', ip)
        except Exception as e:
            print('Starting server. Public IP cannot be determined. (Ensure '
                  'that your device has access to the internet. If using an '
                  'instance on the cloud, ensure that firewalls/security-'
                  'groups/ACLs allow port 25565 traffic to the internet')
        command = f'java -jar server.jar --world {world} --universe {universe}'
        subprocess.call(command.split())
    else:
        raise UsageError('server.jar file does not exist. Aborted!')


@mcserver.command()
def ui():
    """UI interface for managing the server"""
    print('ui')


@mcserver.command()
@click.pass_context
def quickstart(ctx):
    """Download and initialise a MineCraft server in the current working
    directory and prompts questions for common settings.
    """
    # 1) Ask for VERSION or URL
    #    Ask to accept EULA
    #    Download and initialise server
    ctx.invoke(install)

    # 2) Ask for difficulty level
    difficulty_choices = click.Choice(['peaceful',
                                       'easy',
                                       'normal',
                                       'hard'])
    difficulty = click.prompt('Choose difficulty level',
                              type=difficulty_choices,
                              show_choices=True,
                              default='normal')
    ctx.invoke(properties_set, prop='difficulty', value=difficulty)

    # 3) Select gamemode
    gamemode_choices = click.Choice(['survival',
                                     'creative',
                                     'adventure',
                                     'spectator'])
    gamemode = click.prompt('Set gamemode',
                            type=gamemode_choices,
                            show_choices=True,
                            default='survival')
    ctx.invoke(properties_set, prop='gamemode', value=gamemode)

    # 4) Ask for operators
    operators = click.prompt(
        'Write usernames of server operators (whitespace delimited)'
    ).split()
    json.dump(operators, open('ops.json', 'w'))

    # 5) Ask if they would like to use whitelist system -> usernames
    whitelist_on = click.confirm('Would you like to enable a whitelist?')
    ctx.invoke(properties_set, prop='white-list', value=whitelist_on)
    if whitelist_on:
        whitelist = click.prompt(
            'Write usernames of whitelisted players (whitespace delimited)'
        ).split()
        json.dump(whitelist, open('whitelist.json', 'w'))

    # 6) Tell them they can change settings
    print(
        '\nYou can change further settings using commands:',
        'mcserver properties list/set',
        sep='\n\t'
    )
    print(
        'Server settings (not plugins and mods) can be edited by starting the '
        'server and using commands in the MineCraft server console or by using'
        ' operator commands in-game: see https://minecraft.gamepedia.com/Comma'
        'nds#List_and_summary_of_commands'
    )


# ============================ Properties Group ===============================


@mcserver.group()
def properties():
    """Manage properties"""
    if not Path('server.properties').exists():
        raise UsageError('server.properties file does not exist. Please '
                         'initialise a server in the current working '
                         'directory.')


@properties.command('list')
def properties_list():
    """List available properties"""
    with open('server.properties', 'r') as f:
        print('\n\t(Please see '
              'https://minecraft.gamepedia.com/Server.properties for info '
              'about server properties)\n')
        print(f.read())


@properties.command('set')
@click.argument('prop')
@click.argument('value')
def properties_set(prop, value):
    """Set a property to a value"""
    with open('server.properties', 'r') as f:
        props = f.read().split('\n')
    if prop not in [line.split('=')[0] for line in props]:
        raise UsageError(f'{prop} property not found  in server.properties')
    props = [
        f'{prop}={value}' if line.split('=')[0] == prop
        else line for line in props
    ]
    with open('server.properties', 'w') as f:
        f.write('\n'.join(props))
    print('Set', prop, 'to', value)


# ============================= Worlds Group ==================================


@mcserver.group()
def worlds():
    """Manage worlds in the worlds/ directory (universe)"""
    if not Path('server.jar').exists():
        raise UsageError('server.jar file does not exist. Please '
                         'initialise a server in the current working '
                         'directory.')


@worlds.command('list')
def worlds_list():
    """List worlds seen in the worlds/ directory (universe)"""
    print('Worlds in the `--universe worlds/` directory:')
    for w in Path('worlds').glob('*'):
        if w.is_dir():
            print('\t', w.name)


@worlds.command('delete')
@click.argument('name')
@click.option('-y', required=False, is_flag=True, help='Do not ask to confirm')
def worlds_delete(name, y):
    """Delete a world in the worlds/ directory (universe)"""
    world_path = Path('worlds').joinpath(name)
    if world_path not in [w for w in Path('worlds').glob('*')]:
        raise UsageError(f'No world found under {world_path}')
    if not y:
        click.confirm(f'Are you sure you want to delete {world_path}?',
                      abort=True)
    shutil.rmtree(world_path)


# =============================================================================

if __name__ == '__main__':
    mcserver()
