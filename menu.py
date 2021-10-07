import unreal


def add_menu():
    menus = unreal.ToolMenus.get()
    main_menu = menus.find_menu('LevelEditor.MainMenu')  # 获取菜单控件
    added_menu = main_menu.add_sub_menu(main_menu.get_name(), 'new_menu', 'a', 'b')

    entry = unreal.ToolMenuEntry(
        name='entry_name',
        type=unreal.MultiBlockType.MENU_ENTRY,
        insert_position=unreal.ToolMenuInsert('', unreal.ToolMenuInsertType.DEFAULT)
    )
    entry.set_label('entry_label')
    entry.set_string_command(unreal.ToolMenuStringCommandType.PYTHON, 'command_name', 'print("aaa")')

    added_menu.add_menu_entry('section_name', entry)

    menus.refresh_all_widgets()
