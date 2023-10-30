import collections
import re


PATTERN = re.compile(
    r'(?P<word>\w+)(?P<filler>[^\w\n]+)(?P<whore>whore)',
    flags=re.IGNORECASE
)


class Whorpus:

    def __init__(self, text):

        self.text = text
        self.matches = list(PATTERN.finditer(text))

    def concordances(self):

        for match in self.matches:

            start, end = match.span('whore')
            before = self.text[:start].split('\n')[-1]
            after = self.text[end:].split('\n')[0]

            yield before, match.group('whore'), after

    def count(self):

        return collections.Counter([x.group('word') for x in self.matches])
