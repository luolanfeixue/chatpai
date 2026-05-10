# 股票实时数据获取项目计划

## 1. 项目概述

**项目名称**: StockDataCollector
**项目目标**: 获取A股、港股和沪港通股票的实时价格数据及分红信息
**核心功能**: 
- 实时股票行情获取
- 支持多市场数据源
- 股票分红数据获取
- 数据缓存与去重
- 定时数据更新

## 2. 技术方案

### 2.1 主要依赖库
- **akshare**: 主要数据源，支持A股、港股、沪港通、分红数据
- **pandas**: 数据处理和分析
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

## 3. 功能模块设计

### 3.1 数据获取模块 (DataFetcher)
- `fetch_a_stock()`: 获取A股实时行情
- `fetch_hk_stock()`: 获取港股实时行情
- `fetch_hsgt_north()`: 获取沪股通数据
- `fetch_hsgt_south()`: 获取港股通数据
- `fetch_by_codes()`: 根据股票代码批量获取
- `fetch_dividend()`: 获取单只股票分红历史
- `fetch_dividend_batch()`: 批量获取多只股票分红

### 3.2 数据处理模块 (DataProcessor)
- 数据清洗和格式化
- 重复数据去重
- 异常值处理
- 数据类型转换

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

**预计总工期**: 7-12天

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
- requests
