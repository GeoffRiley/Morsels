import re
from html.parser import HTMLParser
from typing import List, Tuple, Union


class Markdownify(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self._paragraphs = []
        self._current = None
        self._anchor = None

    def handle_starttag(self, tag: str, attrs: List[Union[Tuple[(str, str)],
                                                          None]]) -> None:
        if self._current is None:
            # self._paragraphs.append(self._current)
            self._current = ''
        if tag == 'p':
            pass
        elif tag == 'br':
            self._current += '  \n'
        elif tag == 'strong':
            self._current += '**'
        elif tag == 'a':
            href = [v for k, v in attrs if k == 'href']
            if href:
                self._anchor = href[0]
            self._current += '['

    def handle_endtag(self, tag: str) -> None:
        if tag == 'p':
            if self._current is not None:
                self._paragraphs.append(self._current)
                self._current = ''
        elif tag == 'strong':
            self._current += '**'
        elif tag == 'a':
            if self._anchor is not None:
                self._current += f']({self._anchor})'
                self._anchor = None
            else:
                self._current += ']'

    def handle_data(self, data: str) -> None:
        if self._current is None:
            self._current = ''
        self._current += data

    def result(self) -> str:
        if self._current:
            self._paragraphs.append(self._current)
        return '\n\n'.join(self._paragraphs)


def markdownify(html: str) -> str:
    parser = Markdownify()
    src = re.sub(r'\s+', ' ', html)
    parser.feed(src)
    return parser.result()
