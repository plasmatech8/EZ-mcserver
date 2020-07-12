# EZ-mcserver

A CLI tool to easily download, initialise, and run a (Java) MineCraft server.

Also allows installation of 3rd party mods and plugins.

Complete:
```
mcserver versions
mcserver init -v <VERSION> (or -u http://etc/server.jar)
```

In progress:
```
mcserver start
mcserver ui

mcserver mods list/install/uninstall
mcserver plugins list/install/uninstall

mcserver worlds list/delete

mcserver properties list
mcserver properties set <PROP> <VALUE>

mcserver ban list
mcserver ban add <USERNAME>
mcserver ban remove <USERNAME>

mcserver properties list
mcserver properties set <PROP> <VALUE>
```

Backlog:
```
mcserver ipban add <IP>
mcserver ipban remove <IP>
mcserver ipban list

mcserver whitelist add <USERNAME>
mcserver whitelist remove <USERNAME>
mcserver whitelist list

mcserver quickstart
```

Notes
* --universe "worlds" (folder to hold worlds)
* https://minecraft.gamepedia.com/Tutorials/Setting_up_a_server
