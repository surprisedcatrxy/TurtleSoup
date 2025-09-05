# 提示
这是一个正在编纂的demo,目前采取本地qwen3:8b模型，并且需要思考模式才能正确回答，正在完善中  
# Todo
1.模型响应速度优化  

2.修复无法正确识别“是也不是”的情况  

3.实现文件读取，向量识别，rag检索从而实现在海龟汤数据中得到正确汤面

4.实现界面    

# 项目介绍
基于本地思考模型和agent,MCP等实现海龟汤游戏，AI扮演主持人  
# 部署指南
1.下载ollama,执行  
`ollama pull qwen3:8b`  
2.安装依赖，对于visual studio,单击python环境，选择一个python版本，右键选择从requirements.txt安装;对于其他，采取`pip -r install requirements.txt`