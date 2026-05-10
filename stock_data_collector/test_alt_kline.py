"""
使用替代方式获取K线数据进行分析
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
print("📊 股票分红策略分析")
print("=" * 70)

# 测试不同的数据获取方式
print("\n尝试多种方式获取K线数据...\n")

def try_sina_kline(stock_code):
    """尝试新浪K线接口"""
    try:
        print(f"尝试新浪接口: {stock_code}")
        df = ak.stock_zh_a_hist(
            symbol=stock_code,
            period="daily",
            start_date="20200101",
            end_date=datetime.now().strftime("%Y%m%d"),
            adjust="qfq"
        )
        return df
    except Exception as e:
        print(f"  新浪接口失败: {str(e)[:50]}")
        return None

def try_tencent_kline(stock_code):
    """尝试腾讯接口"""
    try:
        print(f"尝试腾讯接口: {stock_code}")
        df = ak.stock_zh_a_daily(
            symbol=f"sh{stock_code}",
            adjust="qfq"
        )
        return df
    except Exception as e:
        print(f"  腾讯接口失败: {str(e)[:50]}")
        return None

# 测试获取K线
test_stocks = ['600519', '000858', '600036']
kline_data = {}

for code in test_stocks:
    print(f"\n{'='*50}")
    print(f"测试股票: {code}")
    print('='*50)
    
    df = try_sina_kline(code)
    if df is not None and not df.empty:
        print(f"✅ 新浪接口成功! 获取 {len(df)} 条数据")
        kline_data[code] = df
        print(df.tail(3))
    else:
        df = try_tencent_kline(code)
        if df is not None and not df.empty:
            print(f"✅ 腾讯接口成功! 获取 {len(df)} 条数据")
            kline_data[code] = df
            print(df.tail(3))

if kline_data:
    print("\n" + "=" * 70)
    print("✅ 部分数据获取成功，可以继续分析")
    print("=" * 70)
else:
    print("\n" + "=" * 70)
    print("❌ 所有K线接口都无法访问")
    print("=" * 70)
