# 股票数据获取与分红策略分析系统

## 项目简介

本项目是一个基于Python的股票数据获取与分析系统，主要功能包括：

- **实时行情数据获取**：支持A股、港股、沪港通股票的实时行情数据
- **分红数据获取**：获取A股和港股的历史分红记录
- **分红策略分析**：分析在除权除息日前N天买入股票的盈利概率
- **可视化报告**：生成专业的分析图表和报告

## 功能特性

### 1. 数据获取

- A股实时行情数据（沪深两市所有股票）
- 港股实时行情数据
- 沪港通/深港通持股明细
- 沪深港通资金流向
- 个股历史K线数据
- 股票分红历史数据
- 高股息率股票筛选

### 2. 分红策略分析

核心研究问题：**如果在股票除权除息日前30天买入股票，持有到除权除息日（含分红收益），盈利概率是多少？**

分析内容包括：
- 价差收益计算
- 分红收益计算
- 总收益率统计
- 盈利概率分析
- 按股息率分组分析
- 按年份分组分析
- 股票表现排名

### 3. 数据存储

- 支持CSV、Excel、JSON格式导出
- 自动带时间戳保存
- 数据追加和备份功能
- 旧文件自动清理

### 4. 定时任务

- 支持定时获取实时行情
- 支持定时更新分红数据
- 灵活的任务调度配置

## 安装指南

### 环境要求

- Python 3.8 或更高版本
- Windows/Linux/macOS

### 安装步骤

1. **克隆项目**
```bash
git clone <repository_url>
cd stock_data_collector
```

2. **创建虚拟环境（推荐）**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

或者使用镜像源加速：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 依赖说明

```
akshare>=1.10.0      # 金融数据获取
pandas>=2.0.0         # 数据处理
numpy>=1.24.0         # 数值计算
matplotlib>=3.7.0     # 数据可视化
seaborn>=0.12.0       # 统计绘图
requests>=2.31.0      # HTTP请求
schedule>=1.2.0       # 定时任务
joblib>=1.3.0         # 数据缓存
pyyaml>=6.0           # 配置文件
```

## 快速开始

### 示例1：获取A股实时行情

```bash
python main.py fetch --market a
```

### 示例2：获取指定股票实时行情

```bash
python main.py fetch --market a --codes 600519,000858
```

### 示例3：获取股票分红数据

```bash
python main.py dividend --codes 600519,000858,600036
```

### 示例4：分析分红策略（默认30天持有期）

```bash
python main.py analyze --codes 600519,000858,600036
```

### 示例5：自定义持有期分析

```bash
python main.py analyze --codes 600519,000858 --days 60
```

### 示例6：获取高股息率股票

```bash
python main.py high-dividend --top 50
```

### 示例7：初始化数据库

```bash
python main.py init-db
```

### 示例8：启动定时任务

```bash
python main.py schedule --task realtime --interval 60
```

## 使用说明

### 命令行参数详解

#### fetch - 获取实时行情

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--market` 或 `-m` | 市场类型：`a`=A股，`hk`=港股 | `a` |
| `--codes` 或 `-c` | 股票代码，多个用逗号分隔 | 全部 |

**示例**：
```bash
# 获取全部A股
python main.py fetch --market a

# 获取指定A股
python main.py fetch --codes 600519,000858

# 获取港股
python main.py fetch --market hk
```

#### dividend - 获取分红数据

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--codes` 或 `-c` | 股票代码（必填） | - |
| `--market` 或 `-m` | 市场类型：`a`=A股，`hk`=港股 | `a` |

**示例**：
```bash
python main.py dividend --codes 600519,000858
```

#### analyze - 分析分红策略

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--codes` 或 `-c` | 股票代码 | 使用默认股票池 |
| `--days` 或 `-d` | 分红前持有天数 | 30 |
| `--market` 或 `-m` | 市场类型 | `a` |
| `--no-chart` | 不生成图表 | False |
| `--no-save` | 不保存结果 | False |

**示例**：
```bash
# 分析指定股票
python main.py analyze --codes 600519,000858,600036

# 自定义持有期
python main.py analyze --codes 600519 --days 45

# 不生成图表
python main.py analyze --codes 600519 --no-chart
```

#### high-dividend - 高股息股票

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--top` 或 `-t` | 返回前N只 | 50 |

**示例**：
```bash
python main.py high-dividend --top 100
```

#### schedule - 定时任务

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--task` | 任务类型：`realtime`=实时行情，`dividend`=分红数据 | `realtime` |
| `--interval` 或 `-i` | 间隔秒数 | 60 |

**示例**：
```bash
# 每分钟获取实时行情
python main.py schedule --task realtime --interval 60

# 每小时更新分红数据
python main.py schedule --task dividend --interval 3600
```

## 配置说明

### 配置文件

项目使用 `config.yaml` 配置文件，默认配置如下：

```yaml
database:
  type: sqlite
  path: stock_data.db

fetch:
  retry_times: 3
  timeout: 30
  interval: 60

markets:
  a_share: true
  hk_stock: true
  hsgt_north: true
  hsgt_south: true
  dividend: true

dividend_strategy:
  lookback_days: 30
  min_sample_size: 10
  min_dividend_yield: 3.0
  exclude_st: true
  exclude_new_stocks: true

cache:
  enabled: true
  directory: cache
  expire_hours: 24

log:
  level: INFO
  file: stock_collector.log
  max_bytes: 10485760
  backup_count: 5
```

### 配置项说明

| 配置项 | 说明 |
|--------|------|
| `database.type` | 数据库类型（sqlite/mysql） |
| `fetch.retry_times` | 请求失败重试次数 |
| `fetch.timeout` | 请求超时时间（秒） |
| `dividend_strategy.lookback_days` | 分红前持有天数 |
| `dividend_strategy.min_dividend_yield` | 最小股息率筛选 |
| `log.level` | 日志级别 |

## 数据说明

### A股/港股实时行情字段

| 字段名 | 说明 |
|--------|------|
| 代码 | 股票代码 |
| 名称 | 股票名称 |
| 最新价 | 当前价格 |
| 涨跌幅 | 涨跌幅百分比 |
| 涨跌额 | 涨跌金额 |
| 成交量 | 成交数量 |
| 成交额 | 成交金额 |
| 开盘 | 开盘价 |
| 最高 | 最高价 |
| 最低 | 最低价 |
| 收盘 | 昨收价 |

### 分红数据字段

| 字段名 | 说明 |
|--------|------|
| 除权除息日 | 分红除权生效日期 |
| 每股派现(元) | 每股派发现金 |
| 股权登记日 | 确定股东名册日期 |
| 派息日 | 实际发放红利日期 |
| 分红年度 | 分红所属年度 |

### 分红策略分析结果字段

| 字段名 | 说明 |
|--------|------|
| stock_code | 股票代码 |
| dividend_date | 除权除息日 |
| price_before | 分红前价格 |
| price_at_dividend | 分红时价格 |
| price_change | 价差收益 |
| dividend_per_share | 每股分红 |
| dividend_yield | 分红收益率 |
| total_return | 总收益率 |
| is_profitable | 是否盈利 |

## 分红策略分析详解

### 策略逻辑

```
买入时机: 除权除息日前30个交易日
持有期间: 30个交易日
收益计算: 
  - 价差收益 = 除权除息日价格 - 买入价格
  - 分红收益 = 每股分红金额
  - 总收益 = 价差收益 + 分红收益
  - 总收益率 = 总收益 / 买入价格 × 100%
```

### 关键日期说明

| 日期类型 | 说明 | 重要提示 |
|---------|------|---------|
| 除权除息日 | 分红除权生效日期 | 这是决定能否获得分红的截止日期 |
| 股权登记日 | 确定股东名册的日期 | T日登记，T+1日才能获得分红 |
| 派息日 | 实际发放红利的日期 | 资金到账日期 |

### 为什么选择"除权除息日前30天"？

1. **信息时效性**：分红预案通常在除权除息日前1-2个月公布
2. **价格规律**：部分股票在分红预期下可能出现上涨
3. **数据可得性**：1个月时间窗口便于统计分析
4. **交易成本**：持有时间适中，交易成本可控

## 输出文件

### 数据文件

| 文件名 | 说明 |
|--------|------|
| `realtime_a_YYYYMMDD.csv` | A股实时行情 |
| `realtime_hk_YYYYMMDD.csv` | 港股实时行情 |
| `dividend_a.csv` | A股分红数据 |
| `dividend_hk.csv` | 港股分红数据 |
| `dividend_strategy_results.csv` | 分红策略分析结果 |
| `high_dividend_stocks.csv` | 高股息股票列表 |

### 图表文件

| 文件名 | 说明 |
|--------|------|
| `dividend_analysis_distribution.png` | 收益率分布图 |
| `dividend_analysis_timeseries.png` | 时间序列分析图 |
| `dividend_analysis_yearly.png` | 年度分析图 |
| `dividend_analysis_yield.png` | 股息率分析图 |
| `dividend_analysis_comparison.png` | 股票对比图 |

## 注意事项

### 数据使用声明

⚠️ **重要提示**：
- akshare数据仅供学术研究用途，不构成任何投资建议
- 过去的盈利概率不代表未来表现
- 实际交易需要考虑佣金、印花税等成本
- 市场风险会影响策略效果

### 请求限制

- 批量获取时建议添加延迟，避免被限流
- 建议每次请求间隔0.5秒以上
- 如遇请求失败会自动重试3次

### 数据完整性

- 部分历史分红数据可能缺失
- 港股分红金额通常以港币计价
- 注意区分年度分红、中期分红、特别分红

### 版本要求

- Python 3.8+
- akshare 最新版
- pandas 2.0+

## 常见问题

### Q1: 安装akshare失败怎么办？

**A**: 尝试使用国内镜像源：
```bash
pip install akshare -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q2: 请求超时怎么解决？

**A**: 在配置文件中增加超时时间：
```yaml
fetch:
  timeout: 60
```

### Q3: 数据获取为空？

**A**: 检查股票代码格式是否正确：
- A股：6位数字，如 `600519`
- 港股：4-5位数字，如 `00700`

### Q4: 如何分析更多股票？

**A**: 修改代码中的默认股票池，或直接传入股票列表：
```bash
python main.py analyze --codes 600519,000858,600036,601318,600887
```

### Q5: 图表显示中文乱码？

**A**: 系统需要安装中文字体，Linux系统可以安装：
```bash
sudo apt-get install fonts-wqy-microhei
```

## 项目结构

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
├── analysis/
│   ├── __init__.py
│   ├── dividend_strategy.py  # 分红策略分析
│   └── visualizer.py        # 可视化模块
├── data/                     # 数据存储目录
├── output/                   # 图表输出目录
├── cache/                    # 缓存目录
├── main.py                   # 主程序入口
├── requirements.txt          # 依赖列表
└── README.md               # 使用说明
```

## 扩展开发

### 添加新的数据源

在 `core/data_fetcher.py` 中添加新方法：

```python
def fetch_new_data(self, symbol: str):
    """获取新数据源的示例"""
    try:
        df = ak.new_data_api(symbol)
        return df
    except Exception as e:
        self.logger.error(f"获取数据失败: {e}")
        return None
```

### 添加新的分析指标

在 `analysis/dividend_strategy.py` 中添加新方法：

```python
def calculate_sharpe_ratio(self, result_df):
    """计算夏普比率"""
    # 实现代码
    pass
```

### 自定义图表

在 `analysis/visualizer.py` 中添加新方法：

```python
def plot_custom_chart(self, result_df, save_path):
    """自定义图表"""
    # 实现代码
    pass
```

## 联系方式

如有问题或建议，请提交Issue或Pull Request。

## 许可证

本项目采用 Apache License 2.0 许可证。

---

**免责声明**：本项目仅供学习和研究使用，不构成任何投资建议。股票投资有风险，入市需谨慎！
