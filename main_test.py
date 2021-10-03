import unittest
import requests
from unittest.mock import patch
from main import postdata

"""
С данным заданием не справился, очень хотелось бы услышать фидбек, 
при запросе post/delete/put у меня выдает ошибку 405
т.е. в теории работать должно, но приложение не дает внести изменения
"""

class ApiTest(unittest.TestCase):
    API_URL = 'http://127.0.0.1:5000/api/task/'
    GET_URL = "http://127.0.0.1:5000/api/task/get_all"
    TASK_URL = '{}'.format(API_URL)
    TASK_OBJ = {
        'title': 'Enter title7',
        'content': 'Enter content7'
}
    TASK_OBJ_NEW = {
        'title': 'Enter title8',
        'content': 'Enter content8'
    }

    def test_1_get_all(self):
        r = requests.get(ApiTest.GET_URL)
        self.assertEqual(r.status_code, 200)

    def test_2_add_new_task(self):
        r = requests.post(ApiTest.API_URL, json=ApiTest.TASK_OBJ)
        self.assertEqual(r.status_code, 200)


    def test_3_get_new_task(self):
        id = 2
        r = requests.get('{}'.format(ApiTest.API_URL, id))
        self.assertEqual(r.status_code, 200)

    def test_3_delete_new_task(self):
        id = 2
        r = requests.delete('{}'.format(ApiTest.API_URL, id))
        self.assertEqual(r.status_code, 200)

    def test_3_put_new_task(self):
        id = 2
        s = requests.put(ApiTest.API_URL, json=ApiTest.TASK_OBJ_NEW)
        self.assertEqual(s.status_code, 200)