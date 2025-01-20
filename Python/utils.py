import unreal
import os
import json


# 获取项目信息
def get_project_dir():
    return unreal.Paths.project_dir()


def get_project_name():
    return get_project_dir().split('/')[-2]


def get_content_dir():
    return unreal.Paths.project_content_dir()


# 资产相关操作
def get_selected_assets():
    return unreal.EditorUtilityLibrary.get_selected_assets()


def get_all_assets(dir_path='/Game'):
    return list(map(unreal.EditorAssetLibrary.load_asset, unreal.EditorAssetLibrary.list_assets(dir_path)))


def get_selected_asset_data():
    return unreal.EditorUtilityLibrary.get_selected_asset_data()


def does_asset_exist(asset_path):
    return unreal.EditorAssetLibrary.does_asset_exist(asset_path)


def load_asset(asset_path):
    return unreal.EditorAssetLibrary.load_asset(asset_path)


def set_metadata(asset, data_name, data_value):
    unreal.EditorAssetLibrary.set_metadata_tag(asset, data_name, data_value)


def get_metadata(asset, data_name):
    return unreal.EditorAssetLibrary.get_metadata_tag(asset, data_name)


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


# 材质相关
def create_mic(parent_material, name):
    return unreal.BlueprintMaterialTextureNodesBPLibrary.create_mic_editor_only(parent_material, name)


def set_mic_parm_value(mic, parm_name, parm_value, association=unreal.MaterialParameterAssociation.GLOBAL_PARAMETER):
    if parm_name == 'Blend Mode':
        unreal.BlueprintMaterialTextureNodesBPLibrary.set_mic_blend_mode_editor_only(mic, eval(parm_value))
    elif parm_name == 'Two Sided':
        unreal.BlueprintMaterialTextureNodesBPLibrary.set_mic_two_sided_editor_only(mic, parm_value)
    elif isinstance(parm_value, unreal.RuntimeVirtualTexture):
        unreal.MaterialEditingLibrary.set_material_instance_runtime_virtual_texture_parameter_value(mic, parm_name,
                                                                                                    parm_value,
                                                                                                    association)
    elif isinstance(parm_value, float):
        unreal.MaterialEditingLibrary.set_material_instance_scalar_parameter_value(mic, parm_name, parm_value,
                                                                                   association)
    elif isinstance(parm_value, unreal.SparseVolumeTexture):
        unreal.MaterialEditingLibrary.set_material_instance_sparse_volume_texture_parameter_value(mic, parm_name,
                                                                                                  parm_value,
                                                                                                  association)
    elif isinstance(parm_value, bool):
        unreal.MaterialEditingLibrary.set_material_instance_static_switch_parameter_value(mic, parm_name, parm_value,
                                                                                          association)
    elif isinstance(parm_value, unreal.Texture):
        unreal.MaterialEditingLibrary.set_material_instance_texture_parameter_value(mic, parm_name, parm_value,
                                                                                    association)
    elif isinstance(parm_value, unreal.LinearColor):
        unreal.MaterialEditingLibrary.set_material_instance_vector_parameter_value(mic, parm_name, parm_value,
                                                                                   association)


def get_mic_parm_value(mic, parm_name, parm_type, association=unreal.MaterialParameterAssociation.GLOBAL_PARAMETER):
    if isinstance(parm_type, unreal.RuntimeVirtualTexture):
        return unreal.MaterialEditingLibrary.get_material_instance_runtime_virtual_texture_parameter_value(mic,
                                                                                                           parm_name,
                                                                                                           association)
    elif isinstance(parm_type, float):
        return unreal.MaterialEditingLibrary.get_material_instance_scalar_parameter_value(mic, parm_name, association)
    elif isinstance(parm_type, unreal.SparseVolumeTexture):
        return unreal.MaterialEditingLibrary.get_material_instance_sparse_volume_texture_parameter_value(mic, parm_name,
                                                                                                         association)
    elif isinstance(parm_type, bool):
        return unreal.MaterialEditingLibrary.get_material_instance_static_switch_parameter_value(mic, parm_name,
                                                                                                 association)
    elif isinstance(parm_type, unreal.Texture):
        return unreal.MaterialEditingLibrary.get_material_instance_texture_parameter_value(mic, parm_name, association)
    elif isinstance(parm_type, unreal.LinearColor):
        return unreal.MaterialEditingLibrary.get_material_instance_vector_parameter_value(mic, parm_name, association)


def get_material_parm_names(material, parm_type):
    if isinstance(parm_type, float):
        return unreal.MaterialEditingLibrary.get_scalar_parameter_names(material)
    elif isinstance(parm_type, bool):
        return unreal.MaterialEditingLibrary.get_static_switch_parameter_names(material)
    elif isinstance(parm_type, unreal.Texture):
        return unreal.MaterialEditingLibrary.get_texture_parameter_names(material)
    elif isinstance(parm_type, unreal.LinearColor):
        return unreal.MaterialEditingLibrary.get_vector_parameter_names(material)


def update_material_instance(material):
    unreal.MaterialEditingLibrary.update_material_instance(material)


# Actor相关操作
def get_selected_actors():
    return unreal.EditorActorSubsystem().get_selected_level_actors()


def delete_actor(actor):
    unreal.EditorLevelLibrary.destroy_actor(actor)


def create_actor(source_asset_path, position=unreal.Vector(), rotation=unreal.Rotator()):
    return unreal.EditorLevelLibrary.spawn_actor_from_object(load_asset(source_asset_path), position, rotation)


def get_static_mesh_asset(static_mesh_actor):
    return static_mesh_actor.get_editor_property('static_mesh_component').get_editor_property('static_mesh')


def set_overlay_material(mesh_actor, material_asset):
    mesh_actor.get_editor_property('static_mesh_component').set_overlay_material(material_asset)


# 视图相关操作
def get_viewport_camera_matrix():
    editor_system = unreal.UnrealEditorSubsystem
    cam_location, cam_rotation = editor_system.get_level_viewport_camera_info()

    if [cam_location, cam_rotation] is None:
        return None

    camera_transform = cam_rotation.transform()
    camera_transform.translation = cam_location

    return camera_transform


# 其他
def load_json(json_name):
    json_path = '{}/{}.json'.format(os.path.dirname(__file__), json_name)
    with open(json_path, 'r') as f:
        f_string = f.read()
    return json.loads(f_string)


def dump_json(json_name, data, json_path=None):
    json_path = json_path or '{}/{}.json'.format(os.path.dirname(__file__), json_name)
    with open(json_path, 'w') as json_file:
        # noinspection PyTypeChecker
        json.dump(data, json_file, sort_keys=True, indent=4, separators=(',', ': '))


def create_dict(d, val, *parm):
    if len(parm) == 1:
        d[parm[0]] = val
        return d
    else:
        if not d.get(parm[0]):
            d[parm[0]] = {}
        create_dict(d[parm[0]], val, *parm[1:])


# 根据命名风格的一些操作
def get_static_mesh_type(static_mesh):
    return static_mesh.get_name().split('_')[1]


def get_texture_type(texture):
    return texture.get_name().rpartition('_')[-1]


def get_asset_type_name(asset):
    return asset.get_full_name().split(' ')[0]


# 文件操作
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