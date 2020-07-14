# EZ-mcserver

A CLI tool to easily download, initialise, and run a (Java) MineCraft server.

Also allows installation of 3rd party mods and plugins.

## How-To

To start a server easily you should:

1. Install EZ-mcserver (TODO)
2. Use command `mcserver quickstart` to install a server
3. Use command `mcserver properties list/set` if there are any hidden properties you would like to change (see https://minecraft.gamepedia.com/Server.properties)
3. Use command `mcserver start` to start the server
4. Use server console / operator commands to adjust any server/administration settings as you would normally do in a MineCraft server (see https://minecraft.gamepedia.com/Commands#List_and_summary_of_commands)

## Schema + Progress

Complete:
```
mcserver versions
mcserver init -v <VERSION> (or -u http://etc/server.jar)
mcserver quickstart
mcserver start
mcserver properties list
mcserver properties set <PROP> <VALUE>
```

In progress:
```
mcserver mods list/install/uninstall
mcserver plugins list/install/uninstall
mcserver worlds list/delete
mcserver howto # shows how to use this tool, and how to do admin after installing a server
```

Backlog:
```
mcserver ui
# (may not be necessary as this can be managed from within server)
mcserver admin ipban add <IP>
mcserver admin ipban remove <IP>
mcserver admin ipban list
mcserver admin ban list
mcserver admin ban add <USERNAME>
mcserver admin ban remove <USERNAME>
mcserver admin whitelist add <USERNAME>
mcserver admin whitelist remove <USERNAME>
mcserver admin whitelist list

```

Notes
* --universe "worlds" (folder to hold worlds)
* https://minecraft.gamepedia.com/Tutorials/Setting_up_a_server
