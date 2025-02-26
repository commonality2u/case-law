# Introduction
This project implements a complete law case&legislation search engine 

Provides a fashion front-end and robust backend contains 1.Live data collection, 2.Indexing, 3.Searching, and ranking 4. Advanced features


**原型预览**：https://www.figma.com/proto/hAXuY8WXL92nn0n783u4GP/TTDS-Prototype?node-id=0-1&t=sKFbeQVN8FmQyz9h-1 

**项目设计**：https://docs.google.com/document/d/1iR4dWmn3iGjx4eRBEfEKTltBKUH3y0mSwQlzFSzifXU/edit?usp=sharing

# Roadmap
**Frontend** @ZYN @QMY
- [ ] 显示总共多少，新增多少 @FRAN
- [ ] 查询补全 @YANG
- [ ] 查询纠错 @YANG

基础搜索 
- [ ] UI
- [ ] 搜案例，搜法条 
- [ ] 检索结果展示 @ZZY
- [ ] 可视化（时间分布，法院占比） @ZZY
- [ ] 筛选条件
- [ ] 高亮词
      

AI搜索
- [ ] 根据输入的query，召回相关case和legislation @ZZY
- [ ] 增强deep seek r1 生成相关回答 @YANG


**DBMS**
- [ ] mongodb(原始文件)，FAISS（向量数据库）
- [ ] Mongodb，1.id->文档内容 2.返回总共多少，新增多少 @FRAN
- [ ] FAISS，1.query的vector->相似的向量 @ZZY

**数据收集** @FRAN
- [X] 主数据案例收集 https://huggingface.co/datasets/isaacus/open-australian-legal-corpus 
- [X] 分开不同类型，两个表 立法，和案例
- [X] 数据缺的，缺时间的，删
- [X] 标准格式  id,citation,text,（ juris..）

- [ ] 新数据收集 https://github.com/isaacus-dev/open-australian-legal-corpus-creator?tab=readme-ov-file 

**索引** @ZZY
- [X] 建立立法和案例的索引
- [X] FST
- [X] delta 
- [X] vbyte
- [ ] 处理更新
- [ ] 并行提速

- [ ] 分割成chunks，生成embedding，存入FAISS，

**搜索**
- [ ] query处理为token
- [ ] 处理布尔搜索和词组搜索
- [ ] 查询合并优化
- [ ] 返回未排序文档列表

**排序**
- [ ] 采用混排策略，BM25
- [ ] （bert精排）
- [ ] 返回排序好的文档

**Evaluations**
- [ ] 设计测试用例（多AND查询）
- [ ] 测试写评估


# News
&bull;[01/27] A basic demo of 30 points CW search engine，contains a frontend and backend work on the tutorial dataset.
&bull;[02/26] A prototype updated.


# Architecture Diagram
<img width="1043" alt="image" src="https://github.com/user-attachments/assets/9a774a9c-b595-4884-918f-e2c73ea5ab51" />

# Getting Started






