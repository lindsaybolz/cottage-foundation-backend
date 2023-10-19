from django.test import TestCase, Client
# from django.test.utils import setup_test_environment
from django.urls import reverse
from rest_api.models import Person
import json

# setup_test_environment()

# Create your tests here.
def create_person(email):
    return Person.objects.create(email=email)

class PersonViewsTests(TestCase):
    def test_email_list_no_people(self):
        response = self.client.get(reverse("rest_api:emails"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])        

    def test_email_list_one_person(self):
        person = create_person('testingOnePerson@gmail.com')
        response = self.client.get(reverse("rest_api:emails"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"id":3,"email":"testingOnePerson@gmail.com"}])

    def test_email_list_two_people(self):
        person1 = create_person('testingOnePerson@gmail.com')
        person2 = create_person('testingTwoPerson@gmail.com')
        response = self.client.get(reverse("rest_api:emails"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"id":4,"email":"testingOnePerson@gmail.com"},{"id":5,"email":"testingTwoPerson@gmail.com"}])

    def test_create_person_valid(self):
        new_email_body = {"email":"newEmail1@gmail.com"}
        response = self.client.post(reverse("rest_api:add"), new_email_body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"id":1, "email": "newEmail1@gmail.com"})

    def test_create_person_invalid_email(self):
        new_email_body = {'email': "testingNotARealEmail"}
        response = self.client.post(reverse("rest_api:add"), new_email_body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'][0].title(), 'Enter A Valid Email Address.')

    def test_create_person_no_email_key(self):
        new_email_body = {'emails': "testingNotARealEmail"}
        response = self.client.post(reverse("rest_api:add"), new_email_body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['email'][0].title(), 'This Field Is Required.')

    def test_get_one_email_valid_id(self):
        person5 = create_person('testingPerson6@gmail.com')
        # print('valid one get: ', Person.objects.all()[0].pk)
        response = self.client.get(reverse("rest_api:one_email", kwargs={'pk': 6}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'id': 6, 'email': 'testingPerson6@gmail.com'})

    def test_get_one_email_invalid_id(self):
        response = self.client.get(reverse("rest_api:one_email", kwargs={'pk': 6}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'].title(), 'Not Found.') 

    def test_put_one_email_valid(self):
        person6 = create_person('testing9@gmail.com')
        # print('valid one: ', Person.objects.all()[0].pk)
        data = {'email': 'testing9updated@gmail.com'}
        response = self.client.put(reverse("rest_api:one_email", kwargs={'pk': 9}), data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {'id': 9, 'email': 'testing9updated@gmail.com'})

    def test_put_one_email_invalid(self):
        person6 = create_person('testing6@gmail.com')
        # print('invalid one: ', Person.objects.all()[0].pk)
        data = {'email': 'testing6updatedInvalid'}
        response = self.client.put(reverse("rest_api:one_email", kwargs={'pk': 7}), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'][0].title(), "Enter A Valid Email Address.")

    def test_put_one_email_invalid_dict(self):
        person6 = create_person('testing7@gmail.com')
        # print('invalid dict: ', Person.objects.all()[0].pk)
        data = {'Noemail': 'testing7updated@gmail.com'}
        response = self.client.put(reverse("rest_api:one_email", kwargs={'pk': 8}), data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['email'][0].title(), "This Field Is Required.")

    def test_put_one_email_invalid_not_found(self):
        data = {'email': 'testing7updated@gmail.com'}
        response = self.client.put(reverse("rest_api:one_email", kwargs={'pk': 20}), data, content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'].title(), "Not Found.")

    def test_delete_successfully(self):
        personDelete = create_person('testingDelete@gmail.com')
        # print('success delete: ', Person.objects.all()[0].pk)
        response = self.client.delete(reverse("rest_api:one_email", kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 204)
        self.assertEqual(response.data, {'Message': 'Successfully deleted'})

    def test_delete_unsuccessful_not_found(self):
        response = self.client.delete(reverse("rest_api:one_email", kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data['detail'].title(), 'Not Found.')