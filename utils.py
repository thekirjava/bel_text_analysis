def read_txt(filename):
    ans = []
    with open(filename, 'r') as file:
        for line in file:
            for word in line.split():
                word = word.strip(".,:;!?'\"(){}[]\\/|1234567890+-=—«»<>")
                if len(word) == 0:
                    continue
                word = word.lower()
                if word[0] == 'ў':
                    word = 'у' + word[1:]
                ans.append(word)
    return ans


def make_word_key(lemma, form, tag, idx):
    return {'lemma': lemma, 'prefix_two': form[:2], 'prefix_three': form[:3],
            'postfix_two:': form[-2:], 'postfix_three': form[-3:], 'tag': tag,
            'id': idx}
