from rest_framework import serializers 
from .models import Tweet
from django.conf import settings
MAX_TWEET_LENGTH= settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTION = settings.TWEET_ACTION_OPTION 
class TweetActionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    def validate_Action(self,value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTION:
            raise serializers.ValidationError("this is not a valid action for tweets")
        return value

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model=Tweet
        fields  =["content"]
    def validate_cintent(self,value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("this tweet is so long")
        return value
