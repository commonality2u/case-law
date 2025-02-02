# TTDS_CW3
This project implements a case law search engine 
search engine,start from

# Roadmap

**Data collection**
- [ ] 结构化现有数据集（主来源）https://huggingface.co/datasets/isaacus/open-australian-legal-corpus 
- [ ] 爬取并结构化每天定时更新新的判决（增量）https://github.com/isaacus-dev/open-australian-legal-corpus-creator?tab=readme-ov-file 
- [ ] 以 id,title,text,（time...）作为标准格式，存入mongodb

**Backend**
- [ ] 引入MongoDB取代文件，以标准格式改造使用
- [ ] 后端解耦 为索引（倒排，向量），搜索，排序
      
索引
- [ ] 索引优化（增量编码） 支持rocksdb
- [ ] 支持增量索引重建
- [ ] 向量化处理

检索
- [ ] 统一处理query，识别各检索类型并调用
- [ ] 返回未排序检索结果list

排序
- [ ] 采用混排策略，BM25作为初步召回
- [ ] 对Top100执行向量化搜索计算语义匹配得分

**Frontend**
- [ ] 熟悉feature在搜索框中的组件实现
- [ ] 高亮搜索词
- [ ] 尝试gpt-like对话框
- [ ] 动画探索

**Features**
- [ ] 处理自然语言query，增加意图分析
- [ ] 自动补全（auto complete）
- [ ] 自动纠错（auto correction）
- [ ] 同义词转化

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





