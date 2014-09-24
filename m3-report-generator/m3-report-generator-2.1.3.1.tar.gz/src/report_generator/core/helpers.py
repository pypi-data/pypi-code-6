#coding: utf-8

import json

from m3.actions import ControllerCache

# Вспомогательные функции

def get_packs():
    """
    Возвращает паки проекта
    Необходимо для праметров запроса
    """

    if not ControllerCache.get_controllers():
        ControllerCache.populate()

    for controller in ControllerCache.get_controllers():
        for pack in controller.get_packs():
            if hasattr(pack, 'get_select_url') and callable(
                pack.get_select_url
            ):
                yield dict(name=unicode(pack.__class__.__name__),
                           verbose_name=unicode(
                               pack.verbose_name or
                               pack.title or
                               pack.__class__.__name__
                           ),
                           absolute_url=unicode(pack.absolute_url()))

def action_on_tree(element, sub_element_key, action, **kwargs):
    """
    Обход дерева с действием.
    Используется алгоритм обхода в ширину
    :param element - элемент, содержащий себе подобных
    :param sub_element_key - ключ под которым в элементе содержатся ему подобные.
    :param action - функция, которая выполняется на узлах дерева
           **kwargs - параметры, которые ей передадим.
    """

    root = dict(element=element, visit=False)
    queue = [root]

    while queue:
        node = queue.pop()

        if not node.get('visit'):
            element = node.get('element')

            action(element, kwargs)

            for sub_element in node.get('element').get(sub_element_key):
                child_node = dict(element=sub_element, visit=False)
                queue.append(child_node)


def serialize_result(f):
    """
    Сериализует результат, возвращаемый функцией
    """

    def wrapper(obj):

        res = f(obj)

        return json.dumps(res)

    return wrapper
