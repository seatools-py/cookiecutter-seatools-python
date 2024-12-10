# Redis使用指南

## 初始化项目框架
1. `pip install cookiecutter`, 确保安装基础依赖
2. `cookiecutter git@gitee.com:seatools-py/cookiecutter-seatools-python.git` 通过模板创建项目

## 初始化项目依赖
1. 进入项目跟目录, `pip install poetry` 安装`poetry`依赖
2. 使用`poetry`更新锁`poetry lock`, 然后安装依赖 `poetry install`

## 应用
1. 使用`seatools-starter-redis`, 安装`poetry add seatools-starter-redis`, 具体使用方式以[`seatools-starter-redis`](https://gitee.com/seatools-py/seatools-starter-redis)为准, 可能会存在更新
2. 在生成的项目的`config/application[-dev|test|pro].yml`任一当前环境的文件中配置数据库, 以`config/application.yml`为例示例如下:
```yaml
seatools:
  redis:
    host: localhost
    port: 6379
    password: 123456
    database: 0
    # redis.Redis.from_url的额外配置
    config:
      decode_responses: true
```
3. 使用方式
```python
from {{cookiecutter.package_name}}.boot import start
from seatools.ioc import Autowired
from redis import Redis

start() # 启动ioc

# 自动装载
r = Autowired(cls=Redis)

r.set(...)
r.get(...)


```