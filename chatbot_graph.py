from question_classifier import *
from question_parser import *
from answer_search import *

'''问答类'''


class ChatBotGraph:
    def __init__(self):
        self.classifier = QuestionClassifier()
        self.parser = QuestionPaser()
        self.searcher = AnswerSearcher()

    def chat_kg_main(self, sent):
        answer = '嘤嘤嘤!'
        res_classify = self.classifier.classify(sent)

        if not res_classify:
            return '超出Bot的知识范围了.'

        if res_classify['question_types'] == ['sensitive']:
            return '我也是个暴脾气,信不信我骂回去'

        res_sql = self.parser.parser_main(res_classify)
        final_answers = self.searcher.search_main(res_sql)
        if not final_answers:
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
