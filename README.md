# TTDS_CW3
This is a coursework project of course TTDS, implement a search engine, which support boolean search, phrase search and proximity search 

Data collection
1.处理现有数据集（大量）https://huggingface.co/datasets/isaacus/open-australian-legal-corpus
2.处理每天定时更新新的判决（少）https://github.com/isaacus-dev/open-australian-legal-corpus-creator?tab=readme-ov-file
3.存入mongodb
4.格式 id,title,text,time...


前端
1.熟悉feature组件实现
2.高亮搜索词
3.尝试对话框


# Demo 
Click this link to quickly view the deployed project：
https://b07c-192-41-114-227.ngrok-free.app

# News
&bull;[01/27] A basic demo of 30 points CW search engine，contains a frontend and backend work on the tutorial dataset.

# Architecture Diagram
<img width="1043" alt="image" src="https://github.com/user-attachments/assets/9a774a9c-b595-4884-918f-e2c73ea5ab51" />

# Getting Started
1. Install python, flask, streamlit
2. ```python backend.py```
to run backend  
3. ```streamlit run frontend.py```
to run fronend

# Roadmap
@Zzy
- [ ] 后端解耦为独立模块
- [ ] 引入MongoDB取代文件
- [ ] 向量相似度排序 feature



