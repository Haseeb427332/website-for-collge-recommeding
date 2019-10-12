from django.db import models
class dym_render(models.Model):
    My_type = models.CharField(primary_key=True,max_length=20)
    My_id = models.CharField(max_length=20) #django default keyword "id"
    My_value = models.CharField(max_length=20) 
class clg_details(models.Model):
    clg_id = models.IntegerField(primary_key=True)
    clg_name = models.CharField(max_length=100)
    Region = models.CharField(max_length=20)
    University = models.CharField(max_length=100)
    contact_details = models.TextField()
class cut_off(models.Model):
    clg_id = models.ForeignKey(clg_details, on_delete=models.CASCADE)
    Department = models.CharField(max_length=30)
    Intake = models.IntegerField()
    GOPENS = models.CharField(max_length=3)
    GSCS = models.CharField(max_length=3)
    GSTS = models.CharField(max_length=3)
    GVJS = models.CharField(max_length=3)
    GNT1S = models.CharField(max_length=3)
    GNT2S = models.CharField(max_length=3)
    GNT3S = models.CharField(max_length=3)
    GOBCS = models.CharField(max_length=3)
    LOPENS = models.CharField(max_length=3)
    LSCS = models.CharField(max_length=3)
    LSTS = models.CharField(max_length=3)
    LVJS = models.CharField(max_length=3)
    LNT1S = models.CharField(max_length=3)
    LNT2S = models.CharField(max_length=3)
    LNT3S = models.CharField(max_length=3)
    LOBCS = models.CharField(max_length=3)
class fees(models.Model):
    clg_id = models.ForeignKey(clg_details, on_delete=models.CASCADE)
    open = models.IntegerField()
    obc = models.IntegerField()
    sc = models.IntegerField()
    st = models.IntegerField()
    sbc = models.IntegerField()
    vj_nt = models.IntegerField()



