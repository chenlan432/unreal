import unreal
import utils


MENUS = {
    # 主菜单
    'LevelEditor.MainMenu': (
        {
            'name': 'CROS Tools',
            'section': 'new_section',
            'tip': 'this is a tool menu for project {}'.format(utils.get_project_name()),
            'type': 'menu',
            'sub': (
                {
                    'name': 'Check Assets',
                    'section': 'check',
                    'type': 'menu',
                    'sub': (
                        {
                            'name': 'Check All',
                            'section': 'check',
                            'type': 'entry',
                            'func': 'check_asset.check_assets_all()'
                        },
                        {
                            'name': 'Check Current',
                            'section': 'check',
                            'type': 'entry',
                            'func': 'check_asset.check_asset_current()'
                        }
                    )
                },
            )
        },
    )
}


def convert_component(component):
    if 'section' not in component:
        component['section'] = ''
    if 'label' not in component:
        component['label'] = ' '.join(component['name'].split('_')).title()
    if 'tip' not in component:
        component['tip'] = ''


def add_menu(parent_menu, component):
    new_menu = parent_menu.add_sub_menu(
        parent_menu.get_name(), component['section'], component['name'], component['label'], component['tip']
    )
    add_component(new_menu, component['sub'])


def add_entry(parent_menu, component):
    entry = unreal.ToolMenuEntry(
        name=component['name'],
        type=unreal.MultiBlockType.MENU_ENTRY,
        insert_position=unreal.ToolMenuInsert('', unreal.ToolMenuInsertType.DEFAULT)
    )
    entry.set_label(component['label'])
    entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, 'Name', component['func'])
    parent_menu.add_menu_entry(component['section'], entry)


def add_component(parent_menu, menu_tuple):
    for component in menu_tuple:
        convert_component(component)
        if component['type'] == 'menu':
            add_menu(parent_menu, component)
        elif component['type'] == 'entry':
            add_entry(parent_menu, component)


def add_menus():
    menus = unreal.ToolMenus.get()

    for main_menu_names, menu_tuple in MENUS.items():
        main_menu = menus.find_menu(main_menu_names)
        add_component(main_menu, menu_tuple)

    menus.refresh_all_widgets()
