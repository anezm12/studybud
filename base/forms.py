from django.forms import ModelForm
from .models import Room

class RoomForm(ModelForm):

    class Meta:
        #specify the Class
        model = Room
        #you can select the fields you need 
        #all the fields in fields must be specify in models.py 
        # fields = ['name', 'body']
        fields = '__all__'
        exclude = ['host', 'participants']

