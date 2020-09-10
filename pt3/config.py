import os.path
import sys

xdg = os.getenv('XDG_CONFIG_HOME') or os.path.join(os.getenv('HOME'), '.config')
conf_file = os.path.join(xdg, 'pytyle3', 'config.py')

if not os.access(conf_file, os.R_OK):
    conf_file = os.path.join('/', 'etc', 'xdg', 'pytyle3', 'config.py')
    if not os.access(conf_file, os.R_OK):
        print('UNRECOVERABLE ERROR: '
              'No configuration file found at %s' % conf_file,
              file=sys.stderr)
        sys.exit(1)

with open(conf_file) as f:
    exec(f.read())
