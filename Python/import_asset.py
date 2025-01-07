import unreal


def import_base(fbx_path, unreal_path, asset_name, options=False):
    import_task = unreal.AssetImportTask()

    import_task.set_editor_property('filename', fbx_path)
    import_task.set_editor_property('destination_path', unreal_path)
    import_task.set_editor_property('destination_name', asset_name)
    import_task.set_editor_property('automated', True)
    if options:
        import_task.set_editor_property('options', options)

    unreal.AssetToolsHelpers.get_asset_tools().import_asset_tasks([import_task])
    imported_assets = import_task.get_editor_property('imported_object_paths')

    if not imported_assets:
        unreal.log_warning('No assets were imported!')
        return

    return unreal.load_asset(imported_assets[0])


def import_static_mesh(fbx_path, unreal_path, asset_name, nanite=True):
    # 导入前设置
    options = unreal.FbxImportUI()

    options.set_editor_property('import_mesh', True)
    options.set_editor_property('import_as_skeletal', False)
    options.set_editor_property('import_materials', False)
    options.set_editor_property('import_textures', False)

    data = unreal.FbxStaticMeshImportData()
    data.set_editor_property('auto_generate_collision', False)
    data.set_editor_property('vertex_color_import_option', unreal.VertexColorImportOption.REPLACE)
    data.set_editor_property('build_reversed_index_buffer', True)
    data.set_editor_property('generate_lightmap_u_vs', False)
    data.set_editor_property('one_convex_hull_per_ucx', True)
    data.set_editor_property('combine_meshes', False)
    data.set_editor_property('distance_field_resolution_scale', 1)
    data.set_editor_property('transform_vertex_to_absolute', True)
    data.set_editor_property('normal_import_method', unreal.FBXNormalImportMethod.FBXNIM_IMPORT_NORMALS)
    data.set_editor_property('normal_generation_method', unreal.FBXNormalGenerationMethod.MIKK_T_SPACE)
    data.set_editor_property('compute_weighted_normals', True)
    data.set_editor_property('import_translation', unreal.Vector(0, 0, 0))
    data.set_editor_property('import_rotation', unreal.Rotator(0, 0, 0))
    data.set_editor_property('import_uniform_scale', 1)
    data.set_editor_property('convert_scene', True)
    data.set_editor_property('force_front_x_axis', False)
    data.set_editor_property('convert_scene_unit', True)

    if nanite:
        data.set_editor_property('build_nanite', True)
        data.set_editor_property('import_mesh_lo_ds', False)
    else:
        data.set_editor_property('build_nanite', False)
        data.set_editor_property('import_mesh_lo_ds', True)
        data.set_editor_property('remove_degenerates', True)

    options.set_editor_property('static_mesh_import_data', data)

    static_mesh = import_base(fbx_path, unreal_path, asset_name, options)

    '''
    # 导入后设置
    settings = unreal.EditorStaticMeshLibrary.get_lod_build_settings(static_mesh, 0)
    settings.set_editor_property('use_high_precision_tangent_basis', True)
    settings.set_editor_property('use_full_precision_u_vs', True)
    unreal.EditorStaticMeshLibrary.set_lod_build_settings(static_mesh, 0, settings)
    '''

    return static_mesh


def import_texture(tex_path, unreal_path, tex_name, setting):
    tex = import_base(tex_path, unreal_path, tex_name)
    tex_type = tex_name.rpartition('_')[-1]

    if tex_type in setting:
        for property_name, property_value in setting[tex_type]:
            tex.set_editor_property(property_name, eval(property_value))
    else:
        for property_name, property_value in setting['default']:
            tex.set_editor_property(property_name, eval(property_value))

    '''
    if tex_type in ['D', 'E']:
        tex.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_DEFAULT)
        tex.set_editor_property('srgb', True)
    elif tex_type in ['N']:
        tex.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_NORMALMAP)
        tex.set_editor_property('srgb', False)
        tex.set_editor_property('flip_green_channel', True)
    else:
        tex.set_editor_property('compression_settings', unreal.TextureCompressionSettings.TC_BC7)
        tex.set_editor_property('srgb', False)
    '''

    return tex
