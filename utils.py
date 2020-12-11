def read_txt(filename):
    ans = []
    with open(filename, 'r') as file:
        for line in file:
            end_of_sentence = False
            for word in line.split():
                is_marked = False
                if word[0].isupper() and end_of_sentence:
                    ans.append("EOS")
                if word[-1] in ".!?»":
                    end_of_sentence = True
                else:
                    end_of_sentence = False
                    if not word[-1].isalpha():
                        is_marked = True
                word = word.strip(".,:;!?'\"(){}[]\\/|1234567890+-=—«»<>")
                if len(word) == 0:
                    continue

                word = word.lower()
                if word[0] == 'ў':
                    word = 'у' + word[1:]
                ans.append(word)
                if is_marked:
                    ans.append('MARK')
    return ans


def make_word_key(lemma, form, tag, idx):
    return {'lemma': lemma, 'prefix_two': form[:2], 'prefix_three': form[:3],
            'postfix_two:': form[-2:], 'postfix_three': form[-3:], 'tag': tag,
            'id': idx}
