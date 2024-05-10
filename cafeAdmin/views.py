from django.shortcuts import render
from .models import Category, MenuItem
from .serializers import CategorySerializer, MenuItemSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser


def categories_view(request):
    if request.method == "GET":
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = CategorySerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=200)
        return JsonResponse(serializer.errors, status=400)
    # return render(request, 'cafeAdmin_temp/cafe_menuList.html')
