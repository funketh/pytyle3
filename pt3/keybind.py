import os.path
import sys

from xpybutil import keybind

bindings = None

#####################
# Get key bindings
xdg = os.getenv('XDG_CONFIG_HOME') or os.path.join(os.getenv('HOME'), '.config')
keybind_file = os.path.join(xdg, 'pytyle3', 'keybind.py')

if not os.access(keybind_file, os.R_OK):
    keybind_file = os.path.join('/', 'etc', 'xdg', 'pytyle3', 'keybind.py')
    if not os.access(keybind_file, os.R_OK):
        print('UNRECOVERABLE ERROR: '
              'No configuration file found at %s' % keybind_file,
              file=sys.stderr)
        sys.exit(1)

with open(keybind_file) as f:
    exec(f.read())
#####################

assert bindings is not None

for key_string, fun in bindings.items():
    if not keybind.bind_global_key('KeyPress', key_string, fun):
        print('Could not bind %s' % key_string, file=sys.stderr)
