from datetime import datetime

import pytest

from jsonmapper import *


def test_validate():
    class Person(Mapping):
        name = TextField()
        age = IntegerField()
        added = DateTimeField(default=datetime.now)
        office = TextField(default=None)

    p = Person(name='John Doe', age=42)
    p.validate()

    # Wrong value for age.
    p = Person.wrap({
        'name': 'John Doe',
        'age': 'a string',
    })
    with pytest.raises(ValueError):
        p.validate()

    # No value for age.
    p = Person()
    with pytest.raises(ValueError):
        p.validate()

    p = Person.wrap({
        'name': 'John Doe',
        'age': 42,
        'unknown': 'data',
    })
    with pytest.raises(ValueError):
        p.validate()
    p.validate(allow_extras=True)


def test_embedded_validation():
    class Post(Mapping):
        title = TextField()
        content = TextField()
        author = DictField(Mapping.build(
            name = TextField(),
            email = TextField()
        ))
        extra = DictField()

    class Blog(Mapping):
        posts = ListField(DictField(Post))

    my_post = Post(title='My Post', content='content')
    with pytest.raises(ValueError):
        my_post.validate()

    blog = Blog(posts=[my_post])
    with pytest.raises(ValueError):
        blog.validate()

    my_post.author.name = 'Adam'
    my_post.author.email = 'adam@example.com'
    my_post.validate()
    blog.validate()

    class ArbitraryMapping(Mapping):
        dict_field = DictField(Mapping.build(
            req_field=TextField(),
            opt_field=TextField(default=None),
        ))

    am = ArbitraryMapping()
    with pytest.raises(ValueError):
        am.validate()

    am.dict_field.req_field = 'Some text'
    am.validate()
