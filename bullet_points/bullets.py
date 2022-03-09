from collections import UserList
from dataclasses import dataclass, field
from textwrap import indent
from typing import List, Optional, Tuple


class BulletList(UserList['Bullet']):
    def __str__(self) -> str:
        return '\n'.join(str(r) for r in self.data)

    def filter(self, filter_by: str) -> 'BulletList':
        filter_by = filter_by.casefold()
        result = BulletList()
        for item in self:
            if filter_by in str(item).casefold():
                result.append(Bullet(item.text))
                if inside := item.children.filter(filter_by):
                    result[-1].children.extend(inside)
        return result


@dataclass
class Bullet:
    text: str
    children: BulletList = field(default_factory=BulletList)
    parent: Optional['Bullet'] = field(default=None)

    # def __repr__(self) -> str:
    #     return f'{self.__class__.__name__}(text="{self.text}")'

    def __str__(self) -> str:
        s = '\n' + indent('\n'.join(
            str(kid)
            for kid in self.children), '    ') if self.children else ''
        return f'- {self.text}{s}'


def parse_bullets(text: str) -> BulletList:
    root: BulletList = BulletList()
    stack: List[Bullet] = []
    last_indent = 0
    for line in text.splitlines(keepends=False):
        this_indent, line = extract_indent(line)
        bullet = Bullet(line[2:])

        # indent of zero is a base entry, resetting all lower levels
        if this_indent == 0:
            root.append(bullet)
            stack = [bullet]
        else:
            # a greater indent means this is a subentry check the last
            # indent to discover if it's a new descent
            if this_indent != last_indent:
                stack = stack[:this_indent]
                stack.append(bullet)
            else:
                stack[-1] = bullet
            stack[-2].children.append(bullet)
            bullet.parent = stack[-2]

        last_indent = this_indent

    return root


def extract_indent(line: str, depth_count: int = 0) -> Tuple[int, str]:
    while line.startswith('    '):
        depth_count += 1
        line = line[4:]
    return depth_count, line

    # return [
    #     Bullet(line.lstrip(' -')) for line in text.splitlines(keepends=False)
    # ]
