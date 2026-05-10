"""
全市场股票分红策略分析 - 使用预设蓝筹股列表
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

print("=" * 70)
print("🎯 全市场股票分红策略分析")
print("   分析A股 + 港股通 主要股票")
print("=" * 70)


class FullMarketDividendAnalyzer:
    """全市场分红策略分析器"""
    
    def __init__(self, lookback_days=30, years_limit=3):
        self.lookback_days = lookback_days
        self.years_limit = years_limit
        self.cutoff_date = datetime.now() - timedelta(days=years_limit * 365)
        self.stats = {'total': 0, 'success': 0, 'failed': 0}
    
    def get_stock_list(self):
        """获取股票列表（使用预设列表+动态获取）"""
        stocks = []
        
        # 预设蓝筹股列表（主要的大盘股）
        blue_chips = [
            ('600519', '贵州茅台', 'A股'),
            ('600036', '招商银行', 'A股'),
            ('601318', '中国平安', 'A股'),
            ('000858', '五粮液', 'A股'),
            ('600887', '伊利股份', 'A股'),
            ('000651', '格力电器', 'A股'),
            ('000333', '美的集团', 'A股'),
            ('002594', '比亚迪', 'A股'),
            ('601288', '农业银行', 'A股'),
            ('600028', '中国石化', 'A股'),
            ('601398', '工商银行', 'A股'),
            ('601939', '建设银行', 'A股'),
            ('600000', '浦发银行', 'A股'),
            ('601166', '兴业银行', 'A股'),
            ('600016', '民生银行', 'A股'),
            ('601328', '交通银行', 'A股'),
            ('600030', '中信证券', 'A股'),
            ('601688', '华泰证券', 'A股'),
            ('600009', '上海机场', 'A股'),
            ('600104', '上汽集团', 'A股'),
            ('600900', '长江电力', 'A股'),
            ('601888', '中国中免', 'A股'),
            ('600585', '海螺水泥', 'A股'),
            ('601012', '隆基绿能', 'A股'),
            ('600690', '海尔智家', 'A股'),
            ('601669', '中国电建', 'A股'),
            ('600606', '绿地控股', 'A股'),
            ('601186', '中国铁建', 'A股'),
            ('601668', '中国建筑', 'A股'),
            ('601628', '中国人寿', 'A股'),
            ('601088', '中国神华', 'A股'),
            ('601857', '中国石油', 'A股'),
            ('600050', '中国联通', 'A股'),
            ('601800', '中国交建', 'A股'),
            ('601898', '中煤能源', 'A股'),
            ('600028', '中国石化', 'A股'),
            ('601390', '中国中铁', 'A股'),
            ('601766', '中国中车', 'A股'),
            ('601989', '中国重工', 'A股'),
            ('600019', '宝钢股份', 'A股'),
            ('600023', '浙能电力', 'A股'),
            ('600795', '国电电力', 'A股'),
            ('600900', '长江电力', 'A股'),
            ('601225', '陕西煤业', 'A股'),
            ('600971', '恒源煤电', 'A股'),
            ('601666', '平煤股份', 'A股'),
            ('600508', '上海能源', 'A股'),
            ('000895', '双汇发展', 'A股'),
            ('000568', '泸州老窖', 'A股'),
            ('000596', '古井贡酒', 'A股'),
            ('000876', '新希望', 'A股'),
            ('000002', '万科A', 'A股'),
            ('000001', '平安银行', 'A股'),
            ('000063', '中兴通讯', 'A股'),
            ('000066', '中国长城', 'A股'),
            ('000100', 'TCL科技', 'A股'),
            ('000338', '潍柴动力', 'A股'),
            ('000157', '中联重科', 'A股'),
            ('000425', '徐工机械', 'A股'),
            ('000528', '柳工', 'A股'),
            ('000651', '格力电器', 'A股'),
            ('000725', '京东方A', 'A股'),
            ('000768', '中航西飞', 'A股'),
            ('000898', '鞍钢股份', 'A股'),
            ('000938', '紫光股份', 'A股'),
            ('002001', '新和成', 'A股'),
            ('002027', '分众传媒', 'A股'),
            ('002044', '美年健康', 'A股'),
            ('002050', '三花智控', 'A股'),
            ('002230', '科大讯飞', 'A股'),
            ('002236', '大华股份', 'A股'),
            ('002252', '上海莱士', 'A股'),
            ('002304', '洋河股份', 'A股'),
            ('002311', '海大集团', 'A股'),
            ('002352', '顺丰控股', 'A股'),
            ('002371', '北方华创', 'A股'),
            ('002415', '海康威视', 'A股'),
            ('002460', '赣锋锂业', 'A股'),
            ('002475', '立讯精密', 'A股'),
            ('002493', '荣盛石化', 'A股'),
            ('002594', '比亚迪', 'A股'),
            ('002601', '龙佰集团', 'A股'),
            ('002607', '亚玛顿', 'A股'),
            ('002714', '牧原股份', 'A股'),
            ('002736', '国信证券', 'A股'),
            ('002841', '视源股份', 'A股'),
            ('002916', '中芯国际', 'A股'),
            ('300001', '特锐德', 'A股'),
            ('300015', '爱尔眼科', 'A股'),
            ('300033', '同花顺', 'A股'),
            ('300059', '东方财富', 'A股'),
            ('300122', '智飞生物', 'A股'),
            ('300124', '汇川技术', 'A股'),
            ('300142', '沃森生物', 'A股'),
            ('300274', '阳光电源', 'A股'),
            ('300347', '泰格医药', 'A股'),
            ('300408', '三环集团', 'A股'),
            ('300498', '温氏股份', 'A股'),
            ('300529', '健帆生物', 'A股'),
            ('300595', '欧普康视', 'A股'),
            ('300601', '康泰生物', 'A股'),
            ('300750', '宁德时代', 'A股'),
            ('300896', '爱美客', 'A股'),
            ('600004', '白云机场', 'A股'),
            ('600009', '上海机场', 'A股'),
            ('600011', '华能国际', 'A股'),
            ('600019', '宝钢股份', 'A股'),
            ('600031', '三一重工', 'A股'),
            ('600036', '招商银行', 'A股'),
            ('600048', '保利发展', 'A股'),
            ('600050', '中国联通', 'A股'),
            ('600089', '特变电工', 'A股'),
            ('600104', '上汽集团', 'A股'),
        ]
        
        stocks.extend(blue_chips)
        
        # 尝试获取更多股票
        try:
            print("尝试获取更多A股...")
            df = ak.stock_info_a_code_name()
            if df is not None and not df.empty:
                for _, row in df.iterrows():
                    code = str(row['code']).zfill(6)
                    name = row['name']
                    if (code, name, 'A股') not in stocks:
                        stocks.append((code, name, 'A股'))
                print(f"  总共获取 {len(stocks)} 只股票")
        except Exception as e:
            print(f"  获取更多股票失败: {e}")
        
        # 尝试获取港股通股票
        try:
            print("\n获取港股通股票...")
            df_hk = ak.stock_hk_spot_em()
            if df_hk is not None and not df_hk.empty:
                for _, row in df_hk.head(50).iterrows():
                    code = str(row['代码']).strip()
                    name = str(row['名称']).strip() if '名称' in row else code
                    stocks.append((code, name, '港股'))
                print(f"  获取 {min(50, len(df_hk))} 只港股")
        except Exception as e:
            print(f"  获取港股失败: {e}")
        
        print(f"\n📊 总共 {len(stocks)} 只股票待分析")
        return stocks
    
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
                df = ak.stock_zh_a_daily(symbol=f"sh{code}", adjust="qfq")
                if df is not None and not df.empty:
                    df['date'] = pd.to_datetime(df['date'])
                    return df
            return None
        except:
            return None
    
    def analyze_single_stock(self, code, name, market='a'):
        """分析单只股票"""
        try:
            self.stats['total'] += 1
            
            # 获取分红数据
            dividend_df = self.get_dividend(code, market)
            if dividend_df is None or dividend_df.empty:
                self.stats['failed'] += 1
                return None
            
            # 筛选列
            if market == 'a':
                date_col = '除权除息日'
                div_col = '派息'
            else:
                if '除净日' not in dividend_df.columns:
                    self.stats['failed'] += 1
                    return None
                date_col = '除净日'
                div_col = '每股派息(港元)'
            
            if date_col not in dividend_df.columns:
                self.stats['failed'] += 1
                return None
            
            dividend_df[date_col] = pd.to_datetime(dividend_df[date_col], errors='coerce')
            dividend_df = dividend_df.dropna(subset=[date_col])
            dividend_df = dividend_df[dividend_df[date_col] >= self.cutoff_date]
            
            if dividend_df.empty:
                self.stats['failed'] += 1
                return None
            
            # 获取K线数据
            kline_df = self.get_kline(code, market)
            if kline_df is None or kline_df.empty:
                self.stats['failed'] += 1
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
                    'stock_name': name,
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
            
            if results:
                self.stats['success'] += 1
            
            return results if results else None
            
        except Exception as e:
            self.stats['failed'] += 1
            return None
    
    def analyze_all(self, stocks):
        """分析所有股票"""
        print(f"\n🚀 开始批量分析 {len(stocks)} 只股票...")
        print(f"   持有期: 除权除息日前{self.lookback_days}天")
        print(f"   分析周期: 最近{self.years_limit}年")
        
        all_results = []
        
        for i, (code, name, market) in enumerate(stocks):
            if (i + 1) % 10 == 0:
                print(f"   进度: {i+1}/{len(stocks)} (成功: {self.stats['success']}, 失败: {self.stats['failed']})")
            
            results = self.analyze_single_stock(code, name, market)
            if results:
                all_results.extend(results)
            
            time.sleep(0.3)  # 避免请求过快
        
        print(f"\n✅ 分析完成！")
        print(f"   总股票数: {self.stats['total']}")
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
        if 'market' in df.columns and df['market'].nunique() > 1:
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
        best_stocks = df.groupby(['stock_code', 'stock_name']).agg({
            'total_return_pct': ['mean', 'count'],
            'is_profitable': 'mean'
        })
        best_stocks.columns = ['平均收益', '分红次数', '盈利概率']
        best_stocks = best_stocks[best_stocks['分红次数'] >= 2]
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

3. 🎯 投资建议:
   - 选择分红稳定的优质股票
   - 关注股息率 > 3% 的标的
   - 在除权除息日前30天分批建仓
   - 设定合理的止损点

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
    stocks = analyzer.get_stock_list()
    
    if not stocks:
        print("\n❌ 无法获取股票列表")
        return
    
    # 批量分析
    df = analyzer.analyze_all(stocks)
    
    if not df.empty:
        # 保存结果
        os.makedirs('data', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'data/full_market_analysis_{timestamp}.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n💾 分析结果已保存到: {filename}")
        
        # 生成报告
        analyzer.generate_report(df)
    else:
        print("\n❌ 没有获取到有效的分析数据")


if __name__ == '__main__':
    main()
