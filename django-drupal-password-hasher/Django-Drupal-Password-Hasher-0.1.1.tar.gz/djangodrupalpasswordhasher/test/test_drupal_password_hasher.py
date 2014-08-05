import hashlib
import os, sys, shutil
from model_mommy.mommy import make
from django.conf import settings
from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from drupalPassHash import DrupalPasswordHasher, DrupalPasswordHasherInvalidHashException

class DrupalPasswordHasherTest(TestCase):
    """
    Test the drupal password hasher for bugs
    """
    def setUp(self):
        super(DrupalPasswordHasherTest, self).setUp()

    def test_pass_hash(self):
        """
        Test the password hasher on a previously created user 
        """
        password = "thequickbrownfoxjumpsoverthelazydog"
        self.user = make(User)
        self.user.set_password(password)
        self.user.save()
        self.assertTrue(self.user.check_password(password))

    def test_no_user(self):
        """
        Test the password hashing functions without using
        a user model
        """
        hasher = DrupalPasswordHasher()
        password = "thequickbrownfoxjumpsoverthelazydog"
        encoded = hasher.encode(password, hasher.salt())
        self.assertTrue(check_password(password, encoded))

    def test_verify(self):
        """
        Test the verify function
        """
        hasher = DrupalPasswordHasher()
        password = "thequickbrownfoxjumpsoverthelazydog"
        encoded = hasher.encode(password, hasher.salt())
        self.assertTrue(hasher.verify(password, encoded))

    def test_verify_old(self):
        """
        Test the verify function when the password comes 
        from an old (emulated) drupal version
        """
        hasher = DrupalPasswordHasher()
        password = "thequickbrownfoxjumpsoverthelazydog"
        digest = '$P$'
        salt = hasher.salt() 
        settings = {
            'count': 1 << hasher._DRUPAL_HASH_COUNT,
            'salt': salt
        }
        encoded_hash = hasher._apply_hash(password, hasher._digests[digest], settings)
        encoded = "drupal$U$P$" + hasher._itoa64[hasher._DRUPAL_HASH_COUNT] + salt + encoded_hash 
        self.assertFalse(hasher.verify(password, encoded))

    def test_bad_digest(self):
        """
        Test the verify function with a bad digest
        """
        hasher = DrupalPasswordHasher()
        password = "thequickbrownfoxjumpsoverthelazydog"
        encoded = hasher.encode(password, hasher.salt())
        temp = encoded.split("$", 1)[1]
        temp = temp[2:]
        encoded = "drupal$$F" + temp
        with self.assertRaises(DrupalPasswordHasherInvalidHashException):
            hasher.verify(password, encoded)

    def test_safe_summary(self):
        """
        Test the safe summary function
        """
        hasher = DrupalPasswordHasher()
        password = "thequickbrownfoxjumpsoverthelazydog"
        encoded = hasher.encode(password, hasher.salt())
        dict = hasher.safe_summary(encoded)
        self.assertEqual(dict['algorithm'], 'drupal')
        self.assertTrue(dict['iterations'] > 0)
        self.assertEqual(len(dict['salt']),8)
        self.assertEqual(len(dict['hash']), hasher._DRUPAL_HASH_LENGTH - 12)

    def test_must_update(self):
        """
        Test the must update function
        """
        hasher = DrupalPasswordHasher()
        password = "thequickbrownfoxjumpsoverthelazydog"
        hash =  hashlib.md5(password).hexdigest()
        encoded = "drupal$U$H$" + hash
        self.assertTrue(hasher.must_update(encoded))

