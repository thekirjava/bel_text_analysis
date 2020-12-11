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
        self.__reduce_R()
        self.__reduce_A()
        self.__reduce_S()
        self.__reduce_N()
        self.__reduce_V()

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

    def __reduce_R(self):
        ans = []
        is_prev = False
        buf = None
        for node in self.__nodes:
            if node.tags[0] == 'R' and not is_prev:
                is_prev = True
                buf = node
                continue
            if is_prev and (node.tags[0][0] == 'V' or node.tags[0] == 'W' or node.tags[0] == 'R'):
                is_prev = False
                new_node = Node(buf.words + node.words, reduce(lambda x, y: x + y, node.tags, ''))
                new_node.left = buf
                new_node.right = node
                continue
            elif is_prev:
                ans.append(buf)
            is_prev = False
            ans.append(node)
        if is_prev:
            ans.append(buf)
        self.__nodes = ans

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

    def __reduce_N(self):
        ans = []
        is_prev = False
        buf = None
        for node in self.__nodes:
            if node.tags[0][0] == 'N' and not is_prev:
                is_prev = True
                buf = node
                # print(buf.words)
                continue
            if is_prev and node.tags[0][0] == 'N':
                # print(buf.words)
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
