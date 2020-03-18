# encoding=utf-8

"""

@desc:main函数，整合整个处理流程。

"""
import KB_query.jena_sparql_endpoint as jena_sparql_endpoint
import KB_query.question2sparql as question2sparql

# TODO 连接Fuseki服务器。
fuseki = jena_sparql_endpoint.JenaFuseki()
# TODO 初始化自然语言到SPARQL查询的模块，参数是外部词典列表。
q2s = question2sparql.Question2Sparql(['KB_query/external_dict/mammo.txt'])


def query_main(question):

    my_query = q2s.get_sparql(question.encode("utf-8").decode('utf-8'))
    if my_query is not None:

        result = fuseki.get_sparql_result(my_query)
        value = fuseki.get_sparql_result_value(result)

        # TODO 查询结果为空，根据OWA，回答“不知道”
        if len(value) == 0:
            return 'I don\'t know.'
        elif len(value) == 1:
            return value[0]
        else:
            output = ''
            for v in value:
                if '#' in v:
                    v = v.split('#')[-1]
                output += v + u'、'
            return output[0:-1]

    else:
        # TODO 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
        return 'I can\'t understand.'


if __name__ == '__main__':
    # TODO 连接Fuseki服务器。
    fuseki = jena_sparql_endpoint.JenaFuseki()
    # TODO 初始化自然语言到SPARQL查询的模块，参数是外部词典列表。
    q2s = question2sparql.Question2Sparql(['./external_dict/mammo.txt'])

    while True:
        question = input()
        # question = '钙化分布有哪些类型'
        my_query = q2s.get_sparql(question.encode("utf-8").decode('utf-8'))

        if my_query is not None:
            # print("-----", my_query)

            result = fuseki.get_sparql_result(my_query)
            value = fuseki.get_sparql_result_value(result)

            # TODO 查询结果为空，根据OWA，回答“不知道”
            if len(value) == 0:
                print('I don\'t know.')
            elif len(value) == 1:
                print(value[0])
            else:
                output = ''
                for v in value:
                    if '#' in v:
                        v = v.split('#')[-1]
                    output += v + u'、'
                print(output[0:-1])

        else:
            # TODO 自然语言问题无法匹配到已有的正则模板上，回答“无法理解”
            print('I can\'t understand.')

