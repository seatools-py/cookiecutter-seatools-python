# Scrapy 项目指南

## 初始化项目框架
1. `pip install cookiecutter`, 确保安装基础依赖
2. `cookiecutter git@gitee.com:seatools-py/cookiecutter-seatools-python.git` 通过模板创建项目

## 初始化项目依赖
1. 进入项目根目录, `pip install poetry` 安装`poetry`依赖
2. 使用`poetry` 更新锁 `poetry lock`, 然后安装依赖 `poetry install`
3. 安装`scrapy`相关依赖, `poetry add scrapy`
4. 使用`seatools-codegen`工具生成`Scrapy`相关基础代码, windows `seatools-codegen.exe scrapy init`, linux/mac: `seatools-codegen scrapy init` 
5. 使用`seatools-codegen`工具生成`Scrapy Spider`爬虫模板代码, windows `seatools-codegen.exe scrapy genspider [name] [domain]`, linux/mac: `seatools-codegen scrapy genspider [name] [domain]`, 示例 `seatools-codegen.exe scrapy genspider quotes quotes.toscrape.com`
6. 运行, `poetry run [name]`即可运行`seatools-codegen`工具生成的爬虫

## 项目结构说明
todo:
