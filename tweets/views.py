from django.shortcuts import render
from django.http import HttpResponse
from .models import Tweet
# Create your views here.
def home_view(request , *arg,**kwargs):
    return HttpResponse("<h1>Hello World</h1>")
def tweet_detile(request , tweet_id,*arg,**kwargs):
    obj = Tweet.objects.get(id=tweet_id)
    return HttpResponse(f"<h1>Hello {tweet_id} {obj.content}</h1>")
