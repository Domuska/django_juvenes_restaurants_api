from todos import testhelloviews
from django.conf.urls import url

urlpatterns = {
    url(r'^$', testhelloviews.sendresponse)
}
