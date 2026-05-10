"""
数据获取模块
使用akshare获取股票数据
"""
import akshare as ak
import pandas as pd
import time
from datetime import datetime, timedelta
from typing import Optional, List, Union
import logging

from utils.logger import get_logger


class DataFetcher:
    """数据获取器"""
    
    def __init__(self, retry_times=3, timeout=30):
        """
        初始化数据获取器
        
        Args:
            retry_times: 重试次数
            timeout: 超时时间（秒）
        """
        self.retry_times = retry_times
        self.timeout = timeout
        self.logger = get_logger()
    
    def _retry_request(self, func, *args, **kwargs):
        """带重试的请求"""
        for i in range(self.retry_times):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                self.logger.warning(f"请求失败（第{i+1}次）: {e}")
                if i < self.retry_times - 1:
                    time.sleep(1 * (i + 1))
                else:
                    self.logger.error(f"请求失败，已达到最大重试次数")
                    raise
    
    def fetch_a_stock_spot(self) -> Optional[pd.DataFrame]:
        """
        获取A股实时行情
        
        Returns:
            DataFrame: A股实时行情数据
        """
        try:
            self.logger.info("正在获取A股实时行情...")
            df = self._retry_request(ak.stock_zh_a_spot_em)
            self.logger.info(f"A股实时行情获取成功，共 {len(df)} 条记录")
            return df
        except Exception as e:
            self.logger.error(f"获取A股实时行情失败: {e}")
            return None
    
    def fetch_hk_stock_spot(self) -> Optional[pd.DataFrame]:
        """
        获取港股实时行情
        
        Returns:
            DataFrame: 港股实时行情数据
        """
        try:
            self.logger.info("正在获取港股实时行情...")
            df = self._retry_request(ak.stock_hk_spot_em)
            self.logger.info(f"港股实时行情获取成功，共 {len(df)} 条记录")
            return df
        except Exception as e:
            self.logger.error(f"获取港股实时行情失败: {e}")
            return None
    
    def fetch_stock_by_codes(self, codes: Union[str, List[str]], market='a') -> Optional[pd.DataFrame]:
        """
        根据股票代码获取实时行情
        
        Args:
            codes: 股票代码列表
            market: 市场类型 ('a' 或 'hk')
        
        Returns:
            DataFrame: 股票实时行情
        """
        if isinstance(codes, str):
            codes = [codes]
        
        try:
            self.logger.info(f"正在获取 {len(codes)} 只股票实时行情...")
            
            if market == 'a':
                spot_df = self.fetch_a_stock_spot()
                if spot_df is not None:
                    df = spot_df[spot_df['代码'].isin(codes)]
                    self.logger.info(f"成功获取 {len(df)} 只股票行情")
                    return df
            elif market == 'hk':
                spot_df = self.fetch_hk_stock_spot()
                if spot_df is not None:
                    df = spot_df[spot_df['代码'].isin(codes)]
                    self.logger.info(f"成功获取 {len(df)} 只股票行情")
                    return df
            
            return None
        except Exception as e:
            self.logger.error(f"批量获取股票行情失败: {e}")
            return None
    
    def fetch_a_stock_history(self, symbol: str, start_date: str, end_date: str, 
                            period: str = "daily", adjust: str = "qfq") -> Optional[pd.DataFrame]:
        """
        获取A股历史K线数据
        
        Args:
            symbol: 股票代码
            start_date: 开始日期 (YYYYMMDD)
            end_date: 结束日期 (YYYYMMDD)
            period: K线周期 ('daily', 'weekly', 'monthly')
            adjust: 复权类型 ('qfq'前复权, 'hfq'后复权, ''不复权)
        
        Returns:
            DataFrame: 历史K线数据
        """
        try:
            self.logger.info(f"正在获取 {symbol} 历史K线数据...")
            df = self._retry_request(
                ak.stock_zh_a_hist,
                symbol=symbol,
                period=period,
                start_date=start_date,
                end_date=end_date,
                adjust=adjust
            )
            self.logger.info(f"{symbol} 历史K线获取成功，共 {len(df)} 条记录")
            return df
        except Exception as e:
            self.logger.error(f"获取 {symbol} 历史K线失败: {e}")
            return None
    
    def fetch_a_stock_dividend(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        获取A股分红历史
        
        Args:
            symbol: 股票代码
        
        Returns:
            DataFrame: 分红历史数据
        """
        try:
            self.logger.info(f"正在获取 {symbol} 分红历史...")
            df = self._retry_request(
                ak.stock_history_dividend_detail,
                symbol=symbol,
                indicator="分红"
            )
            self.logger.info(f"{symbol} 分红历史获取成功，共 {len(df) if df is not None else 0} 条记录")
            return df
        except Exception as e:
            self.logger.error(f"获取 {symbol} 分红历史失败: {e}")
            return None
    
    def fetch_a_stock_bonus(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        获取A股配股数据
        
        Args:
            symbol: 股票代码
        
        Returns:
            DataFrame: 配股历史数据
        """
        try:
            self.logger.info(f"正在获取 {symbol} 配股历史...")
            df = self._retry_request(
                ak.stock_history_dividend_detail,
                symbol=symbol,
                indicator="配股"
            )
            return df
        except Exception as e:
            self.logger.error(f"获取 {symbol} 配股历史失败: {e}")
            return None
    
    def fetch_hk_stock_dividend(self, symbol: str) -> Optional[pd.DataFrame]:
        """
        获取港股分红历史
        
        Args:
            symbol: 股票代码
        
        Returns:
            DataFrame: 分红历史数据
        """
        try:
            self.logger.info(f"正在获取港股 {symbol} 分红历史...")
            df = self._retry_request(
                ak.stock_hk_dividend_payout_em,
                symbol=symbol
            )
            self.logger.info(f"港股 {symbol} 分红历史获取成功")
            return df
        except Exception as e:
            self.logger.error(f"获取港股 {symbol} 分红历史失败: {e}")
            return None
    
    def fetch_hsgt_north(self) -> Optional[pd.DataFrame]:
        """
        获取沪股通/深股通持股明细
        
        Returns:
            DataFrame: 北向资金持股数据
        """
        try:
            self.logger.info("正在获取北向资金持股数据...")
            df = self._retry_request(ak.stock_hsgt_hold_stock_em, symbol="北上")
            self.logger.info(f"北向资金持股数据获取成功，共 {len(df)} 条记录")
            return df
        except Exception as e:
            self.logger.error(f"获取北向资金持股数据失败: {e}")
            return None
    
    def fetch_hsgt_south(self) -> Optional[pd.DataFrame]:
        """
        获取港股通持股明细
        
        Returns:
            DataFrame: 南向资金持股数据
        """
        try:
            self.logger.info("正在获取南向资金持股数据...")
            df = self._retry_request(ak.stock_hsgt_hold_stock_em, symbol="南下")
            self.logger.info(f"南向资金持股数据获取成功，共 {len(df)} 条记录")
            return df
        except Exception as e:
            self.logger.error(f"获取南向资金持股数据失败: {e}")
            return None
    
    def fetch_hsgt_net_flow(self) -> Optional[pd.DataFrame]:
        """
        获取沪深港通资金流向
        
        Returns:
            DataFrame: 资金流向数据
        """
        try:
            self.logger.info("正在获取沪深港通资金流向...")
            df_north = self._retry_request(ak.stock_hsgt_north_net_flow_in_em)
            df_south = self._retry_request(ak.stock_hsgt_south_net_flow_in_em)
            
            result = {
                'north': df_north,
                'south': df_south
            }
            return result
        except Exception as e:
            self.logger.error(f"获取沪深港通资金流向失败: {e}")
            return None
    
    def fetch_dividend_batch(self, codes: List[str], market='a', delay=0.5) -> pd.DataFrame:
        """
        批量获取股票分红数据
        
        Args:
            codes: 股票代码列表
            market: 市场类型
            delay: 请求间隔（秒）
        
        Returns:
            DataFrame: 合并后的分红数据
        """
        all_dividends = []
        
        for code in codes:
            try:
                if market == 'a':
                    df = self.fetch_a_stock_dividend(code)
                else:
                    df = self.fetch_hk_stock_dividend(code)
                
                if df is not None and not df.empty:
                    df = df.copy()
                    df['股票代码'] = code
                    all_dividends.append(df)
                
                time.sleep(delay)
            except Exception as e:
                self.logger.warning(f"获取 {code} 分红数据失败: {e}")
        
        if all_dividends:
            result = pd.concat(all_dividends, ignore_index=True)
            self.logger.info(f"批量获取分红数据成功，共 {len(result)} 条记录")
            return result
        
        return pd.DataFrame()
    
    def fetch_high_dividend_stocks(self, top_n=50) -> Optional[pd.DataFrame]:
        """
        获取高股息率股票
        
        Args:
            top_n: 返回前N只
        
        Returns:
            DataFrame: 高股息率股票列表
        """
        try:
            self.logger.info("正在获取高股息率股票...")
            df = self._retry_request(ak.stock_a_high_dividend)
            if df is not None:
                df = df.head(top_n)
                self.logger.info(f"获取到 {len(df)} 只高股息率股票")
            return df
        except Exception as e:
            self.logger.error(f"获取高股息率股票失败: {e}")
            return None
    
    def fetch_stock_info(self, symbol: str, market='a') -> Optional[pd.DataFrame]:
        """
        获取股票基本信息
        
        Args:
            symbol: 股票代码
            market: 市场类型
        
        Returns:
            DataFrame: 股票基本信息
        """
        try:
            if market == 'a':
                df = self._retry_request(ak.stock_individual_info_em, symbol=symbol)
                return df
            elif market == 'hk':
                df = self._retry_request(ak.stock_hk_spot_em)
                if df is not None:
                    return df[df['代码'] == symbol]
            return None
        except Exception as e:
            self.logger.error(f"获取股票 {symbol} 信息失败: {e}")
            return None
