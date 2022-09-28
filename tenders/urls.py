from django.urls import path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter
from tenders import views

urlpatterns=[
path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Optional UI:
    path(
        "schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "schema/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"
    ),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("categorys/", views.CategoryView.as_view()),
    path("structures/", views.StructureView.as_view()),
    path("profiles/", views.ProfileView.as_view()),
    path("profile/<int:pk>/", views.ProfileDetailView.as_view()),
    path("tenders/", views.TendersView.as_view()),
    path("tender/<int:pk>/", views.TenderView.as_view()),
    path("orders/", views.OrdersView.as_view()),
    path("check_orders/", views.OrdersCheckView.as_view()),
    path("check_tenders/", views.TenderCheckView.as_view()),
    path("CheckUserByChatID/", views.CheckUserByChatIDView.as_view()),
    path("CheckUser/", views.CheckUser.as_view()),
    path("append_tg_user/", views.AppendTGUser.as_view()),
    path("Customer_TG/", views.Customer_TG.as_view()),
    path("EXECUTOR_TG/", views.EXECUTOR_TG.as_view()),
]