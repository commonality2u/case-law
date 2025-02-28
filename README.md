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
- [ ] id->文档信息，文档内容
- [ ] get court case和legislation的统计信息 @FRAN
- [ ] query->1.搜索结果列表，包含基本信息，答案统计信息
- [ ] 补全改错
      
**Deploy**
- [ ] google cloud compute engine
- [ ] 数据上传
- [ ] 后端部署
- [ ] 前端部署


**Frontend** @ZYN @QMY
- [ ] 导航页跳转 @YANG
- [ ] 显示总共多少，新增多少 @FRAN
- [ ] 查询补全 @YANG
- [ ] 查询纠错 @YANG

基础搜索 
- [ ] 案例，法条选择  
- [ ] 检索结果展示 @ZZY
- [ ] 可视化（时间分布，法院占比） @ZZY
- [ ] 筛选条件
- [ ] 高亮词

**数据收集** @FRAN
- [X] 主数据案例收集 https://huggingface.co/datasets/isaacus/open-australian-legal-corpus 
- [X] 数据清理 生成两个表，court case和legislation
- [ ] 定时新数据收集，数据库更新，触发索引 https://github.com/isaacus-dev/open-australian-legal-corpus-creator?tab=readme-ov-file 

**索引** @ZZY
- [X] 分别建立立法和案例的索引，FST提效，delta，vbyte降本
- [ ] 增量索引

**搜索**
- [ ] 处理布尔搜索，词组搜索，临近搜索
- [ ] 查询合并优化

**排序**
- [ ] 对于court case和legislation调整的BM25
- [ ] Bert对前100文档的精排

**Evaluations**


**不紧急功能** 

AI搜索 

根据输入的query，召回相关case和legislation @ZZY
- [ ] 增强deep seek r1 生成相关回答 @YANG



# Architecture Diagram
<img width="1043" alt="image" src="https://github.com/user-attachments/assets/9a774a9c-b595-4884-918f-e2c73ea5ab51" />

# Getting Started






