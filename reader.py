import xml.etree.ElementTree as et
import utils


class Reader:
    def __init__(self, filename):
        self.__postfix_map = {}
        self.__prefix_map = {}
        self.__word_map = {}
        self.__tag_map = {}
        tree = et.parse(filename)
        self.__root = tree.getroot()

    def __make_key(self, lemma, form, tag):
        if form in self.__word_map:
            return
        if form[:2] not in self.__prefix_map:
            self.__prefix_map[form[:2]] = len(self.__prefix_map)
        if form[:3] not in self.__prefix_map:
            self.__prefix_map[form[:3]] = len(self.__prefix_map)
        if form[-2:] not in self.__postfix_map:
            self.__postfix_map[form[-2:]] = len(self.__postfix_map)
        if form[-3:] not in self.__postfix_map:
            self.__postfix_map[form[-3:]] = len(self.__postfix_map)
        self.__word_map[form] = utils.make_word_key(lemma, form, tag, len(self.__word_map))
        if tag not in self.__tag_map:
            self.__tag_map[tag] = len(self.__tag_map)

    def open(self, filename):
        tree = et.parse(filename)
        self.__root = tree.getroot()

    def parse(self):
        self.__postfix_map = {}
        self.__prefix_map = {}
        self.__word_map = {}
        self.__tag_map = {}
        for child in self.__root:
            lemma = child.attrib['lemma']
            lemma = lemma.replace('+', '')
            main_tag = child.attrib['tag']
            if main_tag[0] == 'N' and len(lemma) == 1:
                continue
            for variant in child:
                for form in variant:
                    if form.tag == 'Form':
                        word_form = form.text
                    else:
                        continue
                    if word_form is None:
                        continue
                    word_form = word_form.replace('+', '')
                    tag = main_tag[0]
                    self.__make_key(lemma, word_form, tag)
        return self.__word_map, self.__prefix_map, self.__postfix_map, self.__tag_map
