"""
数据验证工具模块
"""
import re
from datetime import datetime


class StockValidator:
    """股票代码和数据验证器"""
    
    # A股股票代码正则表达式
    A_STOCK_PATTERN = re.compile(r'^[0-9]{6}$')
    # 港股股票代码正则表达式
    HK_STOCK_PATTERN = re.compile(r'^[0-9]{4,5}$')
    # 美股股票代码正则表达式
    US_STOCK_PATTERN = re.compile(r'^[A-Z]{1,5}$')
    
    @classmethod
    def validate_a_stock_code(cls, code):
        """
        验证A股股票代码
        
        Args:
            code: 股票代码
        
        Returns:
            bool: 是否有效
        """
        if not code:
            return False
        code = str(code).strip()
        return bool(cls.A_STOCK_PATTERN.match(code))
    
    @classmethod
    def validate_hk_stock_code(cls, code):
        """
        验证港股股票代码
        
        Args:
            code: 股票代码
        
        Returns:
            bool: 是否有效
        """
        if not code:
            return False
        code = str(code).strip()
        return bool(cls.HK_STOCK_PATTERN.match(code))
    
    @classmethod
    def validate_us_stock_code(cls, code):
        """
        验证美股股票代码
        
        Args:
            code: 股票代码
        
        Returns:
            bool: 是否有效
        """
        if not code:
            return False
        code = str(code).strip().upper()
        return bool(cls.US_STOCK_PATTERN.match(code))
    
    @classmethod
    def validate_stock_code(cls, code, market='a'):
        """
        验证股票代码
        
        Args:
            code: 股票代码
            market: 市场类型 ('a', 'hk', 'us')
        
        Returns:
            bool: 是否有效
        """
        if market == 'a':
            return cls.validate_a_stock_code(code)
        elif market == 'hk':
            return cls.validate_hk_stock_code(code)
        elif market == 'us':
            return cls.validate_us_stock_code(code)
        return False
    
    @staticmethod
    def validate_date(date_str, format='%Y-%m-%d'):
        """
        验证日期格式
        
        Args:
            date_str: 日期字符串
            format: 日期格式
        
        Returns:
            bool: 是否有效
        """
        try:
            datetime.strptime(date_str, format)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_date_range(start_date, end_date):
        """
        验证日期范围
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
        
        Returns:
            bool: 是否有效
        """
        try:
            if isinstance(start_date, str):
                start = datetime.strptime(start_date, '%Y-%m-%d')
            else:
                start = start_date
            
            if isinstance(end_date, str):
                end = datetime.strptime(end_date, '%Y-%m-%d')
            else:
                end = end_date
            
            return start <= end
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_price(price):
        """
        验证价格数据
        
        Args:
            price: 价格值
        
        Returns:
            bool: 是否有效
        """
        try:
            price = float(price)
            return price > 0
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_percentage(pct):
        """
        验证百分比数据
        
        Args:
            pct: 百分比值
        
        Returns:
            bool: 是否有效
        """
        try:
            pct = float(pct)
            return -100 <= pct <= 1000
        except (ValueError, TypeError):
            return False
    
    @classmethod
    def validate_stock_codes(cls, codes, market='a'):
        """
        批量验证股票代码
        
        Args:
            codes: 股票代码列表
            market: 市场类型
        
        Returns:
            tuple: (有效代码列表, 无效代码列表)
        """
        if isinstance(codes, str):
            codes = [c.strip() for c in codes.split(',')]
        
        valid_codes = []
        invalid_codes = []
        
        for code in codes:
            if cls.validate_stock_code(code, market):
                valid_codes.append(code)
            else:
                invalid_codes.append(code)
        
        return valid_codes, invalid_codes
    
    @staticmethod
    def sanitize_stock_code(code):
        """
        清理股票代码
        
        Args:
            code: 股票代码
        
        Returns:
            str: 清理后的代码
        """
        if not code:
            return None
        return str(code).strip().zfill(6)
    
    @staticmethod
    def normalize_market(market):
        """
        标准化市场类型
        
        Args:
            market: 市场标识
        
        Returns:
            str: 标准化的市场类型
        """
        market_map = {
            'a': 'a',
            'A股': 'a',
            'china': 'a',
            'sh': 'a',
            'sz': 'a',
            'hk': 'hk',
            '港股': 'hk',
            'hongkong': 'hk',
            'us': 'us',
            '美股': 'us',
            'america': 'us'
        }
        return market_map.get(str(market).lower().strip(), 'a')
