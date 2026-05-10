"""
获取最佳表现股票的分红时间表
并生成提前一个月买入建议
"""
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta

print("=" * 70)
print("📅 最佳表现股票分红时间表")
print("   提前一个月买入策略")
print("=" * 70)

best_stocks = [
    ('601919', '中远海控'),
    ('601088', '中国神华'),
    ('601166', '兴业银行'),
    ('601668', '中国建筑'),
    ('600036', '招商银行'),  # 补充一只
]

print("\n获取分红数据中...\n")

all_dividends = []

for code, name in best_stocks:
    try:
        df = ak.stock_history_dividend_detail(symbol=code, indicator="分红")
        if df is not None and not df.empty:
            df['股票代码'] = code
            df['股票名称'] = name
            all_dividends.append(df)
            print(f"✅ {name} ({code}): 获取到 {len(df)} 条分红记录")
    except Exception as e:
        print(f"❌ {name} ({code}): 获取失败")

if all_dividends:
    dividend_df = pd.concat(all_dividends, ignore_index=True)
    
    # 筛选关键列
    if '除权除息日' in dividend_df.columns:
        dividend_df['除权除息日'] = pd.to_datetime(dividend_df['除权除息日'], errors='coerce')
        dividend_df = dividend_df[dividend_df['除权除息日'].notna()]
        
        # 只保留最近5年的数据
        cutoff = datetime.now() - timedelta(days=365*5)
        dividend_df = dividend_df[dividend_df['除权除息日'] >= cutoff]
        
        print("\n" + "=" * 70)
        print("📅 历史分红时间表")
        print("=" * 70)
        
        for code, name in best_stocks:
            stock_df = dividend_df[dividend_df['股票代码'] == code].sort_values('除权除息日', ascending=False)
            
            print(f"\n🏭 {name} ({code})")
            print("-" * 50)
            
            if stock_df.empty:
                print("  暂无分红数据")
                continue
            
            for _, row in stock_df.head(5).iterrows():
                ex_date = row['除权除息日']
                buy_date = ex_date - timedelta(days=30)
                div_amount = row.get('派息', 'N/A')
                
                print(f"  📆 除权除息日: {ex_date.strftime('%Y-%m-%d')}")
                print(f"     💰 分红金额: {div_amount} 元/股")
                print(f"     🛒 建议买入日: {buy_date.strftime('%Y-%m-%d')} (提前30天)")
                print()
        
        # 生成未来预测（基于历史规律）
        print("\n" + "=" * 70)
        print("🔮 2026年分红预测（基于历史规律）")
        print("=" * 70)
        
        for code, name in best_stocks:
            stock_df = dividend_df[dividend_df['股票代码'] == code].sort_values('除权除息日', ascending=False)
            
            if stock_df.empty:
                continue
            
            # 计算平均分红月份
            months = stock_df['除权除息日'].dt.month.tolist()
            avg_month = sum(months) / len(months) if months else 6
            
            # 估算2026年分红日期
            predicted_month = int(round(avg_month))
            predicted_date = datetime(2026, predicted_month, 15)
            buy_date = predicted_date - timedelta(days=30)
            
            print(f"\n🏭 {name} ({code})")
            print("-" * 50)
            print(f"  📊 历史分红月份: {sorted(set(months))}")
            print(f"  📈 平均分红月份: {avg_month:.1f}月")
            print(f"  🔮 预测除权日: {predicted_date.strftime('%Y-%m-%d')}")
            print(f"  🛒 建议买入期: {buy_date.strftime('%Y-%m-%d')} 至 {predicted_date.strftime('%Y-%m-%d')}")
        
        # 生成日历视图
        print("\n" + "=" * 70)
        print("📆 2026年买入时间表日历")
        print("=" * 70)
        
        schedule = []
        for code, name in best_stocks:
            stock_df = dividend_df[dividend_df['股票代码'] == code].sort_values('除权除息日', ascending=False)
            
            if stock_df.empty:
                continue
            
            months = stock_df['除权除息日'].dt.month.tolist()
            avg_month = int(round(sum(months) / len(months))) if months else 6
            
            predicted_date = datetime(2026, avg_month, 15)
            buy_date = predicted_date - timedelta(days=30)
            
            schedule.append({
                '股票名称': name,
                '股票代码': code,
                '预测除权日': predicted_date.strftime('%Y-%m-%d'),
                '建议买入开始': buy_date.strftime('%Y-%m-%d'),
                '建议买入截止': (predicted_date - timedelta(days=7)).strftime('%Y-%m-%d'),
                '预测月份': f"{avg_month}月"
            })
        
        schedule_df = pd.DataFrame(schedule)
        print(schedule_df.to_string(index=False))
        
        print("\n" + "=" * 70)
        print("💡 投资建议")
        print("=" * 70)
        print("""
1. 📅 买入时机: 除权除息日前30天开始建仓
2. 💰 资金分配: 建议等权分配，每只股票20%
3. 🎯 止损策略: 如股价下跌超过15%考虑止损
4. 📊 持有期: 从买入日到除权除息日后5天
5. ⚠️ 风险提示: 预测仅为参考，实际分红时间可能调整
""")
        
        # 保存结果
        os.makedirs('data', exist_ok=True)
        schedule_df.to_csv('data/dividend_schedule_2026.csv', index=False, encoding='utf-8-sig')
        print("💾 时间表已保存到: data/dividend_schedule_2026.csv")
        
else:
    print("\n❌ 无法获取分红数据")
