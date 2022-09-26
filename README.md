# unreal
python tools in unreal.

# 设置Autocomplete代码
1. UE中勾选Project Settings里的Developer Mode(all users)，获取stub文件，在[Current Project Directory]/Intermediate/PythonStub下；
2. PyCharm中打开Settings->Project->Python Interpreter->齿轮->Show All...->最右边文件夹层级图标->加号图标->添加stub文件；
3. Help->Edit Custom Properties，添加idea.max.intellisense.filesize = 25000；
