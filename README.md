# 介绍
基于langchain和chatglm搭建自己的聊天机器人，并用tair存储私有数据，为私有数据构建索引。运行本项目前需要确保GPU驱动已经安装，如果没有GPU，需要修改代码使用CPU加载。
CPU机器内存要求参考[chatglm](https://github.com/THUDM/ChatGLM-6B)。

# 环境
* python >= 3.10(最好是3.10.10)

运行以下命令安装本项目所需的第三方库
```angular2html
pip install -r requirementes.txt
```

# 启动
```angular2html
nohup python api_fastapi.py --allow-root 2>&1 &
```

# 其他
提供了jupyter notebook：chatbot.ipynb


