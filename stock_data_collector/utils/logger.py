"""
日志工具模块
"""
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
from datetime import datetime


def setup_logger(name='stock_collector', level='INFO', log_file=None, 
                 max_bytes=10485760, backup_count=5):
    """
    设置日志记录器
    
    Args:
        name: 日志记录器名称
        level: 日志级别
        log_file: 日志文件路径
        max_bytes: 日志文件最大字节数
        backup_count: 保留的备份文件数量
    
    Returns:
        logger: 配置好的日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))
    logger.handlers = []
    
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    if log_file:
        log_dir = Path(log_file).parent
        log_dir.mkdir(parents=True, exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger


def get_logger(name='stock_collector'):
    """获取日志记录器"""
    return logging.getLogger(name)


class LoggerAdapter(logging.LoggerAdapter):
    """日志记录器适配器，添加额外上下文信息"""
    
    def process(self, msg, kwargs):
        extra = self.extra.copy()
        if 'extra' in kwargs:
            extra.update(kwargs['extra'])
            kwargs['extra'] = extra
        else:
            kwargs['extra'] = extra
        return msg, kwargs


def log_execution_time(func):
    """装饰器：记录函数执行时间"""
    def wrapper(*args, **kwargs):
        logger = get_logger()
        start_time = datetime.now()
        logger.info(f"开始执行 {func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"{func.__name__} 执行完成，耗时: {elapsed:.2f}秒")
            return result
        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.error(f"{func.__name__} 执行失败，耗时: {elapsed:.2f}秒，错误: {e}")
            raise
    
    return wrapper
