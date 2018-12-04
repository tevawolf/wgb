import re


class CharacterDecoration:

    big = '%b'
    small = '%s'
    bold = '%bl'
    strike = '%st'
    color = '%c'
    regex = r'[^\x01-\x7E]*[a-zA-Z]*[0-9]*[ｦ-ﾟ]*[ -/:-@\[-~]*'

    def decorate(self, text):
        text = self.decorate_bold(text)
        text = self.decorate_strike(text)
        text = self.decorate_big(text)
        text = self.decorate_small(text)
        text = self.decorate_color(text)
        return text

    def decorate_big(self, text):
        match = re.search(self.big + self.regex + self.big, text)
        while match:
            t = match.group().replace(self.big, '<span style=\"font-size: x-large;\">', 1)
            t = t.replace(self.big, '</span>', 1)
            text = text.replace(match.group(), t, 1)
            match = re.search(self.big + self.regex + self.big, text)
        return text

    def decorate_small(self, text):
        match = re.search(self.small + self.regex + self.small, text)
        while match:
            t = match.group().replace(self.small, '<span style=\"font-size: x-small;\">', 1)
            t = t.replace(self.small, '</span>', 1)
            text = text.replace(match.group(), t, 1)
            match = re.search(self.small + self.regex + self.small, text)
        return text

    def decorate_bold(self, text):
        match = re.search(self.bold + self.regex + self.bold, text)
        while match:
            t = match.group().replace(self.bold, '<span style=\"font-weight: bold;\">', 1)
            t = t.replace(self.bold, '</span>', 1)
            text = text.replace(match.group(), t, 1)
            match = re.search(self.bold + self.regex + self.bold, text)
        return text

    def decorate_strike(self, text):
        match = re.search(self.strike + self.regex + self.strike, text)
        while match:
            t = match.group().replace(self.strike, '<span style=\"text-decoration:line-through;\">', 1)
            t = t.replace(self.strike, '</span>', 1)
            text = text.replace(match.group(), t, 1)
            match = re.search(self.strike + self.regex + self.strike, text)
        return text

    def decorate_color(self, text):
        code_regex = r'\[#?[a-zA-Z]*[0-9]*\]'

        match = re.search(code_regex + self.color + self.regex + self.color, text)
        while match:
            color = re.search(code_regex, match.group())
            if not color:
                raise ValueError

            color_code = color.group().replace('[', '').replace(']', '')

            t = match.group().replace(self.color, '<span style=\"color:{};\">'.format(color_code), 1)
            t = t.replace(color.group(), '', 1)
            t = t.replace(self.color, '</span>', 1)
            text = text.replace(match.group(), t, 1)
            match = re.search(self.color + self.regex + self.color, text)
        return text


if __name__ == '__main__':
    cd = CharacterDecoration()
    print(cd.decorate('jiofa[red]%cisdjfi%coasjdf'))
