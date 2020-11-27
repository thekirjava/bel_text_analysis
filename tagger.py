class Tagger:
    def __init__(self, word_map, filename):
        self.__data = []
        with open(filename, 'r') as file:
            for line in file:
                for word in line.split():
                    word = word.strip(".,!?'\"(){}[]\\/1234567890+-=")
                    self.__data.append(word)
        self.___word_map = word_map

    def open(self, filename):
        self.__data = []
        with open(filename, 'r') as file:
            for line in file:
                for word in line.split():
                    word = word.strip(".,!?'\"(){}[]\\/1234567890+-=")
                    self.__data.append(word)

    def set_word_map(self, word_map):
        self.___word_map = word_map

    def tag(self):
        ans = []
        for word in self.__data:
            if word in self.___word_map:
                ans.append((word, self.___word_map[word]['tag']))
        return ans
