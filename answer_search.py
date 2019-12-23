from py2neo import Graph


class AnswerSearcher:
    def __init__(self):
        self.g = Graph(host="localhost",  # py2neo 3写法
                       user="neo4j",
                       password="123456")
        self.num_limit = 20

    '''执行cypher查询，并返回相应结果'''

    def search_main(self, sqls):
        final_answers = []
        for sql_ in sqls:
            question_type = sql_['question_type']
            queries = sql_['sql']
            answers = []
            for query in queries:
                ress = self.g.run(query).data()
                answers += ress
                # print(answers)
            StockList, final_answer = self.answer_prettify(question_type, answers)
            if final_answer:
                final_answers.append(final_answer)
        return StockList, final_answers

    '''根据对应的qustion_type，调用相应的回复模板'''

    def answer_prettify(self, question_type, answers):
        final_answer = []
        if not answers:
            return ''

        elif question_type == 'stockid_conceptget':
            desc = [i['n.name'] for i in answers]
            subject1 = answers[0]['m.stock_id']
            subject2 = answers[0]['m.name']
            Stock_List = list(set(desc))[:self.num_limit]
            final_answer = '{0} {1}的所属概念是：{2}'.format(subject1, subject2, '；'.join(Stock_List))

        elif question_type == 'stockname_conceptget':
            desc = [i['n.name'] for i in answers]
            subject1 = answers[0]['m.stock_id']
            subject2 = answers[0]['m.name']
            Stock_List = list(set(desc))[:self.num_limit]
            final_answer = '{0} {1}的所属概念是：{2}'.format(subject1, subject2, '；'.join(Stock_List))

        elif question_type == 'concept_stockget':
            desc = [i['m.stock_id'] + ' ' + i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            Stock_List = list(set(desc))[:self.num_limit]
            final_answer = '属于{0}概念的股票有：{1}'.format(subject, '；'.join(Stock_List))

        elif question_type == 'stockid_industryget':
            desc = [i['n.name'] for i in answers]
            subject1 = answers[0]['m.stock_id']
            subject2 = answers[0]['m.name']
            Stock_List = list(set(desc))[:self.num_limit]
            final_answer = '{0} {1}的所属行业是：{2}'.format(subject1, subject2, '；'.join(Stock_List))

        elif question_type == 'stockname_industryget':
            desc = [i['n.name'] for i in answers]
            subject1 = answers[0]['m.stock_id']
            subject2 = answers[0]['m.name']
            Stock_List = list(set(desc))[:self.num_limit]
            final_answer = '{0} {1}的所属行业是：{2}'.format(subject1, subject2, '；'.join(Stock_List))

        elif question_type == 'industry_stockget':
            desc = [i['m.stock_id'] + ' ' + i['m.name'] for i in answers]
            subject = answers[0]['n.name']
            Stock_List = list(set(desc))[:self.num_limit]
            final_answer = '属于{0}行业的股票有：{1}'.format(subject, '；'.join(Stock_List))

        elif question_type == 'stockname_yearget':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            Stock_List = list(set(desc))[:self.num_limit]
            final_answer = '{0} 股票的上市年份为：{1}'.format(subject, '；'.join(Stock_List))

        elif question_type == 'stockid_yearget':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            Stock_List = list(set(desc))[:self.num_limit]
            final_answer = '{0} 股票的上市年份为：{1}'.format(subject, '；'.join(Stock_List))

        elif question_type == 'stockname_areaget':
            desc = [i['n.name'] for i in answers]
            subject = answers[0]['m.name']
            Stock_List = list(set(desc))[:self.num_limit]
            final_answer = '{0} 股票的所属地为：{1}'.format(subject, '；'.join(Stock_List))
        return Stock_List, final_answer


if __name__ == '__main__':
    searcher = AnswerSearcher()
