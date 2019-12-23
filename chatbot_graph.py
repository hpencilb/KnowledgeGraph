from question_classifier import *
from question_parser import *
from answer_search import *
from recommend_stock import *
import random

'''问答类'''
choices = ['摩托车行业有哪些股票?', '燃料电池概念下有哪些股票?', '华谊兄弟是什么概念的股票?', '巨人网络是什么行业的股票?']


class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()
        self.stock_list = []

    def chat_kg_main(self, sent):
        answer = '这我好像不知道,您可以这样问我:'
        res_classify = self.classifier.classify(sent)

        if not res_classify:
            return '超出Bot的知识范围了.您可以这样问我:' + random.choice(choices)

        if res_classify['question_types'] == ['sensitive']:
            return '我也是个暴脾气,信不信我骂回去'

        res_sql = self.parser.parser_main(res_classify)
        if res_classify['question_types'] == ['recommend_get']:
            r = RecommendStock(self.stock_list)
            final_answers = r.find_best()
        else:
            self.stock_list = []
            List, final_answers = self.searcher.search_main(res_sql)
            for li in List:
                self.stock_list.append(li[:6])
        if not final_answers:
            answer += random.choice(choices)
            return answer
        else:
            return '\n'.join(final_answers)


if __name__ == '__main__':
    handler = ChatBotGraph()
    print('Bot:', '您好,我是Bot,欢迎向我提问!')
    while 1:
        question = input('User:')
        answer = handler.chat_kg_main(question)
        print('Bot:', answer)
