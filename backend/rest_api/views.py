from rest_framework.views import APIView
from rest_api.models import Person
from rest_api.serializer import PersonSerializer
from rest_framework.response import Response
from rest_framework import status
import re


def valid_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False

class EmailList(APIView):
    def get(self, request):
        emails = Person.objects.all()
        serializer = PersonSerializer(emails, many=True)
        return Response(serializer.data)

    
class PersonCreate(APIView):
    def validate_data(self, data):
        if not data.get('email'):
            return 'Needs email in key'
        elif not valid_email(data['email']):
            return 'Invalid email'
        else:
            return True
        
    def post(self, request):
        validity = self.validate_data(request.data)
        if validity == 'Invalid email':
            return Response({
                "Error": "The email you entered was invalid, please try again in this format: {\"email\": \"email@company.com\"}"
            }, status=status.HTTP_400_BAD_REQUEST)
        elif validity == 'Needs email in key':
            return Response({
                "Error": "Data must be in the format {\"email\": \"email@company.com\"}"
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = PersonSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)


class OneEmail(APIView):
    def get_person_by_pk(self, pk):
        try:
            email = Person.objects.get(pk=pk)
        except:
            return Response({
                'Error': 'Book does not exist'
            }, status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, pk):
        email = self.get_person_by_pk(pk)
        serializer = PersonSerializer(email)
        return Response(serializer.data)
    

    def put(self, request, pk):
        email = self.get_person_by_pk(pk)
        serializer = PersonSerializer(email, data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
 

    def delete(self, request, pk):
        email = self.get_person_by_pk(pk)
        email.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        