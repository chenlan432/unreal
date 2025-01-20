import menu
import check_asset
import megascan
import utils
import importlib
import unreal


def init():
    menu.add_menus()


def reload_all():
    importlib.reload(check_asset)
    importlib.reload(megascan)
    importlib.reload(menu)
    importlib.reload(utils)


if __name__ == '__main__':
    init()

    # 绑定函数
    import_subsystem = unreal.get_editor_subsystem(unreal.ImportSubsystem)
    on_asset_post_import_delegate = unreal.ImportSubsystem_OnAssetPostImport_Dyn()
    on_asset_post_import_delegate.add_callable(check_asset.check_assets_all)
    import_subsystem.set_editor_property("on_asset_post_import", on_asset_post_import_delegate)
