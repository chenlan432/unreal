import menu
import check_asset
import megascan
import utils
import importlib


def init():
    menu.add_menus()


def reload_all():
    importlib.reload(check_asset)
    importlib.reload(megascan)
    importlib.reload(menu)
    importlib.reload(utils)


if __name__ == '__main__':
    init()
