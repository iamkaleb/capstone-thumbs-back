from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from thumbsapp.models import Group
from django.contrib.auth.models import User

class GroupSerializer(serializers.ModelSerializer):
    '''JSON serializer for groups.
    '''

    class Meta:
        model = Group
        fields = (
            'id',
            'title',
            'creator',
            'description'
        )

class Groups(ViewSet):
    '''Groups for Thumbs app'''

    def retrieve(self, request, pk=None):
        '''Handle GET requests for a single group
        Returns:
            Response -- JSON serialized group instance
        '''

        try:
            group = Group.objects.get(pk=pk)
            creator = User.objects.get(pk=group.creator_id)
            group.creator_id = creator.id
            serializer = GroupSerializer(group, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        '''Handle POST operations
        Returns:
            Response -- JSON serialized Group instance
        '''

        new_group = Group()
        creator = User.objects.get(pk=request.auth.user.id)

        new_group.title = request.data['title']
        new_group.creator = creator
        new_group.description = request.data['description']

        new_group.save()

        serializer = GroupSerializer(new_group, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        Handle DELETE requests for a single group
        Returns:
            Response -- 200, 404, or 500 status code
        '''
        try: 
            group = Group.objects.get(pk=pk)
            group.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Group.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        '''Handle GET requests for all groups
        Returns:
            Response -- JSON serialized list of group instances
        '''

        groups = Group.objects.all()

        title = self.request.query_params.get('title', None)

        search = self.request.query_params.get('search', None)

        if title is not None:
            groups = groups.filter(group__title=title)

        if search is not None:
            groups = groups.filter(title__startswith=search)

        serializer = GroupSerializer(groups, many=True, context={'request': request})

        return Response(serializer.data)