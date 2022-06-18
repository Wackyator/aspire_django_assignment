from django.db import models

class UserQuerySet(models.QuerySet):
  def search(self, query):
    lookup = models.Q(name__icontains=query) | models.Q(username__icontains=query)
    return self.filter(lookup)

class User(models.Model):
  name = models.CharField(max_length=50)
  username = models.CharField(max_length=50)
  email = models.CharField(max_length=50)
  created = models.DateTimeField(auto_now_add=True)
