__author__ = 'berluskuni'


def user_full_name(request):
    return {'USER': request.user}
