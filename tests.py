import json
import unittest
from multiprocessing import Process

import requests

from app import run

headers = {'Authorization': 'Basic cm9vdDpwd2Q=', 'user': 'root'}


class APITestSuit(unittest.TestCase):
    def test_auth_invalid_request(self):
        _headers = {'NotAuthorization': 'Basic cm9vdDpwd2Q=', 'user': 'root'}
        response = requests.get('http://127.0.0.1:8000/products',
                                headers=_headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.text), {'msg': 'Invalid header'})

    def test_auth_unauthorized_request(self):
        _headers = {'Authorization': 'Basic cm9vdDpwd2Q=', 'user': 'Notroot'}
        response = requests.get('http://127.0.0.1:8000/products',
                                headers=_headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            json.loads(response.text), {'msg': 'Unauthorized request'})

    def test_get_all_products(self):
        response = requests.get('http://127.0.0.1:8000/products',
                                headers=headers)
        self.assertEqual(response.status_code, 200)
        jsonObj = json.loads(response.text)
        self.assertEqual(jsonObj['foo'],
                         {'id': 'foo',
                          'seller': 'bar',
                          'price': '99'})

    def test_get_item_not_found(self):
        response = requests.get('http://127.0.0.1:8000/products/test',
                                headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.text), {'msg': 'Item not found'})

    def test_get_invalid_url(self):
        response = requests.get('http://127.0.0.1:8000/products/test/test1',
                                headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.text), {'msg': 'Invalid endpoint'})

    def test_post_product(self):
        response = requests.post(
            'http://127.0.0.1:8000/products',
            headers=headers,
            json={'id': 'bar',
                  'seller': 'foo',
                  'price': '49'})
        self.assertEqual(response.status_code, 201)
        response = requests.get('http://127.0.0.1:8000/products/bar',
                                headers=headers)
        self.assertEqual(
            json.loads(response.text),
            {'price': '49',
             'id': 'bar',
             'seller': 'foo'})

    def test_delete_product(self):
        requests.post(
            'http://127.0.0.1:8000/products',
            headers=headers,
            json={'id': 'bar',
                  'seller': 'foo',
                  'price': '49'})
        response = requests.delete(
            'http://127.0.0.1:8000/products/bar', headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.text), {'msg': 'Item deleted successfully'})

    def test_delete_item_not_found(self):
        response = requests.delete(
            'http://127.0.0.1:8000/products/test', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.text), {'msg': 'Item not found'})

    def test_delete_invalid_url(self):
        response = requests.delete(
            'http://127.0.0.1:8000/products/test/test1', headers=headers)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.text), {'msg': 'Invalid endpoint'})

    def test_put_product(self):
        requests.post(
            'http://127.0.0.1:8000/products',
            headers=headers,
            json={'id': 'bar',
                  'seller': 'foo',
                  'price': '49'})
        response = requests.get('http://127.0.0.1:8000/products/bar',
                                headers=headers)
        self.assertEqual(
            json.loads(response.text),
            {'price': '49',
             'id': 'bar',
             'seller': 'foo'})
        requests.post(
            'http://127.0.0.1:8000/products',
            headers=headers,
            json={'id': 'bar',
                  'seller': 'foo',
                  'price': '109'})
        response = requests.get('http://127.0.0.1:8000/products/bar',
                                headers=headers)
        self.assertEqual(
            json.loads(response.text),
            {'price': '109',
             'id': 'bar',
             'seller': 'foo'})


if __name__ == '__main__':
    p1 = Process(target=run)
    p1.start()
    p2 = Process(target=unittest.main)
    p2.start()
    p2.join()
    p1.terminate()
