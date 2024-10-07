## net utils

a simple network improver


release name explained


```
X.X.XXX <--- this is a shorten SHA hash (changes every update)
^ ^-------------this is defining the version of the code base (gets changed most)
this is defining the version of the program (rarely updated)
```
## net cli

a basic networking command line interface with some commands here are the commands

- `-help`: Display this help message.
- `-cmds`: Display this help message.
- `-values`: Open `config.py`.
- `-debug`: Print debug information.
- `-newmac`: Change MAC address.
- `-netscan`: Scan the network for users.
  - `-l` option will log the output to a file
  - `-m` option will get the mac address of online devices
  - `-o` option will get the os of online devices
- `-rerun`: Rerun the `main.py` script.
  - -`-c`: Rerun the `main.py` into into the console.
- `-return`: Return to the main menu.
- `-clear`: Clear the console.
- `-create`: Allows the user to create their own commands then writes them in `custom_commands.json`.

(there are some bugs with the rerun command)