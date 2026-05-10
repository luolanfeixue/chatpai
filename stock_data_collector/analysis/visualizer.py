"""
可视化模块
生成分红策略分析的可视化图表
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from typing import Optional, List
import logging

from utils.logger import get_logger

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class DividendVisualizer:
    """分红策略可视化器"""
    
    def __init__(self, output_dir: str = 'output'):
        """
        初始化可视化器
        
        Args:
            output_dir: 输出目录
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = get_logger()
    
    def plot_return_distribution(self, result_df: pd.DataFrame,
                               save_path: str = None) -> Optional[str]:
        """
        绘制收益率分布图
        
        Args:
            result_df: 分析结果DataFrame
            save_path: 保存路径
        
        Returns:
            str: 保存的文件路径
        """
        if result_df is None or result_df.empty:
            self.logger.warning("数据为空，跳过绘制")
            return None
        
        try:
            fig, axes = plt.subplots(2, 2, figsize=(14, 10))
            
            # 子图1: 收益率直方图
            ax1 = axes[0, 0]
            ax1.hist(result_df['total_return'], bins=50, edgecolor='black', alpha=0.7)
            ax1.axvline(x=0, color='red', linestyle='--', linewidth=2, label='盈亏平衡点')
            ax1.axvline(x=result_df['total_return'].mean(), color='green', 
                       linestyle='--', linewidth=2, 
                       label=f'平均收益: {result_df["total_return"].mean():.2f}%')
            ax1.set_xlabel("总收益率(%)", fontsize=12)
            ax1.set_ylabel("频数", fontsize=12)
            ax1.set_title("收益率分布", fontsize=14, fontweight='bold')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # 子图2: 盈利vs亏损饼图
            ax2 = axes[0, 1]
            profitable = result_df['is_profitable'].sum()
            loss = len(result_df) - profitable
            colors = ['#2ecc71', '#e74c3c']
            explode = (0.05, 0)
            ax2.pie([profitable, loss], labels=['盈利', '亏损'], 
                   autopct='%1.1f%%', colors=colors, explode=explode,
                   shadow=True, startangle=90)
            ax2.set_title("盈利概率分布", fontsize=14, fontweight='bold')
            
            # 子图3: 分红收益vs价差收益散点图
            ax3 = axes[1, 0]
            scatter = ax3.scatter(result_df['dividend_yield'], 
                                result_df['price_change_pct'],
                                c=result_df['is_profitable'], 
                                cmap='RdYlGn', alpha=0.6, s=50)
            ax3.axhline(y=0, color='red', linestyle='--', alpha=0.5)
            ax3.axvline(x=0, color='red', linestyle='--', alpha=0.5)
            ax3.set_xlabel("分红收益率(%)", fontsize=12)
            ax3.set_ylabel("价差收益率(%)", fontsize=12)
            ax3.set_title("分红收益 vs 价差收益", fontsize=14, fontweight='bold')
            plt.colorbar(scatter, ax=ax3, label='是否盈利')
            ax3.grid(True, alpha=0.3)
            
            # 子图4: 持有期间收益率箱线图
            ax4 = axes[1, 1]
            profitable_returns = result_df[result_df['is_profitable'] == 1]['total_return']
            loss_returns = result_df[result_df['is_profitable'] == 0]['total_return']
            
            box_data = [profitable_returns, loss_returns]
            bp = ax4.boxplot(box_data, labels=['盈利', '亏损'], patch_artist=True)
            
            colors_box = ['#2ecc71', '#e74c3c']
            for patch, color in zip(bp['boxes'], colors_box):
                patch.set_facecolor(color)
                patch.set_alpha(0.7)
            
            ax4.axhline(y=0, color='red', linestyle='--', alpha=0.5)
            ax4.set_xlabel("是否盈利", fontsize=12)
            ax4.set_ylabel("总收益率(%)", fontsize=12)
            ax4.set_title("盈利与亏损收益率对比", fontsize=14, fontweight='bold')
            ax4.grid(True, alpha=0.3, axis='y')
            
            plt.suptitle("分红策略收益率分析", fontsize=16, fontweight='bold', y=1.02)
            plt.tight_layout()
            
            if save_path is None:
                save_path = self.output_dir / "return_distribution.png"
            else:
                save_path = Path(save_path)
            
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"收益率分布图已保存到: {save_path}")
            return str(save_path)
            
        except Exception as e:
            self.logger.error(f"绘制收益率分布图失败: {e}")
            plt.close()
            return None
    
    def plot_time_series(self, result_df: pd.DataFrame,
                        save_path: str = None) -> Optional[str]:
        """
        绘制时间序列分析图
        
        Args:
            result_df: 分析结果DataFrame
            save_path: 保存路径
        
        Returns:
            str: 保存的文件路径
        """
        if result_df is None or result_df.empty:
            self.logger.warning("数据为空，跳过绘制")
            return None
        
        try:
            result_df = result_df.copy()
            result_df['dividend_date'] = pd.to_datetime(result_df['dividend_date'])
            result_df = result_df.sort_values('dividend_date')
            
            fig, axes = plt.subplots(2, 1, figsize=(14, 10))
            
            # 子图1: 收益率时间序列
            ax1 = axes[0]
            ax1.plot(result_df['dividend_date'], result_df['total_return'], 
                    'b-', alpha=0.5, linewidth=0.8, label='日收益率')
            
            # 添加移动平均
            result_df['rolling_return'] = result_df['total_return'].rolling(window=20, min_periods=1).mean()
            ax1.plot(result_df['dividend_date'], result_df['rolling_return'],
                    'r-', linewidth=2, label='20日均线')
            
            ax1.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            ax1.fill_between(result_df['dividend_date'], result_df['total_return'], 0,
                           where=(result_df['total_return'] > 0), color='green', alpha=0.3)
            ax1.fill_between(result_df['dividend_date'], result_df['total_return'], 0,
                           where=(result_df['total_return'] < 0), color='red', alpha=0.3)
            
            ax1.set_xlabel("日期", fontsize=12)
            ax1.set_ylabel("收益率(%)", fontsize=12)
            ax1.set_title("分红收益率时间序列", fontsize=14, fontweight='bold')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            
            # 子图2: 盈利概率移动平均
            ax2 = axes[1]
            result_df['rolling_profit_rate'] = result_df['is_profitable'].rolling(
                window=30, min_periods=1).mean() * 100
            
            ax2.plot(result_df['dividend_date'], result_df['rolling_profit_rate'],
                    'g-', linewidth=2, label='30日盈利概率')
            ax2.axhline(y=50, color='red', linestyle='--', alpha=0.5, label='50%基准线')
            
            ax2.set_xlabel("日期", fontsize=12)
            ax2.set_ylabel("盈利概率(%)", fontsize=12)
            ax2.set_title("盈利概率时间序列", fontsize=14, fontweight='bold')
            ax2.set_ylim(0, 100)
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            
            plt.suptitle("分红策略时间序列分析", fontsize=16, fontweight='bold', y=1.02)
            plt.tight_layout()
            
            if save_path is None:
                save_path = self.output_dir / "time_series.png"
            else:
                save_path = Path(save_path)
            
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"时间序列图已保存到: {save_path}")
            return str(save_path)
            
        except Exception as e:
            self.logger.error(f"绘制时间序列图失败: {e}")
            plt.close()
            return None
    
    def plot_yearly_analysis(self, result_df: pd.DataFrame,
                           save_path: str = None) -> Optional[str]:
        """
        绘制年度分析图
        
        Args:
            result_df: 分析结果DataFrame
            save_path: 保存路径
        
        Returns:
            str: 保存的文件路径
        """
        if result_df is None or result_df.empty:
            self.logger.warning("数据为空，跳过绘制")
            return None
        
        try:
            result_df = result_df.copy()
            result_df['year'] = pd.to_datetime(result_df['dividend_date']).dt.year
            
            yearly_stats = result_df.groupby('year').agg({
                'is_profitable': 'mean',
                'total_return': 'mean'
            })
            
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            
            # 子图1: 年度盈利概率
            ax1 = axes[0]
            years = yearly_stats.index
            profit_rates = yearly_stats['is_profitable'] * 100
            
            bars = ax1.bar(years, profit_rates, color='steelblue', alpha=0.8, edgecolor='black')
            ax1.axhline(y=50, color='red', linestyle='--', label='50%基准线')
            
            for bar, rate in zip(bars, profit_rates):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{rate:.1f}%', ha='center', va='bottom', fontsize=10)
            
            ax1.set_xlabel("年份", fontsize=12)
            ax1.set_ylabel("盈利概率(%)", fontsize=12)
            ax1.set_title("年度盈利概率", fontsize=14, fontweight='bold')
            ax1.set_ylim(0, 100)
            ax1.legend()
            ax1.grid(True, alpha=0.3, axis='y')
            
            # 子图2: 年度平均收益率
            ax2 = axes[1]
            avg_returns = yearly_stats['total_return']
            
            colors = ['green' if x >= 0 else 'red' for x in avg_returns]
            bars2 = ax2.bar(years, avg_returns, color=colors, alpha=0.8, edgecolor='black')
            ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            
            for bar, ret in zip(bars2, avg_returns):
                height = bar.get_height()
                va = 'bottom' if height >= 0 else 'top'
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{ret:.1f}%', ha='center', va=va, fontsize=10)
            
            ax2.set_xlabel("年份", fontsize=12)
            ax2.set_ylabel("平均收益率(%)", fontsize=12)
            ax2.set_title("年度平均收益率", fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3, axis='y')
            
            plt.suptitle("分红策略年度分析", fontsize=16, fontweight='bold', y=1.02)
            plt.tight_layout()
            
            if save_path is None:
                save_path = self.output_dir / "yearly_analysis.png"
            else:
                save_path = Path(save_path)
            
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"年度分析图已保存到: {save_path}")
            return str(save_path)
            
        except Exception as e:
            self.logger.error(f"绘制年度分析图失败: {e}")
            plt.close()
            return None
    
    def plot_yield_analysis(self, result_df: pd.DataFrame,
                          save_path: str = None) -> Optional[str]:
        """
        绘制股息率分析图
        
        Args:
            result_df: 分析结果DataFrame
            save_path: 保存路径
        
        Returns:
            str: 保存的文件路径
        """
        if result_df is None or result_df.empty:
            self.logger.warning("数据为空，跳过绘制")
            return None
        
        try:
            result_df = result_df.copy()
            result_df['yield_group'] = pd.cut(
                result_df['dividend_yield'],
                bins=[0, 2, 4, 6, 100],
                labels=['<2%', '2-4%', '4-6%', '>6%']
            )
            
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            
            # 子图1: 各股息率组的盈利概率
            ax1 = axes[0]
            yield_profit = result_df.groupby('yield_group')['is_profitable'].mean() * 100
            
            bars = ax1.bar(yield_profit.index.astype(str), yield_profit.values,
                          color='coral', alpha=0.8, edgecolor='black')
            ax1.axhline(y=50, color='red', linestyle='--', label='50%基准线')
            
            for bar, rate in zip(bars, yield_profit.values):
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{rate:.1f}%', ha='center', va='bottom', fontsize=10)
            
            ax1.set_xlabel("股息率分组", fontsize=12)
            ax1.set_ylabel("盈利概率(%)", fontsize=12)
            ax1.set_title("不同股息率组的盈利概率", fontsize=14, fontweight='bold')
            ax1.set_ylim(0, 100)
            ax1.legend()
            ax1.grid(True, alpha=0.3, axis='y')
            
            # 子图2: 各股息率组的平均收益率
            ax2 = axes[1]
            yield_return = result_df.groupby('yield_group')['total_return'].mean()
            
            colors = ['green' if x >= 0 else 'red' for x in yield_return.values]
            bars2 = ax2.bar(yield_return.index.astype(str), yield_return.values,
                           color=colors, alpha=0.8, edgecolor='black')
            ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            
            for bar, ret in zip(bars2, yield_return.values):
                height = bar.get_height()
                va = 'bottom' if height >= 0 else 'top'
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{ret:.1f}%', ha='center', va=va, fontsize=10)
            
            ax2.set_xlabel("股息率分组", fontsize=12)
            ax2.set_ylabel("平均收益率(%)", fontsize=12)
            ax2.set_title("不同股息率组的平均收益率", fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3, axis='y')
            
            plt.suptitle("股息率分析", fontsize=16, fontweight='bold', y=1.02)
            plt.tight_layout()
            
            if save_path is None:
                save_path = self.output_dir / "yield_analysis.png"
            else:
                save_path = Path(save_path)
            
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"股息率分析图已保存到: {save_path}")
            return str(save_path)
            
        except Exception as e:
            self.logger.error(f"绘制股息率分析图失败: {e}")
            plt.close()
            return None
    
    def plot_stock_comparison(self, result_df: pd.DataFrame,
                            top_n: int = 10,
                            save_path: str = None) -> Optional[str]:
        """
        绘制股票对比图
        
        Args:
            result_df: 分析结果DataFrame
            top_n: 显示前N只股票
            save_path: 保存路径
        
        Returns:
            str: 保存的文件路径
        """
        if result_df is None or result_df.empty:
            self.logger.warning("数据为空，跳过绘制")
            return None
        
        try:
            stock_stats = result_df.groupby('stock_code').agg({
                'total_return': 'mean',
                'is_profitable': 'mean'
            }).sort_values('total_return', ascending=False).head(top_n)
            
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            
            # 子图1: 股票平均收益率对比
            ax1 = axes[0]
            stocks = stock_stats.index
            returns = stock_stats['total_return']
            
            colors = ['green' if x >= 0 else 'red' for x in returns]
            bars = ax1.barh(stocks, returns, color=colors, alpha=0.8, edgecolor='black')
            ax1.axvline(x=0, color='black', linestyle='-', alpha=0.3)
            
            ax1.set_xlabel("平均收益率(%)", fontsize=12)
            ax1.set_ylabel("股票代码", fontsize=12)
            ax1.set_title(f"股票平均收益率对比 (Top {top_n})", fontsize=14, fontweight='bold')
            ax1.invert_yaxis()
            ax1.grid(True, alpha=0.3, axis='x')
            
            # 子图2: 股票盈利概率对比
            ax2 = axes[1]
            profit_rates = stock_stats['is_profitable'] * 100
            
            colors = plt.cm.RdYlGn(profit_rates / 100)
            bars2 = ax2.barh(stocks, profit_rates, color=colors, alpha=0.8, edgecolor='black')
            ax2.axvline(x=50, color='red', linestyle='--', alpha=0.5, label='50%基准线')
            
            ax2.set_xlabel("盈利概率(%)", fontsize=12)
            ax2.set_ylabel("股票代码", fontsize=12)
            ax2.set_title(f"股票盈利概率对比 (Top {top_n})", fontsize=14, fontweight='bold')
            ax2.invert_yaxis()
            ax2.legend()
            ax2.grid(True, alpha=0.3, axis='x')
            
            plt.suptitle("股票表现对比分析", fontsize=16, fontweight='bold', y=1.02)
            plt.tight_layout()
            
            if save_path is None:
                save_path = self.output_dir / "stock_comparison.png"
            else:
                save_path = Path(save_path)
            
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            self.logger.info(f"股票对比图已保存到: {save_path}")
            return str(save_path)
            
        except Exception as e:
            self.logger.error(f"绘制股票对比图失败: {e}")
            plt.close()
            return None
    
    def generate_full_report(self, result_df: pd.DataFrame,
                           output_prefix: str = "dividend_analysis") -> List[str]:
        """
        生成完整的分析报告图表
        
        Args:
            result_df: 分析结果DataFrame
            output_prefix: 输出文件前缀
        
        Returns:
            list: 保存的文件路径列表
        """
        saved_files = []
        
        self.logger.info("开始生成完整分析报告...")
        
        files = [
            self.plot_return_distribution(result_df, f"{output_prefix}_distribution.png"),
            self.plot_time_series(result_df, f"{output_prefix}_timeseries.png"),
            self.plot_yearly_analysis(result_df, f"{output_prefix}_yearly.png"),
            self.plot_yield_analysis(result_df, f"{output_prefix}_yield.png"),
            self.plot_stock_comparison(result_df, f"{output_prefix}_comparison.png")
        ]
        
        for f in files:
            if f:
                saved_files.append(f)
        
        self.logger.info(f"分析报告生成完成，共 {len(saved_files)} 个文件")
        return saved_files
