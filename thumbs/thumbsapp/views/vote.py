from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from thumbsapp.models import Idea, Vote
from django.contrib.auth.models import User

class VoteSerializer(serializers.ModelSerializer):
    '''JSON serializer for votes.
    '''

    class Meta:
        model = Vote
        fields = (
            'id',
            'user',
            'idea',
            'voteDirection'
        )
        
class Votes(ViewSet):
    '''Votes for Thumbs app'''

    def retrieve(self, request, pk=None):
        '''Handle GET requests for a single vote
        Returns:
            Response -- JSON serialized vote instance
        '''

        try:
            vote = Vote.objects.get(pk=pk)
            user = User.objects.get(pk=vote.user_id)
            vote.user_id = user.id
            serializer = VoteSerializer(vote, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        '''Handle POST operations
        Returns:
            Response -- JSON serialized idea instance
        '''

        new_vote = Vote()
        user = User.objects.get(user=request.auth.user)

        new_vote.vote_direction = request.data['voteDirection']
        new_vote.user = user
        new_vote.idea = request.data['idea']

        new_vote.save()

        serializer = VoteSerializer(new_vote, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        Handle DELETE requests for a single vote
        Returns:
            Response -- 200, 404, or 500 status code
        '''
        try: 
            vote = Vote.objects.get(pk=pk)
            vote.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Vote.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        '''Handle GET requests for all votes
        Returns:
            Response -- JSON serialized list of vote instances
        '''

        votes = Vote.objects.all()
        idea = self.request.query_params.get('idea', None)

        if idea is not None:
            votes = votes.filter(idea__id=idea)

        serializer = VoteSerializer(votes, many=True, context={'request': request})

        return Response(serializer.data)