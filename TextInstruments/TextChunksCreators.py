# Здесь находятся все модули, отвечающие за разбитие всех текстов всех авторов на куски, которые соответствуют некоторым
# критериям (например, размеры кусков не должны слишком сильно отличаться или кол-ва кусков одного автора должны быть
# одни и те же между авторами)

import os
from os import listdir

class Simple_Text_Chunk_Creator:

    def __init__(self, tokenizer, preprocessor, min_words_count=1000, max_word_count_coof=1.5):
        self.tokenizer=tokenizer
        self.preprocessor=preprocessor
        self.min_words_count=min_words_count
        self.max_word_count_coof=max_word_count_coof

    def create_text_chunks(self, authors_path, author_list=None):
        if author_list==None:
            author_list=listdir(authors_path)
        author_text_files=[( author_name, [file_name for file_name in listdir(os.path.join(authors_path,author_name))]) for  author_name in author_list]
        #Сначала найдём минимальное кол-во слов в указанных текстах. От этого кол-ва и будем отталкиваться
        print("Finding minimal words count in text chunks")
        author_texts=[]
        min_text_words_count=5*self.min_words_count
        #sum_words=0
        for author_name, file_names in author_text_files:
            texts=[]
            for file_name in file_names:
                with open(os.path.join(authors_path, author_name, file_name), 'r', encoding='utf-8') as r:
                    text=r.read()
                    text=self.preprocessor.preprocess(text)
                    word_count=self.tokenizer.count_words(text)
                    #sum_words+=word_count
                    if word_count<self.min_words_count: continue
                    if word_count<min_text_words_count:
                        min_text_words_count=word_count
                    texts.append(text)


            author_texts.append((author_name, texts))

        max_text_words_count=self.max_word_count_coof*min_text_words_count

        #Теперь разобьём тексты на куски, которые не больше max_text_words_count и не меньше min_text_words_count.
        #Куски эти будут иметь границу по абзацам (один и тот же кусок может находиться в двух разных частях или главах)
        print("Dividing texts into chunks")
        author_text_chunks=[]
        for author_name, texts in author_texts:
            print("Обрабатываю тексты автора {}".format(author_name))
            text_chunks=[]
            for text in texts:
                articles = [article for article in text.split('\n') if article != '']
                chunk=""
                chunk_words_count=0
                for article in articles:
                    chunk_words_count+=self.tokenizer.count_words(article)
                    if chunk_words_count>max_text_words_count:
                        chunk=""
                        chunk_words_count=0
                        continue
                    chunk+=article+"\n"
                    if (chunk_words_count>=min_text_words_count):
                        text_chunks.append(chunk)
                        chunk=""
                        chunk_words_count = 0

            author_text_chunks.append((author_name, text_chunks))

        return author_text_chunks





