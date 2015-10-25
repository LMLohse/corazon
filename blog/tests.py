from django.test import TestCase


class SimpleTests(TestCase):
    def test_archive(self):
        response = self.client.get('/blog/archive/')
        self.assertEqucal(response.status_code, 200)