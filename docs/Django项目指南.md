# Django 项目指南

## 初始化项目框架
1. `pip install cookiecutter`, 确保安装基础依赖
2. `cookiecutter git@gitee.com:seatools-py/cookiecutter-seatools-python.git` 通过模板创建项目

## 初始化项目依赖
1. 进入项目根目录, `pip install poetry` 安装`poetry`依赖
2. 使用`poetry` 更新锁 `poetry lock`, 然后安装依赖 `poetry install`
3. 安装`django`相关依赖, `poetry add django==4.0.11 uvicorn[standard]`
4. 使用`seatools-codegen`工具生成`Django`相关基础代码, windows `seatools-codegen.exe django`, linux/mac: `seatools-codegen django` 
注意：该项目支持py3.9~py3.13, 而django5.x需要py3.10以上, 若需要安装django, 需要在第三步修改`pyproject.toml`文件中的`[tool.poetry.dependencies]`下的`python = ">=3.9, <3.13"`, 改为`python = ">=3.10, <3.13"`, 然后执行`poetry lock --no-update`更新依赖锁, 再执行`poetry add django`即可
5. `django`命令工具使用方法`poetry run django` 与 `django` 中的 `python manage.py` 效果一致 
6. 运行, 正式环境: `poetry run django_runserver --host 0.0.0.0 --port 8000 --env pro` (使用`uvicorn`服务器), 开发环境: `poetry run django runserver`

## 项目结构说明
todo:
