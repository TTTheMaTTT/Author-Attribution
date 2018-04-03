# В этом файле планируется хранить коды всех токенизаторов (будем считать эти коды простыми и не заслуживающими
# отдельных файлов)

import re

class Simple_Tokenizer:
    def __init__(self, remove_numerals=True):
        self.remove_numerals=remove_numerals

    # Можно написать 2 функции, одна разбивает на слова, а вторая просто считает их. Вторая функция - более дешёвая по памяти.
    # Но это мелочи
    def divide_to_words(self, text):
        """
        Делим текст на слова
        :param text: Рассматриваемый текст
        :return: list, состоящий из слов
        """
        words = []
        # 2 различных режима токенизатора, убирающего или неубирающего числа из текста
        regexp = "[…–«»:\'\"\[\]\{\}\n ,.;!?()-0123456789]" if self.remove_numerals else "[…–«»:\'\"\[\]\{\}\n ,.;!?()-]"
        l = re.split(regexp, text)
        for i in l:
            if len(i):
                words.append(i)

        return words

    def count_words(self, text):
        """
        Считаем кол-во слов в тексте
        :param text: Рассматриваемый текст
        :return: кол-во слов
        """
        words_count = 0
        # 2 различных режима токенизатора, убирающего или неубирающего числа из текста
        regexp = "[…–«»:\'\"\[\]\{\}\n ,.;!?()-0123456789]" if self.remove_numerals else "[…–«»:\'\"\[\]\{\}\n ,.;!?()-]"
        l = re.split(regexp, text)
        for i in l:
            if len(i):
                words_count += 1

        return words_count