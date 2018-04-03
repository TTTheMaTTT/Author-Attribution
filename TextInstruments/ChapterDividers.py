# Здесь будут находиться различные классы, предназначенные для разбиения текста по главам

# Простейший классификатор того, является ли данный кусок текста оглавлением чего-то
class Simple_Chapter_Name_Classifier:
    def __init__(self, tokenizer, special_words=['глава', 'часть', 'i', 'x', 'v', 'c', 'l'],
                 sentence_symbols=["!", "?"], min_words_count=10):
        """
        :param tokenizer: Токенизатор, который может считать слова
        :param special_words: Специальные слова, часто использующиеся в оглавлениях
        :param sentence_symbols: Служебные символы, использующиеся в предложениях. А предложений в оглавлениях не бывает
        :param min_words_count: Минимум кол-ва слов, превысив которое, текст не считается оглавлением
        """
        self.tokenizer = tokenizer
        self.special_words = special_words
        self.sentence_symbols = sentence_symbols
        self.min_words_count = min_words_count

    def classify_chapter_name(self, text):
        """
        Определить, является ли данный текст оглавлением
        :param text: Рассматриваемый текст
        :return: True, значит, текст является оглавлением
        """
        for sentence_symbol in self.sentence_symbols:
            if text.find(sentence_symbol) != -1:
                return False  # считаем, что в оглавлении нет места вопросам и восклицаниям

        words_count = self.tokenizer.count_words(text)
        if words_count == 0:
            return False  # В оглавлении должны быть хоть какие-то слова
        if words_count > self.min_words_count:
            return False  # Считаем, что в оглавлении не может быть так много слов

        if (text == text.upper()):
            return True  # Текст состоит лишь из больших букв

        if text[-1] in self.sentence_symbols or text[-1] == '.':
            return True

        for special_word in self.special_words:
            if text.lower().find(special_word) != -1:
                return True  # В тексте есть специальное слово, обычно использующееся для оглавлений

        # Несомненно, на все эти правила можно найти случаи, которые будут проходиться неправильно, но скорее всего этого не
        # произойдёт на практике

        return True

#Простой разделитель текста на части, начинающиеся с оглавлений
class Simple_Chapter_Divider:

    def __init__(self, chapter_name_classifier, include_chapter_name=False):
        """
        :param chapter_name_classifier: Классификатор названия главы
        :param include_chapter_name: Включать ли название главы в текст?
        """
        self.chapter_name_classifier=chapter_name_classifier
        self.include_chapter_name=include_chapter_name

    def divide_to_chapters(self, text):
        """
        Делим текст на части
        :param text: Рассматриваемый текст
        :return: list из частей разделённого текста
        """
        chapters=[]
        chapter=""
        chapter_name=""
        articles=[article for article in text.split('\n') if article!='']
        for i, article in enumerate(articles):
            if self.chapter_name_classifier.classify_chapter_name(article):
                if (chapter!=""):
                    if (self.include_chapter_name):
                        chapter=chapter_name+'\n'+chapter
                    chapters.append(chapter)
                    chapter=""
                    chapter_name=article
            else:
                chapter+='\n'+article

        if (chapter != ""): #Нужно добавить последнюю часть
            if (self.include_chapter_name):
                chapter = chapter_name + '\n' + chapter
            chapters.append(chapter)

        return chapters


