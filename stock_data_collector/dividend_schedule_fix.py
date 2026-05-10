"""
最佳表现股票分红时间表
"""
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import os

print("=" * 70)
print("📅 最佳表现股票分红时间表")
print("   提前一个月买入策略")
print("=" * 70)

best_stocks = [
    ('601919', '中远海控'),
    ('601088', '中国神华'),
    ('601166', '兴业银行'),
    ('601668', '中国建筑'),
    ('600036', '招商银行'),
]

all_dividends = []
for code, name in best_stocks:
    try:
        df = ak.stock_history_dividend_detail(symbol=code, indicator="分红")
        if df is not None and not df.empty:
            df['股票代码'] = code
            df['股票名称'] = name
            all_dividends.append(df)
    except:
        pass

if all_dividends:
    dividend_df = pd.concat(all_dividends, ignore_index=True)
    
    if '除权除息日' in dividend_df.columns:
        dividend_df['除权除息日'] = pd.to_datetime(dividend_df['除权除息日'], errors='coerce')
        dividend_df = dividend_df[dividend_df['除权除息日'].notna()]
        cutoff = datetime.now() - timedelta(days=365*5)
        dividend_df = dividend_df[dividend_df['除权除息日'] >= cutoff]
        
        schedule = []
        for code, name in best_stocks:
            stock_df = dividend_df[dividend_df['股票代码'] == code].sort_values('除权除息日', ascending=False)
            
            if stock_df.empty:
                continue
            
            months = stock_df['除权除息日'].dt.month.tolist()
            avg_month = int(round(sum(months) / len(months))) if months else 6
            
            predicted_date = datetime(2026, avg_month, 15)
            buy_start = predicted_date - timedelta(days=30)
            buy_end = predicted_date - timedelta(days=7)
            
            schedule.append({
                '股票名称': name,
                '股票代码': code,
                '预测除权日': predicted_date.strftime('%Y-%m-%d'),
                '建议买入开始': buy_start.strftime('%Y-%m-%d'),
                '建议买入截止': buy_end.strftime('%Y-%m-%d'),
                '预测月份': f"{avg_month}月"
            })
        
        schedule_df = pd.DataFrame(schedule)
        
        os.makedirs('data', exist_ok=True)
        schedule_df.to_csv('data/dividend_schedule_2026.csv', index=False, encoding='utf-8-sig')
        print("\n✅ 时间表已保存")
