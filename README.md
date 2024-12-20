# cookiecutter-seatools-python

## 项目地址:
1. https://github.com/seatools-py/cookiecutter-seatools-python
2. https://gitee.com/seatools-py/cookiecutter-seatools-python

## Seatools 工具包地址
1. https://github.com/seatools-py/seatools
2. https://gitee.com/seatools-py/seatools


## 使用方法
1. 安装python3.9+ (省略)
2. 安装cookiecutter: `pip install cookiecutter`
3. 使用该模板生成项目: `cookiecutter git@gitee.com:seatools-py/cookiecutter-seatools-python.git`
4. 通过查看生成项目的`README.md`文件了解具体操作与使用方式


## cookiecutter-seatools-python 是什么？
### 一个基于 `cookiecutter` 的 `python` 项目模板, 项目基于 `poetry` 与 [`seatools`](https://gitee.com/dragons96/seatools.git) IOC框架, 支持如下功能:
1. IOC支持(基于[`seatools`](https://gitee.com/dragons96/seatools.git), 与`Java Spring`类似, 可用于解决复杂系统中的依赖混乱, 循环依赖等问题, 灵活易用, 提供`starter`机制可自行拓展)
2. cmd工具(基于`click`)
3. web服务(可任选`fastapi`, `flask`, `django`), 也可多个`web`同时使用
4. 数据库(支持`sqlalchemy`+[`mysql`|`postgresql`|`clickhouse`|`hive`|`impala`|...], 提供`sqlalchemy`便捷操作工具), 提供启动器：[`seatools-starter-sqlalchemy`](https://gitee.com/seatools-py/seatools-starter-sqlalchemy)
5. Redis(支持`redis`), 提供启动器：[`seatools-starter-redis`](https://gitee.com/seatools-py/seatools-starter-redis)
6. 爬虫(支持`scrapy`, [`undetected-chromedriver`(基于selenium的抹除指纹自动化框架)](https://github.com/ultrafunkamsterdam/undetected-chromedriver))
7. 缓存(基于`cachetools`), 提供启动器：[`seatools-starter-cache`](https://gitee.com/seatools-py/seatools-starter-cache)
8. 自动配置管理(配置文件内容通过在`model`中定义属性将自动注入)
9. 多环境管理(`dev`, `test`, `pro`)
10. 统一日志(基于`loguru`, 对常用组件[`uvicorn`, `sqlalchemy`]等`logging`模块做了`loguru`序列化格式适配)
11. 测试(使用`pytest`)
12. 提供相应代码生成器套件[`seatools-codegen`](https://gitee.com/seatools-py/cookiecutter-seatools-python-codegen), 具体支持功能如下:  
    1. 生成自定义任务类模板, 生成自定义任务类针对任务描述, 日志, 异常等常用操作提供的内置的处理  
    2. 生成自定义命令行入口, 生成命令行模板、执行脚本以及docker相关部署脚本 
    3. 生成`web`(`fastapi`, `flask`, `django`)、`scrapy`模板代码, 支持多种框架集成
13. grpc拓展

### 部署打包支持
1. 支持 `windows`, `linux`, `mac` 多平台的`python`环境运行或使用`pyinstaller`打包后运行
2. 支持 `docker`, `docker-compose`, `k8s` 部署

## 为什么选择 cookiecutter-seatools-python？
1. 完善统一标准的项目结构, 提供各场景的开发规范与指南, 使得项目易于开发与维护
2. 提供配置管理、多环境、日志管理以及代码生成工具等基础建设，大幅度缩减开发成本，提高开发效率
3. 提供执行脚本、部署脚本的自动生成工具，大幅度减少部署过程的时间成本
4. 针对常用框架提供了适配的日志组件与集成方式，使得系统的维护与监控变的更加容易
5. 轻量, 遵从最小化依赖原则, 仅内置项目运行必备的依赖

## 各场景指南
- [`常规脚本项目指南`](./docs/常规脚本任务场景.md)
- [`Django项目指南`](./docs/Django项目指南.md)
- [`FastAPI项目指南`](./docs/FastAPI项目指南.md)
- [`Flask项目指南`](./docs/Flask项目指南.md)
- [`Scrapy项目指南`](./docs/Scrapy项目指南.md)
- [`SqlAlchemy数据库使用指南`](./docs/SqlAlchemy数据库使用指南.md)
- [`Redis使用指南`](./docs/Redis使用指南.md)

#### 简而言之，`cookiecutter-seatools-python` 模板项目提供了从[开发->测试->部署->维护/监控]一整套流程的支持与优化, 墙裂推荐!!!
