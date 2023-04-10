from django.contrib.auth.models import User
from .models import Message

def unread_messages(request):
    if request.user.is_authenticated:
        profile = request.user.profile
        message_requests = profile.messages.all()
        # unread_count = Message.objects.filter(recipient=request.user, is_read=False).count()
        unread_count = message_requests.filter(is_read=False).count()
    else:
        unread_count = 0
    return {'unread_count': unread_count}