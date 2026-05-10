#!/bin/bash
# 克隆仓库脚本

echo "=================================="
echo "克隆股票分析项目到本地"
echo "=================================="

# 设置克隆目标目录
TARGET_DIR="$HOME/stock_project"

# 如果目录已存在，先备份
if [ -d "$TARGET_DIR" ]; then
    echo "备份旧目录..."
    mv "$TARGET_DIR" "${TARGET_DIR}_backup_$(date +%Y%m%d_%H%M%S)"
fi

# 克隆仓库
echo "正在克隆仓库..."
git clone https://github.com/luolanfeixue/chatpai.git "$TARGET_DIR"

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ 克隆成功！"
    echo ""
    echo "项目位置: $TARGET_DIR"
    echo ""
    echo "=================================="
    echo "运行分析"
    echo "=================================="
    
    cd "$TARGET_DIR/stock_data_collector"
    
    # 安装依赖
    echo ""
    echo "正在安装依赖..."
    pip install -r requirements.txt
    
    # 运行全市场分析
    echo ""
    echo "正在运行全市场分红策略分析..."
    echo "（这可能需要较长时间，请耐心等待）"
    echo ""
    
    python full_market_analysis_v2.py
    
    echo ""
    echo "=================================="
    echo "分析完成！"
    echo "=================================="
    echo ""
    echo "结果文件保存在: $TARGET_DIR/stock_data_collector/data/"
    echo ""
else
    echo ""
    echo "❌ 克隆失败！"
    echo ""
fi
