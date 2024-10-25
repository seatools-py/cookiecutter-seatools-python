import os
from loguru import logger
from typing import List
import re


def mkdir(dir_path: str):
    """创建目录"""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        logger.success('创建目录: {}', dir_path)
        return
    logger.warning('目录已存在: {}, 忽略', dir_path)


def create_file(filepath: str, content='', encoding='utf-8', override=False):
    """创建文件"""
    exists = os.path.exists(filepath)
    if override and exists:
        os.remove(filepath)
        exists = False
        logger.info('删除文件: {}', filepath)
    if not exists:
        with open(filepath, 'w', encoding=encoding) as f:
            f.write(content)
        logger.success('创建文件: {}', filepath)
        return
    logger.warning('文件已存在: {}, 忽略', filepath)


def add_poetry_script(project_dir: str, script: str):
    """新增poetry启动脚本"""
    pyproject_toml = project_dir + os.sep + 'pyproject.toml'
    if not os.path.exists(pyproject_toml):
        logger.error('pyproject.toml文件不存在, 无法添加poetry执行脚本')
        return
    with open(pyproject_toml, 'r', encoding='utf-8') as f:
        content = f.read()
    if script in content:
        logger.warning('脚本[{}]已存在, 无需重复添加', script)
        return
    content = content.replace('[tool.poetry.scripts]', f'[tool.poetry.scripts]\n{script}')
    with open(pyproject_toml, 'w', encoding='utf-8') as f:
        f.write(content)
    logger.success('新增poetry执行脚本: [poetry run {}]', script.split('=')[0].strip())


def add_docker_compose_script(project_dir: str, script: str):
    """新增docker-compose启动脚本"""
    docker_compose_yml = project_dir + os.sep + 'docker-compose.yml'
    if not os.path.exists(docker_compose_yml):
        create_file(docker_compose_yml, """version: '3'
services:
""")
        logger.success('docker-compose.yml文件不存在, 创建docker-compose.yml文件')
    with open(docker_compose_yml, 'r', encoding='utf-8') as f:
        content = f.read()
    service_name = script.split('\n')[0].strip().strip('\r').strip(':')
    if service_name in content:
        logger.warning('服务[{}]已存在, 无需重复添加, 忽略', service_name)
        return
    content = content.replace('\nservices:', f'\nservices:\n{script}')
    with open(docker_compose_yml, 'w', encoding='utf-8') as f:
        f.write(content)
    logger.success('新增docker-compose服务: {}', service_name)


def extract_names(name: str) -> List[str]:
    """提取名称分段列表"""
    tmp = re.findall(r'[A-Z][a-z0-9]*', name)
    if not tmp:
        tmp = [name]
    names = []
    for name in tmp:
        ns = name.lower().split('_')
        for n in ns:
            names.extend(n.split('-'))
    return names


def str_format(text: str, **kwargs):
    """字符串格式化, 变量使用${}包裹"""
    pattern = r'\${([^}]*)}'
    express_names = re.findall(pattern, text)
    if not express_names:
        return text
    for express_name in express_names:
        if express_name in kwargs:
            text = text.replace('${' + express_name + '}', str(kwargs[express_name]))
    return text
