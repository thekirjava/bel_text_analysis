import xml.etree.ElementTree as et


class Reader:
    def __init__(self, filename):
        self.__postfix_map = {}
        self.__prefix_map = {}
        self.__word_map = {}
        tree = et.parse(filename)
        self.__root = tree.getroot()

    def __make_key(self, lemma, form, tag):
        if form[:2] not in self.__prefix_map:
            self.__prefix_map[form[:2]] = len(self.__prefix_map)
        if form[:3] not in self.__prefix_map:
            self.__prefix_map[form[:3]] = len(self.__prefix_map)
        if form[-2:] not in self.__postfix_map:
            self.__postfix_map[form[-2:]] = len(self.__postfix_map)
        if form[-3:] not in self.__postfix_map:
            self.__postfix_map[form[-3:]] = len(self.__postfix_map)
        self.__word_map[lemma] = {'lemma': lemma, 'prefix_two': form[:2], 'prefix_three': form[:3],
                                  'postfix_two:': form[-2:], 'postfix_three': form[-3:], 'tag': tag,
                                  'id': len(self.__word_map)}

    def open(self, filename):
        tree = et.parse(filename)
        self.__root = tree.getroot()

    def parse(self):
        self.__postfix_map = {}
        self.__prefix_map = {}
        self.__word_map = {}
        for child in self.__root:
            lemma = child.attrib['lemma']
            lemma = lemma.replace('+', '')
            self.__make_key(lemma, lemma, child.attrib['tag'])
            for variant in child:
                for form in variant:
                    if form.tag == 'Form':
                        word_form = form.text
                    else:
                        continue
                    if word_form is None:
                        continue
                    word_form = word_form.replace('+', '')
                    self.__make_key(lemma, word_form, child.attrib['tag'])
        return [self.__word_map, self.__prefix_map, self.__postfix_map]
