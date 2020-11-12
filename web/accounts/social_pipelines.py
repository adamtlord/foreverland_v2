from accounts.models import UserProfile


def create_profile(user, is_new=False, *args, **kwargs):
    if is_new:
        UserProfile.objects.get_or_create(user=user)
