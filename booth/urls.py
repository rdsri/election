from django.urls import path
from . import views

urlpatterns = [
    path('',views.GetParlimentData.as_view(),name="home"),
    path('/filter_data',views.GetParlimentfilterData.as_view(),name="filter_data"),
    path('/download_csv',views.GetParlimentCsvData.as_view(),name="download_csv"),
    path('/upload_csv',views.UploadParlimentData.as_view(),name="upload_csv"),
    
    # Caste Report 
    path('/caste_data',views.GetCasteData.as_view(),name="caste_data"),
    path('/caste_filter',views.GetCastefilterData.as_view(),name="caste_filter"),
    path('/download_caste_csv',views.GetCasteCsvData.as_view(),name="download_caste_csv"),
    path('/upload_caste_csv',views.UploadCasteData.as_view(),name="upload_caste_csv"),
    
    # State Report
    path('/state_data',views.GetStateData.as_view(),name="state_data"),
    path('/state_filter',views.GetStatefilterData.as_view(),name="state_filter"),
    path('/download_state_csv',views.GetStateCsvData.as_view(),name="download_state_csv"),
    path('/upload_state_csv',views.UploadStateData.as_view(),name="upload_state_csv"),

]


