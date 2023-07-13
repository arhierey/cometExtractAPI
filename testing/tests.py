import unittest
import requests


class UnitTesting(unittest.TestCase):
    def test_invalid_credentials(self):
        response = requests.post('http://localhost:8000/fetch',
                                 json={'email': 'user1@examplecom', 'password': 'pass123'})
        self.assertEqual(response.status_code, 400)

    def test_no_email(self):
        response = requests.post('http://localhost:8000/fetch',
                                 json={'email': '', 'password': 'pass123'})
        self.assertEqual(response.status_code, 400)

    def test_no_password(self):
        response = requests.post('http://localhost:8000/fetch',
                                 json={'email': 'user1@example.com', 'password': ''})
        self.assertEqual(response.status_code, 400)

    def test_no_credentials(self):
        response = requests.post('http://localhost:8000/fetch')
        self.assertEqual(response.status_code, 415)


if __name__ == '__main__':
    unittest.main()
