# -*- coding: utf-8 -*-
# vi:si:et:sw=4:sts=4:ts=4

def wrap(string, length, separator, balance):
    if balance:
        # balance lines: test if same number of lines
        # can be achieved with a shorter line length
        lines = wrap(string, length, separator, False).split(separator)
        if len(lines) > 1:
            while length > max(map(lambda x : len(x), string.split(' '))):
                length -= 1
                if len(wrap(string, length, separator, False).split(separator)) > len(lines):
                    length += 1
                    break
    words = string.split(' ')
    lines = ['']
    for word in words:
        if len(lines[len(lines) - 1] + word + ' ') <= length + 1:
            # word fits in current line
            lines[len(lines) - 1] += word + ' ';
        else:
            if len(word) <= length:
                # word fits in next line
                lines.append(word + ' ')
            else:
                # word is longer than line
                position = length - len(lines[len(lines) - 1]) + 1
                lines[len(lines) - 1] += word[0:position]
                for i in range(position, len(word), length):
                    lines.append(word[i:i+length]);
                lines[len(lines) - 1] += ' '
    return separator.join(lines).strip()
