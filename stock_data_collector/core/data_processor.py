"""
数据处理模块
负责数据的清洗、转换和处理
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
import logging

from utils.logger import get_logger
from utils.validators import StockValidator


class DataProcessor:
    """数据处理器"""
    
    def __init__(self):
        self.logger = get_logger()
        self.validator = StockValidator()
    
    def clean_stock_data(self, df: pd.DataFrame, market='a') -> pd.DataFrame:
        """
        清洗股票数据
        
        Args:
            df: 原始数据
            market: 市场类型
        
        Returns:
            DataFrame: 清洗后的数据
        """
        if df is None or df.empty:
            return pd.DataFrame()
        
        df = df.copy()
        
        try:
            if market == 'a':
                df = self._clean_a_stock_data(df)
            elif market == 'hk':
                df = self._clean_hk_stock_data(df)
            
            self.logger.info(f"数据清洗完成，共 {len(df)} 条记录")
        except Exception as e:
            self.logger.error(f"数据清洗失败: {e}")
        
        return df
    
    def _clean_a_stock_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """清洗A股数据"""
        if '代码' in df.columns:
            df = df.rename(columns={'代码': 'stock_code'})
        if '名称' in df.columns:
            df = df.rename(columns={'名称': 'stock_name'})
        
        numeric_columns = ['最新价', '涨跌幅', '涨跌额', '成交量', '成交额', '开盘', '最高', '最低', '收盘']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def _clean_hk_stock_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """清洗港股数据"""
        return df
    
    def clean_dividend_data(self, df: pd.DataFrame, market='a') -> pd.DataFrame:
        """
        清洗分红数据
        
        Args:
            df: 原始分红数据
            market: 市场类型
        
        Returns:
            DataFrame: 清洗后的分红数据
        """
        if df is None or df.empty:
            return pd.DataFrame()
        
        df = df.copy()
        
        try:
            if market == 'a':
                df = self._clean_a_dividend_data(df)
            elif market == 'hk':
                df = self._clean_hk_dividend_data(df)
            
            self.logger.info(f"分红数据清洗完成，共 {len(df)} 条记录")
        except Exception as e:
            self.logger.error(f"分红数据清洗失败: {e}")
        
        return df
    
    def _clean_a_dividend_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """清洗A股分红数据"""
        date_columns = ['除权除息日', '股权登记日', '派息日']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        numeric_columns = ['每股派现(元)', '派现总额(亿元)']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def _clean_hk_dividend_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """清洗港股分红数据"""
        date_columns = ['除净日', '截至过户日', '发放日']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        return df
    
    def merge_dividend_and_price(self, dividend_df: pd.DataFrame, 
                                price_df: pd.DataFrame,
                                market='a') -> pd.DataFrame:
        """
        合并分红和价格数据
        
        Args:
            dividend_df: 分红数据
            price_df: 价格数据
            market: 市场类型
        
        Returns:
            DataFrame: 合并后的数据
        """
        if dividend_df is None or dividend_df.empty:
            return pd.DataFrame()
        
        if price_df is None or price_df.empty:
            return dividend_df
        
        try:
            if market == 'a':
                date_col = '除权除息日'
            else:
                date_col = '除净日'
            
            merged_data = []
            
            for _, dividend in dividend_df.iterrows():
                ex_right_date = dividend[date_col]
                
                if pd.isna(ex_right_date):
                    continue
                
                if '日期' in price_df.columns:
                    price_match = price_df[price_df['日期'] == ex_right_date]
                else:
                    price_match = pd.DataFrame()
                
                row_data = dividend.to_dict()
                
                if not price_match.empty:
                    price_row = price_match.iloc[0]
                    row_data['收盘价'] = price_row.get('收盘', None)
                    row_data['开盘价'] = price_row.get('开盘', None)
                    row_data['最高价'] = price_row.get('最高', None)
                    row_data['最低价'] = price_row.get('最低', None)
                
                merged_data.append(row_data)
            
            result = pd.DataFrame(merged_data)
            self.logger.info(f"分红与价格数据合并完成，共 {len(result)} 条记录")
            return result
            
        except Exception as e:
            self.logger.error(f"数据合并失败: {e}")
            return dividend_df
    
    def calculate_dividend_yield(self, dividend_df: pd.DataFrame, 
                               price_df: pd.DataFrame) -> pd.DataFrame:
        """
        计算股息率
        
        Args:
            dividend_df: 分红数据
            price_df: 价格数据
        
        Returns:
            DataFrame: 包含股息率的数据
        """
        if dividend_df is None or dividend_df.empty:
            return pd.DataFrame()
        
        df = dividend_df.copy()
        
        try:
            if '每股派现(元)' in df.columns and '收盘价' in df.columns:
                df['股息率'] = (df['每股派现(元)'] / df['收盘价']) * 100
            elif '每股派息(港元)' in df.columns and '收盘价' in df.columns:
                df['股息率'] = (df['每股派息(港元)'] / df['收盘价']) * 100
            
            self.logger.info("股息率计算完成")
        except Exception as e:
            self.logger.error(f"股息率计算失败: {e}")
        
        return df
    
    def filter_by_date_range(self, df: pd.DataFrame, 
                           start_date: str, 
                           end_date: str,
                           date_column: str = '日期') -> pd.DataFrame:
        """
        按日期范围过滤数据
        
        Args:
            df: 数据
            start_date: 开始日期
            end_date: 结束日期
            date_column: 日期列名
        
        Returns:
            DataFrame: 过滤后的数据
        """
        if df is None or df.empty:
            return pd.DataFrame()
        
        try:
            df = df.copy()
            df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
            
            start = pd.to_datetime(start_date)
            end = pd.to_datetime(end_date)
            
            mask = (df[date_column] >= start) & (df[date_column] <= end)
            result = df[mask]
            
            self.logger.info(f"日期过滤完成，保留 {len(result)} 条记录")
            return result
            
        except Exception as e:
            self.logger.error(f"日期过滤失败: {e}")
            return df
    
    def remove_duplicates(self, df: pd.DataFrame, 
                        subset: List[str] = None) -> pd.DataFrame:
        """
        删除重复数据
        
        Args:
            df: 数据
            subset: 用于判断重复的列
        
        Returns:
            DataFrame: 去重后的数据
        """
        if df is None or df.empty:
            return pd.DataFrame()
        
        try:
            original_len = len(df)
            df = df.drop_duplicates(subset=subset, keep='first')
            removed = original_len - len(df)
            
            if removed > 0:
                self.logger.info(f"删除 {removed} 条重复记录")
            
            return df
            
        except Exception as e:
            self.logger.error(f"去重失败: {e}")
            return df
    
    def handle_missing_values(self, df: pd.DataFrame, 
                            strategy: str = 'drop') -> pd.DataFrame:
        """
        处理缺失值
        
        Args:
            df: 数据
            strategy: 处理策略 ('drop', 'fill', 'forward', 'backward')
        
        Returns:
            DataFrame: 处理后的数据
        """
        if df is None or df.empty:
            return pd.DataFrame()
        
        df = df.copy()
        
        try:
            if strategy == 'drop':
                df = df.dropna()
            elif strategy == 'fill':
                df = df.fillna(0)
            elif strategy == 'forward':
                df = df.fillna(method='ffill')
            elif strategy == 'backward':
                df = df.fillna(method='bfill')
            
            self.logger.info(f"缺失值处理完成，使用策略: {strategy}")
        except Exception as e:
            self.logger.error(f"缺失值处理失败: {e}")
        
        return df
    
    def normalize_data(self, df: pd.DataFrame, 
                     columns: List[str]) -> pd.DataFrame:
        """
        标准化数据
        
        Args:
            df: 数据
            columns: 需要标准化的列
        
        Returns:
            DataFrame: 标准化后的数据
        """
        if df is None or df.empty:
            return pd.DataFrame()
        
        df = df.copy()
        
        try:
            for col in columns:
                if col in df.columns:
                    mean = df[col].mean()
                    std = df[col].std()
                    if std > 0:
                        df[f'{col}_normalized'] = (df[col] - mean) / std
            
            self.logger.info(f"数据标准化完成，{len(columns)} 列")
        except Exception as e:
            self.logger.error(f"数据标准化失败: {e}")
        
        return df
    
    def aggregate_by_period(self, df: pd.DataFrame,
                          date_column: str,
                          value_column: str,
                          freq: str = 'M') -> pd.DataFrame:
        """
        按时间周期聚合数据
        
        Args:
            df: 数据
            date_column: 日期列
            value_column: 值列
            freq: 周期 ('D', 'W', 'M', 'Q', 'Y')
        
        Returns:
            DataFrame: 聚合后的数据
        """
        if df is None or df.empty:
            return pd.DataFrame()
        
        try:
            df = df.copy()
            df[date_column] = pd.to_datetime(df[date_column])
            df = df.set_index(date_column)
            
            result = df[value_column].resample(freq).agg(['mean', 'sum', 'count'])
            result = result.reset_index()
            
            self.logger.info(f"数据聚合完成，周期: {freq}")
            return result
            
        except Exception as e:
            self.logger.error(f"数据聚合失败: {e}")
            return df
    
    def calculate_statistics(self, df: pd.DataFrame, 
                           column: str) -> Dict[str, float]:
        """
        计算统计指标
        
        Args:
            df: 数据
            column: 列名
        
        Returns:
            dict: 统计指标
        """
        if df is None or df.empty or column not in df.columns:
            return {}
        
        try:
            stats = {
                'count': len(df),
                'mean': df[column].mean(),
                'median': df[column].median(),
                'std': df[column].std(),
                'min': df[column].min(),
                'max': df[column].max(),
                'q25': df[column].quantile(0.25),
                'q75': df[column].quantile(0.75)
            }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"统计计算失败: {e}")
            return {}
    
    def convert_date_format(self, df: pd.DataFrame,
                          columns: List[str],
                          from_format: str,
                          to_format: str = '%Y-%m-%d') -> pd.DataFrame:
        """
        转换日期格式
        
        Args:
            df: 数据
            columns: 日期列
            from_format: 原格式
            to_format: 目标格式
        
        Returns:
            DataFrame: 转换后的数据
        """
        if df is None or df.empty:
            return pd.DataFrame()
        
        df = df.copy()
        
        try:
            for col in columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], format=from_format, errors='coerce')
                    df[col] = df[col].dt.strftime(to_format)
            
            self.logger.info(f"日期格式转换完成")
        except Exception as e:
            self.logger.error(f"日期格式转换失败: {e}")
        
        return df
    
    def rename_columns(self, df: pd.DataFrame,
                      column_map: Dict[str, str]) -> pd.DataFrame:
        """
        重命名列
        
        Args:
            df: 数据
            column_map: 列名映射
        
        Returns:
            DataFrame: 重命名后的数据
        """
        if df is None or df.empty:
            return pd.DataFrame()
        
        try:
            df = df.rename(columns=column_map)
            self.logger.info(f"列重命名完成，{len(column_map)} 列")
        except Exception as e:
            self.logger.error(f"列重命名失败: {e}")
        
        return df
    
    def select_columns(self, df: pd.DataFrame,
                     columns: List[str]) -> pd.DataFrame:
        """
        选择指定列
        
        Args:
            df: 数据
            columns: 列名列表
        
        Returns:
            DataFrame: 选择后的数据
        """
        if df is None or df.empty:
            return pd.DataFrame()
        
        try:
            existing_columns = [col for col in columns if col in df.columns]
            df = df[existing_columns]
            self.logger.info(f"列选择完成，保留 {len(existing_columns)} 列")
        except Exception as e:
            self.logger.error(f"列选择失败: {e}")
        
        return df
