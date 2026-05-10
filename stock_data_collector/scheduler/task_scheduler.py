"""
定时任务调度模块
"""
import schedule
import time
import threading
from datetime import datetime
from typing import Callable, Dict, Any, Optional
import logging

from utils.logger import get_logger


class TaskScheduler:
    """定时任务调度器"""
    
    def __init__(self):
        self.logger = get_logger()
        self.jobs = {}
        self.is_running = False
        self.thread = None
    
    def add_job(self, func: Callable, interval: int, job_name: str = None):
        """
        添加定时任务
        
        Args:
            func: 要执行的函数
            interval: 执行间隔（秒）
            job_name: 任务名称
        """
        if job_name is None:
            job_name = f"job_{len(self.jobs) + 1}"
        
        def job_wrapper():
            try:
                self.logger.info(f"执行定时任务: {job_name}")
                result = func()
                self.logger.info(f"任务 {job_name} 执行完成")
                return result
            except Exception as e:
                self.logger.error(f"任务 {job_name} 执行失败: {e}")
        
        schedule.every(interval).seconds.do(job_wrapper)
        self.jobs[job_name] = {
            'func': func,
            'interval': interval,
            'last_run': None,
            'next_run': schedule.next_run()
        }
        
        self.logger.info(f"已添加定时任务: {job_name}，间隔: {interval}秒")
    
    def add_daily_job(self, func: Callable, time_str: str, job_name: str = None):
        """
        添加每日定时任务
        
        Args:
            func: 要执行的函数
            time_str: 执行时间 (HH:MM)
            job_name: 任务名称
        """
        if job_name is None:
            job_name = f"daily_job_{len(self.jobs) + 1}"
        
        def job_wrapper():
            try:
                self.logger.info(f"执行每日任务: {job_name}")
                result = func()
                self.logger.info(f"任务 {job_name} 执行完成")
                return result
            except Exception as e:
                self.logger.error(f"任务 {job_name} 执行失败: {e}")
        
        schedule.every().day.at(time_str).do(job_wrapper)
        self.jobs[job_name] = {
            'func': func,
            'time': time_str,
            'last_run': None,
            'next_run': schedule.next_run()
        }
        
        self.logger.info(f"已添加每日任务: {job_name}，时间: {time_str}")
    
    def remove_job(self, job_name: str):
        """
        移除定时任务
        
        Args:
            job_name: 任务名称
        """
        if job_name in self.jobs:
            del self.jobs[job_name]
            schedule.clear(job_name)
            self.logger.info(f"已移除任务: {job_name}")
        else:
            self.logger.warning(f"任务不存在: {job_name}")
    
    def list_jobs(self):
        """列出所有任务"""
        jobs = schedule.get_jobs()
        print("\n" + "=" * 60)
        print("定时任务列表")
        print("=" * 60)
        for job in jobs:
            print(f"  - {job}")
        print("=" * 60)
    
    def start(self, blocking: bool = True):
        """
        启动调度器
        
        Args:
            blocking: 是否阻塞主线程
        """
        if self.is_running:
            self.logger.warning("调度器已在运行中")
            return
        
        self.is_running = True
        self.logger.info("调度器已启动")
        
        def run_scheduler():
            while self.is_running:
                schedule.run_pending()
                time.sleep(1)
        
        if blocking:
            run_scheduler()
        else:
            self.thread = threading.Thread(target=run_scheduler, daemon=True)
            self.thread.start()
    
    def stop(self):
        """停止调度器"""
        self.is_running = False
        schedule.clear()
        self.logger.info("调度器已停止")
    
    def run_once(self):
        """立即执行所有任务（一次性）"""
        self.logger.info("立即执行所有任务...")
        schedule.run_all()
    
    def get_next_run_time(self, job_name: str = None) -> Optional[datetime]:
        """
        获取下次运行时间
        
        Args:
            job_name: 任务名称
        
        Returns:
            datetime: 下次运行时间
        """
        if job_name:
            for job in schedule.get_jobs():
                if job_name in str(job):
                    return job.next_run
        return schedule.next_run()
    
    def get_status(self) -> Dict[str, Any]:
        """
        获取调度器状态
        
        Returns:
            dict: 状态信息
        """
        return {
            'is_running': self.is_running,
            'job_count': len(self.jobs),
            'next_run': self.get_next_run_time()
        }


def create_dividend_update_scheduler(update_func: Callable, interval_hours: int = 6):
    """
    创建分红数据更新调度器
    
    Args:
        update_func: 更新函数
        interval_hours: 更新间隔（小时）
    
    Returns:
        TaskScheduler: 配置好的调度器
    """
    scheduler = TaskScheduler()
    scheduler.add_job(update_func, interval_hours * 3600, "dividend_update")
    return scheduler


def create_realtime_data_scheduler(fetch_func: Callable, interval_seconds: int = 60):
    """
    创建实时数据更新调度器
    
    Args:
        fetch_func: 获取数据函数
        interval_seconds: 更新间隔（秒）
    
    Returns:
        TaskScheduler: 配置好的调度器
    """
    scheduler = TaskScheduler()
    scheduler.add_job(fetch_func, interval_seconds, "realtime_fetch")
    return scheduler
