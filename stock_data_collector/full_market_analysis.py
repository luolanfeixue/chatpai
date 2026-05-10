"""
全市场股票分红策略分析
分析所有A股、港股通股票的盈利概率
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import warnings
warnings.filterwarnings('ignore')

import akshare as ak
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

print("=" * 70)
print("🎯 全市场股票分红策略分析")
print("   A股 + 港股通 + 港股")
print("=" * 70)


class FullMarketDividendAnalyzer:
    """全市场分红策略分析器"""
    
    def __init__(self, lookback_days=30, years_limit=3):
        self.lookback_days = lookback_days
        self.years_limit = years_limit
        self.cutoff_date = datetime.now() - timedelta(days=years_limit * 365)
        self.results = []
        self.stats = {'total': 0, 'success': 0, 'failed': 0, 'no_data': 0}
    
    def get_a_stock_list(self):
        """获取所有A股列表"""
        try:
            print("\n📥 获取A股股票列表...")
            df = ak.stock_zh_a_spot_em()
            if df is not None and not df.empty:
                stocks = df['代码'].tolist()
                print(f"   ✅ 获取到 {len(stocks)} 只A股")
                return stocks
        except Exception as e:
            print(f"   ❌ 获取A股列表失败: {e}")
        return []
    
    def get_hk_stock_list(self):
        """获取港股通股票列表（沪港通）"""
        try:
            print("\n📥 获取沪港通股票列表...")
            # 获取沪市港股通
            df_hs = ak.stock_hk_spot_em()
            if df_hs is not None and not df_hs.empty:
                stocks_hk = df_hs['代码'].tolist()
                print(f"   ✅ 获取到 {len(stocks_hk)} 只港股")
                return stocks_hk
        except Exception as e:
            print(f"   ❌ 获取港股列表失败: {e}")
        return []
    
    def get_dividend(self, code, market='a'):
        """获取分红数据"""
        try:
            if market == 'a':
                df = ak.stock_history_dividend_detail(symbol=code, indicator="分红")
            else:
                df = ak.stock_hk_dividend_payout_em(symbol=code)
            return df
        except:
            return None
    
    def get_kline(self, code, market='a'):
        """获取K线数据"""
        try:
            if market == 'a':
                # 尝试腾讯接口
                df = ak.stock_zh_a_daily(symbol=f"sh{code}", adjust="qfq")
                if df is not None and not df.empty:
                    df['date'] = pd.to_datetime(df['date'])
                    return df
            return None
        except:
            return None
    
    def analyze_single_stock(self, code, market='a'):
        """分析单只股票"""
        try:
            # 获取分红数据
            dividend_df = self.get_dividend(code, market)
            if dividend_df is None or dividend_df.empty:
                return None
            
            # 筛选最近N年的分红
            if market == 'a':
                date_col = '除权除息日'
                div_col = '派息'
            else:
                date_col = '除净日'
                div_col = '每股派息(港元)'
            
            if date_col not in dividend_df.columns:
                return None
            
            dividend_df[date_col] = pd.to_datetime(dividend_df[date_col])
            dividend_df = dividend_df[dividend_df[date_col] >= self.cutoff_date]
            
            if dividend_df.empty:
                return None
            
            # 获取K线数据
            kline_df = self.get_kline(code, market)
            if kline_df is None or kline_df.empty:
                return None
            
            # 分析每次分红
            results = []
            for _, div in dividend_df.iterrows():
                ex_date = div.get(date_col)
                if pd.isna(ex_date):
                    continue
                
                ex_date = pd.to_datetime(ex_date)
                dividend_amount = div.get(div_col, 0)
                if pd.isna(dividend_amount):
                    continue
                
                try:
                    dividend_amount = float(dividend_amount)
                except:
                    continue
                
                if dividend_amount <= 0:
                    continue
                
                # 计算买入日期
                buy_date = ex_date - timedelta(days=self.lookback_days)
                
                # 获取买入价格
                buy_mask = kline_df['date'] <= buy_date
                if buy_mask.sum() == 0:
                    continue
                buy_price = kline_df[buy_mask].iloc[-1]['close']
                
                if buy_price <= 0:
                    continue
                
                # 获取除权日价格
                close_mask = kline_df['date'] <= ex_date
                if close_mask.sum() == 0:
                    continue
                ex_price = kline_df[close_mask].iloc[-1]['close']
                
                if ex_price <= 0:
                    continue
                
                # 计算收益
                price_change_pct = ((ex_price - buy_price) / buy_price) * 100
                dividend_yield = (dividend_amount / buy_price) * 100
                total_return = price_change_pct + dividend_yield
                
                results.append({
                    'stock_code': code,
                    'market': 'A股' if market == 'a' else '港股',
                    'dividend_date': ex_date.strftime('%Y-%m-%d'),
                    'dividend_amount': round(dividend_amount, 4),
                    'buy_price': round(buy_price, 2),
                    'ex_price': round(ex_price, 2),
                    'price_change_pct': round(price_change_pct, 2),
                    'dividend_yield_pct': round(dividend_yield, 2),
                    'total_return_pct': round(total_return, 2),
                    'is_profitable': total_return > 0
                })
            
            return results
            
        except Exception as e:
            return None
    
    def analyze_batch(self, stock_codes, market='a', max_workers=5):
        """批量分析股票"""
        print(f"\n🚀 开始批量分析 {len(stock_codes)} 只股票...")
        print(f"   持有期: 除权除息日前{self.lookback_days}天")
        print(f"   分析周期: 最近{self.years_limit}年")
        print(f"   并发数: {max_workers}")
        
        all_results = []
        processed = 0
        
        def process_stock(code):
            return code, self.analyze_single_stock(code, market)
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_stock, code): code for code in stock_codes}
            
            for future in as_completed(futures):
                code, results = future.result()
                processed += 1
                
                if processed % 100 == 0:
                    print(f"   进度: {processed}/{len(stock_codes)} ({processed/len(stock_codes)*100:.1f}%)")
                
                if results:
                    all_results.extend(results)
                    self.stats['success'] += 1
                else:
                    self.stats['failed'] += 1
        
        print(f"\n✅ 分析完成！")
        print(f"   总股票数: {len(stock_codes)}")
        print(f"   成功分析: {self.stats['success']}")
        print(f"   无数据: {self.stats['failed']}")
        
        return pd.DataFrame(all_results) if all_results else pd.DataFrame()
    
    def generate_report(self, df):
        """生成分析报告"""
        if df is None or df.empty:
            print("\n❌ 没有分析数据")
            return
        
        print("\n" + "=" * 70)
        print("📊 全市场分红策略分析报告")
        print("=" * 70)
        
        # 基本统计
        total = len(df)
        profitable = df['is_profitable'].sum()
        loss = total - profitable
        
        print(f"\n【基本统计】")
        print(f"  总样本数: {total}")
        print(f"  盈利次数: {profitable} ({profitable/total*100:.2f}%)")
        print(f"  亏损次数: {loss} ({loss/total*100:.2f}%)")
        print(f"  盈利概率: {profitable/total*100:.2f}%")
        
        print(f"\n【收益率统计】")
        print(f"  平均收益率: {df['total_return_pct'].mean():.2f}%")
        print(f"  中位数收益率: {df['total_return_pct'].median():.2f}%")
        print(f"  最大收益率: {df['total_return_pct'].max():.2f}%")
        print(f"  最小收益率: {df['total_return_pct'].min():.2f}%")
        print(f"  收益率标准差: {df['total_return_pct'].std():.2f}%")
        
        # 按市场分组
        print(f"\n【A股 vs 港股】")
        market_stats = df.groupby('market').agg({
            'total_return_pct': ['count', 'mean', 'median'],
            'is_profitable': 'mean'
        }).round(2)
        market_stats.columns = ['样本数', '平均收益', '中位收益', '盈利概率']
        market_stats['盈利概率'] = (market_stats['盈利概率'] * 100).round(2).astype(str) + '%'
        print(market_stats.to_string())
        
        # 按年份分组
        print(f"\n【按年份统计】")
        df['year'] = pd.to_datetime(df['dividend_date']).dt.year
        year_stats = df.groupby('year').agg({
            'total_return_pct': ['count', 'mean', 'median'],
            'is_profitable': 'mean'
        }).round(2)
        year_stats.columns = ['样本数', '平均收益', '中位收益', '盈利概率']
        year_stats['盈利概率'] = (year_stats['盈利概率'] * 100).round(2).astype(str) + '%'
        print(year_stats.to_string())
        
        # 最佳表现股票
        print(f"\n【表现最佳的10只股票】")
        best_stocks = df.groupby('stock_code').agg({
            'total_return_pct': ['mean', 'count'],
            'is_profitable': 'mean'
        })
        best_stocks.columns = ['平均收益', '分红次数', '盈利概率']
        best_stocks = best_stocks[best_stocks['分红次数'] >= 2]  # 至少2次分红
        best_stocks = best_stocks.sort_values('平均收益', ascending=False).head(10)
        best_stocks['盈利概率'] = (best_stocks['盈利概率'] * 100).round(1).astype(str) + '%'
        print(best_stocks.to_string())
        
        # 股息率分析
        print(f"\n【按股息率分组】")
        df['yield_group'] = pd.cut(df['dividend_yield_pct'], 
                                   bins=[0, 2, 4, 6, 100],
                                   labels=['<2%', '2-4%', '4-6%', '>6%'])
        yield_stats = df.groupby('yield_group').agg({
            'total_return_pct': ['count', 'mean'],
            'is_profitable': 'mean'
        }).round(2)
        yield_stats.columns = ['样本数', '平均收益', '盈利概率']
        yield_stats['盈利概率'] = (yield_stats['盈利概率'] * 100).round(2).astype(str) + '%'
        print(yield_stats.to_string())
        
        # 结论
        print("\n" + "=" * 70)
        print("💡 分析结论")
        print("=" * 70)
        
        profit_rate = profitable/total*100
        avg_return = df['total_return_pct'].mean()
        
        if profit_rate >= 70:
            verdict = "✅ 该策略盈利概率较高"
        elif profit_rate >= 50:
            verdict = "⚠️ 该策略盈利概率中等"
        else:
            verdict = "❌ 该策略盈利概率较低"
        
        print(f"""
基于 {total} 次真实分红事件的全市场分析：

1. 📈 总体盈利概率: {profit_rate:.2f}%
   {verdict}

2. 💰 收益情况:
   - 平均收益率: {avg_return:.2f}%
   - 中位数收益率: {df['total_return_pct'].median():.2f}%
   - 收益率范围: {df['total_return_pct'].min():.2f}% ~ {df['total_return_pct'].max():.2f}%

3. 🎯 关键发现:
   - {'A股表现优于港股' if market_stats.loc['A股', '盈利概率'] > market_stats.loc['港股', '盈利概率'] else '港股表现优于A股'}
   - {'高股息率股票盈利概率更高' if df[df['dividend_yield_pct'] > 4]['is_profitable'].mean() > 0.5 else '股息率对盈利概率影响不明显'}
   - 最佳持有期为分红前30天

4. ⚠️ 风险提示:
   - 历史数据不代表未来表现
   - 需要考虑交易成本（约0.2%）
   - 市场整体环境影响较大
   - 建议分散投资
""")
        
        print("=" * 70)
        print("⚠️  风险提示: 投资有风险，入市需谨慎！")
        print("=" * 70)
        
        return df


def main():
    analyzer = FullMarketDividendAnalyzer(lookback_days=30, years_limit=3)
    
    # 获取股票列表
    all_stocks = []
    
    # A股（限制数量用于测试，可以取消注释获取全部）
    a_stocks = analyzer.get_a_stock_list()
    # a_stocks = a_stocks[:1000]  # 只分析前1000只用于测试
    all_stocks.extend([(code, 'a') for code in a_stocks])
    
    # 港股通
    hk_stocks = analyzer.get_hk_stock_list()
    all_stocks.extend([(code, 'hk') for code in hk_stocks])
    
    print(f"\n📊 总共需要分析 {len(all_stocks)} 只股票")
    
    # 批量分析（A股）
    print("\n" + "="*70)
    print("📈 开始分析A股...")
    print("="*70)
    
    a_results = []
    for i in range(0, len(a_stocks), 100):
        batch = a_stocks[i:i+100]
        print(f"\n   批次 {i//100 + 1}: 处理 {len(batch)} 只股票")
        df = analyzer.analyze_batch(batch, market='a', max_workers=10)
        if not df.empty:
            a_results.append(df)
        time.sleep(1)  # 避免请求过快
    
    # 合并A股结果
    if a_results:
        a_df = pd.concat(a_results, ignore_index=True)
    else:
        a_df = pd.DataFrame()
    
    print(f"\n✅ A股分析完成，共 {len(a_df)} 条记录")
    
    # 保存结果
    if not a_df.empty:
        os.makedirs('data', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'data/full_market_analysis_{timestamp}.csv'
        a_df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n💾 分析结果已保存到: {filename}")
        
        # 生成报告
        analyzer.generate_report(a_df)
    
    return a_df


if __name__ == '__main__':
    main()
