"""
分红策略分析演示脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import warnings
warnings.filterwarnings('ignore')

from analysis.dividend_strategy import DividendStrategyAnalyzer
from analysis.visualizer import DividendVisualizer
from core.data_storage import DataStorage


def main():
    print("=" * 70)
    print("🎯 股票分红策略分析 - 除权除息日前30天买入盈利概率研究")
    print("=" * 70)
    
    # 分析的股票列表（优质高股息股票）
    stock_codes = [
        '600519',  # 贵州茅台
        '000858',  # 五粮液
        '600036',  # 招商银行
        '000651',  # 格力电器
        '601318',  # 中国平安
        '600887',  # 伊利股份
        '000333',  # 美的集团
        '002594',  # 比亚迪
        '601288',  # 农业银行
        '600028',  # 中国石化
    ]
    
    print(f"\n📊 分析股票: {', '.join(stock_codes)}")
    print(f"📅 持有期: 除权除息日前30天买入，持有到除权除息日")
    
    # 创建分析器
    analyzer = DividendStrategyAnalyzer(lookback_days=30)
    
    # 运行完整分析
    result_df, analysis_results = analyzer.run_full_analysis(stock_codes, market='a')
    
    if result_df is None or result_df.empty:
        print("\n❌ 分析失败，没有获取到数据")
        print("   可能原因：网络问题或数据源不可用")
        return
    
    # 保存结果
    storage = DataStorage()
    storage.save_dividend_strategy_result(result_df)
    print(f"\n💾 分析结果已保存到: data/dividend_strategy_results.csv")
    
    # 生成可视化
    print("\n📈 正在生成可视化图表...")
    visualizer = DividendVisualizer()
    saved_files = visualizer.generate_full_report(result_df)
    print(f"   已生成 {len(saved_files)} 个图表文件")
    
    # 打印详细结果
    print("\n" + "=" * 70)
    print("📋 详细分析记录")
    print("=" * 70)
    print(result_df.to_string(index=False))
    
    # 找出最佳表现股票
    print("\n" + "=" * 70)
    print("🏆 表现最佳的股票 (按平均收益率排名)")
    print("=" * 70)
    best_stocks = analyzer.find_best_stocks(result_df, top_n=5)
    if not best_stocks.empty:
        print(best_stocks.to_string(index=False))
    
    print("\n" + "=" * 70)
    print("💡 分析结论")
    print("=" * 70)
    
    stats = analysis_results.get('statistics', {})
    if stats:
        profitable_rate = float(stats.get('盈利概率', '0%').rstrip('%'))
        avg_return = float(stats.get('平均收益率', '0%').rstrip('%'))
        
        print(f"""
基于对 {len(result_df)} 次分红事件的分析：

1. 📈 盈利概率: {stats.get('盈利概率')}
   - 盈利次数: {stats.get('盈利次数')}
   - 亏损次数: {stats.get('亏损次数')}

2. 💰 收益情况:
   - 平均收益率: {stats.get('平均收益率')}
   - 中位数收益率: {stats.get('中位数收益率')}
   - 收益率范围: {stats.get('最小收益率')} ~ {stats.get('最大收益率')}
   - 波动性(标准差): {stats.get('收益率标准差')}

3. 📊 策略评估:
""")
        if profitable_rate >= 60:
            print("   ✅ 该策略整体具有较高的盈利概率，可以考虑使用")
            print("   ✅ 建议关注高股息率股票，进一步提高盈利概率")
        elif profitable_rate >= 50:
            print("   ⚠️ 该策略盈利概率中等，建议谨慎使用")
            print("   ⚠️ 建议结合其他指标综合判断")
        else:
            print("   ❌ 该策略盈利概率较低，需要谨慎使用")
            print("   ❌ 建议考虑其他投资策略")
        
        print(f"""
4. 🎯 投资建议:
   - 优先选择股息率 > 3% 的股票
   - 关注分红稳定的蓝筹股
   - 注意市场整体环境的影响
   - 考虑交易成本（约0.1-0.3%）
""")
    
    print("=" * 70)
    print("⚠️  风险提示: 历史数据不代表未来表现，投资有风险，入市需谨慎！")
    print("=" * 70)


if __name__ == '__main__':
    main()
