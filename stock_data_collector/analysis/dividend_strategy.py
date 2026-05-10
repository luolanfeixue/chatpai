"""
分红策略分析模块
分析在除权除息日前N天买入股票的盈利概率
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
import logging
import time
import warnings

from core.data_fetcher import DataFetcher
from utils.logger import get_logger

warnings.filterwarnings('ignore')


class DividendStrategyAnalyzer:
    """
    分红策略分析器
    
    研究目标: 分析在除权除息日前N天买入股票的盈利概率
    策略逻辑:
        - 买入时机: 除权除息日前N个交易日
        - 持有期间: N个交易日
        - 收益计算: 价差收益 + 分红收益
    """
    
    def __init__(self, lookback_days: int = 30):
        """
        初始化分析器
        
        Args:
            lookback_days: 分红前多少天买入（默认30天）
        """
        self.lookback_days = lookback_days
        self.fetcher = DataFetcher()
        self.logger = get_logger()
        self.results = []
    
    def analyze_single_stock(self, stock_code: str, 
                           market: str = 'a') -> Optional[pd.DataFrame]:
        """
        分析单只股票的分红策略收益
        
        Args:
            stock_code: 股票代码
            market: 市场类型 ("a" 或 "hk")
        
        Returns:
            DataFrame: 分析结果
        """
        try:
            self.logger.info(f"开始分析 {stock_code} 的分红策略...")
            
            # 1. 获取分红历史
            dividend_df = self._get_dividend_history(stock_code, market)
            if dividend_df is None or dividend_df.empty:
                self.logger.warning(f"{stock_code} 没有分红数据")
                return None
            
            # 2. 获取历史价格数据
            price_df = self._get_price_history(stock_code, market)
            if price_df is None or price_df.empty:
                self.logger.warning(f"{stock_code} 没有价格数据")
                return None
            
            # 3. 计算每次分红的策略收益
            results = []
            for _, dividend in dividend_df.iterrows():
                result = self._calculate_single_dividend_return(
                    stock_code, dividend, price_df, market
                )
                if result:
                    results.append(result)
            
            if not results:
                self.logger.warning(f"{stock_code} 没有计算出有效的分析结果")
                return None
            
            result_df = pd.DataFrame(results)
            self.logger.info(f"{stock_code} 分析完成，共 {len(result_df)} 条记录")
            return result_df
            
        except Exception as e:
            self.logger.error(f"分析 {stock_code} 失败: {e}")
            return None
    
    def _get_dividend_history(self, stock_code: str, market: str) -> Optional[pd.DataFrame]:
        """获取分红历史"""
        try:
            if market == 'a':
                df = self.fetcher.fetch_a_stock_dividend(stock_code)
            else:
                df = self.fetcher.fetch_hk_stock_dividend(stock_code)
            return df
        except Exception as e:
            self.logger.error(f"获取分红历史失败: {e}")
            return None
    
    def _get_price_history(self, stock_code: str, market: str) -> Optional[pd.DataFrame]:
        """获取历史价格数据"""
        try:
            end_date = datetime.now().strftime("%Y%m%d")
            start_date = (datetime.now() - timedelta(days=365*5)).strftime("%Y%m%d")
            
            if market == 'a':
                df = self.fetcher.fetch_a_stock_history(
                    symbol=stock_code,
                    start_date=start_date,
                    end_date=end_date,
                    period="daily",
                    adjust=""
                )
                if df is not None and '日期' in df.columns:
                    df['日期'] = pd.to_datetime(df['日期'])
                return df
            else:
                # 港股价格获取逻辑暂未实现
                return None
                
        except Exception as e:
            self.logger.error(f"获取价格历史失败: {e}")
            return None
    
    def _calculate_single_dividend_return(self, stock_code: str, 
                                        dividend: pd.Series, 
                                        price_df: pd.DataFrame, 
                                        market: str) -> Optional[Dict]:
        """
        计算单次分红的策略收益
        
        Returns:
            dict: 包含所有分析字段的字典
        """
        try:
            # 获取除权除息日
            if market == 'a':
                if '除权除息日' not in dividend:
                    return None
                ex_right_date = pd.to_datetime(dividend['除权除息日'])
                if pd.isna(ex_right_date):
                    return None
                    
                if '每股派现(元)' in dividend and not pd.isna(dividend['每股派现(元)']):
                    dividend_per_share = float(dividend['每股派现(元)'])
                else:
                    return None
            else:
                if '除净日' not in dividend:
                    return None
                ex_right_date = pd.to_datetime(dividend['除净日'])
                if pd.isna(ex_right_date):
                    return None
                dividend_per_share = self._parse_hk_dividend(dividend.get('分红方案', ''))
            
            # 计算买入日期（除权除息日前N天）
            buy_date = ex_right_date - timedelta(days=self.lookback_days)
            
            # 找到最接近买入日期的收盘价
            price_before = self._get_nearest_price(price_df, buy_date, before=True)
            
            # 找到除权除息日当天的收盘价
            price_at_dividend = self._get_nearest_price(price_df, ex_right_date, before=False)
            
            if price_before is None or price_at_dividend is None:
                return None
            
            # 计算收益率
            price_change = price_at_dividend - price_before
            price_change_pct = (price_change / price_before) * 100 if price_before != 0 else 0
            dividend_yield = (dividend_per_share / price_before) * 100 if price_before != 0 else 0
            total_return = price_change_pct + dividend_yield
            
            return {
                'stock_code': stock_code,
                'dividend_date': ex_right_date.strftime('%Y-%m-%d'),
                'price_before': round(price_before, 2),
                'price_at_dividend': round(price_at_dividend, 2),
                'price_change': round(price_change, 2),
                'price_change_pct': round(price_change_pct, 2),
                'dividend_per_share': round(dividend_per_share, 4),
                'dividend_yield': round(dividend_yield, 2),
                'total_return': round(total_return, 2),
                'is_profitable': 1 if total_return > 0 else 0,
                'holding_days': self.lookback_days
            }
            
        except Exception as e:
            self.logger.error(f"计算单次分红收益失败: {e}")
            return None
    
    def _get_nearest_price(self, price_df: pd.DataFrame, 
                          target_date, 
                          before: bool = True) -> Optional[float]:
        """获取最接近目标日期的价格"""
        if price_df is None or price_df.empty:
            return None
        
        try:
            if '日期' not in price_df.columns or '收盘' not in price_df.columns:
                return None
            
            if before:
                mask = price_df['日期'] <= target_date
            else:
                mask = price_df['日期'] == target_date
            
            filtered = price_df[mask]
            
            if filtered.empty:
                return None
            
            if before:
                return float(filtered.iloc[-1]['收盘'])
            else:
                return float(filtered.iloc[0]['收盘'])
                
        except Exception as e:
            self.logger.error(f"获取最近价格失败: {e}")
            return None
    
    def _parse_hk_dividend(self, dividend_plan: str) -> float:
        """解析港股分红方案"""
        import re
        try:
            match = re.search(r'每股派[港币$]*([\d.]+)元?', dividend_plan)
            if match:
                return float(match.group(1))
            return 0.0
        except:
            return 0.0
    
    def analyze_batch(self, stock_codes: List[str], 
                     market: str = 'a',
                     delay: float = 0.5) -> Optional[pd.DataFrame]:
        """
        批量分析多只股票的分红策略
        
        Args:
            stock_codes: 股票代码列表
            market: 市场类型
            delay: 请求间隔（秒）
        
        Returns:
            DataFrame: 汇总分析结果
        """
        self.logger.info(f"开始批量分析 {len(stock_codes)} 只股票...")
        all_results = []
        
        success_count = 0
        fail_count = 0
        
        for code in stock_codes:
            try:
                result = self.analyze_single_stock(code, market)
                if result is not None and not result.empty:
                    all_results.append(result)
                    success_count += 1
                    self.logger.info(f"✓ {code} 分析成功 ({len(result)} 条记录)")
                else:
                    fail_count += 1
                    self.logger.warning(f"✗ {code} 分析失败或无数据")
                
                time.sleep(delay)
                
            except Exception as e:
                fail_count += 1
                self.logger.error(f"分析 {code} 异常: {e}")
        
        if not all_results:
            self.logger.warning("批量分析没有获取到任何结果")
            return None
        
        result_df = pd.concat(all_results, ignore_index=True)
        self.logger.info(f"批量分析完成: 成功 {success_count}, 失败 {fail_count}, 共 {len(result_df)} 条记录")
        
        return result_df
    
    def calculate_statistics(self, result_df: pd.DataFrame) -> Dict[str, Any]:
        """
        计算盈利概率统计
        
        Args:
            result_df: 分析结果DataFrame
        
        Returns:
            dict: 包含各项统计指标的字典
        """
        if result_df is None or result_df.empty:
            return {}
        
        try:
            total_count = len(result_df)
            profitable_count = int(result_df['is_profitable'].sum())
            loss_count = total_count - profitable_count
            
            stats = {
                '总样本数': total_count,
                '盈利次数': profitable_count,
                '亏损次数': loss_count,
                '盈利概率': f"{profitable_count / total_count * 100:.2f}%",
                '亏损概率': f"{loss_count / total_count * 100:.2f}%",
                '平均收益率': f"{result_df['total_return'].mean():.2f}%",
                '中位数收益率': f"{result_df['total_return'].median():.2f}%",
                '最大收益率': f"{result_df['total_return'].max():.2f}%",
                '最小收益率': f"{result_df['total_return'].min():.2f}%",
                '收益率标准差': f"{result_df['total_return'].std():.2f}%"
            }
            
            # 计算不同分红类型的盈利概率
            if 'dividend_type' in result_df.columns:
                stats['按分红类型统计'] = {}
                for div_type in result_df['dividend_type'].dropna().unique():
                    type_df = result_df[result_df['dividend_type'] == div_type]
                    if len(type_df) > 0:
                        type_profitable = type_df['is_profitable'].sum()
                        type_total = len(type_df)
                        stats['按分红类型统计'][div_type] = {
                            '样本数': type_total,
                            '盈利概率': f"{type_profitable / type_total * 100:.2f}%"
                        }
            
            return stats
            
        except Exception as e:
            self.logger.error(f"统计计算失败: {e}")
            return {}
    
    def analyze_by_dividend_yield(self, result_df: pd.DataFrame, 
                                 yield_bins: List[float] = None) -> pd.DataFrame:
        """
        按股息率分组分析盈利概率
        
        Args:
            result_df: 分析结果DataFrame
            yield_bins: 股息率分组区间
        
        Returns:
            DataFrame: 分组统计结果
        """
        if result_df is None or result_df.empty:
            return pd.DataFrame()
        
        if yield_bins is None:
            yield_bins = [0, 2, 4, 6, 100]
        
        try:
            result_df = result_df.copy()
            result_df['股息率分组'] = pd.cut(
                result_df['dividend_yield'], 
                bins=yield_bins,
                labels=['<2%', '2-4%', '4-6%', '>6%']
            )
            
            grouped = result_df.groupby('股息率分组').agg({
                'total_return': ['count', 'mean', 'median', 'std'],
                'is_profitable': 'mean'
            }).round(2)
            
            grouped.columns = ['样本数', '平均收益', '中位收益', '标准差', '盈利概率']
            grouped['盈利概率'] = grouped['盈利概率'].apply(lambda x: f"{x*100:.2f}%" if pd.notna(x) else 'N/A')
            
            return grouped.reset_index()
            
        except Exception as e:
            self.logger.error(f"分组分析失败: {e}")
            return pd.DataFrame()
    
    def analyze_by_year(self, result_df: pd.DataFrame) -> pd.DataFrame:
        """
        按年份分组分析盈利概率
        
        Args:
            result_df: 分析结果DataFrame
        
        Returns:
            DataFrame: 年度统计结果
        """
        if result_df is None or result_df.empty:
            return pd.DataFrame()
        
        try:
            result_df = result_df.copy()
            result_df['year'] = pd.to_datetime(result_df['dividend_date']).dt.year
            
            grouped = result_df.groupby('year').agg({
                'total_return': ['count', 'mean', 'median', 'std'],
                'is_profitable': 'mean'
            }).round(2)
            
            grouped.columns = ['样本数', '平均收益', '中位收益', '标准差', '盈利概率']
            grouped['盈利概率'] = grouped['盈利概率'].apply(lambda x: f"{x*100:.2f}%")
            
            return grouped.reset_index()
            
        except Exception as e:
            self.logger.error(f"年度分析失败: {e}")
            return pd.DataFrame()
    
    def find_best_stocks(self, result_df: pd.DataFrame, 
                        top_n: int = 10) -> pd.DataFrame:
        """
        找出表现最好的股票
        
        Args:
            result_df: 分析结果DataFrame
            top_n: 返回前N只
        
        Returns:
            DataFrame: 表现最好的股票
        """
        if result_df is None or result_df.empty:
            return pd.DataFrame()
        
        try:
            grouped = result_df.groupby('stock_code').agg({
                'total_return': ['mean', 'count'],
                'is_profitable': 'mean'
            }).round(2)
            
            grouped.columns = ['平均收益率', '分红次数', '盈利概率']
            grouped = grouped.reset_index()
            grouped = grouped.sort_values('平均收益率', ascending=False)
            
            return grouped.head(top_n)
            
        except Exception as e:
            self.logger.error(f"查找最佳股票失败: {e}")
            return pd.DataFrame()
    
    def filter_profitable(self, result_df: pd.DataFrame) -> pd.DataFrame:
        """
        筛选盈利的记录
        
        Args:
            result_df: 分析结果DataFrame
        
        Returns:
            DataFrame: 盈利的记录
        """
        if result_df is None or result_df.empty:
            return pd.DataFrame()
        
        return result_df[result_df['is_profitable'] == 1].copy()
    
    def filter_by_yield(self, result_df: pd.DataFrame, 
                       min_yield: float = 3.0) -> pd.DataFrame:
        """
        按股息率筛选
        
        Args:
            result_df: 分析结果DataFrame
            min_yield: 最小股息率
        
        Returns:
            DataFrame: 筛选后的数据
        """
        if result_df is None or result_df.empty:
            return pd.DataFrame()
        
        return result_df[result_df['dividend_yield'] >= min_yield].copy()
    
    def run_full_analysis(self, stock_codes: List[str] = None,
                         market: str = 'a') -> Tuple[Optional[pd.DataFrame], Dict]:
        """
        运行完整的分红策略分析
        
        Args:
            stock_codes: 股票代码列表
            market: 市场类型
        
        Returns:
            tuple: (分析结果DataFrame, 统计信息dict)
        """
        if stock_codes is None:
            stock_codes = ['600519', '000858', '600036', '000651']
        
        self.logger.info("=" * 60)
        self.logger.info(f"股票分红策略分析 - 除权除息日前{self.lookback_days}天买入")
        self.logger.info("=" * 60)
        
        # 1. 批量获取分析数据
        result_df = self.analyze_batch(stock_codes, market)
        
        if result_df is None or result_df.empty:
            self.logger.error("没有获取到任何分析数据！")
            return None, {}
        
        # 2. 计算统计指标
        stats = self.calculate_statistics(result_df)
        
        # 3. 按股息率分组分析
        yield_analysis = self.analyze_by_dividend_yield(result_df)
        
        # 4. 按年份分组分析
        year_analysis = self.analyze_by_year(result_df)
        
        # 5. 找出最佳股票
        best_stocks = self.find_best_stocks(result_df)
        
        # 打印结果
        self._print_analysis_results(result_df, stats, yield_analysis, year_analysis)
        
        return result_df, {
            'statistics': stats,
            'yield_analysis': yield_analysis,
            'year_analysis': year_analysis,
            'best_stocks': best_stocks
        }
    
    def _print_analysis_results(self, result_df: pd.DataFrame,
                              stats: Dict,
                              yield_analysis: pd.DataFrame,
                              year_analysis: pd.DataFrame):
        """打印分析结果"""
        print("\n" + "=" * 60)
        print("分析结果")
        print("=" * 60)
        
        print("\n【基本统计】")
        for key, value in stats.items():
            if key != '按分红类型统计':
                print(f"  {key}: {value}")
        
        if not yield_analysis.empty:
            print("\n【按股息率分组统计】")
            print(yield_analysis.to_string(index=False))
        
        if not year_analysis.empty:
            print("\n【按年份统计】")
            print(year_analysis.to_string(index=False))
