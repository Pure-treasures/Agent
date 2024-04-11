# Agent
本文档包括：环境准备、启动说明、测试说明。

# Env Prepare:
```bash
# 创建虚拟环境
python -m venv agent
or
conda create --name agent python=3.9
# 激活虚拟环境
source /agent/bin/activate
or 
conda activate agent 
# 更新虚拟环境中的pip包
pip install --upgrade pip
# 在虚拟环境中安装poetry
pip install poetry
# 通过poetry进行依赖包安装
poetry install --with agent,test --no-cache
```

# Start Spec:
```bash
python -m server # 等待服务启动完成，进入swagger页面：http://localhost:8000/docs
```

# Test Spec
```bash
# 执行'pytest'命令，运行所有测试脚本
pytest
# 运行'某个'测试脚本
pytest {script_name}
# '-s'参数，输出print日志
pytest -s {script_name}
# 执行指定py文件中的指定测试函数
pytest -k {test_func} {test_file.py}
```