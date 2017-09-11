#!/usr/bin/env bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
xterm -e "/usr/bin/python $DIR/send.py -y -c 'shutdown -h now'"