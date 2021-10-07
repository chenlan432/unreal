import unreal


def add_menu():
    menus = unreal.ToolMenus.get()
    main_menu = menus.find_menu('LevelEditor.MainMenu')  # 获取菜单控件
    added_menu = main_menu.add_sub_menu(main_menu.get_name(), 'new_menu', 'a', 'b')

    menus.refresh_all_widgets()
