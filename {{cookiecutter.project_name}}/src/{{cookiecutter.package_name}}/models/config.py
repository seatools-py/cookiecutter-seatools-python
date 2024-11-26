from typing import Optional
from seatools.models import BaseModel


class Config(BaseModel):
    """ 自定义配置项, 与config/application.yml 保持一致 """
    project_name: Optional[str] = 'undefined_project_name'
    log_dir: Optional[str] = './logs'
