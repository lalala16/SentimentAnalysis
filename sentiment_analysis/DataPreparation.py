#  Author: Yang Kai
#  Date: 9/6/2017
#
#
# *************************************** #
import numpy as np
import pickle
from Document2VecUtility import Document2VecUtility
from Vocabulary import Vocabulary

class DataPreparation(object):
    def __init__(self, original_path, column_x, column_y, single_file=""):

        self.path = original_path
        self.data_x = []
        self.data_y = []
        self.column_x = column_x
        self.column_y = column_y
        self.remove_stopwords = False
        self.stem_words = True
        self.remove_html = False
        self.voc = Vocabulary(self.path)
        self.filelist = ['train.tsv', 'test.tsv', 'dev.tsv']
        self.single_file = single_file
        if len(single_file)==0:
            self.voc.get_vocabulary(self.filelist, self.column_x, self.remove_stopwords, self.stem_words, self.remove_html)
        else:
            self.voc.get_vocabulary([single_file], self.column_x, self.remove_stopwords, self.stem_words,
                                    self.remove_html)
        self.maxlength=self.voc.maxlength
        if len(self.path)==0:
            return 'please give the path to Vocabulary.'

    def get_train_test(self, column_x=3, column_y=2, remove_stopwords=True, stem_words=True, remove_html=False):
        self.voc.save_dict()

        if len(self.single_file)==0:
            train_x=[]
            train_y=[]
            test_x=[]
            test_y=[]
            train_words, result_words = Document2VecUtility.get_x_y(self.path + 'train.tsv', column_x, column_y, remove_stopwords, stem_words, remove_html)
            for line in train_words:
                line_x = []
                for word in line:
                    if self.voc.word2index.has_key(word):
                        line_x.append(self.voc.word2index[word])
                if len(line_x)>self.maxlength:
                    line_x = line_x[:self.maxlength]
                else:
                    for i in range(self.maxlength-len(line_x)):
                        line_x.append(0)
                train_x.append(line_x)
            print 'train size:', len(train_x), len(train_x[0])


            if result_words[0]=='positive' or result_words[0]=='negative':
                for re in result_words:
                    if re=='positive':
                        train_y.append(1)
                    if re=='negative':
                        train_y.append(0)
            if  result_words[0] == 1 or result_words[0] == 0 :
                for item in result_words:
                    train_y.append(item)

            test_words, result_words = Document2VecUtility.get_x_y(self.path + 'test.tsv', column_x, column_y,
                                                                    remove_stopwords, stem_words, remove_html)
            for line in test_words:
                line_x = []
                for word in line:
                    if self.voc.word2index.has_key(word):
                        line_x.append(self.voc.word2index[word])
                if len(line_x) > self.maxlength:
                    line_x = line_x[:self.maxlength]
                else:
                    for i in range(self.maxlength - len(line_x)):
                        line_x.append(0)
                test_x.append(line_x)
            print 'test size:', len(test_x), len(test_x[0])

            if result_words[0] == 'positive' or result_words[0] == 'negative':
                for re in result_words:
                    if re == 'positive':
                        test_y.append(1)
                    if re == 'negative':
                        test_y.append(0)
            if result_words[0] == 1 or result_words[0] == 0:
                for item in result_words:
                    test_y.append(item)
            for item in train_x:
                self.data_x.append(item)
            for item in test_x:
                self.data_x.append(item)
            for item in train_y:
                self.data_y.append(item)
            for item in test_y:
                self.data_y.append(item)
            print 'all x size:', len(self.data_x),len(self.data_x[0])
            print self.data_x[:3]
            print 'all y size:', len(self.data_y)
            print self.data_y[:3]
        else:
            train_words, result_words = Document2VecUtility.get_x_y(self.path + self.single_file, column_x, column_y,
                                                                    remove_stopwords, stem_words, remove_html)
            for line in train_words:
                line_x = []
                for word in line:
                    if self.voc.word2index.has_key(word):
                        line_x.append(self.voc.word2index[word])
                if len(line_x) > self.maxlength:
                    line_x = line_x[:self.maxlength]
                else:
                    for i in range(self.maxlength - len(line_x)):
                        line_x.append(0)
                self.data_x.append(line_x)
            print "data_x:", self.data_x[0][0]
            print 'x size:', len(self.data_x), len(self.data_x[0])
            print 'result_world:', result_words[:20]
            if result_words[0] == 'positive' or result_words[0] == 'negative':
                for re in result_words:
                    if re == 'positive':
                        self.data_y.append(1)
                    if re == 'negative':
                        self.data_y.append(0)
            if result_words[0] == '4' or result_words[0] == '0':
                for item in result_words:
                    if item=='0':
                        self.data_y.append(0)
                    else:
                        self.data_y.append(1)
            print 'y size:', len(self.data_y)
        after_delete_x=[]
        after_delete_y=[]
        for i in range(len(self.data_x)):
            # print i
            # print self.data_x[i]
            if self.data_x[i][0]==0:
                after_delete_x.append(self.data_x[i])
                after_delete_y.append(self.data_y[i])
        self.data_x=after_delete_x
        self.data_y=after_delete_y


    def save_dict(self, file_name):
        # pickle.dump(self.train_x, open(self.path + file_name,'w'))
        # pickle.dump(self.train_y, open(self.path + file_name,'w'))
        # pickle.dump(self.test_y, open(self.path + file_name, 'w'))
        # pickle.dump(self.test_y, open(self.path + file_name, 'w'))
        file = open(self.path + file_name, 'wb')
        pickle.dump(self.data_x, file)
        pickle.dump(self.data_y, file)

    def test_dataset(self,file_name):
        file = open(self.path + file_name, 'rb')
        data_xx = pickle.load(file)
        data_yy = pickle.load(file)

        print np.array(data_xx).shape
        print np.array(data_yy).shape
        for i in range(5):
            print '&&&&&&&&&&&&&'
            print data_xx[i]
            print data_yy[i]


if __name__ == '__main__':
    original_path = '/Users/yangkai/Desktop/hackathon/sentiment-analysis-datasets/tweets-datasets/'
    dp = DataPreparation(original_path,5,0,"training.1600000.processed.noemoticon.csv")
    dp.get_train_test(column_x=5, column_y=0, remove_stopwords=False, stem_words=True, remove_html=False)
    dp.save_dict('dataset.pkl')
    dp.test_dataset('dataset.pkl')







