# di.fm CLI player

* since the beginning of 2016 you need a subscription to use external apps/players

## Requires
pipenv: http://pipenv.readthedocs.io/
mpv: https://mpv.io/installation/

## Get started

- clone repository
- pipenv install ./
- copy $REPO/bin/difm.sh to your $PATH
  - `ln -fs $(pwd)/bin/difm.sh /usr/local/bin/difm`
- edit difm and set INSTALL_PATH
- create the channel cache and default configuration file by running
  - `difm ls`
- edit `$HOME/.difm/config.ini` to set
  - listen password
  - stream format
  - player
- `difm play <channel>`

Enjoy.

## Channel List

The channel list will be cached in `$HOME/.difm/channels.dump` and loaded from
there to minimize network traffic. To fetch the latest channels simply remove
this file and it will be re-created the next time you run the program.
