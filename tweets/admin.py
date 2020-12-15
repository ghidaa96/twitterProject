from django.contrib import admin
from .models import Tweet 
from .models import TweetLike
# Register your models here.

class TweetLikeAdmin(admin.TabularInline):
    class Meta:
        model : Tweet 
class TweetAdmin(admin.ModelAdmin):
    inline = [TweetLikeAdmin]
    list_display = ['__str__','user']
    search_fields = ['content','user__username','user__email']
    class Meta:
        model : Tweet 
admin.site.register(Tweet ,TweetAdmin )
