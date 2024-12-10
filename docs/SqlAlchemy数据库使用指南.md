# SqlAlchemy数据库使用指南

## 初始化项目框架
1. `pip install cookiecutter`, 确保安装基础依赖
2. `cookiecutter git@gitee.com:seatools-py/cookiecutter-seatools-python.git` 通过模板创建项目

## 初始化项目依赖
1. 进入项目根目录, `pip install poetry` 安装`poetry`依赖
2. 使用`poetry` 更新锁 `poetry lock`, 然后安装依赖 `poetry install`

## 应用
1. 使用`seatools-starter-sqlalchemy`, 安装`poetry add seatools-starter-sqlalchemy`即可，具体使用方式以[`seatools-starter-sqlalchemy`](https://gitee.com/seatools-py/seatools-starter-sqlalchemy)为准, 可能会存在更新
2. 在生成的项目的`config/application[-dev|test|pro].yml`任一当前环境的文件中配置数据库, 以`config/application.yml`为例使用`pymysql`驱动配置`mysql`, 安装`poetry add pymysql`, 示例如下:
```yaml
# starter sqlalchemy 配置名称
seatools:
  datasource:
    # ioc bean 名称
    test_db:
      host: 127.0.0.1
      port: 3306
      user: root
      password: 123456
      database: test_db
      # 驱动, 对应sqlalchemy的schema, 例如: sqlite, sqlite+aiosqlite, mysql+pymysql, mysql+aiomysql等等
      driver: mysql+pymysql
      primary: false # 是否默认
      is_async: false # 当driver为异步驱动时, 该值需要设置为true
```
3. 使用方式
```python
from {{cookiecutter.package_name}}.boot import start
from seatools.sqlalchemy.decorators.ioc import new_session
from seatools.sqlalchemy import SqlAlchemyClient
from seatools.ioc import Autowired
from sqlalchemy.orm import Session


@new_session('test_db') # 只有一个db可以不填, 直接 @new_session 或者 @new_session() 均可
def do_anything(session: Session):
    ...


if __name__ == '__main__':
    start() # 启动ioc
    do_anything() # 无需传递session参数, session参数通过装饰器处理
    # 若要获取sqlalchemy engine可通过以下方式获取
    client = Autowired('test_db', cls=SqlAlchemyClient) # 若只有一个db可省略名称, 直接 Autowired(cls=SqlAlchemyClient) 即可
    client.engine() # 获取sqlalchemy引擎
    # 获取session, 该方式较为繁琐, 更推荐使用 seatools.sqlalchemy.decorators.ioc.new_session 或者 seatools.sqlalchemy.decorators.ioc.auto_session 装饰器
    with client.session() as session:
        ...
```
注意: 配置中的`driver`支持配置异步数据库引擎, 配置异步数据库引擎时, @new_session注入的不再是`sqlalchemy.orm.Session` 而是`sqlalchemy.ext.asyncio.AsyncSession`
