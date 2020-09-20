from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from thumbsapp.models import Poll, Group
from django.contrib.auth.models import User

class PollSerializer(serializers.ModelSerializer):
    '''JSON serializer for polls.
    '''

    class Meta:
        model = Poll
        fields = (
            'id',
            'user',
            'group',
            'title',
            'description'
        )
        
class Polls(ViewSet):
    '''Polls for Thumbs app'''

    def retrieve(self, request, pk=None):
        '''Handle GET requests for a single poll
        Returns:
            Response -- JSON serialized poll instance
        '''

        try:
            poll = Poll.objects.get(pk=pk)
            user = User.objects.get(pk=poll.user_id)
            poll.user_id = user.id
            serializer = PollSerializer(poll, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        '''Handle POST operations
        Returns:
            Response -- JSON serialized poll instance
        '''

        new_poll = Poll()
        user = User.objects.get(user=request.auth.user)

        new_poll.title = request.data['title']
        new_poll.user = user
        new_poll.description = request.data['description']

        new_poll.save()

        serializer = PollSerializer(new_poll, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        Handle DELETE requests for a single poll
        Returns:
            Response -- 200, 404, or 500 status code
        '''
        try: 
            poll = Poll.objects.get(pk=pk)
            poll.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Poll.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        '''Handle GET requests for all polls
        Returns:
            Response -- JSON serialized list of poll instances
        '''

        polls = Poll.objects.all()
        group = self.request.query_params.get('group', None)

        if group is not None:
            polls = polls.filter(group__id=group)

        serializer = PollSerializer(polls, many=True, context={'request': request})

        return Response(serializer.data)