"""
数据库配置模块
"""
import sqlite3
import os
from pathlib import Path


class DatabaseConfig:
    """数据库配置类"""
    
    def __init__(self, db_type='sqlite', **kwargs):
        self.db_type = db_type
        self.config = kwargs
        
    def get_connection(self):
        """获取数据库连接"""
        if self.db_type == 'sqlite':
            db_path = self.config.get('path', 'stock_data.db')
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row
            return conn
        elif self.db_type == 'mysql':
            import pymysql
            return pymysql.connect(
                host=self.config.get('host', 'localhost'),
                port=self.config.get('port', 3306),
                user=self.config.get('username', 'root'),
                password=self.config.get('password', ''),
                database=self.config.get('database', 'stock_data'),
                charset='utf8mb4'
            )
        else:
            raise ValueError(f"不支持的数据库类型: {self.db_type}")
    
    def init_database(self):
        """初始化数据库表"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # A股分红数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS a_share_dividend (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_code VARCHAR(10) NOT NULL,
                stock_name VARCHAR(50),
                dividend_year VARCHAR(10),
                per_share_dividend DECIMAL(10,4),
                ex_right_date DATE,
                record_date DATE,
                payment_date DATE,
                total_dividend DECIMAL(20,4),
                dividend_type VARCHAR(20),
                report_period VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 港股分红数据表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hk_stock_dividend (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_code VARCHAR(10) NOT NULL,
                stock_name VARCHAR(50),
                announcement_date DATE,
                fiscal_year VARCHAR(10),
                dividend_plan TEXT,
                allocation_type VARCHAR(20),
                ex_right_date DATE,
                transfer_deadline DATE,
                payment_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 分红策略分析结果表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dividend_strategy_result (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_code VARCHAR(10) NOT NULL,
                stock_name VARCHAR(50),
                dividend_date DATE,
                price_before DECIMAL(10,4),
                price_at_dividend DECIMAL(10,4),
                price_change DECIMAL(10,4),
                price_change_pct DECIMAL(10,4),
                dividend_per_share DECIMAL(10,4),
                dividend_yield DECIMAL(10,4),
                total_return DECIMAL(10,4),
                is_profitable INTEGER,
                holding_days INTEGER,
                dividend_type VARCHAR(20),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # 股票实时行情表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_realtime (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                stock_code VARCHAR(10) NOT NULL,
                stock_name VARCHAR(50),
                market VARCHAR(10),
                price DECIMAL(10,4),
                change DECIMAL(10,4),
                change_pct DECIMAL(10,4),
                volume BIGINT,
                amount DECIMAL(20,4),
                open DECIMAL(10,4),
                high DECIMAL(10,4),
                low DECIMAL(10,4),
                close DECIMAL(10,4),
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(stock_code, update_time)
            )
        ''')
        
        conn.commit()
        cursor.close()
        conn.close()
        print("数据库初始化完成")
