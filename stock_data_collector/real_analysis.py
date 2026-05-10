"""
使用腾讯接口获取K线数据进行真实分红策略分析
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

print("=" * 70)
print("🎯 股票分红策略分析 - 真实数据分析")
print("=" * 70)


class RealDividendStrategyAnalyzer:
    """使用真实数据的分红策略分析器"""
    
    def __init__(self, lookback_days=30):
        self.lookback_days = lookback_days
    
    def get_dividend(self, code):
        """获取分红数据"""
        try:
            return ak.stock_history_dividend_detail(symbol=code, indicator="分红")
        except:
            return None
    
    def get_kline(self, code):
        """使用腾讯接口获取K线数据"""
        try:
            # 尝试腾讯接口
            df = ak.stock_zh_a_daily(symbol=f"sh{code}", adjust="qfq")
            if df is not None and not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                return df
        except:
            pass
        
        try:
            # 尝试东方财富接口
            df = ak.stock_zh_a_hist(
                symbol=code,
                period="daily",
                start_date="20200101",
                end_date=datetime.now().strftime("%Y%m%d"),
                adjust="qfq"
            )
            if df is not None and not df.empty:
                df['date'] = pd.to_datetime(df['日期'])
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
        
        # 获取K线数据
        kline_df = self.get_kline(code)
        if kline_df is None or kline_df.empty:
            print(f"  ❌ 无法获取K线数据")
            return None
        
        print(f"  ✅ 获取到 {len(dividend_df)} 条分红记录")
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
            ex_mask = kline_df['date'] == ex_date
            if ex_mask.sum() == 0:
                # 找最接近的日期
                close_mask = kline_df['date'] <= ex_date
                if close_mask.sum() == 0:
                    continue
                ex_price = kline_df[close_mask].iloc[-1]['close']
            else:
                ex_price = kline_df[ex_mask].iloc[0]['close']
            
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
    ]
    
    analyzer = RealDividendStrategyAnalyzer(lookback_days=30)
    all_results = []
    
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
        print("📊 汇总统计")
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
        
        print("\n" + "=" * 70)
        print("💡 分析结论")
        print("=" * 70)
        
        profit_rate = profitable/total*100
        avg_return = final_df['总收益%'].mean()
        
        if profit_rate >= 60:
            suggestion = "✅ 该策略盈利概率较高，可以考虑使用"
        elif profit_rate >= 50:
            suggestion = "⚠️ 该策略盈利概率中等，建议谨慎使用"
        else:
            suggestion = "❌ 该策略盈利概率较低，需要谨慎"
        
        print(f"""
基于 {total} 次真实分红事件的分析：

1. 📈 盈利概率: {profit_rate:.2f}%
   {suggestion}

2. 💰 收益情况:
   - 平均收益率: {avg_return:.2f}%
   - 中位数收益率: {final_df['总收益%'].median():.2f}%
   - 收益率范围: {final_df['总收益%'].min():.2f}% ~ {final_df['总收益%'].max():.2f}%

3. 🎯 建议:
   - 优先选择分红稳定的蓝筹股
   - 关注股息率较高的股票
   - 注意市场整体环境影响
   - 考虑交易成本(约0.2%)
""")
        
        print("=" * 70)
        print("⚠️ 风险提示: 历史数据不代表未来表现，投资有风险！")
        print("=" * 70)
        
        # 保存结果
        os.makedirs('data', exist_ok=True)
        final_df.to_csv('data/dividend_analysis_real.csv', index=False, encoding='utf-8-sig')
        print(f"\n💾 分析结果已保存到: data/dividend_analysis_real.csv")
        
        return final_df
    else:
        print("\n❌ 未能获取到有效的分析数据")
        return None


if __name__ == '__main__':
    main()
