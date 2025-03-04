# Introduction
This project implements a complete law case&legislation search engine 

Provides a fashion front-end and robust backend contains 1.Live data collection, 2.Indexing, 3.Searching, and ranking 4. Advanced features


**原型预览**：https://www.figma.com/proto/hAXuY8WXL92nn0n783u4GP/TTDS-Prototype?node-id=0-1&t=sKFbeQVN8FmQyz9h-1 

**需求思考**：https://docs.google.com/document/d/1iR4dWmn3iGjx4eRBEfEKTltBKUH3y0mSwQlzFSzifXU/edit?usp=sharing

# News
&bull;[01/27] A basic demo of 30 points CW search engine，contains a frontend and backend work on the tutorial dataset. 

&bull;[02/26] A prototype updated.

# Roadmap

**API**
- [ ] get court case和legislation的统计信息 @FRAN
- [x] id,collection>文档信息，文档内容
- [x] query+...->1.搜索结果, 分页信息，统计信息。
- [ ] 补全改错
      
**Deploy**
- [ ] google cloud compute engine
- [ ] 数据上传
- [ ] 后端部署
- [ ] 前端部署


**Frontend** @ZYN @QMY
- [ ] 显示总共多少，新增多少 @FRAN

- [ ] 查询补全 @YANG
- [ ] 查询纠错 @YANG

基础搜索 
- [x] 案例，法条选择  
- [x] 检索结果展示 @ZZY
- [x] 可视化（时间分布，法院占比） @ZZY
- [x] 筛选条件（时间，source）可拓展
- [x] 分页


**数据收集** @FRAN
- [X] 主数据案例收集9GB https://huggingface.co/datasets/isaacus/open-australian-legal-corpus 
- [X] 数据清理 court case和legislation存入MongoDB，调整顺序，并行批量存入
- [ ] 定时，爬取额外的新数据，生成增量文档，存入数据库，触发索引重建call

**索引** @ZZY
- [X] 分别建立立法和案例的索引，FST提效，delta，vbyte降本，统计词序

**搜索**
- [x] 处理布尔搜索，词组搜索，临近搜索
- [x] 查询合并优化，交集加速

**排序**
- [ ] 对于court case和legislation调整不同的BM25参数
- [ ] 不同词性的词有不同的权重

优化 
小字典优化bm25

**Evaluations**


**不紧急功能** 

AI搜索 

根据输入的query，召回相关case和legislation @ZZY
- [ ] 增强deep seek r1 生成相关回答 @YANG



# Architecture Diagram
<img width="1043" alt="image" src="https://github.com/user-attachments/assets/9a774a9c-b595-4884-918f-e2c73ea5ab51" />

# Getting Started






