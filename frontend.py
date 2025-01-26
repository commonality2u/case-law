import streamlit as st
import requests
from streamlit_pills import pills

def make_request(url, error_message):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json() if response.headers.get("Content-Type") == "application/json" else response.text
        else:
            st.error(f"{error_message}: {response.status_code}")
            return None
    except Exception as e:
        st.error(f"{error_message}: {e}")
        return None

def search_backend(query, search_type, ranking_method):
    # 如果查询为空，直接返回None
    if not query or query.strip() == "":
        return None
    # 添加 k 参数到 URL
    k_param = f"&k={st.session_state['proximity_k']}" if search_type == "proximity" else ""
    # 确保传递 ranking 参数
    url = f"http://localhost:5001/search?query={query}&type={search_type}&ranking={ranking_method.lower()}{k_param}"
    
    return make_request(url, "后端搜索接口请求失败")

def get_document_content(doc_id):
    url = f"http://localhost:5001/document/{doc_id}"
    return make_request(url, "获取文档内容时出错")

def truncate_title(title, max_length=40):
    """截断标题到指定长度，并添加省略号"""
    return title[:max_length] + '...' if len(title) > max_length else title

# Streamlit 页面设置
st.set_page_config(layout="wide")

# 添加自定义 CSS
st.markdown("""
<style>
.doc-content-box {
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 20px;
    background-color: #f8f9fa;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    margin-top: 10px;
    height: 600px;
    overflow-y: auto;
    line-height: 1.6;
}

.search-result-item {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.5;
    max-height: 3em;
    padding: 8px;
    margin: 4px 0;
    border-radius: 4px;
    background-color: #f8f9fa;
}

.search-result-item:hover {
    background-color: #e9ecef;
    cursor: pointer;
}

/* 自定义单选按钮样式 */
div.st-cc {
    padding: 0 !important;
    gap: 0 !important;
}

div.st-cc > div {
    margin: 0 !important;
    padding: 0 !important;
}

.st-cc .st-bq {
    border: none !important;
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)

# 设置标题居中
st.markdown("<h1 style='text-align: center;'>TTDS Demo</h1>", unsafe_allow_html=True)

# 初始化 Session State
if "query_input" not in st.session_state:
    st.session_state["query_input"] = ""
if "search_type" not in st.session_state:
    st.session_state["search_type"] = "Boolean Search"
if "ranking_method" not in st.session_state:
    st.session_state["ranking_method"] = "TF-IDF"
if "search_results" not in st.session_state:
    st.session_state["search_results"] = None
if "selected_source" not in st.session_state:
    st.session_state["selected_source"] = "All"
if "selected_time" not in st.session_state:
    st.session_state["selected_time"] = "All"
if "current_page" not in st.session_state:
    st.session_state["current_page"] = 1

search_type_options = {
    "Boolean Search": "boolean",
    "Phrase Search": "phrase",
    "Proximity Search": "proximity"
}

ranking_options = {
    "TF-IDF": "tf-idf",
    "BM25": "bm25"
}

# 修改左右布局的比例
col1, col2, col3 = st.columns([2, 1, 1])

# 左侧搜索框
with col1:
    query = st.text_input(
        "请输入搜索关键词",
        value=st.session_state["query_input"],
        on_change=lambda: st.session_state.update(
            search_results=(
                search_backend(
                    st.session_state["query_input"], 
                    search_type_options[st.session_state["search_type"]],
                    ranking_options[st.session_state["ranking_method"]]
                ) if st.session_state["query_input"].strip() else None
            )
        ),
        key="query_input"
    )

# 中间搜索类型下拉框
with col2:
    selected_search_type = st.selectbox(
        "选择搜索类型",
        options=list(search_type_options.keys()),
        index=list(search_type_options.keys()).index(st.session_state["search_type"]),
        key="search_type",
        on_change=lambda: st.session_state.update(
            search_results=search_backend(
                st.session_state["query_input"], 
                search_type_options[st.session_state["search_type"]],
                ranking_options[st.session_state["ranking_method"]]
            )
        )
    )
    
    # 初始化 k 的 session state
    if "proximity_k" not in st.session_state:
        st.session_state["proximity_k"] = 5
    
    # 当选择 proximity search 时显示滑动条
    if selected_search_type == "Proximity Search":
        k = st.slider(
            "选择距离值",
            min_value=1,
            max_value=10,
            value=st.session_state["proximity_k"],
            step=1,
            help="设置两个词之间的最大距离",
            key="k_slider",
            on_change=lambda: st.session_state.update(
                proximity_k=st.session_state["k_slider"],
                search_results=search_backend(
                    st.session_state["query_input"], 
                    search_type_options[st.session_state["search_type"]],
                    ranking_options[st.session_state["ranking_method"]]
                ) if st.session_state["query_input"].strip() else None
            )
        )
    else:
        k = 5  # 默认值

# 右侧排序方式下拉框
with col3:
    selected_ranking = st.selectbox(
        "选择排序方式",
        options=list(ranking_options.keys()),
        index=list(ranking_options.keys()).index(st.session_state["ranking_method"]),
        key="ranking_method",
        on_change=lambda: st.session_state.update(
            search_results=search_backend(
                st.session_state["query_input"], 
                search_type_options[st.session_state["search_type"]],
                ranking_options[st.session_state["ranking_method"]]
            )
        )
    )

# 横向排列的 Pills 筛选器
col1, col2 = st.columns([3, 3])

with col1:
    # Time 筛选
    time_options = ["All", "April", "May"]
    selected_time = pills(
        label="Time",
        options=time_options,
        index=time_options.index(st.session_state["selected_time"]),
        key="time_pills"
    )
    
    if selected_time != st.session_state["selected_time"]:
        st.session_state["selected_time"] = selected_time
        if st.session_state.get("query_input"):
            st.session_state["search_results"] = search_backend(
                st.session_state["query_input"], 
                search_type_options[st.session_state["search_type"]],
                ranking_options[st.session_state["ranking_method"]]
            )

with col2:
    # Source 筛选
    sources = ["All", "FT"]
    selected_source = pills(
        label="Source",
        options=sources,
        index=sources.index(st.session_state["selected_source"]),
        key="source_pills"
    )
    
    if selected_source != st.session_state["selected_source"]:
        st.session_state["selected_source"] = selected_source
        if st.session_state.get("query_input"):
            st.session_state["search_results"] = search_backend(
                st.session_state["query_input"], 
                search_type_options[st.session_state["search_type"]],
                ranking_options[st.session_state["ranking_method"]]
            )

# 显示搜索结果
search_results = st.session_state.get("search_results")

# 检查搜索结果
if st.session_state["query_input"].strip():  # 如果有输入查询
    if search_results is None:  # 如果搜索结果为None
        st.warning("未找到有效结果。")
    elif "results" in search_results and isinstance(search_results["results"], list):
        def filter_time(date, selected_time):
            """
            根据时间筛选文件：
            - 'All' 保留所有文件；
            - 'April' 只保留 'April' 的文件；
            - 'May' 只保留 'May' 的文件。
            """
            if selected_time == "All":
                return True
            elif selected_time == "April":
                return "1991-04" in date  # 保留四月的文件
            elif selected_time == "May":
                return "1991-05" in date  # 保留五月的文件
            return False

        # 根据筛选条件过滤结果
        filtered_results = [
            result for result in search_results["results"]
            if (selected_source == "All" or result.get("source") == selected_source) and
               (selected_time == "All" or filter_time(result.get("date"), selected_time))
        ]

        if not filtered_results:  # 如果过滤后没有结果
            st.warning("根据当前筛选条件未找到结果。")
        else:
            # 分页设置
            items_per_page = 10  # 每页显示的结果数
            total_results = len(filtered_results)
            total_pages = (total_results + items_per_page - 1) // items_per_page
            
            # 确保当前页码有效
            if st.session_state["current_page"] > total_pages:
                st.session_state["current_page"] = 1
            
            # 计算当前页的结果
            start_idx = (st.session_state["current_page"] - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, total_results)
            current_page_results = filtered_results[start_idx:end_idx]
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.subheader(f"搜索结果 ({total_results} 条)")
                
                # 使用容器来显示搜索结果
                for result in current_page_results:
                    result_data = {
                        "doc_id": result.get("doc_id", ""),
                        "title": truncate_title(result.get("title", "未知标题")),
                        "source": result.get("source", "未知来源"),
                        "date": result.get("date", "未知日期"),
                    }
                    
                    # 创建可点击的容器
                    result_container = st.container()
                    with result_container:
                        if st.button(
                            f"{result_data['source']} ({result_data['date']})\n{result_data['title']}",
                            key=f"result_{result_data['doc_id']}",
                            use_container_width=True,
                        ):
                            st.session_state["selected_doc"] = result_data
                
                # 保留分页控件
                if total_pages > 1:
                    # 计算要显示的页码范围
                    current_page = st.session_state["current_page"]
                    window_size = 5  # 显示当前页附近的页码数量
                    start_page = max(1, current_page - window_size // 2)
                    end_page = min(total_pages, start_page + window_size - 1)
                    
                    # 调整起始页，确保始终显示 window_size 个页码（如果有足够的页数）
                    if end_page - start_page + 1 < window_size and total_pages >= window_size:
                        start_page = max(1, end_page - window_size + 1)
                    
                    # 创建分页按钮
                    cols = st.columns([0.3] * (end_page - start_page + 3))  # +3 for prev, next buttons
                    
                    # 上一页按钮
                    with cols[0]:
                        if current_page > 1:
                            if st.button("«", key="prev_page", use_container_width=False):
                                st.session_state["current_page"] -= 1
                                st.rerun()
                        else:
                            st.button("«", disabled=True, key="prev_page_disabled", use_container_width=False)
                    
                    # 页码按钮
                    for i, page in enumerate(range(start_page, end_page + 1), 1):
                        with cols[i]:
                            button_style = "primary" if page == current_page else "secondary"
                            if st.button(f"{page}", key=f"page_{page}", type=button_style, use_container_width=False):
                                st.session_state["current_page"] = page
                                st.rerun()
                    
                    # 下一页按钮
                    with cols[-1]:
                        if current_page < total_pages:
                            if st.button("»", key="next_page", use_container_width=False):
                                st.session_state["current_page"] += 1
                                st.rerun()
                        else:
                            st.button("»", disabled=True, key="next_page_disabled", use_container_width=False)

            # 右侧文档内容显示
            with col2:
                st.subheader("文档内容")
                if "selected_doc" in st.session_state and st.session_state["selected_doc"]:
                    content = get_document_content(st.session_state["selected_doc"]["doc_id"])
                    if content:
                        st.markdown(
                            f"""
                            <div class="doc-content-box">
                                {content.strip()}
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
