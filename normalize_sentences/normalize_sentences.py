import re

EMBEDED = re.compile(r'(Dr|P.S|e.g)([.?!])(\s+?)')
EMBEDED2 = re.compile(r'([\w]+?)([.?!])([\w]+?)')

SENTENCE = re.compile(r'(?<!¤)([.!?])[ \t]*(?!\d|\w\.|\n|$)')


def normalize_sentences(text: str) -> str:
    new_text = EMBEDED.sub(r'\1¤\2¤\3', text)
    new_text = EMBEDED2.sub(r'\1¤\2¤\3', new_text)
    new_text = SENTENCE.sub(r'\1  ', new_text)
    new_text = new_text.replace('¤', '')
    return new_text
