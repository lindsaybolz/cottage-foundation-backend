from rest_framework import serializers
from rest_api.models import Person
import re


class PersonSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField()

    class Meta:
       fields = ('id', 'email')
       model = Person

    def create(self, data):
        return Person.objects.create(**data)

    def update(self, instance, data):
        instance.email = data.get('email', instance.email)
        instance.save()
        return instance