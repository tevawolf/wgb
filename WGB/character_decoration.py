import re


class CharacterDecoration:

    BIG = '%b'
    SMALL = '%s'
    BOLD = '%bl'
    STRIKE = '%st'
    COLOR = '%c'
    REGEX = r'.*?'

    def decorate(self, text):
        text = self.decorate_bold(text)
        text = self.decorate_strike(text)
        text = self.decorate_big(text)
        text = self.decorate_small(text)
        text = self.decorate_color(text)
        return text

    def decorate_big(self, text):
        match = re.search(self.BIG + self.REGEX + self.BIG, text)
        while match:
            t = match.group().replace(self.BIG, '<span style=\"font-size: x-large;\">', 1)
            t = t.replace(self.BIG, '</span>', 1)
            text = text.replace(match.group(), t, 1)
            match = re.search(self.BIG + self.REGEX + self.BIG, text)
        return text

    def decorate_small(self, text):
        match = re.search(self.SMALL + self.REGEX + self.SMALL, text)
        while match:
            t = match.group().replace(self.SMALL, '<span style=\"font-size: x-small;\">', 1)
            t = t.replace(self.SMALL, '</span>', 1)
            text = text.replace(match.group(), t, 1)
            match = re.search(self.SMALL + self.REGEX + self.SMALL, text)
        return text

    def decorate_bold(self, text):
        match = re.search(self.BOLD + self.REGEX + self.BOLD, text)
        while match:
            t = match.group().replace(self.BOLD, '<span style=\"font-weight: bold;\">', 1)
            t = t.replace(self.BOLD, '</span>', 1)
            text = text.replace(match.group(), t, 1)
            match = re.search(self.BOLD + self.REGEX + self.BOLD, text)
        return text

    def decorate_strike(self, text):
        match = re.search(self.STRIKE + self.REGEX + self.STRIKE, text)
        while match:
            t = match.group().replace(self.STRIKE, '<span style=\"text-decoration:line-through;\">', 1)
            t = t.replace(self.STRIKE, '</span>', 1)
            text = text.replace(match.group(), t, 1)
            match = re.search(self.STRIKE + self.REGEX + self.STRIKE, text)
        return text

    def decorate_color(self, text):
        code_regex = r'\[#?[a-zA-Z0-9]*\]'

        match = re.search(code_regex + self.COLOR + self.REGEX + self.COLOR, text)
        while match:
            color = re.search(code_regex, match.group())
            if not color:
                raise ValueError

            color_code = color.group().replace('[', '').replace(']', '')

            t = match.group().replace(self.COLOR, '<span style=\"color:{};\">'.format(color_code), 1)
            t = t.replace(color.group(), '', 1)
            t = t.replace(self.COLOR, '</span>', 1)
            text = text.replace(match.group(), t, 1)
            match = re.search(self.COLOR + self.REGEX + self.COLOR, text)
        return text


if __name__ == '__main__':
    cd = CharacterDecoration()
    print(cd.decorate('jiofa[red]%cisdjfi%coasjdf'))
