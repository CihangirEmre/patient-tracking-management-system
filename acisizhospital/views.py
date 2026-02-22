# views.py

from django.shortcuts import render
from .models import Doktor

def doktor_list(request):
    query = request.GET.get('q')
    if query:
        doktorlar = Doktor.objects.filter(Ad__icontains=query) | Doktor.objects.filter(Soyad__icontains=query)
    else:
        doktorlar = Doktor.objects.all()
    return render(request, 'doctors.html', {'doktorlar': doktorlar})
