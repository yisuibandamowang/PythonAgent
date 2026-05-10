"""
为整个工程提供统一的绝对路径
"""
import os

def get_project_root():
    # 获取工程的根目录
    current_file = os.path.abspath(__file__)   # 当前文件绝对路径
    current_dir = os.path.dirname(current_file)  # 当前文件所在目录
    project_root = os.path.dirname(current_dir)  # 工程根目录

    return project_root

def get_abs_path(relative_path):
    """
    获取绝对路径
    :param relative_path: 相对路径
    :return: 绝对路径
    """
    project_root = get_project_root()
    abs_path = os.path.join(project_root, relative_path)
    return abs_path

if __name__ == "__main__":
    print(get_project_root())
    print(get_abs_path("config/config.txt"))
