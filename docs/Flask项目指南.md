# Flask 项目指南

## 初始化项目框架
1. `pip install cookiecutter`, 确保安装基础依赖
2. `cookiecutter git@gitee.com:seatools-py/cookiecutter-seatools-python.git` 通过模板创建项目

## 初始化项目依赖
1. 进入项目根目录, `pip install poetry` 安装`poetry`依赖
2. 使用`poetry` 更新锁 `poetry lock`, 然后安装依赖 `poetry install`
3. 安装`flask`相关依赖, `poetry add flask uvicorn[standard]`
4. 使用`seatools-codegen`工具生成`flask`相关基础代码, windows `seatools-codegen.exe flask`, linux/mac: `seatools-codegen flask`
5. 运行, `poetry run flask --host 0.0.0.0 --port 8000 --env pro`

## 项目结构说明
todo:
