#  Author: Yang Kai
#  Date: 9/6/2017
#
#
# *************************************** #
import re
import nltk


# from bs4 import BeautifulSoup



class Document2VecUtility(object):


    @staticmethod
    def review_to_word_list( review_text, remove_stopwords=True, stem_words=False, remove_html=False ):

        # Remove HTML
        if remove_html:
            # review_text = BeautifulSoup(review_text).get_text()
            pass

        # Remove non-letters
        review_text = re.sub("[^a-zA-Z]"," ", review_text)

        # Convert words to lower case and split them
        words = review_text.lower().split()

        # Optionally remove stop words (false by default)
        if remove_stopwords:

            stops = set([])
            file_stop = open('en.txt')
            st_line = file_stop.readline()
            while st_line:
                stops.add(st_line.strip())
                st_line = file_stop.readline()
            words = [w for w in words if not w in stops]
        if stem_words:
            words = [nltk.PorterStemmer().stem(w) for w in words]

        return(words)

    @staticmethod
    def get_word_list(file_path, column_num, remove_stopwords=True, stem_words=False, remove_html=False):
        data = []
        file = open(file_path, 'r')
        line = file.readline()
        line_num=0
        while(line):
            line_list = line.split(",")
            data.append(Document2VecUtility.review_to_word_list(line_list[column_num], remove_stopwords, stem_words, remove_html))
            line = file.readline()
            if line_num%10000==0:
                print line_num
                print data[-1]
                print line
            line_num=line_num+1
        file.close()
        return data

    @staticmethod
    def get_x_y(file_path, column_x, column_y, remove_stopwords=True, stem_words=False, remove_html=False):
        data = []
        file = open(file_path, 'r')
        line = file.readline()
        result = []
        line_num=0
        while (line):
            line_list = line.split(",")
            result.append(line_list[column_y][1])
            data.append(Document2VecUtility.review_to_word_list(line_list[column_x], remove_stopwords, stem_words, remove_html))
            line = file.readline()
            if line_num%10000==0:
                print line_num
                print data[-1]
                print line
            line_num = line_num + 1
        file.close()
        return data, result

    @staticmethod
    def review2vec(review_data, maxlength, word2index, remove_stopwords=True, stem_words=True, remove_html=False):
        line_x = []
        new_words = Document2VecUtility.review_to_word_list(review_data, remove_stopwords, stem_words, remove_html)
        for word in new_words:
            if word2index.has_key(word):
                line_x.append(word2index[word])
        if len(line_x) > maxlength:
            line_x = line_x[:maxlength]
        else:
            for i in range(maxlength - len(line_x)):
                line_x.append(0)
        return line_x



if __name__ == '__main__':
    original_path = '/Users/yangkai/Desktop/hackathon/sentiment-analysis-datasets/tweets-datasets/'
    Document2VecUtility.get_word_list(original_path + 'training.1600000.processed.noemoticon.csv', 4)
