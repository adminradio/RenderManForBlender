import re


def hashnum(template, number):
    """
    Replace any group of hashes with the number, if needed fill with zeros.
    """
    def repl(match):
        hashnum = len(match.group(1))
        return str(number).zfill(hashnum)

    template = re.sub('(#+)', repl, template)

    return template
