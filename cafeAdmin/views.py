import qrcode
import base64
from io import BytesIO
from django.urls import reverse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .forms import CafeForm
from .models import Cafe
from django.views.generic import DetailView
from core.models import Category, MenuItem
from core.serializers import CategorySerializer, MenuItemSerializer
from django.http import JsonResponse
from rest_framework.parsers import JSONParser


def register_cafe(request):
    if request.method == 'POST':
            form = CafeForm(request.POST)
            if form.is_valid():
                cafe = form.save()
                unique_url = request.build_absolute_uri(reverse('cafe_menu', kwargs={'slug': cafe.slug}))
                qr_code_image = generate_qr_code(unique_url)
    else:
        form = CafeForm()
    return render(request, 'cafeAdmin_temp/register_cafe.html', {'form': form}, {""})


def generate_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str


class CafeMenuView(DetailView):
    model = Cafe
    template_name = 'cafe_menu.html',
    context_object_name = 'cafe'
