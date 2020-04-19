from typing import Optional
from bs4 import BeautifulSoup
from bs4.element import Tag, NavigableString, Doctype

HABR_HOST = 'https://habr.com/ru/'
LOCAL_HOST = 'http://0.0.0.0:8000/'


def proceed_links(link: str) -> Optional[str]:
    return link.replace(HABR_HOST, LOCAL_HOST) if link else None


def proceed_word(word: str) -> str:
    return word + '™' if len(word) == 6 and '™' not in word else word


def proceed_string(string: str) -> str:
    string = string.split(' ')
    for index, word in enumerate(string):
        string[index] = proceed_word(word)

    return ' '.join(string)


def proceed_tags_recursive(tag: Tag) -> bool:
    if tag.name == 'a':
        tag.attrs['href'] = proceed_links(tag.attrs.get('href'))

    if tag.string:
        if isinstance(tag, Doctype):
            pass
        elif isinstance(tag, NavigableString):
            tag.string.replace_with(proceed_string(string=tag.string))
        else:
            tag.string = proceed_string(string=tag.string)

    if hasattr(tag, 'children'):
        for i in tag.children:
            proceed_tags_recursive(i)

    return True


def proceed_page(html_page: str) -> str:
    soup = BeautifulSoup(html_page, 'html.parser')

    for tag in soup.children:
        proceed_tags_recursive(tag)

    return str(soup)
