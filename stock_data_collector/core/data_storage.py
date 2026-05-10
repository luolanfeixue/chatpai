"""
数据存储模块
支持多种存储方式和数据导出
"""
import pandas as pd
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
import logging

from utils.logger import get_logger


class DataStorage:
    """数据存储器"""
    
    def __init__(self, storage_dir='data'):
        """
        初始化存储器
        
        Args:
            storage_dir: 存储目录
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.logger = get_logger()
    
    def save_to_csv(self, df: pd.DataFrame, filename: str, 
                   encoding: str = 'utf-8-sig') -> bool:
        """
        保存数据到CSV文件
        
        Args:
            df: 数据
            filename: 文件名
            encoding: 编码
        
        Returns:
            bool: 是否成功
        """
        if df is None or df.empty:
            self.logger.warning("数据为空，跳过保存")
            return False
        
        try:
            filepath = self.storage_dir / filename
            df.to_csv(filepath, index=False, encoding=encoding)
            self.logger.info(f"数据已保存到: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"保存CSV失败: {e}")
            return False
    
    def save_to_excel(self, df: pd.DataFrame, filename: str,
                    sheet_name: str = 'Sheet1') -> bool:
        """
        保存数据到Excel文件
        
        Args:
            df: 数据
            filename: 文件名
            sheet_name: 工作表名
        
        Returns:
            bool: 是否成功
        """
        if df is None or df.empty:
            self.logger.warning("数据为空，跳过保存")
            return False
        
        try:
            filepath = self.storage_dir / filename
            df.to_excel(filepath, sheet_name=sheet_name, index=False)
            self.logger.info(f"数据已保存到: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"保存Excel失败: {e}")
            return False
    
    def save_to_json(self, df: pd.DataFrame, filename: str,
                   orient: str = 'records') -> bool:
        """
        保存数据到JSON文件
        
        Args:
            df: 数据
            filename: 文件名
            orient: JSON方向
        
        Returns:
            bool: 是否成功
        """
        if df is None or df.empty:
            self.logger.warning("数据为空，跳过保存")
            return False
        
        try:
            filepath = self.storage_dir / filename
            df.to_json(filepath, orient=orient, force_ascii=False, indent=2)
            self.logger.info(f"数据已保存到: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"保存JSON失败: {e}")
            return False
    
    def load_from_csv(self, filename: str, encoding: str = 'utf-8-sig') -> Optional[pd.DataFrame]:
        """
        从CSV文件加载数据
        
        Args:
            filename: 文件名
            encoding: 编码
        
        Returns:
            DataFrame: 加载的数据
        """
        try:
            filepath = self.storage_dir / filename
            if not filepath.exists():
                self.logger.warning(f"文件不存在: {filepath}")
                return None
            
            df = pd.read_csv(filepath, encoding=encoding)
            self.logger.info(f"从 {filepath} 加载了 {len(df)} 条记录")
            return df
        except Exception as e:
            self.logger.error(f"加载CSV失败: {e}")
            return None
    
    def load_from_excel(self, filename: str, sheet_name: str = 0) -> Optional[pd.DataFrame]:
        """
        从Excel文件加载数据
        
        Args:
            filename: 文件名
            sheet_name: 工作表名或索引
        
        Returns:
            DataFrame: 加载的数据
        """
        try:
            filepath = self.storage_dir / filename
            if not filepath.exists():
                self.logger.warning(f"文件不存在: {filepath}")
                return None
            
            df = pd.read_excel(filepath, sheet_name=sheet_name)
            self.logger.info(f"从 {filepath} 加载了 {len(df)} 条记录")
            return df
        except Exception as e:
            self.logger.error(f"加载Excel失败: {e}")
            return None
    
    def load_from_json(self, filename: str) -> Optional[pd.DataFrame]:
        """
        从JSON文件加载数据
        
        Args:
            filename: 文件名
        
        Returns:
            DataFrame: 加载的数据
        """
        try:
            filepath = self.storage_dir / filename
            if not filepath.exists():
                self.logger.warning(f"文件不存在: {filepath}")
                return None
            
            df = pd.read_json(filepath)
            self.logger.info(f"从 {filepath} 加载了 {len(df)} 条记录")
            return df
        except Exception as e:
            self.logger.error(f"加载JSON失败: {e}")
            return None
    
    def append_to_csv(self, df: pd.DataFrame, filename: str,
                    encoding: str = 'utf-8-sig') -> bool:
        """
        追加数据到CSV文件
        
        Args:
            df: 数据
            filename: 文件名
            encoding: 编码
        
        Returns:
            bool: 是否成功
        """
        if df is None or df.empty:
            return False
        
        try:
            filepath = self.storage_dir / filename
            
            if filepath.exists():
                existing_df = pd.read_csv(filepath, encoding=encoding)
                df = pd.concat([existing_df, df], ignore_index=True)
            
            df.to_csv(filepath, index=False, encoding=encoding)
            self.logger.info(f"数据已追加到: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"追加CSV失败: {e}")
            return False
    
    def export_with_timestamp(self, df: pd.DataFrame, prefix: str,
                           format: str = 'csv') -> str:
        """
        带时间戳导出数据
        
        Args:
            df: 数据
            prefix: 文件名前缀
            format: 导出格式
        
        Returns:
            str: 保存的文件名
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{prefix}_{timestamp}.{format}"
        
        if format == 'csv':
            self.save_to_csv(df, filename)
        elif format == 'excel':
            self.save_to_excel(df, filename)
        elif format == 'json':
            self.save_to_json(df, filename)
        
        return filename
    
    def save_dividend_strategy_result(self, df: pd.DataFrame,
                                    stock_code: str = None) -> bool:
        """
        保存分红策略分析结果
        
        Args:
            df: 分析结果
            stock_code: 股票代码
        
        Returns:
            bool: 是否成功
        """
        if stock_code:
            filename = f"dividend_strategy_{stock_code}.csv"
        else:
            filename = "dividend_strategy_results.csv"
        
        return self.save_to_csv(df, filename)
    
    def save_realtime_data(self, df: pd.DataFrame, market: str = 'a') -> bool:
        """
        保存实时行情数据
        
        Args:
            df: 实时行情数据
            market: 市场类型
        
        Returns:
            bool: 是否成功
        """
        timestamp = datetime.now().strftime('%Y%m%d')
        filename = f"realtime_{market}_{timestamp}.csv"
        return self.save_to_csv(df, filename)
    
    def save_dividend_data(self, df: pd.DataFrame, 
                          market: str = 'a') -> bool:
        """
        保存分红数据
        
        Args:
            df: 分红数据
            market: 市场类型
        
        Returns:
            bool: 是否成功
        """
        filename = f"dividend_{market}.csv"
        return self.save_to_csv(df, filename)
    
    def list_files(self, pattern: str = '*') -> List[str]:
        """
        列出存储目录下的文件
        
        Args:
            pattern: 文件模式
        
        Returns:
            list: 文件列表
        """
        try:
            files = list(self.storage_dir.glob(pattern))
            return [f.name for f in files]
        except Exception as e:
            self.logger.error(f"列出文件失败: {e}")
            return []
    
    def delete_file(self, filename: str) -> bool:
        """
        删除文件
        
        Args:
            filename: 文件名
        
        Returns:
            bool: 是否成功
        """
        try:
            filepath = self.storage_dir / filename
            if filepath.exists():
                filepath.unlink()
                self.logger.info(f"已删除文件: {filepath}")
                return True
            return False
        except Exception as e:
            self.logger.error(f"删除文件失败: {e}")
            return False
    
    def get_file_info(self, filename: str) -> Dict[str, Any]:
        """
        获取文件信息
        
        Args:
            filename: 文件名
        
        Returns:
            dict: 文件信息
        """
        try:
            filepath = self.storage_dir / filename
            if not filepath.exists():
                return {}
            
            stat = filepath.stat()
            return {
                'name': filename,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'path': str(filepath)
            }
        except Exception as e:
            self.logger.error(f"获取文件信息失败: {e}")
            return {}
    
    def clean_old_files(self, days: int = 30, pattern: str = '*') -> int:
        """
        清理旧文件
        
        Args:
            days: 保留天数
            pattern: 文件模式
        
        Returns:
            int: 删除的文件数量
        """
        try:
            cutoff = datetime.now() - timedelta(days=days)
            count = 0
            
            for filepath in self.storage_dir.glob(pattern):
                if filepath.is_file():
                    mtime = datetime.fromtimestamp(filepath.stat().st_mtime)
                    if mtime < cutoff:
                        filepath.unlink()
                        count += 1
            
            self.logger.info(f"已清理 {count} 个旧文件")
            return count
        except Exception as e:
            self.logger.error(f"清理文件失败: {e}")
            return 0
    
    def create_backup(self, filename: str) -> bool:
        """
        创建文件备份
        
        Args:
            filename: 文件名
        
        Returns:
            bool: 是否成功
        """
        try:
            filepath = self.storage_dir / filename
            if not filepath.exists():
                return False
            
            backup_name = f"{filename}.bak"
            backup_path = self.storage_dir / backup_name
            
            import shutil
            shutil.copy2(filepath, backup_path)
            self.logger.info(f"已创建备份: {backup_path}")
            return True
        except Exception as e:
            self.logger.error(f"创建备份失败: {e}")
            return False
