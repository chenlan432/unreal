import utils
import re


def rename_assets():
    assets = utils.get_all_assets('/Game/Megascans')
    standard_setup = utils.load_json('asset_option')['Standard']
    fold_dict = {}
    for asset in assets:
        rename_data = utils.get_metadata(asset, 'rename')
        if not rename_data or rename_data != 'Done':
            asset_type = utils.get_asset_type_name(asset)
            asset_setup = standard_setup.get(asset_type, None)

            if asset_setup:
                # e.g: /Game/Megascans/Surfaces/Mossy_Ground_te4efhel/MI_Mossy_Ground_te4efhel.MI_Mossy_Ground_te4efhel
                asset_base_name = asset.get_path_name().split('/')[4].rpartition('_')[0].replace('_', '')
                old_asset_name = asset.get_name()
                old_fold_path = '/'.join(asset.get_path_name().split('/')[:5])
                new_fold_path = '{}/{}/{}'.format(old_fold_path.rpartition('/')[0], asset_base_name,
                                                  standard_setup[asset_type]['folder'])
                match_var = re.search(r'_(Var\d+)_', old_asset_name)
                match_bill = re.search(r'illboard_', old_asset_name)

                asset_name_list = [standard_setup[asset_type]['prefix'], 'Mega', asset_base_name]
                if match_var:
                    asset_name_list.append(match_var.group(1))
                if match_bill:
                    asset_name_list.append('Billboard')
                if asset_type == 'Texture2D':
                    asset_name_list.append(old_asset_name.rpartition('_')[-1])

                utils.move_asset(asset, new_fold_path, '_'.join(asset_name_list))
                utils.set_metadata(asset, 'rename', 'Done')

                if asset_base_name not in fold_dict:
                    fold_dict[asset_base_name] = old_fold_path

    for fold_name, fold_path in fold_dict.items():
        utils.rename_dir(fold_path, '{}/{}'.format(fold_path.rpartition('/')[0], fold_name))
