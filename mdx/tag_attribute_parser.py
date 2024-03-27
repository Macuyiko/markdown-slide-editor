import xml.etree.ElementTree as etree


def parse_attribute_string(string):
    parsed = {'id': None, 'classes': [], 'attrs': {'markdown': '1'}, 'tagname': None, 'closed': False}
    string = string.strip().replace('{', '{ ').replace('}', ' }')
    if string == '':
        return None
    elif not string.startswith('{'):
        parsed['classes'].append(string)
        return parsed
    retained = ''
    for token in string.split():
        if (token.startswith('"') or '="' in token) and not token.endswith('"'):
            retained += token
            continue
        if retained:
            retained += ' ' + token
            if token.endswith('"'):
                token = retained
                retained = ''
            else:
                continue
        if token == '{' or token == '}':
            continue
        elif token.startswith('.'):
            parsed['classes'].append(token[1:])
        elif token.startswith('#'):
            parsed['id'] = token[1:]
        elif token.startswith('/'):
            parsed['closed'] = token.endswith('/')
            parsed['tagname'] = token.strip('/')
        else:
            if '=' in token:
                key, value = token.split('=')
                value = value.strip('"')
                parsed['attrs'][key] = value
            else:
                parsed['attrs'][token] = None
    return parsed

def attributes_to_tag(parsed, default='div', autoclose=False):
    if parsed['tagname']:
        line = '<{}'.format(parsed['tagname'])
    else:
        line = '<{}'.format(default)
    if parsed['closed']:
        return line + '/>'
    if parsed['id']:
        line += ' id="{}"'.format(parsed['id'])
    if parsed['classes']:
        line += ' class="{}"'.format(' '.join(parsed['classes']))
    if parsed['attrs']:
        line += ' ' + ' '.join(['{}="{}"'.format(key, val) for key, val in parsed['attrs'].items() if key != 'tagname'])
    line += '>' if not autoclose else ' />'
    return line

def attributes_to_element(parsed, default='div'):
    if parsed['tagname']:
        el = etree.Element(parsed['tagname'])
    else:
        el = etree.Element(default)
    if parsed['closed']:
        return None
    if parsed['id']:
        el.set('id', parsed['id'])
    if parsed['classes']:
        el.set('class', ' '.join(parsed['classes']))
    if parsed['attrs']:
        for key, val in parsed['attrs'].items():
            el.set(key, val)
    return el

if __name__ == '__main__':
    print(parse_attribute_string('{.class-name-1 .class-name-2 /mark width=400 height="300" #test}'))
    print(parse_attribute_string(' Danger  '))
    print(parse_attribute_string(' {   /span }  '))