from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE

# Create your models here.

class Topic(models.Model):

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    



class Room(models.Model):

#User in the host come from django.contrib.auth.models 
#if parent Topic where down of class Room just wrap Topic in topic= between '' 
#null=True is for the database 
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    #null true means database for that parameter can be empty,
    #blank is the same but the form 

    #-----------
    # that's for many to many relationships
    #User is the one with the many to many relationship
    #since User is used in host with need to give it a related name
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    #the differtent betw is autonowadd just take the time when first register
    #autonow take the time everytime is updated

    #Class Meta read documentation 
    #ordering with - is for the last shown firts
    class Meta:
        ordering = ['-updated', '-created']


    def __str__(self):
        return self.name
    
class Message(models.Model):
# User and Room in the beginning of () represent the parents to conect
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
        
    def __str__(self):
        #[0:50] just mean the first 50 characters
        return self.body[0:50]
    

