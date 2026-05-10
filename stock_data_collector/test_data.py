"""
网络测试和简单数据分析
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("🔍 网络和数据分析测试")
print("=" * 70)

# 测试1: 检查 akshare 版本
print("\n1️⃣ 检查 akshare 安装...")
try:
    import akshare as ak
    print(f"   akshare 版本: {ak.__version__}")
except Exception as e:
    print(f"   ❌ akshare 未安装: {e}")
    sys.exit(1)

# 测试2: 尝试获取一只股票的分红数据
print("\n2️⃣ 测试获取贵州茅台(600519)分红数据...")
try:
    dividend_df = ak.stock_history_dividend_detail(symbol="600519", indicator="分红")
    if dividend_df is not None and not dividend_df.empty:
        print(f"   ✅ 成功获取 {len(dividend_df)} 条分红记录")
        print("\n   最近几次分红记录:")
        print(dividend_df.head(5).to_string())
    else:
        print("   ⚠️ 分红数据为空")
except Exception as e:
    print(f"   ❌ 获取失败: {e}")

# 测试3: 尝试获取实时行情
print("\n3️⃣ 测试获取A股实时行情...")
try:
    spot_df = ak.stock_zh_a_spot_em()
    if spot_df is not None and not spot_df.empty:
        print(f"   ✅ 成功获取 {len(spot_df)} 条行情数据")
        # 显示茅台的行情
        maotai = spot_df[spot_df['代码'] == '600519']
        if not maotai.empty:
            print("\n   贵州茅台当前行情:")
            print(f"   最新价: {maotai['最新价'].values[0]}")
            print(f"   涨跌幅: {maotai['涨跌幅'].values[0]}%")
    else:
        print("   ⚠️ 行情数据为空")
except Exception as e:
    print(f"   ❌ 获取失败: {e}")

# 测试4: 尝试获取历史K线
print("\n4️⃣ 测试获取历史K线数据...")
try:
    from datetime import datetime, timedelta
    end_date = datetime.now().strftime("%Y%m%d")
    start_date = (datetime.now() - timedelta(days=365)).strftime("%Y%m%d")
    
    hist_df = ak.stock_zh_a_hist(
        symbol="600519",
        period="daily",
        start_date=start_date,
        end_date=end_date,
        adjust=""
    )
    if hist_df is not None and not hist_df.empty:
        print(f"   ✅ 成功获取 {len(hist_df)} 条K线数据")
        print("\n   最近5个交易日:")
        print(hist_df.tail(5)[['日期', '开盘', '收盘', '涨跌幅']].to_string())
    else:
        print("   ⚠️ K线数据为空")
except Exception as e:
    print(f"   ❌ 获取失败: {e}")

print("\n" + "=" * 70)
print("测试完成")
print("=" * 70)
