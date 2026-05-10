"""
模拟分红策略分析演示
当无法获取真实数据时，使用模拟数据展示分析流程
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random


def generate_simulated_data():
    """生成模拟的分红策略分析数据"""
    np.random.seed(42)
    random.seed(42)
    
    stocks = {
        '600519': '贵州茅台',
        '000858': '五粮液', 
        '600036': '招商银行',
        '000651': '格力电器',
        '601318': '中国平安',
        '600887': '伊利股份',
        '000333': '美的集团',
        '002594': '比亚迪',
        '601288': '农业银行',
        '600028': '中国石化'
    }
    
    records = []
    
    for code, name in stocks.items():
        # 每只股票生成5-8条历史分红记录
        num_records = random.randint(5, 8)
        
        for i in range(num_records):
            # 随机生成分红日期（过去5年内）
            days_ago = random.randint(30, 1800)
            dividend_date = datetime.now() - timedelta(days=days_ago)
            
            # 随机生成买入价格
            price_before = round(random.uniform(10, 500), 2)
            
            # 随机生成分红金额
            dividend_per_share = round(random.uniform(0.5, 20), 4)
            
            # 生成除权除息日价格（有涨有跌）
            price_change_pct = random.uniform(-15, 20)
            price_at_dividend = round(price_before * (1 + price_change_pct/100), 2)
            
            # 计算收益
            price_change = price_at_dividend - price_before
            price_change_pct = (price_change / price_before) * 100
            dividend_yield = (dividend_per_share / price_before) * 100
            total_return = price_change_pct + dividend_yield
            
            records.append({
                'stock_code': code,
                'stock_name': name,
                'dividend_date': dividend_date.strftime('%Y-%m-%d'),
                'price_before': price_before,
                'price_at_dividend': price_at_dividend,
                'price_change': round(price_change, 2),
                'price_change_pct': round(price_change_pct, 2),
                'dividend_per_share': dividend_per_share,
                'dividend_yield': round(dividend_yield, 2),
                'total_return': round(total_return, 2),
                'is_profitable': 1 if total_return > 0 else 0,
                'holding_days': 30
            })
    
    return pd.DataFrame(records)


def analyze_results(df):
    """分析模拟结果"""
    print("\n" + "=" * 70)
    print("📊 模拟分红策略分析结果")
    print("=" * 70)
    
    # 基本统计
    total = len(df)
    profitable = df['is_profitable'].sum()
    loss = total - profitable
    
    print(f"\n【基本统计】")
    print(f"  总样本数: {total}")
    print(f"  盈利次数: {profitable} ({profitable/total*100:.1f}%)")
    print(f"  亏损次数: {loss} ({loss/total*100:.1f}%)")
    print(f"  盈利概率: {profitable/total*100:.2f}%")
    
    print(f"\n【收益率统计】")
    print(f"  平均收益率: {df['total_return'].mean():.2f}%")
    print(f"  中位数收益率: {df['total_return'].median():.2f}%")
    print(f"  最大收益率: {df['total_return'].max():.2f}%")
    print(f"  最小收益率: {df['total_return'].min():.2f}%")
    print(f"  收益率标准差: {df['total_return'].std():.2f}%")
    
    # 按股票统计
    print(f"\n【各股票表现】")
    stock_stats = df.groupby(['stock_code', 'stock_name']).agg({
        'total_return': ['mean', 'count'],
        'is_profitable': 'mean'
    }).round(2)
    stock_stats.columns = ['平均收益', '分红次数', '盈利概率']
    stock_stats = stock_stats.reset_index()
    stock_stats['盈利概率'] = (stock_stats['盈利概率'] * 100).round(1).astype(str) + '%'
    print(stock_stats.to_string(index=False))
    
    # 按股息率分组
    print(f"\n【按股息率分组统计】")
    df['yield_group'] = pd.cut(df['dividend_yield'], 
                                bins=[0, 2, 4, 6, 100],
                                labels=['<2%', '2-4%', '4-6%', '>6%'])
    yield_stats = df.groupby('yield_group').agg({
        'total_return': 'mean',
        'is_profitable': 'mean'
    }).round(2)
    yield_stats.columns = ['平均收益', '盈利概率']
    yield_stats['盈利概率'] = (yield_stats['盈利概率'] * 100).round(1).astype(str) + '%'
    print(yield_stats)
    
    return {
        'total': total,
        'profitable': profitable,
        'loss': loss,
        'profit_rate': profitable/total*100,
        'avg_return': df['total_return'].mean(),
        'median_return': df['total_return'].median()
    }


def print_conclusion(stats):
    """打印分析结论"""
    print("\n" + "=" * 70)
    print("💡 分析结论")
    print("=" * 70)
    
    profit_rate = stats['profit_rate']
    avg_return = stats['avg_return']
    
    print(f"""
基于对 {stats['total']} 次分红事件的模拟分析：

1. 📈 盈利概率: {profit_rate:.2f}%
   - {'盈利概率较高，策略表现良好' if profit_rate >= 50 else '盈利概率一般，需要谨慎'}

2. 💰 收益情况:
   - 平均收益率: {avg_return:.2f}%
   - 中位数收益率: {stats['median_return']:.2f}%
   - {'整体收益为正' if avg_return > 0 else '整体收益为负'}

3. 📊 关键发现:
   - 高股息率股票(>4%)的盈利概率通常更高
   - 价差收益与分红收益同样重要
   - 持有期内价格波动是主要风险

4. 🎯 投资建议:
   - 优先选择股息率 > 3% 的优质股票
   - 关注分红稳定的蓝筹股
   - 在除权除息日前30天分批建仓
   - 设定合理的止损点

5. ⚠️ 风险提示:
   - 历史数据不代表未来表现
   - 需要考虑交易成本(约0.2%)
   - 注意市场整体环境影响
   - 建议分散投资
""")
    
    print("=" * 70)
    print("📝 说明: 以上为模拟数据演示，真实分析需要联网获取实际数据")
    print("=" * 70)


def show_sample_data(df):
    """显示样例数据"""
    print("\n" + "=" * 70)
    print("📋 分红策略分析样例数据")
    print("=" * 70)
    print(df.head(15).to_string(index=False))


def print_usage_guide():
    """打印使用指南"""
    print("""
================================================================================
🎯 如何在本地运行真实分析
================================================================================

1. 环境准备:
   - 安装 Python 3.8+
   - 确保网络连接正常

2. 安装依赖:
   cd stock_data_collector
   pip install -r requirements.txt

3. 运行分析:
   python run_analysis.py

4. 查看结果:
   - 终端输出统计结果
   - data/ 目录查看CSV数据
   - output/ 目录查看图表

5. 自定义分析:
   - 修改 stock_codes 列表分析其他股票
   - 修改 lookback_days 调整持有期
   - 使用 --codes 参数指定股票

================================================================================
""")


if __name__ == '__main__':
    print("=" * 70)
    print("🎯 股票分红策略分析 - 模拟演示")
    print("=" * 70)
    print("\n📌 说明: 由于当前环境网络限制，使用模拟数据演示分析流程")
    print("📌 真实分析需要在本地电脑运行\n")
    
    # 生成模拟数据
    df = generate_simulated_data()
    
    # 分析结果
    stats = analyze_results(df)
    
    # 显示样例数据
    show_sample_data(df)
    
    # 打印结论
    print_conclusion(stats)
    
    # 使用指南
    print_usage_guide()
