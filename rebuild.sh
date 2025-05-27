#!/bin/bash

# 清理旧的构建文件
rm -rf .deps build/ dist/ && find . -type d -name "__pycache__" -exec rm -r {} + && find . -type f -name "*.pyc" -delete

#编译完整的代码，包含c++
#首先要确保nvcc能够访问，nvcc 可能没有设置到环境变量上
export PATH=/usr/local/cuda/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH


#只编译python相关代码，不包含c++
export VLLM_USE_PRECOMPILED=1 && pip install build && python -m build -v
