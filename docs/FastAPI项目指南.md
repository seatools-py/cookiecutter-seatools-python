# FastAPI 项目指南

## 初始化项目框架
1. `pip install cookiecutter`, 确保安装基础依赖
2. `cookiecutter git@gitee.com:seatools-py/cookiecutter-seatools-python.git` 通过模板创建项目

## 初始化项目依赖
1. 进入项目根目录, `pip install poetry` 安装`poetry`依赖
2. 使用`poetry` 更新锁 `poetry lock`, 然后安装依赖 `poetry install`
3. 安装`fastapi`相关依赖, `poetry add fastapi uvicorn[standard]`
4. 使用`seatools-codegen`工具生成`fastapi`相关基础代码, windows `seatools-codegen.exe fastapi`, linux/mac: `seatools-codegen fastapi`
5. 运行, `poetry run fastapi --host 0.0.0.0 --port 8000 --env pro`

## 细节
具体可见[`cookiecutter-seatools-python-codegen`](https://gitee.com/seatools-py/cookiecutter-seatools-python-codegen)文档


## 项目结构说明
todo: