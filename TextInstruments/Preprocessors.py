# Здесь находятся классы, которые предназначены для обработки текста перед всеми манипуляциями. Под предобработкой
# подразумеваются такие операции, как удаление заголовков, стихотворных текстов, примечаний автора, цифр и т.д.

import re


# Создадим класс, который бы удалял цифры, оглавления и авторские примечания
class Simple_Preprocessor:
    def __init__(self, chapter_name_classifier, min_numeral_sequence_length=4, delete_exp='[«»:*\'\"\[\]\{\}]'):
        self.chapter_name_classifier = chapter_name_classifier
        self.min_numeral_sequence_length = min_numeral_sequence_length
        self.delete_exp = delete_exp

    def delete_numeral_sequence(self, text, initial_value=1):
        """
        Находим возрастающие последовательности чисел и удаляем их
        :param text: Рассматриваемый текст
        :param initial_value: Начальное значение, с которого должна начинаться последовательность
        :return: текст, в котором нет возрастающей последовательнсоти
        """
        value = initial_value
        str_value = str(value)
        work_text = text
        text_fragments = []
        num_index = work_text.find(str_value)
        while (num_index != -1):
            text_fragments.append(work_text[:num_index])
            work_text = work_text[num_index + len(str_value):]
            value += 1
            str_value = str(value)
            num_index = work_text.find(str_value)
        text_fragments.append(work_text)
        if (value - initial_value >= self.min_numeral_sequence_length):
            return "".join(text_fragments)
        else:
            return text

    def delete_chapter_names(self, text):
        """
        Удаляем все заголовки
        :param text: Рассматриваемый текст
        :return: Текст без заголовков
        """
        articles=[article for article in text.split('\n') if article!='']
        articles=[article for article in articles if not self.chapter_name_classifier.classify_chapter_name(article)]

        return "\n".join(articles)

    def delete_author_notes(self, text):
        """
        Удаляем авторские примечания (в данной версии авторское примечание - это текст в конце каждой страницы,
        начинающийся со '*')
        :param text: Рассматриваемый текст
        :return: текст без авторский примечаний
        """
        articles=[article for article in text.split('\n') if article!='']
        new_articles=[]
        for article in articles:
            is_note=False
            for symbol in article:
                if symbol not in[' ', '\t']:
                    if (symbol=='*'):
                        is_note=True
                    break
            if not is_note:
                new_articles.append(article)

        return "\n".join(new_articles)

    def preprocess(self, text):
        """
        Предобработать текст
        :param text: Обрабатываемый текст
        :return: обработанный текст
        """

        text="".join(re.split(self.delete_exp,text)) #Удалим все ненужные символы

        text=self.delete_chapter_names(text)
        text=self.delete_author_notes(text)

        #Удаляем все числовые последовательности (в том числе и числа-ссылки на примечания)
        new_text=self.delete_numeral_sequence(text)
        while (new_text!=text):
            text=new_text
            new_text = self.delete_numeral_sequence(text)
        regexp='[0123456789]'
        numbers=set([numb for numb in re.findall(regexp,text[:1500])])
        for number in numbers:
            numb_index=text.find(number)
            if numb_index==-1:
                continue
            while (text[numb_index+1]in regexp):
                number+=text[numb_index+1]
                numb_index+=1
            text=self.delete_numeral_sequence(text, int(number))

        return text
