from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    '''JSON serializer for users.
    '''

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email'
        )
        
class Users(ViewSet):
    '''Users for Thumbs app'''

    def retrieve(self, request, pk=None):
        '''Handle GET requests for a single user
        Returns:
            Response -- JSON serialized idea instance
        '''

        try:
            user = User.objects.get(pk=request.user.id)

            serializer = UserSerializer(user, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def list(self, request):
        '''Handle GET requests for all users
        Returns:
            Response -- JSON serialized list of user instances
        '''

        if request.user.id:
            users = User.objects.filter(pk=request.user.id)
        
        else:
            users = User.objects.all()

        serializer = UserSerializer(users, many=True, context={'request': request})

        return Response(serializer.data)