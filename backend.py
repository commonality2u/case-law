from flask import Flask, request, jsonify
import os
import re
import math
import xml.etree.ElementTree as ET
from collections import defaultdict
from datetime import datetime

app = Flask(__name__)

class DocumentProcessor:
    def __init__(self):
        self.tokenizer = re.compile(r'\b\w+\b')
        self.stop_words = set(["a", "an", "the", "and", "or", "but", "on", "in", "with", 
                             "by", "for", "to", "of", "at", "as", "is", "it", "this", 
                             "that", "these", "those"])
        
    def extract_metadata(self, headline):
        source = ""
        date = ""
        title = headline
        corrected = False

        # 提取来源
        source_match = re.search(r'^([A-Z]{2,})\b', headline)
        if source_match:
            source = source_match.group(1)
            title = title[len(source):].strip()

        # 提取日期
        date_match = re.search(r'(\d{1,2} [A-Z]{3} \d{2})', headline)
        if date_match:
            raw_date = date_match.group(1)
            try:
                parsed_date = datetime.strptime(raw_date, '%d %b %y')
                date = parsed_date.strftime('%Y-%m-%d')
                title = title.replace(raw_date, '').strip()
            except ValueError:
                pass

        # 检查是否为更正文章
        if "corrected" in headline.lower():
            corrected = True
            title = re.sub(r'\bcorrected\b', '', title, flags=re.IGNORECASE).strip()

        # 清理标题
        title = re.sub(r'[\n\r\t]+', ' ', title)
        title = re.sub(r'[\W_]+', ' ', title).strip()

        return {
            "source": source,
            "date": date,
            "corrected": corrected,
            "title": title
        }

class IndexBuilder:
    def __init__(self, processor):
        self.processor = processor
        self.inverted_index = defaultdict(lambda: defaultdict(list))
        self.doc_metadata = {}
        self.doc_term_freq = defaultdict(lambda: defaultdict(int))
        
    def build_from_xml(self, file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()

        for doc in root.findall('DOC'):
            self._process_document(doc)

        return (dict(self.inverted_index), self.doc_metadata, 
                dict(self.doc_term_freq), len(self.doc_metadata))

    def _process_document(self, doc):
        doc_id = doc.find('DOCNO').text.strip()
        headline = doc.find('HEADLINE').text.strip() if doc.find('HEADLINE') is not None else ''
        text = doc.find('TEXT').text if doc.find('TEXT') is not None else ''

        # 提取元数据
        metadata = self.processor.extract_metadata(headline)
        metadata['text'] = text
        self.doc_metadata[doc_id] = metadata

        # 构建索引
        content = f"{headline} {text}".lower()
        tokens = self.processor.tokenizer.findall(content)
        
        for position, token in enumerate(tokens):
            if token not in self.processor.stop_words and not token.isdigit():
                self.inverted_index[token][doc_id].append(position)
                self.doc_term_freq[doc_id][token] += 1

class SearchEngine:
    def __init__(self, inverted_index, doc_metadata):
        self.inverted_index = inverted_index
        self.doc_metadata = doc_metadata

    def boolean_search(self, query):
        # 预处理查询，处理括号和操作符
        tokens = self._tokenize_query(query.lower())
        if not tokens:
            return []
        
        # 使用 Shunting Yard 算法处理操作符优先级
        postfix = self._to_postfix(tokens)
        result = self._evaluate_postfix(postfix)
        
        return self._format_results(sorted(list(result)) if result else [])

    def _tokenize_query(self, query):
        # 将查询分解为 tokens，识别操作符和括号
        operators = {'and', 'or', 'not', '(', ')'}
        tokens = []
        current_word = ''
        
        for char in query + ' ':  # 添加空格以处理最后一个词
            if char.isspace():
                if current_word:
                    if current_word.lower() in operators:
                        tokens.append(current_word.lower())
                    else:
                        tokens.append(('term', current_word))
                    current_word = ''
            elif char in '()':
                if current_word:
                    if current_word.lower() in operators:
                        tokens.append(current_word.lower())
                    else:
                        tokens.append(('term', current_word))
                    current_word = ''
                tokens.append(char)
            else:
                current_word += char
                
        return tokens

    def _to_postfix(self, tokens):
        # 使用 Shunting Yard 算法将中缀表达式转换为后缀表达式
        precedence = {'not': 3, 'and': 2, 'or': 1}
        output = []
        operator_stack = []
        
        for token in tokens:
            if isinstance(token, tuple) and token[0] == 'term':
                output.append(token)
            elif token == '(':
                operator_stack.append(token)
            elif token == ')':
                while operator_stack and operator_stack[-1] != '(':
                    output.append(operator_stack.pop())
                if operator_stack and operator_stack[-1] == '(':
                    operator_stack.pop()
            else:  # operator
                while (operator_stack and operator_stack[-1] != '(' and 
                       precedence.get(operator_stack[-1], 0) >= precedence.get(token, 0)):
                    output.append(operator_stack.pop())
                operator_stack.append(token)
        
        while operator_stack:
            output.append(operator_stack.pop())
            
        return output

    def _evaluate_postfix(self, postfix):
        stack = []
        
        for token in postfix:
            if isinstance(token, tuple) and token[0] == 'term':
                # 获取包含该词的文档集合
                term = token[1]
                if term in self.inverted_index:
                    stack.append(set(self.inverted_index[term].keys()))
                else:
                    stack.append(set())
            else:  # operator
                if token == 'not':
                    operand = stack.pop()
                    # 对所有文档取补集
                    all_docs = set(self.doc_metadata.keys())
                    stack.append(all_docs - operand)
                else:
                    right = stack.pop()
                    left = stack.pop()
                    if token == 'and':
                        stack.append(left & right)
                    elif token == 'or':
                        stack.append(left | right)
        
        return stack[0] if stack else set()

    def phrase_search(self, phrase):
        words = phrase.lower().split()
        if not all(word in self.inverted_index for word in words):
            return []

        candidate_docs = set.intersection(*(set(self.inverted_index[word].keys()) for word in words))
        results = []

        for doc_id in candidate_docs:
            positions = [self.inverted_index[word][doc_id] for word in words]
            for start_pos in positions[0]:
                if all(start_pos + i in positions[i] for i in range(1, len(words))):
                    results.append(doc_id)
                    break

        return self._format_results(sorted(results))

    def proximity_search(self, query, k):
        words = query.lower().split()
        if len(words) != 2:
            return []

        word1, word2 = words
        candidate_docs = set(self.inverted_index[word1].keys()) & set(self.inverted_index[word2].keys())
        results = []

        for doc_id in candidate_docs:
            positions1 = self.inverted_index[word1][doc_id]
            positions2 = self.inverted_index[word2][doc_id]
            if any(abs(p1 - p2) <= k for p1 in positions1 for p2 in positions2):
                results.append(doc_id)

        return self._format_results(sorted(results))

    def _format_results(self, doc_ids):
        return [{
            "doc_id": doc_id,
            **{k: v for k, v in self.doc_metadata[doc_id].items() if k != 'text'}
        } for doc_id in doc_ids]

class RankingEngine:
    @staticmethod
    def compute_tf_idf(doc_term_freq, inverted_index, total_docs):
        tf_idf_scores = defaultdict(dict)
        doc_freq = {term: len(docs) for term, docs in inverted_index.items()}

        for doc_id, term_freqs in doc_term_freq.items():
            for term, freq in term_freqs.items():
                tf = freq / sum(term_freqs.values())
                idf = math.log((total_docs + 1) / (doc_freq[term] + 1)) + 1
                tf_idf_scores[doc_id][term] = tf * idf

        return tf_idf_scores

    @staticmethod
    def compute_bm25(doc_term_freq, inverted_index, total_docs, k1=1.5, b=0.75):
        bm25_scores = defaultdict(dict)
        doc_freq = {term: len(docs) for term, docs in inverted_index.items()}
        
        # 计算平均文档长度
        doc_lengths = {doc_id: sum(freqs.values()) for doc_id, freqs in doc_term_freq.items()}
        avg_doc_length = sum(doc_lengths.values()) / len(doc_lengths)
        
        for doc_id, term_freqs in doc_term_freq.items():
            doc_length = doc_lengths[doc_id]
            for term, freq in term_freqs.items():
                # BM25 TF component
                tf = (freq * (k1 + 1)) / (freq + k1 * (1 - b + b * doc_length / avg_doc_length))
                # IDF component
                idf = math.log((total_docs - doc_freq[term] + 0.5) / (doc_freq[term] + 0.5) + 1)
                bm25_scores[doc_id][term] = tf * idf
        
        return bm25_scores

    @staticmethod
    def rank_by_tf_idf(query, tf_idf_scores, doc_metadata):
        terms = query.lower().split()
        scores = defaultdict(float)

        for term in terms:
            for doc_id, score in tf_idf_scores.items():
                scores[doc_id] += score.get(term, 0)

        ranked_docs = sorted(scores.keys(), key=lambda doc: scores[doc], reverse=True)
        return [{
            "doc_id": doc_id,
            "score": scores[doc_id],
            **{k: v for k, v in doc_metadata[doc_id].items() if k != 'text'}
        } for doc_id in ranked_docs]

    @staticmethod
    def rank_by_bm25(query, bm25_scores, doc_metadata):
        terms = query.lower().split()
        scores = defaultdict(float)

        for term in terms:
            for doc_id, score in bm25_scores.items():
                scores[doc_id] += score.get(term, 0)

        ranked_docs = sorted(scores.keys(), key=lambda doc: scores[doc], reverse=True)
        return [{
            "doc_id": doc_id,
            "score": scores[doc_id],
            **{k: v for k, v in doc_metadata[doc_id].items() if k != 'text'}
        } for doc_id in ranked_docs]

# 全局变量
search_engine = None
ranking_engine = None
doc_metadata = None
tf_idf_scores = None
bm25_scores = None  # 新增 BM25 分数

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    search_type = request.args.get('type', 'boolean')
    ranking_method = request.args.get('ranking', 'tf-idf')
    k = int(request.args.get('k', 5))

    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    try:
        # 首先根据搜索类型获取初始结果
        if search_type == 'boolean':
            initial_results = search_engine.boolean_search(query)
        elif search_type == 'phrase':
            initial_results = search_engine.phrase_search(query)
        elif search_type == 'proximity':
            initial_results = search_engine.proximity_search(query, k)
        else:
            return jsonify({"error": "Invalid search type"}), 400

        # 获取初始结果的文档ID列表
        doc_ids = [doc["doc_id"] for doc in initial_results]
        
        # 根据选择的排序方法对结果进行排序
        if ranking_method == 'tf-idf':
            ranked_results = RankingEngine.rank_by_tf_idf(query, tf_idf_scores, doc_metadata)
        elif ranking_method == 'bm25':
            ranked_results = RankingEngine.rank_by_bm25(query, bm25_scores, doc_metadata)
        else:
            return jsonify({"error": "Invalid ranking method"}), 400

        # 只保留在初始搜索结果中的文档
        final_results = [r for r in ranked_results if r["doc_id"] in doc_ids]

        return jsonify({
            "query": query,
            "type": search_type,
            "ranking": ranking_method,
            "results": final_results
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/document/<doc_id>', methods=['GET'])
def get_document(doc_id):
    if doc_id in doc_metadata:
        return doc_metadata[doc_id]["text"], 200, {'Content-Type': 'text/plain; charset=utf-8'}
    else:
        return jsonify({"error": "Document not found"}), 404

if __name__ == '__main__':
    input_file = 'trec.sample.xml'

    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        exit(1)

    # 初始化系统
    processor = DocumentProcessor()
    index_builder = IndexBuilder(processor)
    inverted_index, doc_metadata, doc_term_freq, total_docs = index_builder.build_from_xml(input_file)
    
    # 设置全局变量
    search_engine = SearchEngine(inverted_index, doc_metadata)
    tf_idf_scores = RankingEngine.compute_tf_idf(doc_term_freq, inverted_index, total_docs)
    bm25_scores = RankingEngine.compute_bm25(doc_term_freq, inverted_index, total_docs)  # 计算 BM25 分数
    
    app.run(host='0.0.0.0', port=5001)
