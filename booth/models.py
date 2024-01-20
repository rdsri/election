from django.db import models

# Create your models here.
class ParlimentReport(models.Model):
    parliment_Assembly_Name=models.CharField(max_length=255,null=True)
    state_Assembly_Name=models.CharField(max_length=255,null=True)
    booth_Name=models.CharField(max_length=255,null=True)
    Party_Name=models.CharField(max_length=255,null=True)
    vote_Percentage=models.CharField(max_length=255,null=True)
    total_Vote=models.CharField(max_length=255,null=True)
    year=models.CharField(max_length=255,null=True)


class CasteReport(models.Model):
    parliment_Assembly_Name=models.CharField(max_length=255,null=True)
    state_Assembly_Name=models.CharField(max_length=255,null=True)
    booth_Name=models.CharField(max_length=255,null=True)
    caste_name=models.CharField(max_length=255,null=True)
    count=models.CharField(max_length=255,null=True)

class StateReport(models.Model):
    state_Assembly_Name=models.CharField(max_length=255,null=True)
    booth_Name=models.CharField(max_length=255,null=True)
    Party_Name=models.CharField(max_length=255,null=True)
    vote_Percentage=models.CharField(max_length=255,null=True)
    total_Vote=models.CharField(max_length=255,null=True)
    year=models.CharField(max_length=255,null=True)