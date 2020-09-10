from pt3 import config


def debug(s):
    if not config.debug:
        return
    print(s, flush=True)
