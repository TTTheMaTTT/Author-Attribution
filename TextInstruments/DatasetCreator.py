# В этом файле будет содержаться код, который, используя различные подмодули, приводит тексты авторов в пригодный для
# обработки вид ( хоть сразу (или почти сразу) подавай в модель).

import jsonpickle
import os

# Пока что это будет самая простая тестовая версия
# Она проходит по папкам с нужными авторами, создаёт список из авторов их текстов, поделённых на куски, затем разбивает
# Каждый кусок на предложения, а каждое предложение на слова
# Также она сохраняет всё это в json-овский файл
class Simple_RNN_Dataset_Creator:

    def __init__(self, tokenizer, sentence_divider, chapter_name_classifier, preprocessor, text_chunks_creator):
        """
        :param tokenizer: Токенизатор
        :param sentence_divider: Разбивальщик по предложениям
        :param chapter_name_classifier: Классификатор заголовков
        :param preprocessor: Препроцессор
        :param text_chunks_creator: Разбивальщик текстов по кускам
        """
        self.tokenizer=tokenizer
        self.sentence_divider=sentence_divider
        self.chapter_name_classifier=chapter_name_classifier(self.tokenizer)
        self.preprocessor=preprocessor(self.chapter_name_classifier)
        self.text_chunks_creator=text_chunks_creator(self.tokenizer, self.preprocessor)

    def process_text(self,authors_path, author_list=None, savepath=None):
        """
        Обрабатывает все тексты из папок авторов, создаёт датасет, на котором можно запустить RNN
        :param authors_path: Путь, в котором находятся авторские папки
        :param author_list: Список рассматриваемых авторов
        :param savepath: Путь, по которому сохраняются результаты
        :return: Список из словарей с ключами: автор, текстовые отрывки (список с элементами, соответствующие предложениям отрывка,
        каждый из которых содержит в себе список из токенов предложения), кол-во отрывков
        """
        author_text_chunks=self.text_chunks_creator.create_text_chunks(authors_path, author_list)
        author_parsed_chunks=[{"author":author,
                               "chunks_count":0,
                               "text_chunks":[[[word for word in self.tokenizer.divide_to_words(sentence)]
                                               for sentence in self.sentence_divider.divide_to_sentences(text_chunk)]
                                              for text_chunk in text_chunks]}
                              for author, text_chunks in author_text_chunks]
        for one_author_chunks in author_parsed_chunks:
            one_author_chunks["chunks_count"]=len(one_author_chunks["text_chunks"])

        if (savepath!=None):
            with open(os.path.join(savepath,'rnn_dataset.json'), "w") as f:
                f.write(jsonpickle.encode(author_parsed_chunks, f))

        return author_parsed_chunks
