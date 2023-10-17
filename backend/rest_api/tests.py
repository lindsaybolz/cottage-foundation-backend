from django.test import TestCase, Client
# from django.test.utils import setup_test_environment
from django.urls import reverse
from rest_api.models import Person

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
        self.assertEqual(response.data, [{"id":2,"email":"testingOnePerson@gmail.com"}])

    def test_email_list_two_people(self):
        person1 = create_person('testingOnePerson@gmail.com')
        person2 = create_person('testingTwoPerson@gmail.com')
        response = self.client.get(reverse("rest_api:emails"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [{"id":3,"email":"testingOnePerson@gmail.com"},{"id":4,"email":"testingTwoPerson@gmail.com"}])

    def test_create_person_valid(self):
        new_email_body = {"email":"newEmail1@gmail.com"}
        response = self.client.post(reverse("rest_api:add"), new_email_body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"id":1, "email": "newEmail1@gmail.com"})

    def test_create_person_invalid_email(self):
        new_email_body = {'email': "testingNotARealEmail"}
        response = self.client.post(reverse("rest_api:add"), new_email_body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'Error': 'The email you entered was invalid, please try again in this format: {"email": "email@company.com"}'})

    def test_create_person_no_email_key(self):
        new_email_body = {'emails': "testingNotARealEmail"}
        response = self.client.post(reverse("rest_api:add"), new_email_body)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'Error': 'Data must be in the format {"email": "email@company.com"}'})

    def test_get_one_email_valid_id(self):
        # person5 = create_person('testingPerson5@gmail.com')
        response = self.client.get(reverse("rest_api:one_email", kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"id":5,"email":"testingPerson5@gmail.com"})
