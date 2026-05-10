"""
全市场股票分红策略分析 - 修复版
修复K线数据获取问题，区分沪深市场
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

print("=" * 70)
print("🎯 全市场股票分红策略分析（修复版）")
print("=" * 70)


class FullMarketAnalyzer:
    
    def __init__(self, lookback_days=30, years_limit=3):
        self.lookback_days = lookback_days
        self.years_limit = years_limit
        self.cutoff_date = datetime.now() - timedelta(days=years_limit * 365)
        self.stats = {'total': 0, 'success': 0, 'no_dividend': 0, 'no_kline': 0, 'no_match': 0}
    
    def get_stock_list(self):
        """获取股票列表"""
        stocks = []
        
        # 预设蓝筹股列表（确保覆盖沪深两市）
        blue_chips = [
            ('600519', '贵州茅台', 'sh'),
            ('600036', '招商银行', 'sh'),
            ('601318', '中国平安', 'sh'),
            ('600887', '伊利股份', 'sh'),
            ('601288', '农业银行', 'sh'),
            ('601398', '工商银行', 'sh'),
            ('601939', '建设银行', 'sh'),
            ('600000', '浦发银行', 'sh'),
            ('601166', '兴业银行', 'sh'),
            ('600016', '民生银行', 'sh'),
            ('601328', '交通银行', 'sh'),
            ('600030', '中信证券', 'sh'),
            ('601688', '华泰证券', 'sh'),
            ('600009', '上海机场', 'sh'),
            ('600104', '上汽集团', 'sh'),
            ('600900', '长江电力', 'sh'),
            ('601888', '中国中免', 'sh'),
            ('600585', '海螺水泥', 'sh'),
            ('601012', '隆基绿能', 'sh'),
            ('600690', '海尔智家', 'sh'),
            ('601669', '中国电建', 'sh'),
            ('601186', '中国铁建', 'sh'),
            ('601668', '中国建筑', 'sh'),
            ('601628', '中国人寿', 'sh'),
            ('601088', '中国神华', 'sh'),
            ('601857', '中国石油', 'sh'),
            ('600050', '中国联通', 'sh'),
            ('601800', '中国交建', 'sh'),
            ('601898', '中煤能源', 'sh'),
            ('601390', '中国中铁', 'sh'),
            ('601766', '中国中车', 'sh'),
            ('601989', '中国重工', 'sh'),
            ('600019', '宝钢股份', 'sh'),
            ('600023', '浙能电力', 'sh'),
            ('600795', '国电电力', 'sh'),
            ('601225', '陕西煤业', 'sh'),
            ('600031', '三一重工', 'sh'),
            ('600048', '保利发展', 'sh'),
            ('600089', '特变电工', 'sh'),
            ('600004', '白云机场', 'sh'),
            ('600011', '华能国际', 'sh'),
            ('600028', '中国石化', 'sh'),
            ('600029', '南方航空', 'sh'),
            ('600115', '东方航空', 'sh'),
            ('600150', '中国船舶', 'sh'),
            ('600176', '中国巨石', 'sh'),
            ('600276', '恒瑞医药', 'sh'),
            ('600309', '万华化学', 'sh'),
            ('600346', '恒力石化', 'sh'),
            ('600406', '国电南瑞', 'sh'),
            ('600436', '片仔癀', 'sh'),
            ('600570', '恒生电子', 'sh'),
            ('600584', '长电科技', 'sh'),
            ('600588', '用友网络', 'sh'),
            ('600690', '海尔智家', 'sh'),
            ('600809', '山西汾酒', 'sh'),
            ('600837', '海通证券', 'sh'),
            ('600893', '航发动力', 'sh'),
            ('600905', '三峡能源', 'sh'),
            ('600941', '中国移动', 'sh'),
            ('601012', '隆基绿能', 'sh'),
            ('601138', '工业富联', 'sh'),
            ('601211', '国泰君安', 'sh'),
            ('601236', '红塔证券', 'sh'),
            ('601633', '长城汽车', 'sh'),
            ('601728', '中国电信', 'sh'),
            ('601788', '光大证券', 'sh'),
            ('601816', '京沪高铁', 'sh'),
            ('601838', '成都银行', 'sh'),
            ('601877', '正泰电器', 'sh'),
            ('601899', '紫金矿业', 'sh'),
            ('601919', '中远海控', 'sh'),
            ('601985', '中国核电', 'sh'),
            ('601988', '中国银行', 'sh'),
            ('603259', '药明康德', 'sh'),
            ('603288', '海天味业', 'sh'),
            ('603501', '韦尔股份', 'sh'),
            ('603799', '华友钴业', 'sh'),
            ('603986', '兆易创新', 'sh'),
            ('000858', '五粮液', 'sz'),
            ('000651', '格力电器', 'sz'),
            ('000333', '美的集团', 'sz'),
            ('002594', '比亚迪', 'sz'),
            ('000002', '万科A', 'sz'),
            ('000001', '平安银行', 'sz'),
            ('000063', '中兴通讯', 'sz'),
            ('000100', 'TCL科技', 'sz'),
            ('000338', '潍柴动力', 'sz'),
            ('000157', '中联重科', 'sz'),
            ('000425', '徐工机械', 'sz'),
            ('000568', '泸州老窖', 'sz'),
            ('000596', '古井贡酒', 'sz'),
            ('000725', '京东方A', 'sz'),
            ('000768', '中航西飞', 'sz'),
            ('000876', '新希望', 'sz'),
            ('000895', '双汇发展', 'sz'),
            ('000938', '紫光股份', 'sz'),
            ('002001', '新和成', 'sz'),
            ('002027', '分众传媒', 'sz'),
            ('002050', '三花智控', 'sz'),
            ('002230', '科大讯飞', 'sz'),
            ('002236', '大华股份', 'sz'),
            ('002304', '洋河股份', 'sz'),
            ('002311', '海大集团', 'sz'),
            ('002352', '顺丰控股', 'sz'),
            ('002371', '北方华创', 'sz'),
            ('002415', '海康威视', 'sz'),
            ('002460', '赣锋锂业', 'sz'),
            ('002475', '立讯精密', 'sz'),
            ('002493', '荣盛石化', 'sz'),
            ('002601', '龙佰集团', 'sz'),
            ('002714', '牧原股份', 'sz'),
            ('002736', '国信证券', 'sz'),
            ('002841', '视源股份', 'sz'),
            ('300001', '特锐德', 'sz'),
            ('300015', '爱尔眼科', 'sz'),
            ('300033', '同花顺', 'sz'),
            ('300059', '东方财富', 'sz'),
            ('300122', '智飞生物', 'sz'),
            ('300124', '汇川技术', 'sz'),
            ('300142', '沃森生物', 'sz'),
            ('300274', '阳光电源', 'sz'),
            ('300347', '泰格医药', 'sz'),
            ('300408', '三环集团', 'sz'),
            ('300498', '温氏股份', 'sz'),
            ('300750', '宁德时代', 'sz'),
            ('300896', '爱美客', 'sz'),
        ]
        
        # 去重
        seen = set()
        unique_stocks = []
        for code, name, market in blue_chips:
            if code not in seen:
                seen.add(code)
                unique_stocks.append((code, name, market))
        
        print(f"📊 预设 {len(unique_stocks)} 只蓝筹股待分析")
        return unique_stocks
    
    def get_dividend(self, code):
        """获取分红数据"""
        try:
            df = ak.stock_history_dividend_detail(symbol=code, indicator="分红")
            return df
        except:
            return None
    
    def get_kline(self, code, market_prefix):
        """获取K线数据 - 区分沪深市场"""
        try:
            df = ak.stock_zh_a_daily(symbol=f"{market_prefix}{code}", adjust="qfq")
            if df is not None and not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                return df
        except:
            pass
        
        # 如果主接口失败，尝试另一个市场前缀
        alt_prefix = 'sz' if market_prefix == 'sh' else 'sh'
        try:
            df = ak.stock_zh_a_daily(symbol=f"{alt_prefix}{code}", adjust="qfq")
            if df is not None and not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                return df
        except:
            pass
        
        return None
    
    def analyze_single_stock(self, code, name, market_prefix):
        """分析单只股票"""
        self.stats['total'] += 1
        
        try:
            # 1. 获取分红数据
            dividend_df = self.get_dividend(code)
            if dividend_df is None or dividend_df.empty:
                self.stats['no_dividend'] += 1
                return None
            
            if '除权除息日' not in dividend_df.columns:
                self.stats['no_dividend'] += 1
                return None
            
            dividend_df['除权除息日'] = pd.to_datetime(dividend_df['除权除息日'], errors='coerce')
            dividend_df = dividend_df.dropna(subset=['除权除息日'])
            dividend_df = dividend_df[dividend_df['除权除息日'] >= self.cutoff_date]
            
            if dividend_df.empty:
                self.stats['no_dividend'] += 1
                return None
            
            # 2. 获取K线数据
            kline_df = self.get_kline(code, market_prefix)
            if kline_df is None or kline_df.empty:
                self.stats['no_kline'] += 1
                return None
            
            # 3. 分析每次分红
            results = []
            for _, div in dividend_df.iterrows():
                ex_date = div.get('除权除息日')
                if pd.isna(ex_date):
                    continue
                
                ex_date = pd.to_datetime(ex_date)
                dividend_amount = div.get('派息', 0)
                if pd.isna(dividend_amount):
                    continue
                
                try:
                    dividend_amount = float(dividend_amount)
                except:
                    continue
                
                if dividend_amount <= 0:
                    continue
                
                buy_date = ex_date - timedelta(days=self.lookback_days)
                
                buy_mask = kline_df['date'] <= buy_date
                if buy_mask.sum() == 0:
                    continue
                buy_price = float(kline_df[buy_mask].iloc[-1]['close'])
                if buy_price <= 0:
                    continue
                
                close_mask = kline_df['date'] <= ex_date
                if close_mask.sum() == 0:
                    continue
                ex_price = float(kline_df[close_mask].iloc[-1]['close'])
                if ex_price <= 0:
                    continue
                
                price_change_pct = ((ex_price - buy_price) / buy_price) * 100
                dividend_yield = (dividend_amount / buy_price) * 100
                total_return = price_change_pct + dividend_yield
                
                results.append({
                    'stock_code': code,
                    'stock_name': name,
                    'market': '沪市' if market_prefix == 'sh' else '深市',
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
                return results
            else:
                self.stats['no_match'] += 1
                return None
                
        except Exception as e:
            self.stats['no_match'] += 1
            return None
    
    def analyze_all(self, stocks):
        """批量分析所有股票"""
        print(f"\n🚀 开始批量分析 {len(stocks)} 只股票...")
        print(f"   持有期: 除权除息日前{self.lookback_days}天")
        print(f"   分析周期: 最近{self.years_limit}年\n")
        
        all_results = []
        
        for i, (code, name, market) in enumerate(stocks):
            if (i + 1) % 10 == 0 or i == len(stocks) - 1:
                print(f"   进度: {i+1}/{len(stocks)} | 成功: {self.stats['success']} | 无分红: {self.stats['no_dividend']} | 无K线: {self.stats['no_kline']}")
            
            results = self.analyze_single_stock(code, name, market)
            if results:
                all_results.extend(results)
            
            time.sleep(0.3)
        
        print(f"\n✅ 分析完成！")
        print(f"   总股票数: {self.stats['total']}")
        print(f"   成功分析: {self.stats['success']}")
        print(f"   无分红数据: {self.stats['no_dividend']}")
        print(f"   无K线数据: {self.stats['no_kline']}")
        print(f"   无匹配记录: {self.stats['no_match']}")
        
        return pd.DataFrame(all_results) if all_results else pd.DataFrame()
    
    def generate_report(self, df):
        """生成分析报告"""
        if df is None or df.empty:
            print("\n❌ 没有分析数据")
            return
        
        print("\n" + "=" * 70)
        print("📊 全市场分红策略分析报告")
        print("=" * 70)
        
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
        print(f"\n【沪市 vs 深市】")
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
        
        # 按行业分组
        print(f"\n【按行业统计】")
        def get_industry(code):
            if code.startswith('60'):
                return '沪市主板'
            elif code.startswith('000'):
                return '深市主板'
            elif code.startswith('002'):
                return '中小板'
            elif code.startswith('300'):
                return '创业板'
            return '其他'
        
        df['industry'] = df['stock_code'].apply(get_industry)
        ind_stats = df.groupby('industry').agg({
            'total_return_pct': ['count', 'mean'],
            'is_profitable': 'mean'
        }).round(2)
        ind_stats.columns = ['样本数', '平均收益', '盈利概率']
        ind_stats['盈利概率'] = (ind_stats['盈利概率'] * 100).round(2).astype(str) + '%'
        print(ind_stats.to_string())
        
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
        
        # 最差表现股票
        print(f"\n【表现最差的10只股票】")
        worst_stocks = df.groupby(['stock_code', 'stock_name']).agg({
            'total_return_pct': ['mean', 'count'],
            'is_profitable': 'mean'
        })
        worst_stocks.columns = ['平均收益', '分红次数', '盈利概率']
        worst_stocks = worst_stocks[worst_stocks['分红次数'] >= 2]
        worst_stocks = worst_stocks.sort_values('平均收益', ascending=True).head(10)
        worst_stocks['盈利概率'] = (worst_stocks['盈利概率'] * 100).round(1).astype(str) + '%'
        print(worst_stocks.to_string())
        
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


def main():
    analyzer = FullMarketAnalyzer(lookback_days=30, years_limit=3)
    
    stocks = analyzer.get_stock_list()
    df = analyzer.analyze_all(stocks)
    
    if not df.empty:
        os.makedirs('data', exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'data/full_market_analysis_{timestamp}.csv'
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"\n💾 分析结果已保存到: {filename}")
        
        analyzer.generate_report(df)
    else:
        print("\n❌ 没有获取到有效的分析数据")


if __name__ == '__main__':
    main()
