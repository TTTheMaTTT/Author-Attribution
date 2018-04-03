from TextInstruments.Tokenizers import Simple_Tokenizer
from TextInstruments.SentenceDividers import Simple_Sentence_Divider
from TextInstruments.ChapterDividers import Simple_Chapter_Name_Classifier
from TextInstruments.Preprocessors import Simple_Preprocessor
from TextInstruments.TextChunksCreators import  Simple_Text_Chunk_Creator
from TextInstruments.DatasetCreator import Simple_RNN_Dataset_Creator
import os
import jsonpickle

authors_path="D:\Chisto Moya Papka!!!\Works\Phystech\Интеллектуальные системы\Author Attribution\DatasetRaw"
savepath="D:\Chisto Moya Papka!!!\Works\Phystech\Интеллектуальные системы\Author Attribution\Dataset"
author_list=['Белый Андрей',]


dataset_creator=Simple_RNN_Dataset_Creator(Simple_Tokenizer(remove_numerals=False),Simple_Sentence_Divider(),
                                           Simple_Chapter_Name_Classifier, Simple_Preprocessor, Simple_Text_Chunk_Creator)

result=dataset_creator.process_text(authors_path=authors_path,author_list=author_list,savepath=savepath)

print("Everything is Awesome")
#print(result)
