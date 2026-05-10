# 股票实时数据获取项目计划

## 1. 项目概述

**项目名称**: StockDataCollector
**项目目标**: 获取A股、港股和沪港通股票的实时价格数据、分红信息及分红策略分析
**核心功能**: 
- 实时股票行情获取
- 支持多市场数据源
- 股票分红数据获取
- **分红策略收益率分析**
- 数据缓存与去重
- 定时数据更新

## 2. 技术方案

### 2.1 主要依赖库
- **akshare**: 主要数据源，支持A股、港股、沪港通、分红数据、历史K线
- **pandas**: 数据处理和分析
- **numpy**: 数值计算
- **matplotlib/seaborn**: 数据可视化
- **schedule**: 定时任务调度
- **requests**: HTTP请求库
- **logging**: 日志记录

### 2.2 数据范围
- **A股**: 上海和深圳交易所上市的所有股票
- **港股**: 香港交易所上市的所有股票
- **沪港通**:
  - 沪股通（北向）：上海交易所的港资可投资股票
  - 港股通（南向）：香港交易所的A股可投资股票
- **分红数据**: A股和港股的历史分红记录
- **历史价格**: 分红前后至少2个月的价格数据

## 3. 功能模块设计

### 3.1 数据获取模块 (DataFetcher)
- `fetch_a_stock()`: 获取A股实时行情
- `fetch_hk_stock()`: 获取港股实时行情
- `fetch_hsgt_north()`: 获取沪股通数据
- `fetch_hsgt_south()`: 获取港股通数据
- `fetch_by_codes()`: 根据股票代码批量获取
- `fetch_dividend()`: 获取单只股票分红历史
- `fetch_dividend_batch()`: 批量获取多只股票分红
- `fetch_stock_history()`: 获取股票历史K线数据

### 3.2 数据处理模块 (DataProcessor)
- 数据清洗和格式化
- 重复数据去重
- 异常值处理
- 数据类型转换
- 分红前后价格对齐

### 3.3 存储模块 (DataStorage)
- 支持MySQL/MongoDB存储
- 支持CSV/JSON文件导出
- 数据历史记录管理

### 3.4 调度模块 (Scheduler)
- 定时任务配置
- 增量更新策略
- 失败重试机制

### 3.5 监控模块 (Monitor)
- 运行状态监控
- 数据质量检查
- 异常告警通知

### 3.6 分红策略分析模块 (DividendStrategyAnalyzer) ⭐新增
- 计算分红前1个月价格
- 计算除权除息日价格
- 计算含分红总收益率
- 统计分析盈利概率
- 生成可视化报告

## 4. 项目结构

```
stock_data_collector/
├── config/
│   ├── __init__.py
│   ├── settings.py          # 配置文件
│   └── database.py          # 数据库配置
├── core/
│   ├── __init__.py
│   ├── data_fetcher.py      # 数据获取
│   ├── data_processor.py    # 数据处理
│   └── data_storage.py      # 数据存储
├── scheduler/
│   ├── __init__.py
│   └── task_scheduler.py    # 定时任务
├── utils/
│   ├── __init__.py
│   ├── logger.py           # 日志工具
│   └── validators.py       # 数据验证
├── analysis/                 # ⭐新增
│   ├── __init__.py
│   ├── dividend_strategy.py  # 分红策略分析
│   └── visualizer.py        # 可视化模块
├── main.py                  # 主程序入口
├── requirements.txt         # 依赖列表
└── README.md               # 使用说明
```

## 5. 实施步骤

### 阶段一：基础框架搭建
- [ ] 创建项目目录结构
- [ ] 配置开发环境
- [ ] 安装必要依赖
- [ ] 配置日志系统

### 阶段二：核心功能实现
- [ ] 实现数据获取模块（行情+分红）
- [ ] 实现数据处理模块
- [ ] 实现数据存储模块
- [ ] 单元测试

### 阶段三：高级功能
- [ ] 实现定时任务调度
- [ ] 添加数据监控
- [ ] 实现异常处理机制
- [ ] 添加配置管理

### 阶段四：优化和完善
- [ ] 性能优化
- [ ] 错误处理完善
- [ ] 文档编写
- [ ] 用户使用指南

### 阶段五：分红策略分析 ⭐新增
- [ ] 设计分红策略分析模块
- [ ] 实现收益率计算逻辑
- [ ] 统计盈利概率分析
- [ ] 生成可视化报告

## 6. 数据字段说明

### 6.1 A股/港股实时行情字段
| 字段名 | 说明 | 示例 |
|--------|------|------|
| code | 股票代码 | 600000 |
| name | 股票名称 | 浦发银行 |
| price | 当前价格 | 10.25 |
| change | 涨跌额 | 0.15 |
| change_pct | 涨跌幅% | 1.49 |
| volume | 成交量 | 5000000 |
| amount | 成交额 | 51250000 |
| open | 开盘价 | 10.10 |
| high | 最高价 | 10.30 |
| low | 最低价 | 10.05 |
| close | 昨收价 | 10.10 |
| timestamp | 更新时间 | 2024-01-01 09:30:00 |

### 6.2 沪港通数据字段
| 字段名 | 说明 |
|--------|------|
| code | 股票代码 |
| name | 股票名称 |
| north_net_amount | 北向资金净流入 |
| south_net_amount | 南向资金净流入 |
| hold_amount | 持股数量 |
| market | 市场(沪/深/港) |

### 6.3 A股分红数据字段
| 字段名 | 说明 |
|--------|------|
| 分红年度 | 分红所属年份 |
| 每股派现(元) | 每股派发现金金额 |
| 除权除息日 | 分红除权生效日期 |
| 股权登记日 | 确定股东名册的日期 |
| 派息日 | 实际发放红利日期 |
| 派现总额(亿元) | 总派现金额 |
| 分红类型 | 年度分红、中期分红等 |
| 报告时间 | 对应哪年的财务报告 |

### 6.4 港股分红数据字段
| 字段名 | 说明 |
|--------|------|
| 最新公告日期 | 分红公告发布时间 |
| 财政年度 | 所属财年 |
| 分红方案 | 具体分红方案描述 |
| 分配类型 | 年度分配/特别分配 |
| 除净日 | 除权日期 |
| 截至过户日 | 股权登记截止日期 |
| 发放日 | 实际发放日期 |

### 6.5 分红策略分析结果字段 ⭐新增
| 字段名 | 说明 |
|--------|------|
| stock_code | 股票代码 |
| stock_name | 股票名称 |
| dividend_date | 除权除息日 |
| price_before | 分红前1个月收盘价 |
| price_at_dividend | 除权除息日价格 |
| price_change | 价差收益(元) |
| price_change_pct | 价差收益率(%) |
| dividend_per_share | 每股分红(元) |
| dividend_yield | 分红收益率(%) |
| total_return | 含分红总收益率(%) |
| is_profitable | 是否盈利 |
| holding_days | 持有天数 |

## 7. API接口设计

### 7.1 命令行接口
```bash
# 获取A股实时数据
python main.py fetch --market a --codes 600000,000001

# 获取港股实时数据
python main.py fetch --market hk --codes 00700,09988

# 获取沪港通数据
python main.py fetch --market hsgt --type north

# 获取单只股票分红数据
python main.py dividend --code 600519

# 批量获取股票分红数据
python main.py dividend --codes 600519,000858,600036

# ⭐分红策略分析
python main.py analyze --strategy dividend --codes 600519,000858 --months 1

# 分析全部A股高股息股票
python main.py analyze --strategy dividend --market a --min-yield 3.0

# 启动定时任务
python main.py schedule --interval 60
```

### 7.2 配置文件格式
```yaml
database:
  type: mysql
  host: localhost
  port: 3306
  database: stock_data
  username: root
  password: ""

fetch:
  retry_times: 3
  timeout: 30
  interval: 60  # 秒

markets:
  a_share: true
  hk_stock: true
  hsgt_north: true
  hsgt_south: true
  dividend: true

# ⭐分红策略配置
dividend_strategy:
  lookback_months: 1  # 分红前几个月买入
  min_sample_size: 10  # 最少样本数量
  min_dividend_yield: 3.0  # 最小股息率(%)
  exclude_st: true  # 排除ST股票
  exclude_new_stocks: true  # 排除上市不足1年的股票
```

## 8. 错误处理策略

### 8.1 网络错误
- 自动重试3次
- 指数退避策略
- 记录失败请求

### 8.2 数据错误
- 数据格式校验
- 异常值过滤
- 告警通知

### 8.3 系统错误
- 日志记录
- 优雅降级
- 状态恢复

## 9. 性能指标

- 单次请求响应时间: < 5秒
- 批量获取1000支股票: < 60秒
- 系统可用性: 99.5%
- 数据更新频率: 每60秒

## 10. 后续扩展方向

- Web界面展示
- 数据分析功能
- 价格预警通知
- 移动端App
- 量化交易接口

## 11. 风险评估

| 风险类型 | 影响程度 | 应对措施 |
|---------|---------|---------|
| 数据源API变更 | 高 | 预留多数据源切换 |
| 网络不稳定 | 中 | 添加本地缓存 |
| 数据延迟 | 中 | 明确标注数据时间 |
| 存储容量 | 低 | 定期清理历史数据 |

## 12. 资源需求

- Python 3.8+
- 内存: 2GB+
- 存储: 10GB+
- 网络: 稳定的互联网连接

## 13. 时间规划

- **阶段一**: 1-2天
- **阶段二**: 3-5天
- **阶段三**: 2-3天
- **阶段四**: 1-2天
- **阶段五**: 2-3天

**预计总工期**: 9-15天

---

# 分红数据获取详细说明

## 14. 分红数据获取方案

### 14.1 数据来源

使用 **akshare** 库获取分红数据，主要接口：

#### A股分红数据
1. **stock_history_dividend_detail**: 获取单只股票历史分红详情
   ```python
   import akshare as ak
   
   # 获取贵州茅台分红历史
   df = ak.stock_history_dividend_detail(symbol="600519", indicator="分红")
   ```

2. **stock_dividend_cninfo**: 通过巨潮资讯获取详细分红信息
   ```python
   # 获取格力电器分红详情
   df = ak.stock_dividend_cninfo(symbol="000651")
   ```

#### 港股分红数据
1. **stock_hk_dividend_payout_em**: 获取港股历史分红记录
   ```python
   # 获取腾讯控股分红历史
   df = ak.stock_hk_dividend_payout_em(symbol="00700")
   ```

#### 历史价格数据
```python
# 获取股票历史K线数据
stock_hist = ak.stock_zh_a_hist(
    symbol="600519", 
    period="daily", 
    start_date="20200101", 
    end_date="20241231"
)
```

### 14.2 关键日期说明

| 日期类型 | 说明 | 重要提示 |
|---------|------|---------|
| **除权除息日** | 分红除权生效日期 | 这是决定能否获得分红的截止日期 |
| **股权登记日** | 确定股东名册的日期 | T日登记，T+1日才能获得分红 |
| **派息日** | 实际发放红利的日期 | 资金到账日期 |

### 14.3 分红数据类型

- **年度分红**: 每年年度分红
- **中期分红**: 半年报分红
- **特别分红**: 特殊情况下的一次性分红
- **送股**: 股票股利
- **转增**: 公积金转增股本

### 14.4 批量获取示例代码

```python
import akshare as ak
import pandas as pd
import time

def fetch_a_stock_dividend_batch(stock_codes):
    """批量获取A股分红数据"""
    all_dividends = []
    
    for code in stock_codes:
        try:
            df = ak.stock_history_dividend_detail(symbol=code, indicator="分红")
            if df is not None and not df.empty:
                df["股票代码"] = code
                all_dividends.append(df)
            time.sleep(0.5)  # 避免请求过快
        except Exception as e:
            print(f"获取 {code} 分红数据失败: {e}")
    
    if all_dividends:
        result = pd.concat(all_dividends, ignore_index=True)
        result.to_csv("stock_dividends.csv", index=False, encoding="utf-8-sig")
        return result
    return None

def fetch_hk_stock_dividend_batch(stock_codes):
    """批量获取港股分红数据"""
    all_dividends = []
    
    for code in stock_codes:
        try:
            df = ak.stock_hk_dividend_payout_em(symbol=code)
            if df is not None and not df.empty:
                df["股票代码"] = code
                all_dividends.append(df)
            time.sleep(0.5)
        except Exception as e:
            print(f"获取 {code} 分红数据失败: {e}")
    
    if all_dividends:
        result = pd.concat(all_dividends, ignore_index=True)
        result.to_csv("hk_stock_dividends.csv", index=False, encoding="utf-8-sig")
        return result
    return None

# 使用示例
a_stock_list = ["600519", "000858", "600036", "000651"]
hk_stock_list = ["00700", "09988", "03690"]

print("开始获取A股分红数据...")
a_dividends = fetch_a_stock_dividend_batch(a_stock_list)
print(f"A股分红数据获取完成，共 {len(a_dividends) if a_dividends is not None else 0} 条记录")

print("\n开始获取港股分红数据...")
hk_dividends = fetch_hk_stock_dividend_batch(hk_stock_list)
print(f"港股分红数据获取完成，共 {len(hk_dividends) if hk_dividends is not None else 0} 条记录")
```

### 14.5 数据分析应用

#### 计算股息率
```python
import akshare as ak

def calculate_dividend_yield(stock_code, market="a"):
    """计算股票股息率"""
    # 获取当前股价
    if market == "a":
        stock_spot = ak.stock_zh_a_spot()
        stock_info = stock_spot[stock_spot["代码"] == stock_code]
        if stock_info.empty:
            return None
        current_price = float(stock_info["最新价"].values[0])
    else:
        stock_spot = ak.stock_hk_spot_em()
        stock_info = stock_spot[stock_spot["代码"] == stock_code]
        if stock_info.empty:
            return None
        current_price = float(stock_info["最新价"].values[0])
    
    # 获取最新分红
    if market == "a":
        dividend_df = ak.stock_history_dividend_detail(symbol=stock_code, indicator="分红")
    else:
        dividend_df = ak.stock_hk_dividend_payout_em(symbol=stock_code)
    
    if dividend_df is None or dividend_df.empty:
        return None
    
    # 计算股息率
    latest_dividend = dividend_df.iloc[0]
    if market == "a":
        dividend_per_share = float(latest_dividend["每股派现(元)"])
    else:
        # 港股需要解析分红方案
        dividend_plan = latest_dividend["分红方案"]
        # 解析逻辑...
    
    dividend_yield = (dividend_per_share / current_price) * 100
    return dividend_yield

# 示例：计算贵州茅台股息率
yield_rate = calculate_dividend_yield("600519")
print(f"贵州茅台股息率: {yield_rate:.2f}%" if yield_rate else "无法计算")
```

#### 筛选高股息率股票
```python
def screen_high_dividend_stocks(stock_list, min_yield=5.0):
    """筛选高股息率股票"""
    results = []
    
    for code in stock_list:
        try:
            yield_rate = calculate_dividend_yield(code)
            if yield_rate and yield_rate >= min_yield:
                results.append({
                    "股票代码": code,
                    "股息率": yield_rate
                })
        except Exception as e:
            print(f"处理 {code} 时出错: {e}")
    
    return pd.DataFrame(results)
```

## 15. 分红数据存储设计

### 15.1 数据库表结构

```sql
-- A股分红数据表
CREATE TABLE a_share_dividend (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    stock_code VARCHAR(10) NOT NULL COMMENT '股票代码',
    stock_name VARCHAR(50) COMMENT '股票名称',
    dividend_year VARCHAR(10) COMMENT '分红年度',
    per_share_dividend DECIMAL(10,4) COMMENT '每股派现(元)',
    ex_right_date DATE COMMENT '除权除息日',
    record_date DATE COMMENT '股权登记日',
    payment_date DATE COMMENT '派息日',
    total_dividend DECIMAL(20,4) COMMENT '派现总额(亿元)',
    dividend_type VARCHAR(20) COMMENT '分红类型',
    report_period VARCHAR(20) COMMENT '报告时间',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_stock_code (stock_code),
    INDEX idx_ex_right_date (ex_right_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 港股分红数据表
CREATE TABLE hk_stock_dividend (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    stock_code VARCHAR(10) NOT NULL COMMENT '股票代码',
    stock_name VARCHAR(50) COMMENT '股票名称',
    announcement_date DATE COMMENT '最新公告日期',
    fiscal_year VARCHAR(10) COMMENT '财政年度',
    dividend_plan TEXT COMMENT '分红方案',
    allocation_type VARCHAR(20) COMMENT '分配类型',
    ex_right_date DATE COMMENT '除净日',
    transfer_deadline DATE COMMENT '截至过户日',
    payment_date DATE COMMENT '发放日',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_stock_code (stock_code),
    INDEX idx_ex_right_date (ex_right_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 分红策略分析结果表 ⭐新增
CREATE TABLE dividend_strategy_result (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    stock_code VARCHAR(10) NOT NULL COMMENT '股票代码',
    stock_name VARCHAR(50) COMMENT '股票名称',
    dividend_date DATE COMMENT '除权除息日',
    price_before DECIMAL(10,4) COMMENT '分红前1个月收盘价',
    price_at_dividend DECIMAL(10,4) COMMENT '除权除息日价格',
    price_change DECIMAL(10,4) COMMENT '价差收益(元)',
    price_change_pct DECIMAL(10,4) COMMENT '价差收益率(%)',
    dividend_per_share DECIMAL(10,4) COMMENT '每股分红(元)',
    dividend_yield DECIMAL(10,4) COMMENT '分红收益率(%)',
    total_return DECIMAL(10,4) COMMENT '含分红总收益率(%)',
    is_profitable TINYINT COMMENT '是否盈利(1=是,0=否)',
    holding_days INT COMMENT '持有天数',
    dividend_type VARCHAR(20) COMMENT '分红类型',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_stock_code (stock_code),
    INDEX idx_dividend_date (dividend_date),
    INDEX idx_total_return (total_return),
    INDEX idx_is_profitable (is_profitable)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 15.2 数据导出格式

支持导出格式：
- CSV（默认，utf-8-sig编码）
- Excel（xlsx格式）
- JSON
- 数据库

## 16. 定时分红数据更新

```python
import schedule
import time
import akshare as ak
import pandas as pd

def update_dividend_data():
    """定时更新分红数据"""
    print("开始更新分红数据...")
    
    # 获取最新分红公告
    try:
        # 获取A股分红数据
        stock_list = ["600519", "000858", "600036", "000651"]
        for code in stock_list:
            df = ak.stock_history_dividend_detail(symbol=code, indicator="分红")
            # 存储逻辑...
            print(f"更新 {code} 分红数据成功")
    except Exception as e:
        print(f"更新分红数据失败: {e}")

# 配置定时任务
schedule.every().day.at("18:00").do(update_dividend_data)  # 每天18点更新

while True:
    schedule.run_pending()
    time.sleep(60)
```

## 17. 注意事项

1. **数据使用声明**: akshare数据仅供学术研究用途，不构成投资建议
2. **请求频率**: 批量获取时建议添加0.5秒延迟，避免被限流
3. **数据完整性**: 部分历史分红数据可能缺失，需要做好异常处理
4. **港股分红**: 港股分红金额通常以港币或美元计价，需要注意汇率转换
5. **分红类型**: 注意区分年度分红、中期分红、特别分红等类型
6. **复权信息**: 结合分红数据进行股价复权计算时需要注意

## 18. 故障排除

### 常见问题及解决方案

| 问题 | 可能原因 | 解决方案 |
|-----|---------|---------|
| 请求超时 | 网络不稳定 | 增加超时时间，添加重试机制 |
| 数据为空 | 股票代码错误 | 验证股票代码格式 |
| 字段缺失 | 数据源更新 | 检查akshare版本，升级到最新 |
| 请求频率限制 | 请求过快 | 降低请求频率，添加延迟 |
| 中文乱码 | 编码问题 | 使用utf-8-sig编码保存CSV |

### 版本要求
- Python 3.8+
- akshare 最新版
- pandas
- numpy
- matplotlib
- requests

---

# ⭐分红策略分析详细说明

## 19. 分红策略研究背景

### 19.1 研究问题

**核心问题**: 如果在股票除权除息日前1个月买入股票，持有到除权除息日（含分红收益），盈利概率是多少？

### 19.2 策略逻辑

```
买入时机: 除权除息日前30个交易日
持有期间: 30个交易日
收益计算: 
  - 价差收益 = 除权除息日价格 - 买入价格
  - 分红收益 = 每股分红金额
  - 总收益 = 价差收益 + 分红收益
  - 总收益率 = 总收益 / 买入价格 × 100%
```

### 19.3 为什么选择"除权除息日前1个月"？

1. **信息时效性**: 分红预案通常在除权除息日前1-2个月公布
2. **价格规律**: 部分股票在分红预期下可能出现上涨
3. **数据可得性**: 1个月时间窗口便于统计分析
4. **交易成本**: 持有时间适中，交易成本可控

## 20. 分红策略分析模块设计

### 20.1 核心算法

```python
class DividendStrategyAnalyzer:
    """
    分红策略分析器
    
    研究目标: 分析在除权除息日前N天买入股票的盈利概率
    """
    
    def __init__(self, lookback_days=30):
        """
        初始化分析器
        
        Args:
            lookback_days: 分红前多少天买入（默认30天）
        """
        self.lookback_days = lookback_days
        self.results = []
    
    def analyze_single_stock(self, stock_code, market="a"):
        """
        分析单只股票的分红策略收益
        
        Args:
            stock_code: 股票代码
            market: 市场类型 ("a" 或 "hk")
        
        Returns:
            DataFrame: 分析结果
        """
        # 1. 获取分红历史
        dividend_df = self._get_dividend_history(stock_code, market)
        
        # 2. 获取历史价格数据
        price_df = self._get_price_history(stock_code, market)
        
        # 3. 计算每次分红的策略收益
        results = []
        for _, dividend in dividend_df.iterrows():
            result = self._calculate_single_dividend_return(
                stock_code, dividend, price_df, market
            )
            if result:
                results.append(result)
        
        return pd.DataFrame(results)
    
    def _get_dividend_history(self, stock_code, market):
        """获取分红历史"""
        if market == "a":
            df = ak.stock_history_dividend_detail(symbol=stock_code, indicator="分红")
        else:
            df = ak.stock_hk_dividend_payout_em(symbol=stock_code)
        return df
    
    def _get_price_history(self, stock_code, market):
        """获取历史价格数据"""
        if market == "a":
            # 获取近5年数据，确保覆盖所有分红记录
            end_date = datetime.now().strftime("%Y%m%d")
            start_date = (datetime.now() - timedelta(days=365*5)).strftime("%Y%m%d")
            df = ak.stock_zh_a_hist(
                symbol=stock_code,
                period="daily",
                start_date=start_date,
                end_date=end_date
            )
        else:
            # 港股价格获取逻辑
            pass
        return df
    
    def _calculate_single_dividend_return(self, stock_code, dividend, price_df, market):
        """
        计算单次分红的策略收益
        
        Returns:
            dict: 包含所有分析字段的字典
        """
        try:
            # 获取除权除息日
            if market == "a":
                ex_right_date = pd.to_datetime(dividend["除权除息日"])
                dividend_per_share = float(dividend["每股派现(元)"])
            else:
                ex_right_date = pd.to_datetime(dividend["除净日"])
                # 港股需要解析分红方案
                dividend_per_share = self._parse_hk_dividend(dividend["分红方案"])
            
            # 计算买入日期（除权除息日前N天）
            buy_date = ex_right_date - timedelta(days=self.lookback_days)
            
            # 找到最接近买入日期的收盘价
            price_before = self._get_nearest_price(price_df, buy_date, before=True)
            
            # 找到除权除息日当天的收盘价
            price_at_dividend = self._get_nearest_price(price_df, ex_right_date, before=False)
            
            if price_before is None or price_at_dividend is None:
                return None
            
            # 计算收益率
            price_change = price_at_dividend - price_before
            price_change_pct = (price_change / price_before) * 100
            dividend_yield = (dividend_per_share / price_before) * 100
            total_return = price_change_pct + dividend_yield
            
            return {
                "stock_code": stock_code,
                "dividend_date": ex_right_date,
                "price_before": price_before,
                "price_at_dividend": price_at_dividend,
                "price_change": price_change,
                "price_change_pct": price_change_pct,
                "dividend_per_share": dividend_per_share,
                "dividend_yield": dividend_yield,
                "total_return": total_return,
                "is_profitable": 1 if total_return > 0 else 0,
                "holding_days": self.lookback_days
            }
        except Exception as e:
            print(f"计算 {stock_code} 分红收益失败: {e}")
            return None
    
    def _get_nearest_price(self, price_df, target_date, before=True):
        """获取最接近目标日期的价格"""
        if price_df is None or price_df.empty:
            return None
        
        # 转换日期格式
        price_df = price_df.copy()
        if "日期" in price_df.columns:
            price_df["日期"] = pd.to_datetime(price_df["日期"])
            target_col = "日期"
        elif "date" in price_df.columns.str.lower():
            price_df["date"] = pd.to_datetime(price_df["date"])
            target_col = "date"
        else:
            return None
        
        if before:
            # 找目标日期之前的数据
            mask = price_df[target_col] <= target_date
        else:
            # 找目标日期当天的数据
            mask = price_df[target_col] == target_date
        
        filtered = price_df[mask]
        
        if filtered.empty:
            return None
        
        if before:
            # 返回最接近目标日期的价格（最后一行）
            return float(filtered.iloc[-1]["收盘"])
        else:
            return float(filtered.iloc[0]["收盘"])
    
    def _parse_hk_dividend(self, dividend_plan):
        """解析港股分红方案"""
        import re
        # 例如: "每股派港币4.5元"
        match = re.search(r'每股派[港币$]*([\d.]+)元?', dividend_plan)
        if match:
            return float(match.group(1))
        return 0.0
```

### 20.2 批量分析功能

```python
def analyze_batch_stocks(stock_codes, market="a", lookback_days=30):
    """
    批量分析多只股票的分红策略
    
    Args:
        stock_codes: 股票代码列表
        market: 市场类型
        lookback_days: 分红前多少天买入
    
    Returns:
        DataFrame: 汇总分析结果
    """
    analyzer = DividendStrategyAnalyzer(lookback_days=lookback_days)
    all_results = []
    
    for code in stock_codes:
        try:
            result = analyzer.analyze_single_stock(code, market)
            if result is not None and not result.empty:
                all_results.append(result)
            time.sleep(0.5)  # 避免请求过快
        except Exception as e:
            print(f"分析 {code} 失败: {e}")
    
    if all_results:
        return pd.concat(all_results, ignore_index=True)
    return None
```

## 21. 统计分析方法

### 21.1 核心统计指标

```python
def calculate_statistics(result_df):
    """
    计算盈利概率统计
    
    Returns:
        dict: 包含各项统计指标的字典
    """
    if result_df is None or result_df.empty:
        return None
    
    total_count = len(result_df)
    profitable_count = result_df["is_profitable"].sum()
    loss_count = total_count - profitable_count
    
    stats = {
        "总样本数": total_count,
        "盈利次数": profitable_count,
        "亏损次数": loss_count,
        "盈利概率": f"{profitable_count / total_count * 100:.2f}%",
        "亏损概率": f"{loss_count / total_count * 100:.2f}%",
        "平均收益率": f"{result_df['total_return'].mean():.2f}%",
        "中位数收益率": f"{result_df['total_return'].median():.2f}%",
        "最大收益率": f"{result_df['total_return'].max():.2f}%",
        "最小收益率": f"{result_df['total_return'].min():.2f}%",
        "收益率标准差": f"{result_df['total_return'].std():.2f}%",
    }
    
    # 计算不同分红类型的盈利概率
    if "dividend_type" in result_df.columns:
        stats["按分红类型统计"] = {}
        for div_type in result_df["dividend_type"].unique():
            type_df = result_df[result_df["dividend_type"] == div_type]
            type_profitable = type_df["is_profitable"].sum()
            type_total = len(type_df)
            stats["按分红类型统计"][div_type] = {
                "样本数": type_total,
                "盈利概率": f"{type_profitable / type_total * 100:.2f}%"
            }
    
    return stats
```

### 21.2 分组分析

```python
def analyze_by_dividend_yield(result_df, yield_bins=[0, 2, 4, 6, 100]):
    """
    按股息率分组分析盈利概率
    
    Args:
        result_df: 分析结果DataFrame
        yield_bins: 股息率分组区间
    
    Returns:
        DataFrame: 分组统计结果
    """
    result_df = result_df.copy()
    result_df["股息率分组"] = pd.cut(
        result_df["dividend_yield"], 
        bins=yield_bins,
        labels=["<2%", "2-4%", "4-6%", ">6%"]
    )
    
    grouped = result_df.groupby("股息率分组").agg({
        "total_return": ["count", "mean", "median", "std"],
        "is_profitable": "mean"
    }).round(2)
    
    grouped.columns = ["样本数", "平均收益", "中位收益", "标准差", "盈利概率"]
    grouped["盈利概率"] = grouped["盈利概率"].apply(lambda x: f"{x*100:.2f}%")
    
    return grouped
```

## 22. 可视化分析

### 22.1 收益率分布图

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_return_distribution(result_df, save_path="return_distribution.png"):
    """绘制收益率分布图"""
    plt.figure(figsize=(12, 8))
    
    # 子图1: 收益率直方图
    plt.subplot(2, 2, 1)
    sns.histplot(result_df["total_return"], bins=50, kde=True)
    plt.axvline(x=0, color='red', linestyle='--', label='盈亏平衡点')
    plt.axvline(x=result_df["total_return"].mean(), color='green', 
                linestyle='--', label=f'平均收益: {result_df["total_return"].mean():.2f}%')
    plt.xlabel("总收益率(%)")
    plt.ylabel("频数")
    plt.title("收益率分布")
    plt.legend()
    
    # 子图2: 盈利vs亏损饼图
    plt.subplot(2, 2, 2)
    profitable = result_df["is_profitable"].sum()
    loss = len(result_df) - profitable
    plt.pie([profitable, loss], labels=["盈利", "亏损"], 
            autopct='%1.1f%%', colors=["lightgreen", "lightcoral"])
    plt.title("盈利概率分布")
    
    # 子图3: 分红收益vs价差收益散点图
    plt.subplot(2, 2, 3)
    plt.scatter(result_df["dividend_yield"], result_df["price_change_pct"],
                c=result_df["is_profitable"], cmap="coolwarm", alpha=0.6)
    plt.axhline(y=0, color='red', linestyle='--')
    plt.xlabel("分红收益率(%)")
    plt.ylabel("价差收益率(%)")
    plt.title("分红收益 vs 价差收益")
    
    # 子图4: 持有期间收益率箱线图
    plt.subplot(2, 2, 4)
    result_df.boxplot(column="total_return", by="is_profitable")
    plt.xlabel("是否盈利 (0=亏损, 1=盈利)")
    plt.ylabel("总收益率(%)")
    plt.title("盈利与亏损收益率对比")
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.show()
```

### 22.2 时间序列分析

```python
def plot_time_series_analysis(result_df, save_path="time_series.png"):
    """绘制时间序列分析图"""
    result_df = result_df.copy()
    result_df["dividend_year"] = result_df["dividend_date"].dt.year
    
    plt.figure(figsize=(14, 6))
    
    # 年度盈利概率趋势
    plt.subplot(1, 2, 1)
    yearly_stats = result_df.groupby("dividend_year").agg({
        "is_profitable": "mean",
        "total_return": "mean"
    })
    
    ax1 = plt.gca()
    ax2 = ax1.twinx()
    
    yearly_stats["is_profitable"].plot(kind="bar", ax=ax1, 
                                       color="steelblue", alpha=0.7, label="盈利概率")
    yearly_stats["total_return"].plot(kind="line", ax=ax2, 
                                       color="red", marker="o", label="平均收益率")
    
    ax1.set_xlabel("年份")
    ax1.set_ylabel("盈利概率", color="steelblue")
    ax2.set_ylabel("平均收益率(%)", color="red")
    ax1.set_ylim(0, 1)
    plt.title("年度盈利概率与收益率趋势")
    
    # 移动平均盈利概率
    plt.subplot(1, 2, 2)
    result_df = result_df.sort_values("dividend_date")
    result_df["rolling_profit_rate"] = result_df["is_profitable"].rolling(window=30).mean()
    result_df["rolling_return"] = result_df["total_return"].rolling(window=30).mean()
    
    plt.plot(result_df["dividend_date"], result_df["rolling_profit_rate"],
             label="盈利概率(30日均线)")
    plt.plot(result_df["dividend_date"], result_df["rolling_return"],
             label="平均收益率(30日均线)")
    plt.axhline(y=0, color='red', linestyle='--')
    plt.xlabel("时间")
    plt.ylabel("指标值")
    plt.title("盈利概率与收益率时间序列")
    plt.legend()
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    plt.show()
```

## 23. 完整分析流程示例

```python
import akshare as ak
import pandas as pd
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

def run_full_analysis(stock_list=["600519", "000858", "600036", "000651", 
                                   "601318", "600887", "000333", "002594"]):
    """
    完整的分红策略分析流程
    """
    print("=" * 60)
    print("股票分红策略分析 - 除权除息日前30天买入")
    print("=" * 60)
    
    # 1. 批量获取分析数据
    print("\n步骤1: 获取股票分红和价格数据...")
    all_results = []
    analyzer = DividendStrategyAnalyzer(lookback_days=30)
    
    for code in stock_list:
        print(f"  分析 {code}...", end=" ")
        try:
            result = analyzer.analyze_single_stock(code, market="a")
            if result is not None and not result.empty:
                all_results.append(result)
                print(f"成功 ({len(result)}条记录)")
            else:
                print("无数据")
        except Exception as e:
            print(f"失败: {e}")
    
    if not all_results:
        print("\n没有获取到任何分析数据！")
        return None
    
    # 合并所有结果
    all_results_df = pd.concat(all_results, ignore_index=True)
    print(f"\n共获取 {len(all_results_df)} 条分析记录")
    
    # 2. 计算统计指标
    print("\n步骤2: 计算统计指标...")
    stats = calculate_statistics(all_results_df)
    for key, value in stats.items():
        if key != "按分红类型统计":
            print(f"  {key}: {value}")
    
    # 3. 按股息率分组分析
    print("\n步骤3: 按股息率分组分析...")
    yield_analysis = analyze_by_dividend_yield(all_results_df)
    print(yield_analysis)
    
    # 4. 生成可视化
    print("\n步骤4: 生成可视化报告...")
    try:
        plot_return_distribution(all_results_df, "return_distribution.png")
        print("  已保存: return_distribution.png")
        
        plot_time_series_analysis(all_results_df, "time_series.png")
        print("  已保存: time_series.png")
    except Exception as e:
        print(f"  可视化生成失败: {e}")
    
    # 5. 保存详细结果
    print("\n步骤5: 保存分析结果...")
    all_results_df.to_csv("dividend_strategy_results.csv", 
                         index=False, encoding="utf-8-sig")
    print("  已保存: dividend_strategy_results.csv")
    
    # 6. 生成分析报告
    print("\n" + "=" * 60)
    print("分析结论")
    print("=" * 60)
    
    profitable_rate = stats["盈利概率"]
    avg_return = stats["平均收益率"]
    
    print(f"""
    根据对 {len(all_results_df)} 次分红事件的分析：
    
    1. 盈利概率: {profitable_rate}
       - 盈利次数: {stats['盈利次数']}
       - 亏损次数: {stats['亏损次数']}
    
    2. 收益情况:
       - 平均收益率: {avg_return}
       - 中位数收益率: {stats['中位数收益率']}
       - 收益率范围: {stats['最小收益率']} ~ {stats['最大收益率']}
       - 波动性(标准差): {stats['收益率标准差']}
    
    3. 策略建议:
       {"该策略整体具有较高的盈利概率，可以考虑使用" if float(profitable_rate.rstrip("%")) > 50 else "该策略盈利概率较低，需要谨慎使用"}
    """)
    
    return all_results_df

# 运行完整分析
if __name__ == "__main__":
    result = run_full_analysis()
```

## 24. 研究扩展方向

### 24.1 多时间窗口分析

- 分析不同持有期（15天、30天、45天、60天）的盈利概率
- 找出最优持有期

### 24.2 行业分析

- 按行业分组统计盈利概率
- 找出分红策略最有效的行业

### 24.3 市值分析

- 按市值分组（大、中、小盘）
- 分析市值对分红策略效果的影响

### 24.4 分红类型分析

- 区分现金分红、送股、转增
- 分析不同分红类型的策略效果

### 24.5 市场周期分析

- 分析在不同市场周期（牛市、熊市、震荡市）的策略表现
- 找出策略最有效的市场环境

### 24.6 机器学习预测

- 使用历史数据训练模型
- 预测未来分红的盈利概率

## 25. 风险提示

⚠️ **重要声明**:

1. **历史数据不代表未来**: 过去的盈利概率不代表未来表现
2. **交易成本**: 实际交易需要考虑佣金、印花税等成本
3. **价格波动**: 除权除息日价格可能受多种因素影响
4. **信息滞后**: 分红预案可能发生变化
5. **市场风险**: 整体市场环境会影响策略效果

**本分析仅供学术研究参考，不构成投资建议！**

## 26. 性能优化建议

### 26.1 数据缓存

```python
import joblib
import os

class DataCache:
    """数据缓存管理器"""
    
    def __init__(self, cache_dir="cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get(self, key):
        """获取缓存数据"""
        path = os.path.join(self.cache_dir, f"{key}.pkl")
        if os.path.exists(path):
            return joblib.load(path)
        return None
    
    def set(self, key, data):
        """设置缓存数据"""
        path = os.path.join(self.cache_dir, f"{key}.pkl")
        joblib.dump(data, path)
    
    def clear(self):
        """清空缓存"""
        for f in os.listdir(self.cache_dir):
            os.remove(os.path.join(self.cache_dir, f))
```

### 26.2 并行处理

```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def analyze_parallel(stock_codes, max_workers=5):
    """并行分析多只股票"""
    analyzer = DividendStrategyAnalyzer()
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(analyzer.analyze_single_stock, code): code 
            for code in stock_codes
        }
        
        results = []
        for future in as_completed(futures):
            code = futures[future]
            try:
                result = future.result()
                if result is not None:
                    results.append(result)
            except Exception as e:
                print(f"分析 {code} 失败: {e}")
    
    if results:
        return pd.concat(results, ignore_index=True)
    return None
```

### 26.3 增量更新

```python
def incremental_analysis(existing_results, new_stock_codes):
    """
    增量分析 - 只分析新增的股票
    """
    existing_codes = set(existing_results["stock_code"].unique())
    codes_to_analyze = [c for c in new_stock_codes if c not in existing_codes]
    
    if codes_to_analyze:
        new_results = analyze_batch_stocks(codes_to_analyze)
        if new_results is not None:
            return pd.concat([existing_results, new_results], ignore_index=True)
    
    return existing_results
```
