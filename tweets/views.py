import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.conf import settings
from .models import Tweet
from django.utils.http import is_safe_url
from .forms import TweetForm
from .serializers import TweetSerializer ,TweetActionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes,authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
# Create your views here.
ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *arg, **kwargs):
    return render(request, 'pages/home.html')
@api_view(['POST'])
#@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *arg, **kwargs):
    Serializer = TweetSerializer(data=request.POST )
    if Serializer.is_valid(raise_exception=True):
        Serializer.save(user=request.user)
        return Response(Serializer.data,status=201)
    return Response({},status=400)
@api_view(['GET'])
def tweet_list(request, *arg, **kwargs):
    tweets = Tweet.objects.all()
    Serializer = TweetSerializer(tweets,many=True)
    return Response(Serializer.data,status=200)
@api_view(['GET'])
def tweet_detile(request, tweet_id,*arg, **kwargs):
    tweet = Tweet.objects.filter(id=tweet_id)
    if not tweet.exists():
        return Response({},status=404)
    obj = tweet.first()
    Serializer = TweetSerializer(obj)
    return Response(Serializer.data,status=200)
@api_view(['DELETE','POST'])
@permission_classes([IsAuthenticated])
def tweet_delete(request, tweet_id,*arg, **kwargs):
    tweet = Tweet.objects.filter(id=tweet_id)
    if not tweet.exists():
        return Response({},status=404)
    tweet = tweet.filter(user=request.user)
    if not tweet.exists():
        return Response({"message":"you can't delet this tweet"},status=401)
    obj = tweet.first()
    obj.delete()
    return Response({"message":"tweet removed"},status=200)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action(request,*arg, **kwargs):
    Serializer = TweetActionSerializer(data=request.POST )
    if Serializer.is_valid(raise_exception=True):
        data = Serializer.validated_data
        tweet_id = data.get("id")
        action = data.get("action")
    tweet = Tweet.objects.filter(id=tweet_id)
    if not tweet.exists():
        return Response({},status=404)
    obj = tweet.first()
    if action == "like":
        obj.like.add(request.user)
    elif action == "unlike":
        obj.like.remove(request.user)
    elif action == "retweet":
        #to do 
    
        return Response({"message":"tweet removed"},status=200)
def tweet_create_view_pure_django(request, *arg, **kwargs):
    user = request.user
    if not request.user.is_authenticated:
        user = None
        if request.is_ajax():
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if request.is_ajax():
            return JsonResponse(obj.serialize(), status=201)
        if next_url != None and is_safe_url(next_url, ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        if request.is_ajax():
            return JsonResponse(form.errors, status=400)

    contex = {"form": form}
    return render(request, 'components/form.html', contex)



def tweet_list_pure_django(request, *arg, **kwargs):
    tweets = Tweet.objects.all()
    tweets_list = [tweet.serialize() for tweet in tweets]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)


def tweet_detile_pure_django(request, tweet_id, *arg, **kwargs):
    try:
        obj = Tweet.objects.get(id=tweet_id)
    except:
        raise Http404
    return HttpResponse(f"<h1>Hello {tweet_id} {obj.content}</h1>")
