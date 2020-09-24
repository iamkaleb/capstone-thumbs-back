from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from thumbsapp.models import GroupUser, Group
from django.contrib.auth.models import User

class GroupUserSerializer(serializers.ModelSerializer):
    '''JSON serializer for group users.
    '''

    class Meta:
        model = GroupUser
        fields = (
            'id',
            'group',
            'user'
        )
        depth = 1

class GroupUsers(ViewSet):
    '''Group Users for Thumbs app'''

    def retrieve(self, request, pk=None):
        '''Handle GET requests for a single group user
        Returns:
            Response -- JSON serialized group instance
        '''

        try:
            group_user = GroupUser.objects.get(pk=pk)
            user = User.objects.get(pk=group_user.user_id)
            group_user.user_id = user.id
            serializer = GroupUserSerializer(group_user, many=False, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        '''Handle POST operations
        Returns:
            Response -- JSON serialized Group User instance
        '''

        new_group_user = GroupUser()
        user = User.objects.get(pk=request.auth.user.id)

        new_group_user.group_id = request.data['groupId']
        new_group_user.user = user

        new_group_user.save()

        serializer = GroupUserSerializer(new_group_user, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        Handle DELETE requests for a single group user
        Returns:
            Response -- 200, 404, or 500 status code
        '''
        try: 
            group_user = GroupUser.objects.get(pk=pk)
            group_user.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except GroupUser.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        '''Handle GET requests for all group users
        Returns:
            Response -- JSON serialized list of product instances
        '''
        
        group_users = GroupUser.objects.all()

        group = self.request.query_params.get('group', None)

        user = self.request.query_params.get('user', None)

        if group is not None:
            group_users = group_users.filter(group__id=group)

        if user is not None:
            group_users = group_users.filter(user__id=request.user.id)

        serializer = GroupUserSerializer(group_users, many=True, context={'request': request})

        return Response(serializer.data)