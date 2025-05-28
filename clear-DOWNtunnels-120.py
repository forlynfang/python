import time
from datetime import datetime

def clear_txt_file(file_path):
    """清空指定txt文件内容"""
    with open(file_path, 'w') as f:
        f.write('')
    print(f"{datetime.now()} - 已清空文件: {file_path}")

def schedule_clear(file_path, interval_seconds):
    """定期清空文件"""
    while True:
        clear_txt_file(file_path)
        time.sleep(interval_seconds)

# 使用示例
schedule_clear('DOWNtunnels.txt', 120)  # 每天清空一次(86400秒=24小时)