from py2neo import Graph
import pandas as pd
import re


# corpus="所处的构造位置是哪里"#输入模板匹配得到的问句
# wordlist="个旧锡矿"#输入语义解析获得的实体


def contain(string, string_set):
    global s
    for s in string_set:
        if s in string:
            return s
    return False


def clean(strings):
    pattern = r'[$#?]'  # 匹配 $ 和 #？
    cleaned_strings = []
    for string in strings:
        cleaned_string = re.sub(pattern, '', string)
        cleaned_strings.append(cleaned_string)
    print(cleaned_strings)
    return cleaned_strings


def check_characters_presence(string_list, target_string):
    a=[]
    for i in range(len(string_list)):
        if string_list[i]==target_string:
            b=True
            a.append(b)
        else:
            b=False
            a.append(b)
    if any(a):
        return True
    else:
        return False
        #all_present = all(char in target_string for char in string_list[i])


def queryGraph_fact(corpus, wordlist):
    # 定义函数，功能为将上一步得到的问句匹配相应的问句模板
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "woshixlf123"))  # 接入neo4j服务，密码为自行设置的密码
    if contain(corpus, {"的找矿标志是什么", "围岩蚀变有哪些", "主要围岩蚀变有哪些", "近矿围岩蚀变有哪些",
                        "主要近矿围岩蚀变有哪些", "矿化蚀变类型有哪些", "主要矿化蚀变类型有哪些"}):
        JG = graph.run("MATCH (s:`矿床`)-[r:hasAlteration]->(o:`蚀变类型`)\
        where s.name='%s'\
        return s,r,o " % wordlist).to_data_frame()
        r = "hasAlteration"
    elif contain(corpus, {"的主要导矿构造有哪些", "的主要容矿构造有哪些", "的断裂构造有哪些", "的控岩控矿构造有哪些"}):
        JG = graph.run("MATCH (s:`矿床`)-[r:isControlledBy]->(o:`构造`)\
        where s.name='%s'\
        return s,r,o " % wordlist).to_data_frame()
        r = "isControlledBy"
    elif contain(corpus, {"所处的构造位置是哪里", "的区域构造位置是哪里", "的区域构造位置是哪里", "位于哪里"}):
        JG = graph.run("MATCH (s:`矿床`)-[r:isLocatedIn]->(o)\
        where s.name='%s'\
        return s,r,o " % wordlist).to_data_frame()
        r = "isLocatedIn"
    elif contain(corpus,
                 {"赋存哪些地层", "出露地层有哪些", "赋矿层位有哪些", "有哪些地层呢", "含矿层位有哪些", "赋存于哪里",
                  "主要容矿底层有哪些", "分布于哪里", "赋矿地层有哪些", "包含哪些地层"}):
        JG = graph.run("MATCH (s:`矿床`)-[r:isRelatedTo]->(o:`地层`)\
        where s.name='%s'\
        return s,r,o " % wordlist).to_data_frame()
        r = "isRelatedTo"
    elif contain(corpus, {"成矿作用有哪些", "经历过哪些地质作用", "经历过哪些成矿作用"}):
        JG = graph.run("MATCH (s:`矿床`)-[r:isRelatedTo]->(o:`地质作用`)\
        where s.name='%s'\
        return s,r,o " % wordlist).to_data_frame()
        r = "isRelatedTo"
    elif contain(corpus, {"含有哪些岩浆岩", "含有哪些岩石", "含有哪些沉积岩", "含有哪些变质岩"}):
        JG = graph.run("MATCH (s:`矿床`)-[r:isRelatedTo]->(o:`岩石`)\
        where s.name='%s'\
        return s,r,o " % wordlist).to_data_frame()
        r = "isRelatedTo"
    elif contain(corpus, {"赋矿地层是哪个时代", "出露时代有哪些"}):
        JG = graph.run("MATCH (s:`矿床`)-[r:isFormedIn]->(o:`成矿时代`)\
        where s.name='%s'\
        return s,r,o " % wordlist).to_data_frame()
        r = "isFormedIn"
    elif contain(corpus, {"有哪些矿物"}):
        JG = graph.run("MATCH (s:`矿床`)-[r:hasMinerals]->(o:`矿物`)\
        where s.name='%s'\
        return s,r,o " % wordlist).to_data_frame()
        r = "hasMinerals"
    elif contain(corpus, {"属于哪个构造带"}):
        JG = graph.run("MATCH (s:`矿床`)-[r:isFormedIn]->(o:`地质背景`)\
        where s.name='%s'\
        return s,r,o " % wordlist).to_data_frame()
        r = "isFormedIn"
    elif contain(corpus, {"异常有哪些"}):
        JG = graph.run("MATCH (s:`矿床`)-[r:isFoundIn]->(o)\
        where s.name='%s'\
        return s,r,o " % wordlist).to_data_frame()
        r = "isFoundIn"
    elif contain(corpus, {"组成部分有哪些"}):
        JG = graph.run("MATCH (s:`矿床`)-[r:isReletedTo]->(o)\
        where s.name='%s'\
        return s,r,o " % wordlist).to_data_frame()
        r = "isReletedTo"
    elif contain(corpus, {"有哪些岩体组成"}):
        JG = graph.run("MATCH (s:`矿床`{name:'%s'})-[r:isRelatedTo]->(o:`岩石`)\
        where s.name contains ['岩体','岩株','岩基']\
        return s,r,o " % wordlist).to_data_frame()
        r = "isRelatedTo"
    elif contain(corpus, {"起控制作用"}):
        JG = graph.run("MATCH (s:`矿床`{name:'%s'})-[r:isControledBy]->(o)\
        return s,r,o " % wordlist).to_data_frame()
        r = "isControlledBy"
    elif contain(corpus, {"的断裂构造有哪些"}):
        JG = graph.run("MATCH (s:`矿床`{name:'%s'})-[r:isControlledBy]->(o:`构造`)\
        WHERE s.name CONTAINS '断裂'\
        return s,r,o" % wordlist).to_data_frame()
        r = "isControlledBy"
    elif contain(corpus, {"有哪些共生矿物", "有哪些特征共生矿物"}):
        JG = graph.run("MATCH (s:`矿床`{name:'%s'})-[r:hasMinerals]->(o:`矿物`)\
        where s.name in['自然金','黑钨矿','白钨矿','独居石','金红石','褐钇铌矿','白铅矿','闪锌矿','黄铜矿','方铅矿']\
        return s,r,o" % wordlist).to_data_frame()
        r = "hasMinerals"
    elif contain(corpus, {"有哪些次生氧化矿物"}):
        JG = graph.run("MATCH (s:`矿床`{name:'%s'})-[r:hasMinerals]->(o:`矿物`)\
        where s.name in['赤铁矿','针铁矿','褐铁矿']\
        return s,r,o" % wordlist).to_data_frame()
        r = "hasMinerals"
    elif contain(corpus, {"有哪些伴生有益矿物组份"}):
        JG = graph.run("MATCH (s:`矿床`{name:'%s'})-[r:hasMinerals]->(o:`矿物`)\
        where s.name in['自然金','黑钨矿','白钨矿','钇铌铁矿','辉钼矿','闪锌矿']\
        return s,r,o" % wordlist).to_data_frame()
        r = "hasMinerals"
    elif contain(corpus, {"包含哪些碱金属元素"}):
        JG = graph.run("MATCH (s:`矿床`{name:'%s'})-[r:hasElement]->(o:`元素`)\
        where s.name in['锂','钠','钾','铷','铯','钫']\
        return s,r,o" % wordlist).to_data_frame()
        r = "hasElement"
    elif contain(corpus, {"包含哪些金属元素"}):
        JG = graph.run("MATCH (s:`矿床`{name:'%s'})-[r:hasElement]->(o:`元素`)\
        where not s.name in ['氟','硼','砷','硫','氧','溴','硅']\
        return s,r,o" % wordlist).to_data_frame()
        r = "hasElementhasElement"
    elif contain(corpus, {"包含哪些有益元素"}):
        JG = graph.run("MATCH (s:`矿床`{name:'%s'})-[r:hasElement]->(o:`元素`)\
        where s.name in ['锡','钨','金','铌','钽','锌']\
        return s,r,o" % wordlist).to_data_frame()
        r = "hasElement"
    elif contain(corpus, {"包含哪些伴生有害元素"}):
        JG = graph.run("MATCH (s:`矿床`{name:'%s'})-[r:hasElement]->(o:`元素`)\
        where s.name in ['砷','铋','铜','铁','铅','锑']\
        return s,r,o" % wordlist).to_data_frame()
        r = "hasElement"
    elif contain(corpus, {"包含哪些元素"}):
        JG = graph.run("MATCH (s:`矿床`)-[r:hasElement]->(o:`元素`)\
        where s.name='%s'\
        return s,r,o" % wordlist).to_data_frame()
        r = "hasElement"
    else:
        JG = "无答案"
    return JG


# 以上为问句匹配模板并在neo4j执行查询语句的过程，并得到相应的关系

# result=queryGraph(corpus,wordlist)
# print(result)
# 将问句，问句模板，图数据查询结果存入列表
# q = "矽卡岩化是不是个旧锡矿的找矿标志"
# # q="是不是的找矿标志"
# n = "个旧锡矿"  # 头实体
# o = "电气石化"  # 尾实体

# 读取Excel文件
df = pd.read_excel(r'I:\GeoKGQA第一版\GeoKGQA_V2\111.xlsx')

# 提取某一列的数据
column_data1 = df['AT'].tolist()
column_data2 = df['CB'].tolist()
column_data3 = df['LI'].tolist()
column_data4 = df['FI'].tolist()
column_data5 = df['HM'].tolist()
column_data6 = df['HE'].tolist()
column_data7 = df['IF'].tolist()
column_data8 = df['IA'].tolist()
column_data9 = df['IR'].tolist()

# 给列表命名
AT_list = column_data1
CB_list = column_data2
LI_list = column_data3
FI_list = column_data4
HM_list = column_data5
HE_list = column_data6
IF_list = column_data7
IA_list = column_data8
IR_list = column_data9

global JG, logic
def queryGraph_judgment(corpus, wordlist):
    global JG, logic
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "woshixlf123"))
    if check_characters_presence(AT_list, corpus):
        JG = graph.run("MATCH (s:`矿床`)-[r:hasAlteration]->(o)\
        where s.name='%s'\
        return s,r,o " % wordlist[0]).to_data_frame()
        r = "hasAlteration"
        end_entity_list = JG['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, wordlist[1])
    elif check_characters_presence(CB_list, corpus):
        JG = graph.run("MATCH (s:`矿床`)-[r:isControlledBy]->(o)\
        where s.name='%s'\
        return s,r,o " % wordlist[0]).to_data_frame()
        r = "isControlledBy"
        end_entity_list = JG['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, wordlist[1])
    elif check_characters_presence(LI_list, corpus):
        JG = graph.run("MATCH (s:`矿床`)-[r:isLocatedIn]->(o)\
        where s.name='%s'\
        return s,r,o " % wordlist[0]).to_data_frame()
        r = "isControlledBy"
        end_entity_list = JG['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, wordlist[1])
    elif check_characters_presence(FI_list, corpus):
        JG = graph.run("MATCH (s:`矿床`)-[r:isFormedIn]->(o)\
        where s.name='%s'\
        return s,r,o " % wordlist[0]).to_data_frame()
        r = "isFormedIn"
        end_entity_list = JG['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, wordlist[1])
    elif check_characters_presence(HM_list, corpus):
        JG = graph.run("MATCH (s:`矿床`)-[r:hasMinerals]->(o)\
        where s.name='%s'\
        return s,r,o " % wordlist[0]).to_data_frame()
        r = "hasMinerals"
        end_entity_list = JG['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, wordlist[1])
    elif check_characters_presence(HE_list, corpus):
        JG = graph.run("MATCH (s:`矿床`)-[r:hasElement]->(o)\
        where s.name='%s'\
        return s,r,o" % wordlist[0]).to_data_frame()
        r = "hasElement"
        end_entity_list = JG['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, wordlist[1])
    elif check_characters_presence(IF_list, corpus):
        JG = graph.run("MATCH (s:`矿床`{name:'%s'})-[r:isFoundIn]->(o)\
        return s,r,o " % wordlist[0]).to_data_frame()
        r = "isFoundIn"
        end_entity_list = JG['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, wordlist[1])
    elif check_characters_presence(IA_list, corpus):
        JG = graph.run("MATCH (s:`矿床`{name:'%s'})-[r:isAnalyzedBy]->(o)\
        return s,r,o " % wordlist[0]).to_data_frame()
        r = "isAnalyzedBy"
        end_entity_list = JG['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, wordlist[1])
    elif check_characters_presence(IR_list, corpus):
        JG = graph.run("MATCH (s:`矿床`{name:'%s'})-[r:isRelatedTo]->(o)\
        return s,r,o " % wordlist[0]).to_data_frame()
        r = "isRelatedTo"
        end_entity_list = JG['o'].to_list()
        desired_list = [node['name'] for node in end_entity_list]
        logic = check_characters_presence(desired_list, wordlist[1])
    else:
        print('无结果')
    #end_entity_list = JG['o'].to_list()

    # 提取节点的name属性值
    #desired_list = [node['name'] for node in end_entity_list]
    #logic = check_characters_presence(desired_list,wordlist[1] )
    return JG, logic
