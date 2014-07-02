# -*- coding:utf-8 -*-
import unittest
from datetime import datetime
import os
os.environ["DJANGO_SETTINGS_MODULE"] = "djangosqlash.tests.settings"
from django.db import models


class Group(models.Model):
    name = models.CharField("NAME", max_length=255)
    created_at = models.DateTimeField(default=lambda: datetime(1999, 12, 31))


class User(models.Model):
    group = models.ForeignKey(Group)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=lambda: datetime(1999, 12, 31))


class A0(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=lambda: datetime(1999, 12, 31))


class A1(models.Model):
    a0 = models.ForeignKey(A0)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=lambda: datetime(1999, 12, 31))


class A2(models.Model):
    a1 = models.ForeignKey(A1)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=lambda: datetime(1999, 12, 31))


class Team(models.Model):
    name = models.CharField("NAME", max_length=255)
    created_at = models.DateTimeField(default=lambda: datetime(1999, 12, 31))


class Member(models.Model):
    teams = models.ManyToManyField(Team)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=lambda: datetime(1999, 12, 31))


def datetime_for_human(dt, r):
    return dt.strftime("%Y/%m/%d %H:%M:%S")


def int_for_human(v, r):
    return "this is {}".format(v)


class BasicCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        from djangosqlash.testing import create_table
        create_table(Group)
        create_table(User)

    def _getTarget(self):
        from djangosqlash import SerializerFactory
        return SerializerFactory

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_simple(self):
        target = self._makeOne({})()
        group = Group(id=1, name="foo")
        result = target.serialize(group, ["name"])
        self.assertEqual(result, {"name": "foo"})

    def test_convert(self):
        from datetime import datetime
        from django.db.models import DateTimeField
        target = self._makeOne({DateTimeField: datetime_for_human})()
        group = Group(id=1, name="foo", created_at=datetime(2000, 1, 1))
        result = target.serialize(group, ["created_at"])
        self.assertEqual(result, {'created_at': '2000/01/01 00:00:00'})

    def test_foreignkey(self):
        from django.db.models import IntegerField
        user = User(id=1)
        user.group_id = 1
        target = self._makeOne({IntegerField: int_for_human})()
        result = target.serialize(user, ["group_id"])
        self.assertEqual(result, {'group_id': 'this is 1'})

    def test_relation_onetomany(self):
        from datetime import datetime
        from djangosqlash import Pair

        target = self._makeOne()()
        group = Group(id=1, name="foo")
        group.user_set.add(User(id=1, group=group, name="boo", created_at=datetime(2000, 1, 1)))
        group.user_set.add(User(id=2, group=group, name="yoo", created_at=datetime(2000, 1, 1)))
        result = target.serialize(group, ["name", Pair("user_set", ["name"])])
        self.assertEqual(result, {'user_set': [{'name': 'boo'}, {'name': 'yoo'}], 'name': 'foo'})

    def test_relation_manytoone(self):
        from datetime import datetime
        from djangosqlash import Pair

        target = self._makeOne()()
        group = Group(id=1, name="foo")
        group.user_set.add(User(id=1, group=group, name="boo", created_at=datetime(2000, 1, 1)))
        group.user_set.add(User(id=2, group=group, name="yoo", created_at=datetime(2000, 1, 1)))
        result = target.serialize(group.user_set.get(pk=1), ["name", Pair("group", ["name"])])
        self.assertEqual(result, {'group': {'name': 'foo'}, 'name': 'boo'})

    def test_abbreviation(self):
        from datetime import datetime
        from django.db.models import IntegerField, DateTimeField, AutoField

        user = User(name="foo", created_at=datetime(2000, 1, 1))
        target = self._makeOne({IntegerField: int_for_human,
                                AutoField: int_for_human,
                                DateTimeField: datetime_for_human})()
        result = target.serialize(user, ["*"])
        self.assertEqual(result, {'name': 'foo', 'created_at': '2000/01/01 00:00:00', 'id': 'this is None'})

    def test_renaming(self):
        from datetime import datetime
        from django.db.models import IntegerField, DateTimeField, AutoField

        user = User(name="foo", created_at=datetime(2000, 1, 1))
        factory = self._makeOne({IntegerField: int_for_human,
                                AutoField: int_for_human,
                                DateTimeField: datetime_for_human})
        target = factory({"name": "Name", "created_at": "CreatedAt", "id": "Id"})
        result = target.serialize(user, ["*"])
        self.assertEqual(result, {'Name': 'foo', 'CreatedAt': '2000/01/01 00:00:00', 'Id': 'this is None'})


class NestedCaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        from djangosqlash.testing import create_table
        create_table(A0)
        create_table(A1)
        create_table(A2)

    def _getTarget(self):
        from djangosqlash import SerializerFactory
        return SerializerFactory

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_deep_nested(self):
        from django.db.models import DateTimeField
        from datetime import datetime
        from djangosqlash import Pair

        target = self._makeOne({DateTimeField: datetime_for_human})()
        a2 = A2(id=1, a1=A1(id=1, a0=A0(id=1, created_at=datetime(2000, 1, 1))))
        result = target.serialize(a2, [Pair("a1", [Pair("a0", ["created_at"])])])
        assert result == {'a1': {'a0': {'created_at': '2000/01/01 00:00:00'}}}


class ManyToManyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from djangosqlash.testing import create_table, _setup_db
        _setup_db()
        create_table(Team)
        create_table(Member)

    def _getTarget(self):
        from djangosqlash import SerializerFactory
        return SerializerFactory

    def _makeOne(self, *args, **kwargs):
        return self._getTarget()(*args, **kwargs)

    def test_many_to_many(self):
        from django.db.models import DateTimeField
        from djangosqlash import Pair

        target = self._makeOne({DateTimeField: datetime_for_human})()

        team0 = Team(id=1, name="foo"); team0.save()
        team1 = Team(id=2, name="boo"); team1.save()
        member0 = Member(id=1, name="x"); member0.save()
        member1 = Member(id=2, name="y"); member1.save()
        member2 = Member(id=3, name="z"); member2.save()
        team0.member_set.add(member0)
        team0.member_set.add(member1)
        team1.member_set.add(member1)
        team1.member_set.add(member2)
        result = target.serialize(team0, ["name", "created_at", Pair("member_set", ["name", "created_at"])])
        self.assertEqual(result, {'created_at': '1999/12/31 00:00:00',
                                  'member_set': [{'created_at': '1999/12/31 00:00:00', 'name': 'x'},
                                                 {'created_at': '1999/12/31 00:00:00', 'name': 'y'}], 'name': 'foo'})

    def test_many_to_many_reverse(self):
        from django.db.models import DateTimeField
        from djangosqlash import Pair

        target = self._makeOne({DateTimeField: datetime_for_human})()

        team0 = Team(id=1, name="foo"); team0.save()
        team1 = Team(id=2, name="boo"); team1.save()
        member0 = Member(id=1, name="x"); member0.save()
        member1 = Member(id=2, name="y"); member1.save()
        member2 = Member(id=3, name="z"); member2.save()
        team0.member_set.add(member0)
        team0.member_set.add(member1)
        team1.member_set.add(member1)
        team1.member_set.add(member2)
        result = target.serialize(member1, ["name", "created_at", Pair("teams", ["name", "created_at"])])
        self.assertEqual(result, {'name': 'y',
                                  'created_at': '1999/12/31 00:00:00',
                                  'teams': [{'name': 'foo', 'created_at': '1999/12/31 00:00:00'},
                                            {'name': 'boo', 'created_at': '1999/12/31 00:00:00'}]})
