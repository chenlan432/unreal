import unreal
import os
import json


def get_project_name():
    return unreal.Paths.project_dir().split('/')[-2]


def get_assets():
    return unreal.EditorUtilityLibrary().get_selected_assets()


def get_all_assets(dir_path='/Game'):
    return list(map(unreal.EditorAssetLibrary.load_asset, unreal.EditorAssetLibrary.list_assets(dir_path)))


def load_json(json_name):
    json_path = '{}/{}.json'.format(os.path.dirname(__file__), json_name)
    with open(json_path, 'r') as f:
        f_string = f.read()
    return json.loads(f_string)


def check_property(asset, prop_name, prop_value):
    if isinstance(prop_value, str):
        if asset.get_editor_property(prop_name) == eval(prop_value):
            return True
        else:
            return False
    else:
        if asset.get_editor_property(prop_name) == prop_value:
            return True
        else:
            return False


def set_property(asset, prop_name, prop_value):
    if isinstance(prop_value, str):
        asset.set_editor_property(prop_name, eval(prop_value))
    else:
        asset.set_editor_property(prop_name, prop_value)


def get_static_mesh_type(static_mesh):
    return static_mesh.get_name().split('_')[1]


def get_texture_type(texture):
    return texture.get_name().rpartition('_')[-1]


def get_asset_type_name(asset):
    return asset.get_full_name().split(' ')[0]


def set_metadata(asset, data_name, data_value):
    unreal.EditorAssetLibrary.set_metadata_tag(asset, data_name, data_value)


def get_metadata(asset, data_name):
    return unreal.EditorAssetLibrary.get_metadata_tag(asset, data_name)


def rename_dir(source_path, new_path):
    unreal.EditorAssetLibrary.rename_directory(source_path, new_path)


def move_asset(asset, new_path, new_name=''):
    old_path_name = asset.get_path_name()
    new_name = new_name or asset.get_name()
    unreal.EditorAssetLibrary.rename_asset(old_path_name, '{}/{}.{}'.format(new_path, new_name, new_name))


def delete_dir(dir_path):
    unreal.EditorAssetLibrary.delete_directory(dir_path)


if __name__ == '__main__':
    print('aaaa')