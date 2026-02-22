from django.urls import path
from . import views
# http://127.0.0.1:8000/


urlpatterns=[
    path("",views.index),
    path("homePage",views.index),
    path("SearchDoctor",views.SearchDoctor),
    path("profilduzenle",views.profilduzenle),
    path("SearchPatient",views.SearchPatient),
    path("profilim",views.profilim),
    path("doktorProfilim",views.doktorProfilim),
    path("hastaArayuz",views.hastaArayuz),
    path("randevuArayuz",views.randevuArayuz),
    path("doktorRandevularim",views.doktor_randevularim),
    path("Randevularim",views.randevularim),
    path("doktorArayuz",views.doktor_arayuz),
    path("Doctors",views.Doctors),
    path("Manager",views.Manager),
    path("Patient",views.Patient),
    path("RaporView",views.rapor_view),
]