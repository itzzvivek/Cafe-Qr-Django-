from django.shortcuts import render


def menu(request):
    return render(request, 'user_temp/user_menu.html')
