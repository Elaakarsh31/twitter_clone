from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import Profile, Tweet

# Unregister Groups.
admin.site.unregister(Group)

# Mix profile info into user info
class ProfileInline(admin.StackedInline):
    model = Profile
    
# Extend USer model 
class UserAdmin(admin.ModelAdmin):
    model = User
    # Just display the username fields on admin page
    fields = ['username']
    inlines = [ProfileInline]

# Unregister initale User
admin.site.unregister(User)
# Reregister User
admin.site.register(User, UserAdmin)

admin.site.register(Tweet)