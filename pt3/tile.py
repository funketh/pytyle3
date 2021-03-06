import xpybutil
import xpybutil.event as event
import xpybutil.util as util

from . import state
from .debug import debug
from .layouts import layouts

try:
    from config import tile_on_startup
except ImportError:
    tile_on_startup = False

tilers = {}


def debug_state():
    debug('-' * 45)
    for d in tilers:
        if d not in state.visible_desktops:
            continue
        tiler, _ = get_active_tiler(d)
        debug(tiler)
        debug(tiler.store)
        debug('-' * 45)


def cmd(action):
    def _cmd():
        if state.desktop not in tilers:
            return

        tiler, _ = get_active_tiler(state.desktop)

        if action == 'tile':
            tiler.tile()
        elif tiler.tiling:
            if action == 'cycle':
                cycle_current_tiler()
            else:
                getattr(tiler, action)()

    return _cmd


def cycle_current_tiler():
    assert state.desktop in tilers

    tiler, i = get_active_tiler(state.desktop)
    new_tiler = tilers[state.desktop][(i + 1) % len(tilers[state.desktop])]

    tiler.active = False
    tiler.tiling = False
    new_tiler.active = True

    debug('Switching tiler from %s to %s on desktop %d' % (
        tiler.__class__.__name__, new_tiler.__class__.__name__,
        state.desktop))

    new_tiler.tile(save=False)


def get_active_tiler(desk):
    assert desk in tilers

    for i, tiler in enumerate(tilers[desk]):
        if tiler.active:
            return tiler, i


def update_client_moved(c):
    assert c.desk in tilers

    tiler, _ = get_active_tiler(c.desk)
    if tiler.tiling:
        tiler.tile()


def update_client_desktop(c, old_desk):
    assert c.desk in tilers

    if old_desk in tilers:
        for tiler in tilers[old_desk]:
            tiler.remove(c)

    for tiler in tilers[c.desk]:
        tiler.add(c)


def update_client_add(c):
    assert c.desk in tilers

    for tiler in tilers[c.desk]:
        tiler.add(c)


def update_client_removal(c):
    assert c.desk in tilers

    for tiler in tilers[c.desk]:
        tiler.remove(c)


def update_tilers():
    for d in range(state.desk_num):
        if d not in tilers:
            debug('Adding tilers to desktop %d' % d)
            tilers[d] = []
            for lay in layouts:
                t = lay(d)
                tilers[d].append(t)
            tilers[d][0].active = True
            if tile_on_startup:
                tilers[d][0].tiling = True
                tilers[d][0].tile()
    for d in list(tilers.keys()):
        if d >= state.desk_num:
            debug('Removing tilers from desktop %d' % d)
            del tilers[d]


def cb_property_notify(e):
    atom_name = util.get_atom_name(e.atom)

    if atom_name == '_NET_NUMBER_OF_DESKTOPS':
        update_tilers()
    elif atom_name == '_NET_CURRENT_DESKTOP':
        if len(state.visible_desktops) == 1:
            tiler, _ = get_active_tiler(state.desktop)
            if tiler.tiling:
                tiler.tile()
    elif atom_name == '_NET_VISIBLE_DESKTOPS':
        for d in state.visible_desktops:
            tiler, _ = get_active_tiler(d)
            if tiler.tiling:
                tiler.tile()


event.connect('PropertyNotify', xpybutil.root, cb_property_notify)
