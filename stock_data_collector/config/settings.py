"""
配置管理模块
"""
import os
from pathlib import Path
import yaml


class Settings:
    """系统配置类"""
    
    def __init__(self, config_file=None):
        self.base_dir = Path(__file__).resolve().parent.parent
        self.config_file = config_file or self.base_dir / 'config.yaml'
        self.config = self._load_config()
        
    def _load_config(self):
        """加载配置文件"""
        default_config = {
            'database': {
                'type': 'sqlite',
                'path': 'stock_data.db'
            },
            'fetch': {
                'retry_times': 3,
                'timeout': 30,
                'interval': 60
            },
            'markets': {
                'a_share': True,
                'hk_stock': True,
                'hsgt_north': True,
                'hsgt_south': True,
                'dividend': True
            },
            'dividend_strategy': {
                'lookback_days': 30,
                'min_sample_size': 10,
                'min_dividend_yield': 3.0,
                'exclude_st': True,
                'exclude_new_stocks': True
            },
            'cache': {
                'enabled': True,
                'directory': 'cache',
                'expire_hours': 24
            },
            'log': {
                'level': 'INFO',
                'file': 'stock_collector.log',
                'max_bytes': 10485760,
                'backup_count': 5
            }
        }
        
        if self.config_file and os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    default_config.update(user_config)
        
        return default_config
    
    def get(self, section, key=None):
        """获取配置项"""
        if key:
            return self.config.get(section, {}).get(key)
        return self.config.get(section)
    
    def set(self, section, key, value):
        """设置配置项"""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value
    
    def save(self):
        """保存配置到文件"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            yaml.dump(self.config, f, allow_unicode=True, default_flow_style=False)


# 全局配置实例
settings = Settings()
