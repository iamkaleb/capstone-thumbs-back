from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token
from thumbsapp.views import register_user, login_user
from thumbsapp.views import *
from thumbsapp.models import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'groups', Groups, 'group')
router.register(r'groupusers', GroupUsers, 'groupuser')
router.register(r'polls', Polls, 'poll')
router.register(r'ideas', Ideas, 'idea')
router.register(r'ideaimages', IdeaImages, 'ideaimage')
router.register(r'votes', Votes, 'vote')
router.register(r'users', Users, 'user')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user),
    path('login/', login_user),
    path('api-token-auth/', obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]