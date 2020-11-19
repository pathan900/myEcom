from django.urls import path
from .import views
urlpatterns = [
   path("", views.index, name="shophome"),
   path("about/", views.about, name="about"),
   path("contact/", views.contact, name="contactus"),
   path("tracker/", views.tracker, name="tracker"),
   path("product/<int:myid>", views.product, name="productview"),
   path("mycart/", views.mycart, name="mycart"),
   path("checkout/", views.checkout, name="checkout"),
   path("search/", views.search, name="search"),
   #path("handlerequest/", views.handlerequest, name="HandleRequest"),
]
