from rest_framework.views import APIView
from rest_api.models import Person
from rest_api.serializer import PersonSerializer
from rest_framework.response import Response
from rest_framework import status
from django.forms import ValidationError
from django.http import Http404
# import re


# def valid_email(email):
#     regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
#     if(re.fullmatch(regex, email)):
#         return True
#     else:
#         return False

class EmailList(APIView):
    def get(self, request):
        emails = Person.objects.all()
        serializer = PersonSerializer(emails, many=True)
        return Response(serializer.data)

    
class PersonCreate(APIView):
    def post(self, request):
        serializer = PersonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class OneEmail(APIView):
    def get_person_by_pk(self, pk):
        try:
            return Person.objects.get(pk=pk)
        except:
            raise Http404('That email does not exist')

    def get(self, request, pk):
        email = self.get_person_by_pk(pk)
        serializer = PersonSerializer(email)
        return Response(serializer.data)
    
    def put(self, request, pk):
        email = self.get_person_by_pk(pk)
        serializer = PersonSerializer(email, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        email = self.get_person_by_pk(pk)
        email.delete()
        return Response({'Message': 'Successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
        