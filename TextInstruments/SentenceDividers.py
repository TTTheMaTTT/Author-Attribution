# Здесь будут находиться различные версии модулей, предназначенные для разбивки текста на предложения

#Простейшая версия, которая плохо работает со стихами
class Simple_Sentence_Divider:

    def __init__(self):
        pass

    def divide_to_sentences(self, text):
        """
        Разбиваем текст на предложения
        :param text:
         text: разбиваемый текст
        :return: list, состоящий из предложений
        """
        all_letters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"
        letters = []
        for c in all_letters:
            letters.append(c)

        spliter = [".", "!", "?", "…", "\n"]
        sentences = []
        sentence = ""

        for i in range(len(text) - 1):

            if text[i] not in spliter:
                sentence += text[i]

            if text[i + 1] in spliter and text[i] not in spliter:

                # Если у нас стоит точка, это ещё не значит, что мы имеем дело с концом предложения, а не с сокращением.
                if text[i + 1] == ".":
                    # Будем рассуждать так:
                    # Если точка стоит после большой буквы - это аббревиатура (А.С.Пушкин)
                    # Если следующая за точкой буква не является большой - это сокращение (размеры 10 см. на 20 дм.)
                    # Все остальные случаи считаем не существенными
                    is_abbrev = False

                    j = 0
                    # Проверка на сокращение
                    while (j < len(text) - i - 2):
                        next_symbol = text[i + 1 + j]
                        if next_symbol in letters:
                            if next_symbol != next_symbol.upper():
                                is_abbrev = True
                            break
                        j += 1

                    # Проверка на аббревиатуру
                    if text[i] == text[i].upper() and text[i] in letters:
                        is_abbrev = True

                    if is_abbrev:
                        sentence += text[i + 1]
                        continue

                sentences.append(sentence)
                sentence = ""

        return sentences


    def count_sentences(self, text):
        """
        Считаем число предложений в тексте
        :param text:
         text: рассматриваемый текст
        :return: кол-во предложений
        """
        all_letters = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNMёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ"
        letters = []
        for c in all_letters:
            letters.append(c)

        spliter = [".", "!", "?", "…", "\n"]
        sentences_count = 0

        for i in range(len(text) - 1):
            if text[i + 1] in spliter and text[i] not in spliter:

                # Если у нас стоит точка, это ещё не значит, что мы имеем дело с концом предложения, а не с сокращением.
                if text[i + 1] == ".":
                    # Будем рассуждать так:
                    # Если точка стоит после большой буквы - это аббревиатура (А.С.Пушкин)
                    # Если следующая за точкой буква не является большой - это сокращение (размеры 10 см. на 20 дм.)
                    # Все остальные случаи считаем не существенными
                    is_abbrev = False

                    # Проверка на сокращение
                    j = 0
                    while (j < len(text) - i - 2):
                        next_symbol = text[i + 1 + j]
                        if next_symbol in letters:
                            if next_symbol != next_symbol.upper():
                                is_abbrev = True
                            break
                        j += 1

                    # Проверка на аббревиатуру
                    if text[i] == text[i].upper() and text[i] in letters:
                        is_abbrev = True

                    if is_abbrev:
                        continue

                sentences_count += 1

        return sentences_count