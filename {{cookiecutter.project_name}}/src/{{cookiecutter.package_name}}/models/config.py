from typing import Optional
from seatools.models import BaseModel
from seatools.sqlalchemy.dbconfig import SqlalchemyConfig


class MultiDBConfig(BaseModel):
    """多 DB 配置

    引入 seatools.sqlalchemy.dbconfig 中的各种数据库配置类型属性, 并在application[-[dev|test|pro]].yml文件中添加相应配置
    """


class Config(BaseModel):
    """ 自定义配置项, 与config/application.yml 保持一致 """
    project_name: Optional[str] = 'undefined_project_name'
    log_dir: Optional[str] = './logs'
    db: Optional[MultiDBConfig] = MultiDBConfig()
    # 如需拓展sqlalchemy配置属性只需要定义新类型继承seatools.sqlalchemy.dbconfig.SqlalchemyConfig添加额外属性, 并修改此处类型和配置文件即可
    sqlalchemy: Optional[SqlalchemyConfig] = SqlalchemyConfig()
