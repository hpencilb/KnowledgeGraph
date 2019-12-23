class QuestionPaser:
    """构建实体节点"""

    def build_entitydict(self, args):
        entity_dict = {}
        for arg, types in args.items():
            for type in types:
                if type not in entity_dict:
                    entity_dict[type] = [arg]
                else:
                    entity_dict[type].append(arg)

        return entity_dict

    '''解析主函数'''

    def parser_main(self, res_classify):
        args = res_classify['args']
        entity_dict = self.build_entitydict(args)
        question_types = res_classify['question_types']
        sqls = []
        for question_type in question_types:
            sql_ = {'question_type': question_type}
            sql = []

            if question_type == 'stockid_conceptget':
                sql = self.sql_transfer(question_type, entity_dict.get('stockid'))

            elif question_type == 'stockname_conceptget':
                sql = self.sql_transfer(question_type, entity_dict.get('stockname'))

            elif question_type == 'concept_stockget':
                sql = self.sql_transfer(question_type, entity_dict.get('concept'))

            elif question_type == 'stockid_industryget':
                sql = self.sql_transfer(question_type, entity_dict.get('stockid'))

            elif question_type == 'stockname_industryget':
                sql = self.sql_transfer(question_type, entity_dict.get('stockname'))

            elif question_type == 'industry_stockget':
                sql = self.sql_transfer(question_type, entity_dict.get('industry'))

            if sql:
                sql_['sql'] = sql

                sqls.append(sql_)

        return sqls

    '''针对不同的问题，分开进行处理'''

    def sql_transfer(self, question_type, entities):
        if not entities:
            print('in not entities\n')
            return []

        # 查询语句
        sql = []

        # 按股票代码查询所属概念
        if question_type == 'stockid_conceptget':
            sql = [
                "MATCH (m)-[r:concept_of]->(n:Concept) where m.stock_id = '{}' return m.stock_id, m.name, r.name, n.name".format(
                    i) for i in entities]

        # 按股票名称查询所属概念
        elif question_type == 'stockname_conceptget':
            sql = [
                "MATCH (m)-[r:concept_of]->(n:Concept) where m.name = '{}' return m.stock_id, m.name, r.name, n.name".format(
                    i) for i in entities]

        # 根据概念查股
        elif question_type == 'concept_stockget':
            sql = [
                "MATCH (m)-[r:concept_of]->(n:Concept) where n.name = '{}' return m.stock_id, m.name, n.name".format(
                    i) for i in entities]

        # 按股票代码查询所属行业
        elif question_type == 'stockid_industryget':
            sql = [
                "MATCH (m)-[r:industry_of]->(n:Industry) where m.stock_id = '{}' return m.stock_id, m.name, r.name, n.name".format(
                    i) for i in entities]

        # 按股票名称查询所属行业
        elif question_type == 'stockname_industryget':
            sql = [
                "MATCH (m)-[r:industry_of]->(n:Industry) where m.name = '{}' return m.stock_id, m.name, r.name, n.name".format(
                    i) for i in entities]

        # 按行业查询股票
        elif question_type == 'industry_stockget':
            sql = [
                "MATCH (m)-[r:industry_of]->(n:Industry) where n.name = '{}' return m.stock_id, m.name, n.name".format(
                    i) for i in entities]

        return sql


if __name__ == '__main__':
    handler = QuestionPaser()
