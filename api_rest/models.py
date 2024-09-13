from django.db import models

class User(models.Model):

    user_nickname = models.CharField(max_length=100, primary_key=True, default='') #nenhum usuario vai ter nickname repetido
    user_name = models.CharField(max_length=100, default='')
    user_email = models.EmailField(default='')
    user_age = models.IntegerField(default=0)

    def __str__(self):
        return f'Nickname: {self.user_nickname} | E-mail:{self.user_email}'
    
# Create your models here.