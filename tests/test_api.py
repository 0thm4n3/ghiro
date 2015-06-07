# Ghiro - Copyright (C) 2013-2015 Ghiro Developers.
# This file is part of Ghiro.
# See the file 'docs/LICENSE.txt' for license terms.

from django.test import Client
from django.test import TestCase

from users.models import Profile
from analyses.models import Case

class AuthenticationTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test", email="a@a.cp,", password="Test")
        self.c = Client()

    def test_fail_new_cas_no_api(self):
        """Tests failed auth with no api key."""
        response = self.c.post("/api/cases/new", {"name": "test", "description": "test"})
        self.assertEqual(response.status_code, 403)

    def test_fail_new_case_wrong_api(self):
        """Tests failed auth with wrong api key."""
        response = self.c.post("/api/cases/new", {"name": "test", "description": "test", "api_key": "aaaaa"})
        self.assertEqual(response.status_code, 403)

    def test_success_new_case(self):
        """Tests success auth.."""
        response = self.c.post("/api/cases/new", {"name": "test", "description": "test", "api_key": self.user.api_key})
        self.assertEqual(response.status_code, 200)

class NewCaseTest(TestCase):
    def setUp(self):
        self.user = Profile.objects.create_user(username="test", email="a@a.cp,", password="Test")
        self.c = Client()

    def test_success_new_case_with_description(self):
        response = self.c.post("/api/cases/new", {"name": "test", "description": "test", "api_key": self.user.api_key})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Case.objects.filter(name="test").exists())

    def test_success_new_case_no_description(self):
        response = self.c.post("/api/cases/new", {"name": "test2", "api_key": self.user.api_key})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Case.objects.filter(name="test2").exists())