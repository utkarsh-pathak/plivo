
from django.test import TestCase

# Create your tests here.
# from django.utils import unittest
from .models import ContactBook
import unittest, json
from django.test.client import RequestFactory
from .views import ContactBookCRUD

class SimpleTest(unittest.TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        # ContactBook.objects.create(name="test_plivo", email_address="test_plivo@gmail.com")

    def test_create(self):
        # Create an instance of a Post request.
        dummy_data = {"name": "dummy_1", "email_address": "dummy1_plivo_11@gmail.com"}
        request = self.factory.post('/plivo/', data=dummy_data)
        c = ContactBookCRUD.as_view()
        response = c(request)
        self.assertEqual(response.status_code, 201)

    def test_get(self):
        # Create a row to fetch later in the methdo
        dummy_data = {"name": "dummy_1", "email_address": "dummy1_plivo@gmail.com"}
        request = self.factory.post('/plivo/', data=dummy_data)
        c = ContactBookCRUD.as_view()
        response = c(request)
        self.assertEqual(response.status_code, 201)

        ## test value returned from POST API
        if response.status_code == 201:
            resp_str = response._container[0].decode('utf-8')
            resp_dict = json.loads(resp_str)
            id = resp_dict["res_data"]["id"]
        
            ## test get method

            request = self.factory.get('/plivo/?id=' + str(id))
            c = ContactBookCRUD.as_view()
            response = c(request)
            self.assertEqual(response.status_code, 200, msg="Get API Fails while getting valid ID from DB")


    def test_delete(self):

        # Create a row to fetch later in the methdo
        dummy_data = {"name": "dummy_1", "email_address": "dummyplivo@gmail.com"}
        request = self.factory.post('/plivo/', data=dummy_data)
        c = ContactBookCRUD.as_view()
        response = c(request)
        self.assertEqual(response.status_code, 201)


        if response.status_code == 201:
            resp_str = response._container[0].decode('utf-8')
            resp_dict = json.loads(resp_str)
            id = resp_dict["res_data"]["id"]

            request = self.factory.delete('/plivo/' + str(id) + '/')
            c = ContactBookCRUD.as_view()
            response = c(request)
            self.assertEqual(response.status_code, 205, msg="Delete API Fails")
        
    
    def test_update(self):

        # Create a row to fetch later in the methdo
        dummy_data = {"name": "dummy_1", "email_address": "dummy_plivo_1@gmail.com"}
        request = self.factory.post('/plivo/', data=dummy_data)
        c = ContactBookCRUD.as_view()
        response = c(request)
        self.assertEqual(response.status_code, 201)


        if response.status_code == 201:
            resp_str = response._container[0].decode('utf-8')
            resp_dict = json.loads(resp_str)
            id = resp_dict["res_data"]["id"]

            dummy_data = {"name": "mod_plivo_1"}
            request = self.factory.put('/plivo/' + str(id) + '/')
            c = ContactBookCRUD.as_view()
            response = c(request, id)
            self.assertEqual(response.status_code, 200, msg="Update API Fails")

        