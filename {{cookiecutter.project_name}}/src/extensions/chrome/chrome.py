import os
import zipfile
from typing import List
import httpx
from colorama import Fore
from tqdm import tqdm
from {{cookiecutter.package_name}} import utils
from {{cookiecutter.package_name}}.config import get_extensions_dir

DEFAULT_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'


def list_chrome(**kwargs) -> List[str]:
    """查询所有可用的chrome/chromedriver版本, 仅支持114以上版本

    Returns:

    """
    url = 'https://registry.npmmirror.com/-/binary/chrome-for-testing/'
    res = httpx.get(url, headers={'User-Agent': kwargs.get('user_agent', DEFAULT_UA)})
    assert res.status_code == 200, '获取浏览器版本失败, 响应状态码: {}'.format(res.status_code)
    """
    [{
        `"id": "6509cadd0e50dbc7735c266c", // ID
        "category": "chrome-for-testing", // 类别
        "name": "113.0.5672.0/", // 版本名称
        "date": "1121455", // 数据大小, bytes
        "type": "dir", // 类型
        "url": "https://registry.npmmirror.com/-/binary/chrome-for-testing/113.0.5672.0/", //地址
        "modified": "2023-09-19T16:23:34.738Z"` // 上一次修改时间
    }]
    """
    ans = ["版本"]
    for item in res.json():
        ans.append(item['name'].rstrip('/'))
    return ans


def common_download_chrome(project_dir: str, package_dir: str, version: str, system: str = 'win64',
                           type_: str = 'chromedriver', **kwargs):
    """下载并解压chrome/chromedriver

    Args:
        project_dir: 项目目录
        package_dir: 包目录
        version: 下载的chrome版本
        system: 系统, 支持: linux64, mac-arm64, mac-x64, win32, win64
        type_: 类型, 支持: chromedriver, chrome
    """
    # 检查是否存在
    _check_chrome_version_system(version, system, type_, **kwargs)
    # 拓展目录处理
    extensions_dir = utils.get_absolute_path(kwargs.get('extensions_dir', get_extensions_dir()).rstrip('/'))
    if not os.path.exists(extensions_dir):
        os.makedirs(extensions_dir)
        print(Fore.LIGHTYELLOW_EX + '[{}]拓展目录[{}]不存在, 创建该目录'.format(type_, extensions_dir))
    zip_file = extensions_dir + os.sep + '{}-{}.zip'.format(type_, system)
    # 下载
    _common_download_zip(version, system, type_, zip_file=zip_file, **kwargs)
    # 解压
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extensions_dir)
    print(Fore.LIGHTGREEN_EX + '[{}]解压压缩包[{}]完成'.format(type_, zip_file))
    # 删除压缩包
    os.remove(zip_file)
    print(Fore.LIGHTGREEN_EX + '[{}]删除压缩包[{}]完成'.format(type_, zip_file))


def _check_chrome_version_system(version: str, system: str, type_: str, **kwargs):
    # 检查是否存在
    url = 'https://registry.npmmirror.com/-/binary/chrome-for-testing/{}/{}/'.format(version, system)
    headers = {'User-Agent': kwargs.get('user_agent', DEFAULT_UA)}
    res = httpx.get(url, headers=headers)
    if res.status_code == 404:
        print(Fore.LIGHTRED_EX + '[{}]未找到版本[{}]系统[{}], 请检查或切换版本重试'.format(type_, version, system))
        exit(1)
    return res


def _common_download_zip(version: str, system: str, type_: str, zip_file: str, **kwargs):
    # 检查是否存在
    url = 'https://registry.npmmirror.com/-/binary/chrome-for-testing/{}/{}/{}-{}.zip'.format(version, system, type_,
                                                                                              system)
    print(Fore.LIGHTWHITE_EX + '[{}]开始下载压缩包, 下载地址: {}'.format(type_, url))
    headers = {'User-Agent': kwargs.get('user_agent', DEFAULT_UA)}
    _download_file(url, zip_file, headers=headers)
    print(Fore.LIGHTGREEN_EX + '[{}]下载压缩包完成, 下载文件路径[{}]'.format(type_, zip_file))


def _download_file(url, filename, headers=None, **kwargs):
    # 发起请求，获取文件总大小
    response = httpx.head(url, headers=headers, **kwargs)
    total_size = int(response.headers.get('content-length', 0))

    # 使用GET请求下载文件
    with httpx.stream('GET', url, headers=headers, follow_redirects=True, **kwargs) as r:
        r.raise_for_status()
        # 总长度
        total_length = int(r.headers.get('content-length', total_size))
        # 已下载
        downloaded = 0

        # 打开文件准备写入
        with open(filename, 'wb') as f:
            # 使用tqdm作为文件写入的缓冲区
            for chunk in tqdm(r.iter_bytes(chunk_size=8192),
                              total=total_length // 8192,
                              unit='KB'):
                f.write(chunk)
                downloaded += len(chunk)
            # 确保文件完整写入
            f.flush()
