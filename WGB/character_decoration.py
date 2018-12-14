import re


class CharacterDecoration:

    BIG = '%b'
    SMALL = '%s'
    BOLD = '%bl'
    STRIKE = '%st'
    COLOR = '%c'
    REGEX = r'.*?'
    ANCHOR = r'&gt;&gt;[0-9]*'
    URL = r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'

    def decorate(self, text, number=0):
        text = self.decorate_bold(text)
        text = self.decorate_strike(text)
        text = self.decorate_big(text)
        text = self.decorate_small(text)
        text = self.decorate_color(text)
        if number != 0:
            text = self.decorate_anchor(text, number)
        return text

    def decorate_big(self, text):
        iterator = re.finditer(self.BIG + self.REGEX + self.BIG, text)
        for match in iterator:
            t = match.group().replace(self.BIG, '<span style=\"font-size: x-large;\">', 1)
            t = t.replace(self.BIG, '</span>', 1)
            text = text.replace(match.group(), t, 1)
        return text

    def decorate_small(self, text):
        iterator = re.finditer(self.SMALL + self.REGEX + self.SMALL, text)
        for match in iterator:
            t = match.group().replace(self.SMALL, '<span style=\"font-size: x-small;\">', 1)
            t = t.replace(self.SMALL, '</span>', 1)
            text = text.replace(match.group(), t, 1)
        return text

    def decorate_bold(self, text):
        iterator = re.finditer(self.BOLD + self.REGEX + self.BOLD, text)
        for match in iterator:
            t = match.group().replace(self.BOLD, '<span style=\"font-weight: bold;\">', 1)
            t = t.replace(self.BOLD, '</span>', 1)
            text = text.replace(match.group(), t, 1)
        return text

    def decorate_strike(self, text):
        iterator = re.finditer(self.STRIKE + self.REGEX + self.STRIKE, text)
        for match in iterator:
            t = match.group().replace(self.STRIKE, '<span style=\"text-decoration:line-through;\">', 1)
            t = t.replace(self.STRIKE, '</span>', 1)
            text = text.replace(match.group(), t, 1)
        return text

    def decorate_color(self, text):
        code_regex = r'\[#?[a-zA-Z0-9]*\]'

        iterator = re.finditer(code_regex + self.COLOR + self.REGEX + self.COLOR, text)
        for match in iterator:
            color = re.search(code_regex, match.group())
            if not color:
                raise ValueError

            color_code = color.group().replace('[', '').replace(']', '')

            t = match.group().replace(self.COLOR, '<span style=\"color:{};\">'.format(color_code), 1)
            t = t.replace(color.group(), '', 1)
            t = t.replace(self.COLOR, '</span>', 1)
            text = text.replace(match.group(), t, 1)
        return text

    def decorate_anchor(self, text, from_number):
        iterator = re.finditer(self.ANCHOR, text)
        for match in iterator:
            to_number = match.group().replace('&gt;&gt;', '')
            t = '<a id="anchor_from_{0}_to_{1}" href="javascript:void(0);" onclick=\"showAnchorWindow({0}, {1});\">'.format(from_number, to_number) + match.group() + '</a>'
            text = text.replace(match.group(), t, 1)
        return text

    def decorate_url(self, text):
        iterator = re.finditer(self.URL, text)
        for match in iterator:
            t = '<a href="{0}" target="_blank">'.format(match.group()) + match.group() + '</a>'
            text = text.replace(match.group(), t, 1)
        return text


if __name__ == '__main__':
    cd = CharacterDecoration()
    print(cd.decorate('jiofa[red]%cisdjfi%coasjdf'))
