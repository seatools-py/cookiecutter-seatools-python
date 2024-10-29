from typing import Optional
from seatools.models import BaseModel


class CommonDBConfig(BaseModel):
    """通用 DB 配置"""
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    db: Optional[str] = None
    # sqlalchemy的schema, 仅使用sqlalchemy需要配置, 例如:sqlite, mysql+pymysql等等
    sqlalchemy_schema: Optional[str] = None
    # 是否是async连接
    is_async: Optional[bool] = False
    # 是否是ioc primary实例
    primary: Optional[bool] = False


class SqliteConfig(CommonDBConfig):
    """Sqlite 配置"""
    sqlalchemy_schema: Optional[str] = 'sqlite'


class AsyncSqliteConfig(CommonDBConfig):
    """Sqlite async配置"""
    sqlalchemy_schema: Optional[str] = 'sqlite+aiosqlite'
    is_async: Optional[bool] = True


class MysqlConfig(CommonDBConfig):
    """Mysql 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 3306
    user: Optional[str] = 'root'
    sqlalchemy_schema: Optional[str] = 'mysql+pymysql'


class AsyncMysqlConfig(CommonDBConfig):
    """Mysql async配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 3306
    user: Optional[str] = 'root'
    sqlalchemy_schema: Optional[str] = 'mysql+aiomysql'
    is_async: Optional[bool] = True


class PostgresqlConfig(CommonDBConfig):
    """postgresql 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 5432
    user: Optional[str] = 'root'
    sqlalchemy_schema: Optional[str] = 'postgresql+psycopg2'


class AsyncPostgresqlConfig(CommonDBConfig):
    """postgresql async配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 5432
    user: Optional[str] = 'root'
    sqlalchemy_schema: Optional[str] = 'postgresql+asyncpg'
    is_async: Optional[bool] = True


class RedisConfig(CommonDBConfig):
    """Redis 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 6379


class HiveConfig(CommonDBConfig):
    """Hive 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 10000
    sqlalchemy_schema: Optional[str] = 'hive'


class ImpylaConfig(CommonDBConfig):
    """Impala 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 21050
    sqlalchemy_schema: Optional[str] = 'impala'


class ClickhouseConfig(CommonDBConfig):
    """Clickhouse 配置"""
    host: Optional[str] = '127.0.0.1'
    port: Optional[int] = 8123
    user: Optional[str] = 'root'
    sqlalchemy_schema: Optional[str] = 'clickhouse'


class SqlalchemyConfig(BaseModel):
    """sqlalchemy相关配置"""
    echo: Optional[bool] = True
    # 连接池回收周期
    pool_recycle: Optional[int] = -1


class MultiDBConfig(BaseModel):
    """多 DB 配置"""


class Config(BaseModel):
    """ 自定义配置项, 与config/application.yml 保持一致 """
    project_name: Optional[str] = 'undefined_project_name'
    log_dir: Optional[str] = './logs'
    db: Optional[MultiDBConfig] = MultiDBConfig()
    sqlalchemy: Optional[SqlalchemyConfig] = SqlalchemyConfig()
