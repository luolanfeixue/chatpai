"""
使用最近3年真实数据进行分析
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import warnings
warnings.filterwarnings('ignore')

import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

print("=" * 70)
print("🎯 股票分红策略分析 - 最近3年数据")
print("=" * 70)


class RealDividendStrategyAnalyzer:
    """使用真实数据的分红策略分析器"""
    
    def __init__(self, lookback_days=30, years_limit=3):
        self.lookback_days = lookback_days
        self.years_limit = years_limit
        self.cutoff_date = datetime.now() - timedelta(days=years_limit * 365)
    
    def get_dividend(self, code):
        """获取分红数据"""
        try:
            return ak.stock_history_dividend_detail(symbol=code, indicator="分红")
        except:
            return None
    
    def get_kline(self, code):
        """使用腾讯接口获取K线数据"""
        try:
            df = ak.stock_zh_a_daily(symbol=f"sh{code}", adjust="qfq")
            if df is not None and not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                return df
        except:
            pass
        return None
    
    def analyze(self, code, name):
        """分析单只股票"""
        print(f"\n{'='*60}")
        print(f"📈 分析: {name} ({code})")
        print('='*60)
        
        # 获取分红数据
        dividend_df = self.get_dividend(code)
        if dividend_df is None or dividend_df.empty:
            print(f"  ❌ 无法获取分红数据")
            return None
        
        # 筛选最近3年的分红
        dividend_df['除权除息日'] = pd.to_datetime(dividend_df['除权除息日'])
        dividend_df = dividend_df[dividend_df['除权除息日'] >= self.cutoff_date]
        
        if dividend_df.empty:
            print(f"  ⚠️ 最近3年没有分红记录")
            return None
        
        # 获取K线数据
        kline_df = self.get_kline(code)
        if kline_df is None or kline_df.empty:
            print(f"  ❌ 无法获取K线数据")
            return None
        
        print(f"  ✅ 最近3年 {len(dividend_df)} 次分红记录")
        print(f"  ✅ 获取到 {len(kline_df)} 条K线数据")
        
        # 分析每次分红
        results = []
        for _, div in dividend_df.iterrows():
            ex_date = div.get('除权除息日')
            if pd.isna(ex_date):
                continue
            
            ex_date = pd.to_datetime(ex_date)
            dividend_amount = div.get('派息', 0)
            if pd.isna(dividend_amount):
                continue
            dividend_amount = float(dividend_amount)
            
            # 计算买入日期
            buy_date = ex_date - timedelta(days=self.lookback_days)
            
            # 获取买入价格
            buy_mask = kline_df['date'] <= buy_date
            if buy_mask.sum() == 0:
                continue
            buy_price = kline_df[buy_mask].iloc[-1]['close']
            
            # 获取除权日价格
            close_mask = kline_df['date'] <= ex_date
            if close_mask.sum() == 0:
                continue
            ex_price = kline_df[close_mask].iloc[-1]['close']
            
            # 计算收益
            price_change = ex_price - buy_price
            price_change_pct = (price_change / buy_price) * 100
            dividend_yield = (dividend_amount / buy_price) * 100
            total_return = price_change_pct + dividend_yield
            
            results.append({
                '股票代码': code,
                '股票名称': name,
                '除权除息日': ex_date.strftime('%Y-%m-%d'),
                '分红金额': dividend_amount,
                '买入价格': round(buy_price, 2),
                '除权价格': round(ex_price, 2),
                '价差收益%': round(price_change_pct, 2),
                '分红收益%': round(dividend_yield, 2),
                '总收益%': round(total_return, 2),
                '是否盈利': '✅' if total_return > 0 else '❌'
            })
        
        if results:
            result_df = pd.DataFrame(results)
            return result_df
        return None


def main():
    # 分析的股票列表
    stocks = [
        ('600519', '贵州茅台'),
        ('600036', '招商银行'),
        ('000858', '五粮液'),
        ('000651', '格力电器'),
        ('601318', '中国平安'),
        ('600887', '伊利股份'),
        ('000333', '美的集团'),
    ]
    
    years = 3
    analyzer = RealDividendStrategyAnalyzer(lookback_days=30, years_limit=years)
    all_results = []
    
    print(f"\n📅 只分析最近 {years} 年的数据")
    print(f"📅 持有期: 除权除息日前30天买入")
    
    for code, name in stocks:
        result = analyzer.analyze(code, name)
        if result is not None and not result.empty:
            all_results.append(result)
            print(f"\n  分析结果 (共 {len(result)} 次分红):")
            print(result[['除权除息日', '分红金额', '总收益%', '是否盈利']].to_string(index=False))
    
    if all_results:
        # 合并所有结果
        final_df = pd.concat(all_results, ignore_index=True)
        
        print("\n" + "=" * 70)
        print("📊 最近3年汇总统计")
        print("=" * 70)
        
        total = len(final_df)
        profitable = (final_df['是否盈利'] == '✅').sum()
        loss = total - profitable
        
        print(f"\n总样本数: {total}")
        print(f"盈利次数: {profitable} ({profitable/total*100:.1f}%)")
        print(f"亏损次数: {loss} ({loss/total*100:.1f}%)")
        print(f"盈利概率: {profitable/total*100:.2f}%")
        print(f"\n平均收益率: {final_df['总收益%'].mean():.2f}%")
        print(f"中位数收益率: {final_df['总收益%'].median():.2f}%")
        print(f"最大收益率: {final_df['总收益%'].max():.2f}%")
        print(f"最小收益率: {final_df['总收益%'].min():.2f}%")
        
        # 按股票分组
        print("\n" + "=" * 70)
        print("📊 各股票表现")
        print("=" * 70)
        stock_stats = final_df.groupby('股票名称').agg({
            '总收益%': ['count', 'mean', 'min', 'max'],
            '是否盈利': lambda x: (x == '✅').sum()
        }).round(2)
        stock_stats.columns = ['次数', '平均收益%', '最小收益%', '最大收益%', '盈利次数']
        stock_stats['盈利概率%'] = (stock_stats['盈利次数'] / stock_stats['次数'] * 100).round(1).astype(str) + '%'
        print(stock_stats[['次数', '平均收益%', '盈利概率%']].to_string())
        
        print("\n" + "=" * 70)
        print("💡 分析结论 (最近3年)")
        print("=" * 70)
        
        profit_rate = profitable/total*100
        avg_return = final_df['总收益%'].mean()
        
        if profit_rate >= 80:
            suggestion = "✅ 该策略在最近3年表现优秀"
        elif profit_rate >= 60:
            suggestion = "⚠️ 该策略盈利概率中等"
        else:
            suggestion = "❌ 该策略盈利概率较低"
        
        print(f"""
基于 {total} 次最近3年真实分红事件的分析：

1. 📈 盈利概率: {profit_rate:.2f}%
   {suggestion}

2. 💰 收益情况:
   - 平均收益率: {avg_return:.2f}%
   - 中位数收益率: {final_df['总收益%'].median():.2f}%
   - 收益率范围: {final_df['总收益%'].min():.2f}% ~ {final_df['总收益%'].max():.2f}%

3. 📋 详细记录:
""")
        print(final_df.to_string(index=False))
        
        print("\n" + "=" * 70)
        print("⚠️ 风险提示: 历史数据不代表未来表现，投资有风险！")
        print("=" * 70)
        
        # 保存结果
        os.makedirs('data', exist_ok=True)
        final_df.to_csv('data/dividend_analysis_3years.csv', index=False, encoding='utf-8-sig')
        print(f"\n💾 分析结果已保存到: data/dividend_analysis_3years.csv")
        
        return final_df
    else:
        print("\n❌ 未能获取到有效的分析数据")
        return None


if __name__ == '__main__':
    main()
