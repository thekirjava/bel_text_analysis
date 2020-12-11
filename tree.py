from functools import reduce


class Node:
    def __init__(self, word, tag):
        self.words = [word]
        if tag == 'MARK':
            self.tags = [tag]
        elif tag[0] == 'A' or tag[0] == 'M' or tag[0] == 'P' or tag[0] == 'S':
            self.tags = [tag[0], tag[1:]]
        elif tag[0] == 'N':
            self.tags = [tag[:4], tag[4:]]
        elif tag[0] == 'V':
            self.tags = [tag[:3], tag[3:]]
        else:
            self.tags = [tag]
        self.left = None
        self.right = None

    def __str__(self):
        return str(self.words) + str(self.tags)


class Tree:
    def __init__(self, text):
        self.__nodes = [Node(word[0], word[1]) for word in text]
        self.__root = None

    def reduce(self):
        self.__reduce_C_E_I()
        self.__reduce_marked_C_E_I()
        self.__reduce_S()
        self.__reduce_R()
        self.__reduce_A()
        self.__reduce_N()
        self.__reduce_V()
        self.__reduce_MARKS()
        self.__reduce_marked_N()
        self.__reduce_marked_V()
        self.__reduce_sentence_part()

    def get(self):
        return self.__nodes

    def get_root(self):
        if self.__root is None:
            self.reduce()
        return self.__root

    def __reduce_C_E_I(self):
        ans = []
        is_prev = False
        buf = None
        for node in self.__nodes:
            if (node.tags[0] == 'E' or node.tags[0] == 'I' or node.tags[0] == 'C') and not is_prev:
                is_prev = True
                buf = node
                continue
            if is_prev and node.words[0] != 'MARK':
                is_prev = False
                new_node = Node(buf.words + node.words, reduce(lambda x, y: x + y, node.tags, ''))
                new_node.left = buf
                new_node.right = node
                ans.append(new_node)
                continue
            elif is_prev:
                ans.append(buf)
            ans.append(node)
            is_prev = False
        if is_prev:
            ans.append(buf)
        self.__nodes = ans
        retry = False
        is_prev = False
        for node in self.__nodes:
            if retry:
                break
            retry = is_prev and node.words[0] != 'MARK'
            if node.tags[0] == 'E' or node.tags[0] == 'I' or node.tags[0] == 'C':
                is_prev = True
            else:
                is_prev = False
        if retry:
            self.__reduce_C_E_I()

    def __reduce_R(self):
        ans = []
        is_prev = False
        buf = None
        for node in self.__nodes:
            if node.tags[0] == 'R' and (not is_prev):
                is_prev = True
                buf = node
                continue
            if is_prev and (node.tags[0][0] == 'V' or node.tags[0] == 'W' or node.tags[0] == 'R'):
                is_prev = False
                new_node = Node(buf.words + node.words, reduce(lambda x, y: x + y, node.tags, ''))
                new_node.left = buf
                new_node.right = node
                ans.append(new_node)
                continue
            elif is_prev:
                ans.append(buf)
            is_prev = False
            ans.append(node)
        if is_prev:
            ans.append(buf)
        self.__nodes = ans
        retry = False
        is_prev = False
        for node in self.__nodes:
            if retry:
                break
            retry = is_prev and (node.tags[0][0] == 'V' or node.tags[0] == 'W' or node.tags[0] == 'R')
            if node.tags[0] == 'R' and (not is_prev):
                is_prev = True
            else:
                is_prev = False
        if retry:
            self.__reduce_R()

    def __reduce_A(self):
        ans = []
        is_prev = False
        buf = None
        for node in self.__nodes:
            if node.tags[0] == 'A' and not is_prev:
                is_prev = True
                buf = node
                continue
            if is_prev and (node.tags[0] == 'A' or node.tags[0][0] == 'N'):
                is_prev = False
                new_node = Node(buf.words + node.words, reduce(lambda x, y: x + y, node.tags, ''))
                new_node.left = buf
                new_node.right = node
                ans.append(new_node)
                continue
            elif is_prev and node.words[0] == 'MARK':
                continue
            elif is_prev:
                ans.append(buf)
            is_prev = False
            ans.append(node)
        if is_prev:
            ans.append(buf)
        self.__nodes = ans
        retry = False
        is_prev = False
        for node in self.__nodes:
            if retry:
                break
            retry = is_prev and (node.tags[0] == 'A' or node.tags[0][0] == 'N')
            if node.tags[0][0] == 'A' and (not is_prev):
                is_prev = True
            else:
                is_prev = False
        if retry:
            self.__reduce_A()

    def __reduce_S(self):
        ans = []
        is_prev = False
        buf = None
        for node in self.__nodes:
            if node.tags[0] == 'S' and not is_prev:
                is_prev = True
                buf = node
                continue
            if is_prev and (node.tags[0][0] == 'V' or node.tags[0][0] == 'N' or node.tags[0] == 'S'):
                is_prev = False
                new_node = Node(buf.words + node.words, reduce(lambda x, y: x + y, node.tags, ''))
                new_node.left = buf
                new_node.right = node
                ans.append(new_node)
                continue
            elif is_prev:
                ans.append(buf)
            is_prev = False
            ans.append(node)
        if is_prev:
            ans.append(buf)
        self.__nodes = ans
        retry = False
        is_prev = False
        for node in self.__nodes:
            if retry:
                break
            retry = is_prev and (node.tags[0][0] == 'V' or node.tags[0][0] == 'N' or node.tags[0] == 'S')
            if node.tags[0] == 'S' and (not is_prev):
                is_prev = True
            else:
                is_prev = False
        if retry:
            self.__reduce_S()

    def __reduce_N(self):
        ans = []
        is_prev = False
        buf = None
        for node in self.__nodes:
            if node.tags[0][0] == 'N' and not is_prev:
                is_prev = True
                buf = node
                continue
            if is_prev and node.tags[0][0] == 'N':
                is_prev = False
                new_node = Node(buf.words + node.words, reduce(lambda x, y: x + y, node.tags, ''))
                new_node.left = buf
                new_node.right = node
                ans.append(new_node)
                continue
            elif is_prev:
                ans.append(buf)
            is_prev = False
            ans.append(node)
        if is_prev:
            ans.append(buf)
        self.__nodes = ans
        retry = False
        is_prev = False
        for node in self.__nodes:
            if retry:
                break
            retry = is_prev and node.tags[0][0] == 'N'
            if node.tags[0][0] == 'N' and (not is_prev):
                is_prev = True
            else:
                is_prev = False
        if retry:
            self.__reduce_N()

    def __reduce_V(self):
        ans = []
        is_prev = False
        buf = None
        for node in self.__nodes:
            if node.tags[0][0] == 'V' and not is_prev:
                is_prev = True
                buf = node
                continue
            if is_prev and node.tags[0][0] == 'V':
                is_prev = False
                new_node = Node(buf.words + node.words, reduce(lambda x, y: x + y, node.tags, ''))
                new_node.left = buf
                new_node.right = node
                ans.append(new_node)
                continue
            elif is_prev:
                ans.append(buf)
            is_prev = False
            ans.append(node)
        if is_prev:
            ans.append(buf)
        self.__nodes = ans
        retry = False
        is_prev = False
        for node in self.__nodes:
            if retry:
                break
            retry = is_prev and node.tags[0][0] == 'V'
            if node.tags[0][0] == 'V' and (not is_prev):
                is_prev = True
            else:
                is_prev = False
        if retry:
            self.__reduce_V()

    def __reduce_marked_C_E_I(self):
        i = 0
        while i < len(self.__nodes):
            if (self.__nodes[i].tags[0] == 'C' or self.__nodes[i].tags[0] == 'C' or self.__nodes[i].tags[0] == 'C') and \
                    self.__nodes[i + 1].words[0] == 'MARK':
                j = i + 2
                while self.__nodes[j].words[0] != 'MARK':
                    j += 1
                j += 1
                new_node = Node(self.__nodes[i].words + self.__nodes[j].words,
                                reduce(lambda x, y: x + y, self.__nodes[j].tags, ''))
                new_node.left = self.__nodes[i]
                new_node.right = self.__nodes[j]
                self.__nodes[j] = new_node
                self.__nodes.pop(i)
                i -= 1
            i += 1

    def __reduce_MARKS(self):
        i = 0
        while i < len(self.__nodes):
            if self.__nodes[i].words[0] == 'MARK':
                if i == 1 or i + 2 == len(self.__nodes) or self.__nodes[i - 1].words[0][0] == \
                        self.__nodes[i + 1].words[0][0]:
                    self.__nodes.pop(i)
                    continue
            i += 1

    def __reduce_marked_N(self):
        i = 0
        prev = None
        while i < len(self.__nodes):
            if self.__nodes[i].tags[0][0] == 'N' and prev is None:
                prev = i
            elif self.__nodes[i].tags[0][0] == 'N' and prev is not None:
                new_node = Node(self.__nodes[prev].words + self.__nodes[i].words,
                                reduce(lambda x, y: x + y, self.__nodes[i].tags, ''))
                new_node.left = self.__nodes[prev]
                new_node.right = self.__nodes[i]
                self.__nodes[i] = new_node
                self.__nodes.pop(prev)
                i -= 1
                prev = None
            elif self.__nodes[i].words[0] == 'MARK':
                prev = None
            i += 1

    def __reduce_marked_V(self):
        i = 0
        prev = None
        while i < len(self.__nodes):
            if self.__nodes[i].tags[0][0] == 'V' and prev is None:
                prev = i
            elif self.__nodes[i].tags[0][0] == 'V' and prev is not None:
                new_node = Node(self.__nodes[prev].words + self.__nodes[i].words,
                                reduce(lambda x, y: x + y, self.__nodes[i].tags, ''))
                new_node.left = self.__nodes[prev]
                new_node.right = self.__nodes[i]
                self.__nodes[i] = new_node
                self.__nodes.pop(prev)
                i -= 1
                prev = None
            elif self.__nodes[i].words[0] == 'MARK':
                prev = None
            i += 1

    def __reduce_sentence_part(self):
        ans = []
        for i in range(len(self.__nodes)):
            if i % 3 != 0 or i + 1 == len(self.__nodes):
                continue
            new_node = Node(self.__nodes[i].words + self.__nodes[i + 1].words,
                            'SPART')
            new_node.left = self.__nodes[i]
            new_node.right = self.__nodes[i + 1]
            ans.append(new_node)
        self.__nodes = ans
