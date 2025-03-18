from django.shortcuts import render
from .models import OposicionBOE

def oposiciones_boe(request):
    oposiciones = OposicionBOE.objects.all().order_by('-fecha_publicacion')
    return render(request, "scraper/oposiciones_boe.html", {"oposiciones": oposiciones})


