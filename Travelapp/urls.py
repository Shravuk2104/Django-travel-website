from django.urls import path
from Travelapp import views
from django.conf.urls.static import static
from Travel import settings

urlpatterns = [
    path('index',views.index),
    path('catfilter/<cv>',views.catfilter),
    path('pdetails/<pid>',views.pdetails),
    path('viewbook',views.viewbook),
    path('register',views.register),
    path('ulogin',views.ulogin),
    path('ulogout',views.ulogout),
    path('About',views.About),
    path('services',views.services),
     path('sort/<sv>',views.sort),
    path('range',views.range),
    path('updateqty/<qv>/<cid>',views.updateqty),
    path('makepayment',views.makepayment),
    path('addtobook/<pid>',views.addtobook),
    path('remove/<cid>',views.remove),
    path('confirmbooking',views.confirmbooking),
    path('search',views.search),
    path('senduseremail',views.senduseremail)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)