from py2neo import Graph
import pandas as pd
import re

tablefile = r'E:/GeoKGQA_V2/relationship_classification.xlsx'


def link_graph():
    try:
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))  # 接入neo4j服务，密码为自行设置的密码
        return graph
    except Exception as e:
        raise ValueError(f'An error occurred while connecting to the Neo4j database:{e}')


def contain(string, string_list):
    """Check if any substring in substrings exists in target_string"""
    for substr in string_list:
        if substr in string:
            return substr
    return False


def clean(strings):
    """
    Clean strings by removing specific characters.
    :param strings: A list of strings to clean.
    :return: A list of cleaned strings.
    """
    pattern = r'[$#?]'  # Match $, #, and ?
    cleaned_strings = []
    for string in strings:
        cleaned_string = re.sub(pattern, '', string)
        cleaned_strings.append(cleaned_string)
    # print(cleaned_strings)
    return ''.join(cleaned_strings)


def check_characters_presence(template_list, target_string):
    """Check if target_entity exists in entity_list"""
    return target_string in template_list


def query_graph_fact(corpus, entity):
    """
    Execute fact-based query based on matched template and entity

    Args:
        corpus (str): Matched question template
        entity (str): Extracted entity from user question

    Returns:
        pd.DataFrame: Query results from Neo4j
    """
    graph = link_graph()

    corpus = clean(corpus)
    if contain(corpus, {"的找矿标志是什么", "围岩蚀变有哪些", "主要围岩蚀变有哪些", "近矿围岩蚀变有哪些",
                        "主要近矿围岩蚀变有哪些", "矿化蚀变类型有哪些", "主要矿化蚀变类型有哪些"}):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:hasAlteration]->(o:`蚀变类型`) where s.name='%s' return s,r,o " % entity).to_data_frame()
        r = "hasAlteration"
    elif contain(corpus, {"的主要导矿构造有哪些", "的主要容矿构造有哪些", "的断裂构造有哪些", "的控岩控矿构造有哪些"}):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:isControlledBy]->(o:`构造`) where s.name='%s' return s,r,o " % entity).to_data_frame()
        r = "isControlledBy"
    elif contain(corpus, {"所处的构造位置是哪里", "的区域构造位置是哪里", "的区域构造位置是哪里", "位于哪里"}):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:isLocatedIn]->(o) where s.name='%s' return s,r,o " % entity).to_data_frame()
        r = "isLocatedIn"
    elif contain(corpus,
                 {"赋存哪些地层", "出露地层有哪些", "赋矿层位有哪些", "有哪些地层呢", "含矿层位有哪些", "赋存于哪里",
                  "主要容矿底层有哪些", "分布于哪里", "赋矿地层有哪些", "包含哪些地层"}):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:isRelatedTo]->(o:`地层`) where s.name='%s' return s,r,o " % entity).to_data_frame()
        r = "isRelatedTo"
    elif contain(corpus, {"成矿作用有哪些", "经历过哪些地质作用", "经历过哪些成矿作用"}):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:isRelatedTo]->(o:`地质作用`) where s.name='%s' return s,r,o " % entity).to_data_frame()
        r = "isRelatedTo"
    elif contain(corpus, {"含有哪些岩浆岩", "含有哪些岩石", "含有哪些沉积岩", "含有哪些变质岩"}):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:isRelatedTo]->(o:`岩石`) where s.name='%s' return s,r,o " % entity).to_data_frame()
        r = "isRelatedTo"
    elif contain(corpus, {"赋矿地层是哪个时代", "出露时代有哪些"}):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:isFormedIn]->(o:`成矿时代`) where s.name='%s' return s,r,o " % entity).to_data_frame()
        r = "isFormedIn"
    elif contain(corpus, {"有哪些矿物"}):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:hasMinerals]->(o:`矿物`) where s.name='%s' return s,r,o " % entity).to_data_frame()
        r = "hasMinerals"
    elif contain(corpus, {"属于哪个构造带"}):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:isFormedIn]->(o:`地质背景`) where s.name='%s' return s,r,o " % entity).to_data_frame()
        r = "isFormedIn"
    elif contain(corpus, {"异常有哪些"}):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:isFoundIn]->(o) where s.name='%s' return s,r,o " % entity).to_data_frame()
        r = "isFoundIn"
    elif contain(corpus, {"组成部分有哪些"}):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:isReletedTo]->(o) where s.name='%s' return s,r,o " % entity).to_data_frame()
        r = "isReletedTo"
    elif contain(corpus, {"有哪些岩体组成"}):
        result = graph.run(
            "MATCH (s:`矿床`{name:'%s'})-[r:isRelatedTo]->(o:`岩石`) where s.name contains ['岩体','岩株','岩基'] return s,r,o " % entity).to_data_frame()
        r = "isRelatedTo"
    elif contain(corpus, {"起控制作用"}):
        result = graph.run("MATCH (s:`矿床`{name:'%s'})-[r:isControledBy]->(o) return s,r,o " % entity).to_data_frame()
        r = "isControlledBy"
    elif contain(corpus, {"的断裂构造有哪些"}):
        result = graph.run(
            "MATCH (s:`矿床`{name:'%s'})-[r:isControlledBy]->(o:`构造`) WHERE s.name CONTAINS '断裂' return s,r,o" % entity).to_data_frame()
        r = "isControlledBy"
    elif contain(corpus, {"有哪些共生矿物", "有哪些特征共生矿物"}):
        result = graph.run(
            "MATCH (s:`矿床`{name:'%s'})-[r:hasMinerals]->(o:`矿物`) where s.name in['自然金','黑钨矿','白钨矿','独居石','金红石','褐钇铌矿','白铅矿','闪锌矿','黄铜矿','方铅矿'] return s,r,o" % entity).to_data_frame()
        r = "hasMinerals"
    elif contain(corpus, {"有哪些次生氧化矿物"}):
        result = graph.run(
            "MATCH (s:`矿床`{name:'%s'})-[r:hasMinerals]->(o:`矿物`) where s.name in['赤铁矿','针铁矿','褐铁矿'] return s,r,o" % entity).to_data_frame()
        r = "hasMinerals"
    elif contain(corpus, {"有哪些伴生有益矿物组份"}):
        result = graph.run(
            "MATCH (s:`矿床`{name:'%s'})-[r:hasMinerals]->(o:`矿物`) where s.name in['自然金','黑钨矿','白钨矿','钇铌铁矿','辉钼矿','闪锌矿'] return s,r,o" % entity).to_data_frame()
        r = "hasMinerals"
    elif contain(corpus, {"包含哪些碱金属元素"}):
        result = graph.run(
            "MATCH (s:`矿床`{name:'%s'})-[r:hasElement]->(o:`元素`) where s.name in['锂','钠','钾','铷','铯','钫'] return s,r,o" % entity).to_data_frame()
        r = "hasElement"
    elif contain(corpus, {"包含哪些金属元素"}):
        result = graph.run(
            "MATCH (s:`矿床`{name:'%s'})-[r:hasElement]->(o:`元素`) where not s.name in ['氟','硼','砷','硫','氧','溴','硅'] return s,r,o" % entity).to_data_frame()
        r = "hasElementhasElement"
    elif contain(corpus, {"包含哪些有益元素"}):
        result = graph.run(
            "MATCH (s:`矿床`{name:'%s'})-[r:hasElement]->(o:`元素`) where s.name in ['锡','钨','金','铌','钽','锌'] return s,r,o" % entity).to_data_frame()
        r = "hasElement"
    elif contain(corpus, {"包含哪些伴生有害元素"}):
        result = graph.run(
            "MATCH (s:`矿床`{name:'%s'})-[r:hasElement]->(o:`元素`) where s.name in ['砷','铋','铜','铁','铅','锑'] return s,r,o" % entity).to_data_frame()
        r = "hasElement"
    elif contain(corpus, {"包含哪些元素"}):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:hasElement]->(o:`元素`) where s.name='%s' return s,r,o" % entity).to_data_frame()
        r = "hasElement"
    else:
        result = "无答案"
    return result


def get_relation_classifier(tablefile):
    # 读取Excel文件
    df = pd.read_excel(tablefile)

    # 提取某一列的数据
    AT_list = df['AT'].tolist()
    CB_list = df['CB'].tolist()
    LI_list = df['LI'].tolist()
    FI_list = df['FI'].tolist()
    HM_list = df['HM'].tolist()
    HE_list = df['HE'].tolist()
    IF_list = df['IF'].tolist()
    IA_list = df['IA'].tolist()
    IR_list = df['IR'].tolist()

    return AT_list, CB_list, LI_list, FI_list, HM_list, HE_list, IF_list, IA_list, IR_list


def query_graph_judgment(corpus, entitielist):
    """
    Execute judgment-based query to verify relationships

    Args:
        corpus (str): Matched judgment template
        entitielist (list): List containing head and tail entities

    Returns:
        tuple: (query_result, logic_result)
    """
    # global result, logic
    graph = link_graph()
    AT_list, CB_list, LI_list, FI_list, HM_list, HE_list, IF_list, IA_list, IR_list = get_relation_classifier(tablefile)

    if check_characters_presence(AT_list, corpus):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:hasAlteration]->(o) where s.name='%s' return s,r,o " % entitielist[0]).to_data_frame()
        r = "hasAlteration"
        end_entity_list = result['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, entitielist[1])
    elif check_characters_presence(CB_list, corpus):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:isControlledBy]->(o) where s.name='%s' return s,r,o " % entitielist[0]).to_data_frame()
        r = "isControlledBy"
        end_entity_list = result['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, entitielist[1])
    elif check_characters_presence(LI_list, corpus):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:isLocatedIn]->(o) where s.name='%s' return s,r,o " % entitielist[0]).to_data_frame()
        r = "isControlledBy"
        end_entity_list = result['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, entitielist[1])
    elif check_characters_presence(FI_list, corpus):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:isFormedIn]->(o) where s.name='%s' return s,r,o " % entitielist[0]).to_data_frame()
        r = "isFormedIn"
        end_entity_list = result['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, entitielist[1])
    elif check_characters_presence(HM_list, corpus):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:hasMinerals]->(o) where s.name='%s' return s,r,o " % entitielist[0]).to_data_frame()
        r = "hasMinerals"
        end_entity_list = result['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, entitielist[1])
    elif check_characters_presence(HE_list, corpus):
        result = graph.run(
            "MATCH (s:`矿床`)-[r:hasElement]->(o) where s.name='%s' return s,r,o" % entitielist[0]).to_data_frame()
        r = "hasElement"
        end_entity_list = result['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, entitielist[1])
    elif check_characters_presence(IF_list, corpus):
        result = graph.run(
            "MATCH (s:`矿床`{name:'%s'})-[r:isFoundIn]->(o) return s,r,o " % entitielist[0]).to_data_frame()
        r = "isFoundIn"
        end_entity_list = result['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, entitielist[1])
    elif check_characters_presence(IA_list, corpus):
        result = graph.run(
            "MATCH (s:`矿床`{name:'%s'})-[r:isAnalyzedBy]->(o) return s,r,o " % entitielist[0]).to_data_frame()
        r = "isAnalyzedBy"
        end_entity_list = result['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, entitielist[1])
    elif check_characters_presence(IR_list, corpus):
        result = graph.run(
            "MATCH (s:`矿床`{name:'%s'})-[r:isRelatedTo]->(o) return s,r,o " % entitielist[0]).to_data_frame()
        r = "isRelatedTo"
        end_entity_list = result['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, entitielist[1])
    else:
        print('无结果')
    return result, logic
