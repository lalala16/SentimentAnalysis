#  Author: Yang Kai
#  Date: 9/6/2017
#
#
# *************************************** #
import pickle
from Document2VecUtility import Document2VecUtility


class Vocabulary(object):
    def __init__(self, original_path=""):
        self.word2index = {}
        self.index2word = {}
        self.wordcount = {}
        self.maxlength = -1
        self.path = original_path
        self.filter_set=set(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
                         'p','q','r','s','t','u','v','w','x','y','z'])
        if len(self.path)==0:
            return 'please give the path to Vocabulary.'

    def get_vocabulary(self, file_list=[], column_num=4, remove_stopwords=False, stem_words=True, remove_html=False):
        for file_name in file_list:
            tem_data = Document2VecUtility.get_word_list(self.path + file_name, column_num, remove_stopwords, stem_words, remove_html)
            print 'read ready~'


            for line in tem_data:
                if len(line)>self.maxlength and len(line)<=1000:
                    self.maxlength = len(line)
                for word in line:
                    if self.wordcount.has_key(word):
                        self.wordcount[word] = self.wordcount[word] + 1
                    else:
                        self.wordcount[word] = 1
        sort_count = sorted(self.wordcount.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)

        index=1
        # for word in self.wordcount.keys():
        #     self.word2index[word] = index
        #     self.index2word[index] = word
        #     index = index + 1
        # start_pos=0
        # end_pos=30000

        top_count=33365
        for count_tuple in sort_count:
            word = count_tuple[0]
            if word not in self.filter_set:
                self.word2index[word] = index
                self.index2word[index] = word
                index = index+1
                if index>top_count:
                    break

        self.word2index[""] = 0
        self.index2word[0] = ""
        print "*************"
        print 'wordset: ',len(self.wordcount)
        print 'w2i:', len(self.word2index)
        print 'i2w', len(self.index2word)

    def save_dict(self):
        file = open(self.path+'dictionary.pkl','wb')
        pickle.dump(self.word2index, file)
        pickle.dump(self.index2word, file)

    def save_wordcount(self):

        tt=sorted(self.wordcount.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
        f1 = open(self.path+'count.txt','w+')
        for key in tt:
            f1.write(str(key[0])+":"+str(key[1])+"\n")
        f1.close()

if __name__ == '__main__':

    original_path = '/Users/yangkai/Desktop/hackathon/sentiment-analysis-datasets/tweets-datasets/'
    voc = Vocabulary(original_path)
    # Document2VecUtility.get_wordlist(original_path + 'train.tsv', 3)
    filelist = ['training.1600000.processed.noemoticon.csv']
    # filelist = ['train.tsv','test.tsv','dev.tsv']
    voc.get_vocabulary(filelist, column_num=5)
    # voc.save_dict()
    voc.save_wordcount()






