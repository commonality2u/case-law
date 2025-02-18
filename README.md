# Introduction
This project implements a complete case law search engine 

Provides comprehensive backend support for data collection, indexing, searching, and ranking, along with an innovative frontend.

**项目设计**：https://docs.google.com/document/d/1iR4dWmn3iGjx4eRBEfEKTltBKUH3y0mSwQlzFSzifXU/edit?usp=sharing

# Roadmap
**Frontend** @ZYN @QMY

- [ ] 搜索框
- [ ] 显示总共多少，新增多少 @FRAN
- [ ] 查询补全 @YANG
- [ ] 查询纠错 @YANG

基础搜索 
- [ ] 搜案例，搜法条 
- [ ] 检索结果展示，时间轴 @ZZY
- [ ] 可视化，时间分布，法院占比 @ZZY
- [ ] 筛选条件
- [ ] 按相关性排序，按时间排序
- [ ] 高亮词
- [ ] AI总结 @ZZY

AI搜索
- [ ] 根据输入的query，召回10个相关案例 @ZZY
- [ ] 增强deep seek r1 生成可能判的罪，以及怎么判 @YANG


**DBMS**
- [ ] mongodb(原始文件), RocksDB(倒排索引)，FAISS（向量数据库）
- [ ] Mongodb，1.id->文档内容 2.返回总共多少，新增多少@ FRAN
- [ ] RocksDB，2.token->索引 @ZZY
- [ ] FAISS，1.query的vector->相似的向量 @ZZY

**数据收集** @FRAN
- [ ] 主数据案例收集 https://huggingface.co/datasets/isaacus/open-australian-legal-corpus 
- [ ] 分开不同类型，分成多个表 立法，和案例
- [ ] 数据缺的，缺时间的，删
- [ ] 标准格式  id,citation,text,（ juris..）

- [ ] 新数据收集 https://github.com/isaacus-dev/open-australian-legal-corpus-creator?tab=readme-ov-file 

**索引** @ZZY
- [ ] 建立倒排索引存入RocksDB
- [ ] 优化，跳表，
- [ ] 分割成chunks，生成embedding，存入FAISS，

**搜索**
- [ ] query处理为token
- [ ] 处理三类查询，高级搜索
- [ ] 返回未排序文档

**排序**
- [ ] 采用混排策略，融合BM25和vector相关性
- [ ] 返回排序好的文档

**Evaluations**
- [ ] 设计案例
- [ ] 测试写评估


# News
&bull;[01/27] A basic demo of 30 points CW search engine，contains a frontend and backend work on the tutorial dataset.

# Architecture Diagram
<img width="1043" alt="image" src="https://github.com/user-attachments/assets/9a774a9c-b595-4884-918f-e2c73ea5ab51" />

# Getting Started






