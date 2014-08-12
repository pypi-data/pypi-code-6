import re
from django.db.models.loading import get_model


def collect_text(app, model_name, fields):
    texts = []
    model = get_model(app, model_name)
    for field in fields:
        objects = model.objects.all()
        for obj in objects:
            texts.append({'model': model,
                          'object_pk': obj.pk,
                          'field': field,
                          'content': getattr(obj, field),
                          'modified': False})

    return texts


def find_text_occurrences(word, text):
    matches = []
    if len(word) > 0:
        rule = r'( |^)%s([ .,?!:;]|$)' % word

        match = re.finditer(rule, text, re.UNICODE | re.IGNORECASE)
        for item in match:
            print 'Found "%s" on %s. Context: "%s"' % (item.group(),
                                                       item.span(),
                                                       text[item.start() - 30 if item.start() > 30 else 0 :item.end() + 30])
            matches.append({'word': item.group().strip(' .,?!:;'),
                            'start': item.start() if item.group()[0].isalnum() else item.start() + 1,
                            'end': item.end() if item.group()[-1].isalnum() else item.end() - 1})

    return matches


def add_links(text, matches, url):
    offset = 0

    for match in matches:
        prefix = text['content'][:match['start'] + offset]
        suffix = text['content'][match['end'] + offset:]

        prefix_tag = '<a href="{url}" alt="{alt}" title="{alt}">'.format(url=url, alt=match['word'])
        suffix_tag = '</a>'
        offset += len(prefix_tag) + len(suffix_tag)

        text['content'] = prefix + prefix_tag + match['word'] + suffix_tag + suffix

        text['modified'] = True

    return text


def add_permalinks(app, model_name, fields, words, url, dry_run=True):
    texts = collect_text(app, model_name, fields)
    for word in words:
        for text in texts:
            matches = find_text_occurrences(word, text['content'])
            objects = text['model'].objects.filter(pk=text['object_pk'])
            text = add_links(text, matches, url)
            if not dry_run:
                for item in objects:
                    setattr(item, text['field'], text['content'])
                    item.save()
            else:
                if text['modified']:
                    print '\nModified text:\n'
                    print text['content'] + '\n'
