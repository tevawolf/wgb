from django.test import TestCase
from . import models


class UserAccountTests(TestCase):
    def test_blank_icon(self):
        account = models.UserAccount()
        account.username = 'test'
        account.password = 'test'
        account.nickname = 'test'
        account.save()

        saved = models.UserAccount.objects.get(username='test')
        self.assertEqual(saved.username, 'test')

