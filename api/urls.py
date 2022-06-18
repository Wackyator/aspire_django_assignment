from django.urls import path
from rest_framework.routers import DefaultRouter

from api.views import UserAPI, UserViewSet, SearchListView

router = DefaultRouter()
router.register('api/users', UserViewSet)

urlpatterns = [
  path('api/users/', UserAPI.as_view()),
  path('api/users/search/', SearchListView.as_view()),
  # path('api/users/<int:id>/', UserDetailAPI.as_view()),
]

urlpatterns += router.urls