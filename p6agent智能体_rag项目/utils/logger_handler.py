from datetime import datetime
import logging
from p6agent智能体_rag项目.utils.path_tool import get_abs_path
import os

# 日志保存根目录
LOG_ROOT_PATH = get_abs_path("logs")

# 确保日志目录存在
os.makedirs(LOG_ROOT_PATH, exist_ok=True)

#日志的格式配置     error   info  debug
DEFAULT_LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

def get_logger(name:str = "agent", level=logging.INFO,file_level=logging.DEBUG,log_file=None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # 避免重复添加 handler
    if logger.handlers:
        return logger

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)

    # 文件输出
    if not log_file :     # 如果没有指定日志文件，则使用默认的日志文件名
        log_file = os.path.join(LOG_ROOT_PATH, f"{name}_{datetime.now().strftime('%Y%m%d')}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)

    return logger


# 快捷获取日志管理器
logger = get_logger()

if __name__ == "__main__":
    logger.debug("debug")
    logger.info("info")
    logger.warning("warning")
    logger.error("error")
