# {{ cookiecutter.friendly_name }}

### 项目仓库地址: https://{{cookiecutter.git_type}}.com/{{cookiecutter.git_user}}/{{ cookiecutter.project_name }}

## 安装依赖
1. pip install poetry
2. poetry lock
3. 开发环境安装依赖：poetry install (若出现哪个包安装不了先单独pip install 某个包再执行poetry install)
4. 正式环境安装依赖：poetry install --only main (若出现哪个包安装不了先单独pip install 某个包再执行poetry install)
5. 需要安装新增的依赖, 以sqlalchemy为例, `poetry add sqlalchemy`
6. 安装的依赖仅本地环境需要而正式环境不需要则可使用--group dev参数, 以pyinstaller为例, `poetry add --group dev pyinstaller`

## 运行
1. 示例方法, `poetry run main`

## 实践指南
前置步骤:
1. 初始化更新poetry lock, `poetry lock`
2. 安装poetry依赖, `poetry install`

开发细节：
1. 推荐使用[`httpx`](https://www.python-httpx.org/)代替`requests`, `httpx`支持`async`, API与`requests`相似, 替换需要注意的事项:
   1. `httpx`请求`timeout`默认是`5s`超时, `requests` 默认不超时
   2. `httpx`请求默认不会自动重定向, 重定向需要增加`follow_redirects=True`参数, `requests`默认自动重定向
2. 推荐使用`sqlalchemy` + `sqlacodegen_v2` + `数据库驱动` 代替各数据库特定包, 使用统一的API便于管理、维护与迁移, 数据库表`Model`(继承`seatools.sqlalchemy.Base`)代替`sqlalchemy`的`declarative_base`, `seatools.sqlalchemy.Base` 提供了基础通用数据库操作以及字典, `pydantic Model`转换的方法
3. 推荐使用自定义`Model`(继承`seatools.models.BaseModel`) 代替各种`dict`字典, 业务上频繁使用`dict`不直观难以维护

### 任务类脚本
1. 执行生成任务命令, `seatools-codegen task --class DemoTask --name 示例任务`, 将会生成`src/{{cookiecutter.package_name}}/tasks/demo_task.py`文件, 此处编写任务逻辑
2. 执行生成CMD命令, `seatools-codegen cmd --name demo`, 将会在`src/{{cookiecutter.package_name}}/cmd/demo_main.py`文件, 此处编写命令逻辑
3. 编辑`src/{{cookiecutter.package_name}}/tasks/demo_task.py`任务文件:
```python
... # 省略

class DemoTask(Task):

    def _run(self, *args, **kwargs):
        # 编辑任务逻辑
        self._logger.info('示例任务执行')

... # 省略
```
4. 编辑`src/{{cookiecutter.package_name}}/cmd/demo_main.py`CMD入口文件:
```python
... # 省略

def main(project_dir: Optional[str] = None,
         env: Optional[str] = 'dev',
         log_level: Optional[str] = 'INFO') -> None:
    ... # 省略

    # 执行任务
    from {{cookiecutter.package_name}}.tasks.demo_task import DemoTask
    DemoTask().run()

... # 省略
```
5. 运行, 支持多种方式如下:
```shell
# 方式1
poetry run demo --env [dev|test|pro]
# 方式2
sh bin/demo.sh --env [dev|test|pro]
bash bin/demo.sh --env [dev|test|pro]
# 方式3 docker-compose
docker-compose up demo
```
6. 部署:
```shell
# 1. 服务器拉取代码并安装python>=3.9环境
# 2. 执行命令安装虚拟环境及依赖
bash bin/install.sh
# 3. 运行
bash bin/demo.sh
```
7. [可选]打包
```shell
poetry add --group dev pyinstaller

# 打包
poetry run pyinstaller --onefile "./src/{{cookiecutter.package_name}}/cmd/demo_main.py"
# 运行
./dist/demo_main --project_dir . --env [dev|test|pro]
```

### Web服务 (以fastapi为例)
1. 执行生成`fastapi`代码命令, `seatools-codegen fastapi`
2. fastapi相关组件位于 `src/{{cookiecutter.package_name}}/fastapi/`, 入口CMD位于`src/{{cookiecutter.package_name}}/cmd/fastapi_main.py`
3. 启动项目: `poetry run fastapi`
4. 访问`http://localhost:8000`, 返回`Hello {{ cookiecutter.project_name }} by FastAPI!` 则说明运行成功
5. 服务器运行:
```shell
# 方式1
# 其中 --port 指定应用端口, --workers 工作进程数
nohup poetry run fastapi --env [dev|test|pro] --port 8000 --workers 1 >> demo.log &
# 方式2
sh bin/fastapi.sh --env [dev|test|pro]  --port 8000 --workers 1
bash bin/fastapi.sh --env [dev|test|pro]  --port 8000 --workers 1
# 方式3 docker-compose
docker-compose up -d fastapi
```
6. 部署:
```shell
# 1. 服务器拉取代码并安装python>=3.9环境
# 2. 执行命令安装虚拟环境及依赖
bash bin/install.sh
# 3. 运行
bash bin/demo.sh
```

## 新增 CMD 命令
该操作会生成基于`poetry`的CMD命令, sh脚本, Dockerfile配置, docker-compose配置
1. 生成`poetry`命令: `seatools-codegen cmd --name {name}`, 示例如下:
```shell
seatools-codegen cmd --name hello

# 将会在 src/{{ cookiecutter.package_name }}/cmd 目录下生成 hello_main.py 文件

# 执行hello命令
poetry run hello
# 执行脚本执行
sh bin/hello.sh
bash bin/hello.sh
# 使用docker-compose打包运行, 仅执行hello服务
docker-compose up hello
# docker-compose后台运行
docker-compose up -d hello
```

## FastAPI 配置
1. 生成模板代码: `seatools-codegen fastapi`
2. 安装相关依赖: `poetry add fastapi uvicorn[standard]`
3. 运行 `poetry run fastapi`, 对应 `src/{{ cookiecutter.package_name }}/cmd/fastapi_main.py`

## Flask 配置
1. 生成模板代码: `seatools-codegen flask`
2. 安装相关依赖: `poetry add flask uvicorn[standard]`
3. 运行 `poetry run flask`, 对应 `src/{{ cookiecutter.package_name }}/cmd/flask_main.py`

## Django 配置
1. 生成模板代码: `seatools-codegen django`
2. 安装相关依赖: `poetry add django==4.2.11` (由于django>=5.0需要python>=3.10, 若要安装django5.x版本需要修改`pyproject.toml`中的`python = ">=3.9, <3.13"`改成`python = ">=3.10, <3.13"`然后`poetry lock`后再安装即可)
3. 运行 `poetry run django_runserver` 启动django生产级服务, 对应 `src/{{ cookiecutter.package_name}}/cmd/django_main.py`
4. 运行django命令用法: `poetry run django "{runserver|createsuperuser|migrate|...} ..."`, 对应 `src/{{ cookiecutter.package_name}}/cmd/django_cmd.py`


## Grpc 配置
1. 在`src`目录下新建`proto`目录编写`*.proto`文件
2. 安装相关依赖: `poetry add grpcio grpcio-tools`
3. 生成模板及pb2文件命令: `seatools-codegen grpc --pyi` (其中`--pyi`参数非必须, 不传该参数将不会生成对应的`.pyi`文件)
4. 生成的代码均在`src/{{cookiecutter.package_name}}/grpc`下, 建议grpc相关依赖逻辑在该包下完成, `pb2`文件在`src/{{cookiecutter.package_name}}/grpc/proto`包下

## Scrapy 配置
1. 生成模板代码: `seatools-codegen scrapy init`
2. 安装相关依赖: `poetry add scrapy`
- 生成xxx爬虫: `seatools-codegen scrapy genspider {name} {domain}`, 该命令生成的Spider在`src/{{ cookiecutter.package_name}}/scrapy/spiders`下, 同时会生成可执行的cmd文件`src/{{ cookiecutter.package_name}}/cmd/{name}.py`
- 执行xxx爬虫: `poetry run {name} --env [dev|test|pro]`, 部署执行`bash bin/{name}.sh` 或者`docker`执行, 具体参考上文`新增 CMD 命令`
3. 使用其他的scrapy命令 `poetry run scrapy {shell|...} ...`

## Chrome 配置
1. 查询`chrome`/`chromedriver`版本: `seatools-chrome list`
2. 下载指定系统版本的`chrome`: `seatools-chrome downlaod --type chrome --version 128.0.6613.84 --system win64`, (下载路径为当前项目路径/extensions)
3. 下载指定系统版本的`chromedriver`: `seatools-chrome download --type chromedriver --version 128.0.6613.84 --system win64`
4. 更多下载参数说明可使用`-h`参数: `seatools-chrome download -h`

**PS: 使用自动化工具推荐使用`undetected-chromedriver`代替`selenium`**

## 任务生成
1. 生成任务代码: `seatools-codegen task --task_class xxx --task_name 示例任务 [--async]`
- task_class: 任务类名
- task_name: 任务名称
- async[可选]: 是否生成async的任务

## 环境变量
1. PROJECT_DIR: 项目路径, 通常无需设置, pyinstaller打包后需设置
2. `seatools`包提供的ENV: 当前环境, dev=开发环境, test=测试环境, pro=生产环境

## 项目结构说明
1. `bin/`: 项目运行脚本
2. `config/`: 项目配置文件
3. `docs/`: 项目文档
4. `src/`: 项目源码
5. `src/{{cookiecutter.package_name}}`: 项目源码主包, 所有代码均放在该包下
6. `src/{{cookiecutter.package_name}}/cmd`: 代码命令行入口
7. `src/{{cookiecutter.package_name}}/config/`: 配置信息, 默认仅包含路径配置
8. `tests/`: 测试代码

## 功能说明
### 1.配置管理
1. 在 `config/application.yml` 或 `config/application-[dev|test|pro].yml`对应环境的文件中配置内容, 以如下`application.yml`为例:
```yaml
mysql:
  host: 127.0.0.1
  port: 3306
  user: root
  password:
  db: test_db
```
2. 在`src/{{ cookiecutter.package_name }}` 下创建 `models.py` 文件, 代码如下:
```python
from seatools.models import
```

### 2. DB支持
内置基于sqlalchemy2.x支持, 使用步骤如下(以mysql为例, 其他同理):
1. 在 `src/{{ cookiecutter.package_name }}/boot/ioc.py` 文件新增db的`starter`:
```python
from seatools import ioc
from {{ cookiecutter.package_name }}.config import get_config_dir


def ioc_starter():
    # 运行ioc
    ioc.run(scan_package_names=[
        'seatools.ioc.starter.sqlalchemy', # 自动装载db bean实例
        '{{cookiecutter.package_name}}'
    ],
            config_dir=get_config_dir(),
            # 需要过滤扫描的模块, 示例: {{ cookiecutter.package_name }}.xxx
            exclude_modules=[])

```
2. 在配置文件 `config/application.yml` 或 环境配置文件 `config/application-{env}.yml` 中添加如下配置:
```yaml
# ...省略无用配置

db:
  # 这里要与 MultiDBConfig 中配置的变量名一致
  mysql_test_db:
    host: 127.0.0.1
    port: 3306
    user: root
    password: 123456
    db: test_db
```
3. 操作数据库:
```python
from {{ cookiecutter.package_name }}.boot import start
from seatools.sqlalchemy.utils import new_client
from sqlalchemy import text
from {{ cookiecutter.package_name }}.config import cfg

# 启动依赖
start()

"""
推荐方式, 装饰器
auto_session 与 new_session区别

auto_session: 同一线程和同一协程中session保持一致性
new_session: 每次都是新建一个session
"""
from seatools.sqlalchemy.decorators.ioc import auto_session, new_session
from sqlalchemy.orm import Session


@auto_session(db="mysql_test_db") # 名称与配置一致, 只有一个db或者primary=true可省略 @auto_session() 或 @auto_session
def xxx(session: Session):
    data = session.execute(text('select 1')).all()

# 调用
xxx()


@new_session(db="mysql_test_db") # 名称与配置一致, 只有一个db或者primary=true可省略 @auto_session() 或 @auto_session
def yyy(session: Session):
    data = session.execute(text('select 1')).all()

# 调用
yyy()

# new_client的参数为配置属性与sqlalchemy配置 该方式不再推荐
with new_client(cfg().db.mysql_test_db, cfg().sqlalchemy).session() as session:
    # 这里获取的session对象就是 sqlalchemy 的 session 对象, 按照sqlalchemy 的 session 使用方式操作数据库即可
    data = session.execute(text('select 1')).all()
```
4. 安装`sqlacodegen_v2`来生成数据库模型, `poetry add --group dev sqlacodegen_v2`
5. 使用`sqlacodegen_v2`生成数据库模型, 命令如下:
```shell
# 生成完成之后注意检查文件编码是否为utf-8, 若不是则需要将文件转换为utf-8
sqlacodegen mysql://root:123456@127.0.0.1:3306/test_db --outfile ./src/{{cookiecutter.package_name}}/models/db/test_db.py
```
6. 修改`/src/{{cookiecutter.package_name}}/models/db/test_db.py`文件中的`Base`类, 改为使用`from seatools.sqlalchemy import Base`提供的`Base`, 该`Base`类提供了与字典, `pydantic model`相互转化的方法


## 拓展
本项目集成[seatools](https://gitee.com/dragons96/seatools)工具框架

## 部署
1. 确保环境变量存在一个python3.9+的环境
2. 执行 `sh bin/install.sh` 安装当前项目环境
3. 执行脚本 `sh bin/main.sh` 或其他自定义命令运行项目

## 打包
PS: `ioc` 模式需要额外添加相关依赖, 待更新
### 一、使用pyinstaller打包
安装 `poetry add -D pyinstaller`
#### 1. 打包普通命令行任务
1. 打包, `pyinstaller --onefile ./src/{{cookiecutter.package_name}}/cmd/main.py --name {{cookiecutter.project_name}}`
2. 运行, `./dist/{{cookiecutter.project_name}}.exe --project_dir .` 或 `./dist/{{cookiecutter.project_name}} --project_dir .`
#### 2. 打包FastAPI命令行任务
1. 打包, `pyinstaller --onefile ./src/{{cookiecutter.package_name}}/cmd/fastapi_main.py --hidden-import "{{cookiecutter.package_name}}.fastapi.app" --name fastapi_{{cookiecutter.project_name}}`
2. 运行, `./dist/fastapi_{{cookiecutter.project_name}}.exe --project_dir .` 或 `./dist/fastapi_{{cookiecutter.project_name}} --project_dir .` (更多参数执行`./dist/fastapi_{{cookiecutter.project_name}}.exe -h` 或 `./dist/fastapi_{{cookiecutter.project_name}} -h`)
#### 3. 打包Flask命令行任务
1. 打包, `pyinstaller --onefile ./src/{{cookiecutter.package_name}}/cmd/flask_main.py --hidden-import "{{cookiecutter.package_name}}.flask.app" --name flask_{{cookiecutter.project_name}}`
2. 运行, `./dist/flask_{{cookiecutter.project_name}}.exe --project_dir .` 或 `./dist/flask_{{cookiecutter.project_name}} --project_dir .` (更多参数执行`./dist/flask_{{cookiecutter.project_name}}.exe -h` 或 `./dist/flask_{{cookiecutter.project_name}} -h`)
