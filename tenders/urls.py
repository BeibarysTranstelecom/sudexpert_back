from django.urls import path

from tenders import views

urlpatterns=[
    path("categorys/", views.CategoryView.as_view()),
    path("structures/", views.StructureView.as_view()),
    path("profiles/", views.ProfileView.as_view()),
    path("tenders/", views.TendersView.as_view()),
    path("orders/", views.OrdersView.as_view()),
]