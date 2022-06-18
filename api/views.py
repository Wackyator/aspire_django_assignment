from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import  generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import User
from api.serializers import UserSerializer

class UserAPI(APIView):

  def get(self, request,):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

  def post(self, request):
    data = request.data
    resp_obj = dict()
    added = list()
    errors = list()

    if isinstance(data, list):
      for item in data:
        serializer = UserSerializer(data=item)
        if serializer.is_valid():
          serializer.save()
          added.append(serializer.data)
        else:
          errors.append({'data': serializer.data, 'error': (serializer.errors)})
    else:
      serializer = UserSerializer(data=data)
      if serializer.is_valid():
        serializer.save()
        added.append(serializer.data)
      else:
        errors.append({'data': serializer.data,'error': serializer.errors})

    if added:
      resp_obj['success'] = added
    if errors:
      resp_obj['errors'] = errors

    return Response(resp_obj)

# class UserDetailAPI(APIView):
#   def get_object(self, id):
#     user = get_object_or_404(User, id=id)
#     return user

#   def get(self, request, id):
#     user = self.get_object(id=id)
#     serializer = UserSerializer(user)
#     return Response(serializer.data)

#   def put(self, request, id):
#     user = self.get_object(id=id)
#     serializer = UserSerializer(user, data=request.data)
#     if serializer.is_valid():
#       serializer.save()
#       return Response(serializer.data)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#   def delete(self, request, id):
#     user = self.get_object(id=id)
#     user.delete()
#     return Response(status=status.HTTP_204_NO_CONTENT)

class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer
  lookup_field = 'id'

#  https://learndjango.com/tutorials/django-search-tutorial
class SearchListView(generics.ListAPIView):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def get_queryset(self, *args, **kwargs):
      q = self.request.GET.get('q')
      results = User.objects.none()
      if q is not None:
        results = User.objects.filter(
          Q(name__icontains=q) | Q(username__icontains=q)
        )
      return results 