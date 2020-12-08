import utils


class Tagger:
    def __init__(self, word_map, filename):
        self.__data = utils.read_txt(filename)
        self.___word_map = word_map

    def open(self, filename):
        self.__data = utils.read_txt(filename)

    def set_word_map(self, word_map):
        self.___word_map = word_map

    def tag(self):
        ans = []
        prev = ['', '']
        for word in self.__data:
            if word == "EOS":
                prev = ['', '']
                ans.append(("EOS", "EOS", ['', '']))
                continue
            if word in self.___word_map:
                ans.append((word, self.___word_map[word]['tag'], prev.copy()))
                prev.append(self.___word_map[word]['tag'])
                while len(prev) > 2:
                    prev.pop(0)
            else:
                print(word)
        return ans
