import generate_summary
import query
from entityextraction import predict
from entityextraction.train import load_model
from templatematching.top5 import template_match
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
项目名称: A Lightweight Knowledge Graph-Driven Question Answering System
文件名: main.py
作者: Mingguo Wang1, 3, Chengbin Wang 2*, Jianguo Chen1, 2, Bo Wang2, Wei Wang4, Xiaogang Ma5, Jiangtao Ren2, Zichen Li2, Yicai Ye2, Jiakai Zhang2, Yue Wang2
团队:    1 Key Laboratory of Geological Survey and Evaluation of Ministry of Education, China University of Geosciences, Wuhan 430074, China
        2 School of Earth Resources & Ministry of Natural Resources Key Laboratory of Resource Quantitative Evaluation and Information Engineering, China University of Geosciences, Wuhan 430074, China
        3 Yunnan Geological Big Data Center, Geological Survey and Mapping Institute of Yunnan Province, Kunming 650218, China 
        4 ZGIS Corporation, Wuhan 430000, China
        5 Department of Computer Science, University of Idaho, 875 Perimeter Drive, MS 1010, Moscow, ID 83844-1010, USA
创建日期: 2023-06-22
最后修改日期: 2025-05-27
联系人: wangchengbin@cug.edu.cn (C. Wang)。
"""

def start():
    while True:
        # Template matching
        user_question = input('Enter question (type "esc" to exit): ')
        '''Examples:1.个旧锡矿所处的区域构造位置在哪里、2.个旧锡矿出露地层有哪些、3.个旧锡矿圈定异常有哪些、4.个旧锡矿有哪些矿石、5.红毛岭锡矿出露地层有哪些、
                    1.个旧锡矿是否赋存永宁镇组地层、2.红毛岭锡矿是不是有金红石矿石、3.个旧锡矿区的区域构造是否包括五子山复式背斜·、
                    1.个旧锡矿的找矿标志是什么 2.黄铁矿化是不是个旧锡矿的找矿标志?
                  
        '''

        # check if exit
        if user_question.lower() == 'esc':
            print("Exiting program...")
            break

        # Question classification
        question_type = predict.classify_question_type(user_question)
        matched_corpus = template_match(question_type, user_question)
        corpus = matched_corpus[0]
        # print(corpus)

        # Named Entity Recognition
        model_path = './entityextraction/model/crf_c2.pkl'
        model = load_model(model_path)

        # Named Entity Recognition output
        word_list, label_list = predict.word_split(user_question, model)

        if question_type:
            wordlist_fact = predict.fuzzy_matching(word_list[0])

            # Factual question processing
            result = query.query_graph_fact(corpus, wordlist_fact)
            result0 = str(result)

            # Generate factual answer summary
            summary = generate_summary.make_fact_summary(user_question, corpus, result0)

        else:
            # Judgment question processing
            wordlist_judgment = predict.fuzzy_matching(word_list[0])
            word_list[0] = wordlist_judgment

            # Query knowledge graph for judgment question
            result = query.query_graph_judgment(corpus, word_list)
            result1 = str(result[0])

            # Generate judgment answer summary
            summary = generate_summary.make_judgment_summary(user_question, corpus, result1, result[1])

        print(summary)


if __name__ == '__main__':
    try:
        start()
    except Exception as e:
        print(f"{str(e)}")
