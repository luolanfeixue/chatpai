"""
股票数据获取与分红策略分析系统
主程序入口
"""
import sys
import os
import argparse
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.settings import Settings
from config.database import DatabaseConfig
from core.data_fetcher import DataFetcher
from core.data_processor import DataProcessor
from core.data_storage import DataStorage
from analysis.dividend_strategy import DividendStrategyAnalyzer
from analysis.visualizer import DividendVisualizer
from scheduler.task_scheduler import TaskScheduler
from utils.logger import setup_logger, get_logger

warnings.filterwarnings('ignore')


class StockDataCollectorApp:
    """股票数据获取与分红策略分析应用"""
    
    def __init__(self, config_file=None):
        self.settings = Settings(config_file)
        setup_logger(
            name='stock_collector',
            level=self.settings.get('log', 'level'),
            log_file=self.settings.get('log', 'file')
        )
        self.logger = get_logger()
        
        self.fetcher = DataFetcher(
            retry_times=self.settings.get('fetch', 'retry_times'),
            timeout=self.settings.get('fetch', 'timeout')
        )
        self.processor = DataProcessor()
        self.storage = DataStorage()
        self.visualizer = DividendVisualizer()
    
    def fetch_realtime_data(self, market='a', codes=None):
        """获取实时行情数据"""
        try:
            self.logger.info(f"开始获取 {market} 市场实时数据...")
            
            if codes:
                df = self.fetcher.fetch_stock_by_codes(codes, market)
            elif market == 'a':
                df = self.fetcher.fetch_a_stock_spot()
            elif market == 'hk':
                df = self.fetcher.fetch_hk_stock_spot()
            else:
                self.logger.error(f"不支持的市场类型: {market}")
                return
            
            if df is not None and not df.empty:
                self.storage.save_realtime_data(df, market)
                print(f"\n成功获取 {len(df)} 条数据")
                print(df.head(10))
            else:
                self.logger.warning("没有获取到数据")
                
        except Exception as e:
            self.logger.error(f"获取实时数据失败: {e}")
    
    def fetch_dividend_data(self, codes, market='a'):
        """获取分红数据"""
        try:
            if isinstance(codes, str):
                codes = [c.strip() for c in codes.split(',')]
            
            self.logger.info(f"开始获取 {len(codes)} 只股票的分红数据...")
            
            df = self.fetcher.fetch_dividend_batch(codes, market)
            
            if df is not None and not df.empty:
                self.storage.save_dividend_data(df, market)
                print(f"\n成功获取 {len(df)} 条分红数据")
                print(df.head(10))
            else:
                self.logger.warning("没有获取到分红数据")
                
        except Exception as e:
            self.logger.error(f"获取分红数据失败: {e}")
    
    def analyze_dividend_strategy(self, codes=None, market='a', lookback_days=30,
                               generate_charts=True, save_results=True):
        """分析分红策略"""
        try:
            if codes:
                if isinstance(codes, str):
                    codes = [c.strip() for c in codes.split(',')]
            else:
                codes = ['600519', '000858', '600036', '000651']
            
            self.logger.info(f"开始分红策略分析，持有期: {lookback_days} 天")
            
            analyzer = DividendStrategyAnalyzer(lookback_days=lookback_days)
            result_df, analysis_results = analyzer.run_full_analysis(codes, market)
            
            if result_df is not None and not result_df.empty:
                if save_results:
                    self.storage.save_dividend_strategy_result(result_df)
                    print(f"\n分析结果已保存")
                
                if generate_charts:
                    self.logger.info("生成可视化图表...")
                    saved_files = self.visualizer.generate_full_report(result_df)
                    print(f"已生成 {len(saved_files)} 个图表文件")
                
                print(f"\n分析完成，共 {len(result_df)} 条记录")
                print(result_df.head(10))
                
                return result_df, analysis_results
            else:
                self.logger.warning("分析没有返回有效结果")
                return None, {}
                
        except Exception as e:
            self.logger.error(f"分红策略分析失败: {e}")
            return None, {}
    
    def init_database(self):
        """初始化数据库"""
        try:
            db_config = DatabaseConfig()
            db_config.init_database()
            self.logger.info("数据库初始化完成")
        except Exception as e:
            self.logger.error(f"数据库初始化失败: {e}")
    
    def run_scheduler(self, task_type='realtime', interval=60):
        """运行定时任务"""
        try:
            scheduler = TaskScheduler()
            
            if task_type == 'realtime':
                scheduler.add_job(
                    lambda: self.fetch_realtime_data('a'),
                    interval,
                    'realtime_fetch'
                )
            elif task_type == 'dividend':
                codes = ['600519', '000858', '600036']
                scheduler.add_job(
                    lambda: self.fetch_dividend_data(codes, 'a'),
                    interval * 60,
                    'dividend_fetch'
                )
            
            self.logger.info(f"定时任务已启动，间隔: {interval} 秒")
            scheduler.start()
            
        except Exception as e:
            self.logger.error(f"定时任务运行失败: {e}")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='股票数据获取与分红策略分析系统',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  # 获取A股实时行情
  python main.py fetch --market a

  # 获取指定股票实时行情
  python main.py fetch --market a --codes 600519,000858

  # 获取港股实时行情
  python main.py fetch --market hk

  # 获取股票分红数据
  python main.py dividend --codes 600519,000858

  # 分析分红策略（默认30天持有期）
  python main.py analyze --codes 600519,000858

  # 分析分红策略（自定义持有期）
  python main.py analyze --codes 600519,000858 --days 60

  # 获取高股息股票
  python main.py high-dividend --top 50

  # 初始化数据库
  python main.py init-db

  # 启动定时任务
  python main.py schedule --task realtime --interval 60
        """
    )
    
    parser.add_argument('command', nargs='?', choices=[
        'fetch', 'dividend', 'analyze', 'high-dividend', 'init-db', 'schedule'
    ], help='命令类型')
    
    parser.add_argument('--market', '-m', default='a', choices=['a', 'hk'],
                       help='市场类型 (默认: a)')
    
    parser.add_argument('--codes', '-c', type=str,
                       help='股票代码，多个用逗号分隔')
    
    parser.add_argument('--days', '-d', type=int, default=30,
                       help='分红前持有天数 (默认: 30)')
    
    parser.add_argument('--top', '-t', type=int, default=50,
                       help='返回前N条 (默认: 50)')
    
    parser.add_argument('--task', default='realtime', choices=['realtime', 'dividend'],
                       help='定时任务类型 (默认: realtime)')
    
    parser.add_argument('--interval', '-i', type=int, default=60,
                       help='定时任务间隔秒数 (默认: 60)')
    
    parser.add_argument('--no-chart', action='store_true',
                       help='不生成图表')
    
    parser.add_argument('--no-save', action='store_true',
                       help='不保存结果')
    
    parser.add_argument('--config', type=str,
                       help='配置文件路径')
    
    args = parser.parse_args()
    
    app = StockDataCollectorApp(args.config)
    
    if args.command is None:
        parser.print_help()
        return
    
    try:
        if args.command == 'fetch':
            app.fetch_realtime_data(args.market, args.codes)
        
        elif args.command == 'dividend':
            if not args.codes:
                print("错误: 获取分红数据需要指定 --codes 参数")
                return
            app.fetch_dividend_data(args.codes, args.market)
        
        elif args.command == 'analyze':
            app.analyze_dividend_strategy(
                codes=args.codes,
                market=args.market,
                lookback_days=args.days,
                generate_charts=not args.no_chart,
                save_results=not args.no_save
            )
        
        elif args.command == 'high-dividend':
            df = app.fetcher.fetch_high_dividend_stocks(args.top)
            if df is not None and not df.empty:
                app.storage.save_to_csv(df, 'high_dividend_stocks.csv')
                print(f"\n成功获取 {len(df)} 只高股息率股票")
                print(df.head(20))
        
        elif args.command == 'init-db':
            app.init_database()
        
        elif args.command == 'schedule':
            app.run_scheduler(args.task, args.interval)
    
    except KeyboardInterrupt:
        print("\n用户中断操作")
    except Exception as e:
        print(f"执行失败: {e}")
        app.logger.error(f"执行失败: {e}", exc_info=True)


if __name__ == '__main__':
    main()
