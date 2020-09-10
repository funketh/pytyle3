import sys

from distutils.core import setup

try:
    import xpybutil
except ImportError:
    print('')
    print('pytyle3 requires xpybutil')
    print('See: https://github.com/BurntSushi/xpybutil')
    sys.exit(1)

setup(
    name='pytyle3',
    author='Andrew Gallant <andrew@pytyle.com>, Theodor Kurt Funke <theodor.k.funke@gmail.com>',
    version='4.0.0',
    license='GPLv3+',
    description='A new and much more lightweight pytyle that supports Openbox Multihead',
    long_description='See README.md',
    url='https://github.com/funketh/pytyle3',
    platforms='POSIX',
    packages=['pt3', 'pt3/layouts'],
    data_files=[('share/doc/pytyle3', ['README.md', 'LICENSE']),
                ('/etc/xdg/pytyle3', ['config.py', 'keybind.py'])],
    scripts=['pytyle3']
)
