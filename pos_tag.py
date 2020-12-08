from sklearn import svm
import utils


class POSTagger:
    def __init__(self, words, prefix, postfix, tags):
        self.__clf = svm.SVC()
        self.__words = words
        self.__prefix = prefix
        self.__postfix = postfix
        self.__tags = tags
        self.__words[''] = utils.make_word_key('', '', None, -1)
        self.__tags[''] = -1

    def __make_vector(self, word, prev):
        if word not in self.__words:
            self.__words[word] = utils.make_word_key(word, word, None, len(self.__words))
        if word[:2] not in self.__prefix:
            self.__prefix[word[:2]] = len(self.__prefix)
        if word[:3] not in self.__prefix:
            self.__prefix[word[:3]] = len(self.__prefix)
        if word[-2:] not in self.__postfix:
            self.__postfix[word[-2:]] = len(self.__postfix)
        if word[-3:] not in self.__postfix:
            self.__postfix[word[-3:]] = len(self.__postfix)
        return [self.__words[word]['id'], self.__tags[prev[0]], self.__tags[prev[1]],
                self.__prefix[word[:2]], self.__prefix[word[:3]], self.__postfix[word[-2:]],
                self.__postfix[word[-3:]]]

    def train(self, text):
        X = []
        y = []
        for wordData in text:
            word, tag, prev = wordData
            if word == 'EOS':
                continue
            X.append(self.__make_vector(word, prev))
            y.append(self.__tags[tag])
        self.__clf.fit(X, y)

    def tag(self, text):
        ans = []
        prev = ['', '']
        for word in text:
            tag = ''
            if word == 'EOS':
                prev = ['', '']
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
            if self.__words[word]['tag'] is None:
                self.__words[word]['tag'] = tag
            while len(prev) > 2:
                prev.pop(0)
        return ans
