import unreal
import utils


REGULAR_MESH = ['Tree', 'Grass', 'Wat']


def check_assets():
    assets = utils.get_all_assets('/Game/{}/Art'.format(utils.get_project_name()))
    # assets = utils.get_all_assets('/Game/CodeAxis/Art')
    error_textures = []
    error_static_meshes = []
    settings = utils.load_json('asset_option')

    for asset in assets:
        if isinstance(asset, unreal.Texture2D):
            # [texture_object, error_prop01, error_prop02, ...]
            check_texture(asset, error_textures, settings['Texture2D'])
        elif isinstance(asset, unreal.StaticMesh):
            check_static_meshes(asset, error_static_meshes, settings['StaticMesh'])

    title = 'Check Assets'
    if error_textures:  # or error_static_meshes:
        is_change_properties = pop_up_error(title, error_textures, error_static_meshes)
        if is_change_properties == unreal.AppReturnType.YES:
            change_texture(error_textures, settings['Texture2D'])
            # change_static_mesh(error_static_meshes, settings['StaticMesh'])
    else:
        unreal.EditorDialog.show_message(title, message='All Asset is Okay!', message_type=unreal.AppMsgType.OK)


def pop_up_error(title, error_textures, error_static_meshes):
    error_message = '\n'.join([error_texture[0].get_path_name().rpartition('.')[0]
                               for error_texture in error_textures])
    # error_message += '\n'+'\n'.join([error_static_mesh[0].get_path_name().rpartition('.')[0]
    #                                  for error_static_mesh in error_static_meshes])
    message = 'Problems with these assets:\n\n{}\n\nDo you want to change them? (Only Texture2D)'.format(error_message)
    return unreal.EditorDialog.show_message(title, message, message_type=unreal.AppMsgType.YES_NO)


def check_texture_property(texture, error_texture, setting):
    for prop_name, prop_value in setting.items():
        if not utils.check_property(texture, prop_name, prop_value):
            error_texture.append(prop_name)


def check_texture(asset, error_textures, settings):
    error_texture = [asset]
    texture_type = asset.get_name().rpartition('_')[-1]
    if texture_type in settings:
        check_texture_property(asset, error_texture, settings[texture_type])
    else:
        check_texture_property(asset, error_texture, settings['default'])

    if len(error_texture) > 1:
        error_textures.append(error_texture)


def change_texture_property(texture, props, setting):
    for prop in props:
        prop_value = setting[prop]
        utils.set_property(texture, prop, prop_value)


def change_texture(error_textures, settings):
    for error_texture in error_textures:
        texture = error_texture[0]
        texture_type = utils.get_texture_type(texture)
        props = error_texture[1:]
        if texture_type in settings:
            change_texture_property(texture, props, settings[texture_type])
        else:
            change_texture_property(texture, props, settings['default'])

        unreal.EditorAssetLibrary.save_loaded_asset(texture)


def check_static_meshes_import_data(import_data, error_static_mesh, setting):
    for prop_name, prop_value in setting.items():
        if not utils.check_property(import_data, prop_name, prop_value):
            error_static_mesh.append(prop_name)


def check_static_meshes(static_mesh, error_static_meshes, settings):
    error_static_mesh = [static_mesh]
    static_mesh_import_data = static_mesh.get_editor_property('asset_import_data')
    if utils.get_static_mesh_type(static_mesh) in REGULAR_MESH:
        check_static_meshes_import_data(static_mesh_import_data, error_static_mesh, settings['Regular']['ImportData'])
    else:
        check_static_meshes_import_data(static_mesh_import_data, error_static_mesh, settings['Nanite']['ImportData'])

    if len(error_static_mesh) > 1:
        error_static_meshes.append(error_static_mesh)


def change_static_mesh_import_data(static_mesh, import_data, props, setting):
    for prop_name in props:
        prop_value = setting[prop_name]
        utils.set_property(import_data, prop_name, prop_value)
        static_mesh.set_editor_property('asset_import_data', import_data)


def change_static_mesh(error_static_meshes, settings):
    for error_static_mesh in error_static_meshes:
        static_mesh = error_static_mesh[0]
        static_mesh_type = utils.get_static_mesh_type(static_mesh)
        props = error_static_mesh[1:]
        import_data = static_mesh.get_editor_property('asset_import_data')

        if static_mesh_type in REGULAR_MESH:
            change_static_mesh_import_data(static_mesh, import_data, props, settings['Regular']['ImportData'])
        else:
            change_static_mesh_import_data(static_mesh, import_data, props, settings['Nanite']['ImportData'])

        # unreal.EditorAssetLibrary.save_loaded_asset(static_mesh)