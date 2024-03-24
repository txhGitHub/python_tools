import os

def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        for file in files:
            print(os.path.join(root, file))

# 用法示例
list_files(r'C:\Users\pc\Desktop\test_log')