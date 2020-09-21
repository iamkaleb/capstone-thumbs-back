from django.http import HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import action
from thumbsapp.models import Idea, IdeaImage

class IdeaImageSerializer(serializers.ModelSerializer):
    '''JSON serializer for idea images.
    '''

    class Meta:
        model = IdeaImage
        fields = (
            'id',
            'idea',
            'url'
        )
        
class IdeaImages(ViewSet):
    '''Ideas for Thumbs app'''

    def retrieve(self, request, pk=None):
        '''Handle GET requests for a single idea image
        Returns:
            Response -- JSON serialized idea image instance
        '''

        try:
            idea_image = IdeaImage.objects.get(pk=pk)
            
            serializer = IdeaImageSerializer(idea_image, context={'request': request})
            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)
    
    def create(self, request):
        '''Handle POST operations
        Returns:
            Response -- JSON serialized idea image instance
        '''

        new_idea_image = IdeaImage()

        new_idea.idea_id = request.data['ideaId']
        new_idea.url = request.data['url']

        new_idea_image.save()

        serializer = IdeaImageSerializer(new_idea_image, context={'request': request})

        return Response(serializer.data)

    def destroy(self, request, pk=None):
        '''
        Handle DELETE requests for a single idea image
        Returns:
            Response -- 200, 404, or 500 status code
        '''
        try: 
            idea_image = IdeaImage.objects.get(pk=pk)
            idea_image.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        
        except IdeaImage.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def list(self, request):
        '''Handle GET requests for all idea images
        Returns:
            Response -- JSON serialized list of idea image instances
        '''

        idea_images = IdeaImage.objects.all()
        idea = self.request.query_params.get('idea', None)

        if idea is not None:
            idea_images = idea_images.filter(idea__id=idea)

        serializer = IdeaImageSerializer(idea_images, many=True, context={'request': request})

        return Response(serializer.data)