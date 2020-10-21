import re
def pad_sequence(sequence,n):
    sequence = iter(sequence)
    return sequence
def ngrams(sequence,n):
    sequence = pad_sequence(sequence,n)
    history = []
    while n>1:
        try:
            next_item = next(sequence)
        except StopIteration:
            return
        history.append(next_item)
        n-=1
    for item in sequence:
        history.append(item)
        yield tuple(history)
        del history[0]

select = "I am a manager"
pat = '[a-zA-Z]+'
tokens = re.findall(pat,select)


