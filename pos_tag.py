from sklearn import svm
from sklearn.model_selection import train_test_split
import utils


class POSTagger:
    def __init__(self, words, prefix, postfix, tags, text):
        self.__clf = svm.SVC()
        self.__words = words
        self.__prefix = prefix
        self.__postfix = postfix
        self.__tags = tags
        self.__words[''] = utils.make_word_key('', '', None, -1)
        self.__tags[''] = -1
        self.__X, self.__y = self.__build_data(text)

    def __make_vector(self, word, prev):
        if word[:2] not in self.__prefix:
            self.__prefix[word[:2]] = len(self.__prefix)
        if word[:3] not in self.__prefix:
            self.__prefix[word[:3]] = len(self.__prefix)
        if word[-2:] not in self.__postfix:
            self.__postfix[word[-2:]] = len(self.__postfix)
        if word[-3:] not in self.__postfix:
            self.__postfix[word[-3:]] = len(self.__postfix)
        return [self.__tags[prev[0]], self.__tags[prev[1]],
                self.__prefix[word[:2]], self.__prefix[word[:3]]]

    def __build_data(self, text):
        X = []
        y = []
        for wordData in text:
            word, tag, prev = wordData
            if word == 'EOS' or word == 'MARK':
                continue
            X.append(self.__make_vector(word, prev))
            y.append(self.__tags[tag])
        return X, y

    def score(self, size):
        X_train, X_test, y_train, y_test = train_test_split(self.__X, self.__y, test_size=size, random_state=0)
        self.__clf.fit(X_train, y_train)
        return self.__clf.score(X_test, y_test)

    def train(self):
        self.__clf.fit(self.__X, self.__y)

    def tag(self, text):
        ans = []
        prev = ['', '']
        for word in text:
            tag = ''
            if word == 'EOS':
                ans.append(['EOS', 'EOS'])
                prev = ['', '']
                continue
            elif word == 'MARK':
                ans.append(['MARK', 'MARK'])
                continue
            if word in self.__words:
                tag = self.__words[word]['tag']
            else:
                tag_idx = self.__clf.predict([self.__make_vector(word, prev)])[0]
                for key, value in self.__tags.items():
                    if value == tag_idx:
                        tag = key
                        break
            ans.append([word, tag])
            prev.append(tag)
            while len(prev) > 2:
                prev.pop(0)
        return ans
