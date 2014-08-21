import re


def collect_text(app, model_name, fields):
    from django.db.models.loading import get_model
    texts = []
    model = get_model(app, model_name)
    if not fields:
        print "\n No fields specified for model %s, starting lookup\n\n" % model_name
        modelfields = model._meta.fields
        for field in modelfields:
            if field.__class__.__name__ in [u'CharField', u'TextField'] and field.name != 'id':
                decision = raw_input('Do you want to use field %s? y/n: ' % field.name)
                if decision.lower() in ['y', 'yes']:
                    fields.append(field.name)

    for field in fields:
        objects = model.objects.all()
        for obj in objects:
            texts.append({'model': model,
                          'object_pk': obj.pk,
                          'field': field,
                          'content': getattr(obj, field),
                          'modified': False})

    return texts


def find_text_occurrences(word, text_dict):
    matches = []
    if not len(word) > 0:
        return matches

    content = text_dict.get('content', '')
    model = text_dict.get('model', '')
    field = text_dict.get('field', '')

    rule = r'( |^)%s([ .,?!:;]|$)' % word

    match = re.finditer(rule, content, re.UNICODE | re.IGNORECASE)
    for item in match:
        print 'Found "%s" on %s in model %s, field "%s". Context: "%s"' % (item.group(),
                                                   item.span(), model, field,
                                                   content[item.start() - 30 if item.start() > 30
                                                                                     else 0 :item.end() + 30])
        matches.append({'word': item.group().strip(' .,?!:;'),
                        'start': item.start() if item.group()[0].isalnum() else item.start() + 1,
                        'end': item.end() if item.group()[-1].isalnum() else item.end() - 1})

    return matches


def insert_links_to_text(text, matches, url, target=False, max_occurrence=-1):
    """

    :param text:
    :param matches:
    :param url:
    :param target:
    :param max_occurrence:
    :return:
    """
    offset = 0

    for occurrence, match in enumerate(matches):
        if occurrence == max_occurrence:
            break

        prefix = text['content'][:match['start'] + offset]
        suffix = text['content'][match['end'] + offset:]

        prefix_tag = '<a href="{url}" alt="{alt}" title="{alt}"'.format(url=url, alt=match['word'])
        if target:
            prefix_tag += ' target="' + target + '"'
        prefix_tag += '>'

        suffix_tag = '</a>'
        offset += len(prefix_tag) + len(suffix_tag)

        text['content'] = prefix + prefix_tag + match['word'] + suffix_tag + suffix

        text['modified'] = True
    return text


def add_links(app, model_name, fields, words, url, target=False, occurrence=-1, dry_run=True):
    """

    :param app:
    :param model_name:
    :param fields:
    :param words:
    :param url:
    :param target:
    :param occurrence:
    :param dry_run:
    :return:
    """
    texts = collect_text(app, model_name, fields)
    for word in words:
        for text in texts:
            matches = find_text_occurrences(word, text)
            objects = text['model'].objects.filter(pk=text['object_pk'])
            text = insert_links_to_text(text, matches, url, target, occurrence)
            if not dry_run:
                for item in objects:
                    setattr(item, text['field'], text['content'])
                    item.save()
            else:
                if text['modified']:
                    print '\nModel: %s, field name: %s, modified text:\n' % (text['model'], text['field'])
                    print text['content'] + '\n'
