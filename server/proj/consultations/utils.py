from .models import UserProfile


def get_user_profile(id):
    print(id)
    return UserProfile.objects.get(pk=id)






