from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from myapp import views
#from myapp.views import MusicRankingListView
urlpatterns = [
    path("admin/", admin.site.urls),
    #path('', MusicRankingListView.as_view(), name='home') api專用
    path('', include('myapp.urls')),
    path('', include('music.urls')),
    #path('api/', include('myapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
