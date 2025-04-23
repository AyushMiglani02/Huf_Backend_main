from django.urls import path
from . import views

urlpatterns = [
    path("join-us", views.join_us, name="join-us"),
    # path("join-us-otp-verify", views.join_us_otp_verify, name="verify-join-us-otp"),
    # path("resend-join-us-opt", views.resend_join_us_otp, name="resend-join-us-otp"),
    path("share-experience", views.share_experience, name="share-experience"),
    path("ask-suggestion", views.ask_suggestion, name="ask-suggestion"),
]
