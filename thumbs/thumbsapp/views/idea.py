from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from thumbsapp.models import Idea, Poll
from django.contrib.auth.models import User

class IdeaSerializer(serializers.ModelSerializer):
    '''JSON serializer for ideas.
    '''

    class Meta:
        model = Idea
        fields = (
            'id',
            'user',
            'poll',
            'title',
            'description'
        )
        
class Ideas(ViewSet):
    '''Ideas for Thumbs app'''

    def retrieve(self, request, pk=None):
        '''Handle GET requests for a single idea
        Returns:
            Response -- JSON serialized idea instance
        '''

        try:
            idea = Idea.objects.get(pk=pk)
            user = User.objects.get(pk=idea.user_id)
            idea.user_id = user.id
            serializer = IdeaSerializer(idea, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        '''Handle POST operations
        Returns:
            Response -- JSON serialized idea instance
        '''

        new_idea = Idea()
        user = User.objects.get(pk=request.auth.user.id)

        new_idea.poll_id = request.data['pollId']
        new_idea.title = request.data['title']
        new_idea.user = user
        new_idea.description = request.data['description']

        new_idea.save()

        serializer = IdeaSerializer(new_idea, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        Handle DELETE requests for a single idea
        Returns:
            Response -- 200, 404, or 500 status code
        '''
        try: 
            idea = Idea.objects.get(pk=pk)
            idea.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except Idea.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        '''Handle GET requests for all ideas
        Returns:
            Response -- JSON serialized list of idea instances
        '''

        ideas = Idea.objects.all()
        poll = self.request.query_params.get('poll', None)

        if poll is not None:
            ideas = ideas.filter(poll__id=poll)

        serializer = IdeaSerializer(ideas, many=True, context={'request': request})

        return Response(serializer.data)