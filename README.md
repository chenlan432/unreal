# unreal
python tools in unreal.

# 设置Autocomplete代码
1. UE中勾选Project Settings里的Developer Mode(all users)，获取stub文件，在[Current Project Directory]/Intermediate/PythonStub下；
2. PyCharm中打开Settings->Project->Python Interpreter->齿轮->Show All...->最右边文件夹层级图标->加号图标->添加stub文件所在的文件夹；
3. Help->Edit Custom Properties，添加idea.max.intellisense.filesize = 25000；

# 同步PyCharm和GitHub
1. 下载Git；
2. PyCharm中Settings->Version Control->Git->Path to Git executable设置Git路径；（如果安装Git是默认路径，则跳过这一步）
3. PyCharm中Settings->Version Control->GitHub->Add account...->Log in via GitHub...登录，修改Connection timeout:30 seconds；
