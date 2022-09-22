from django.db import models

class Other(models.Model):
    ip          = models.CharField("IP", max_length=19) 
    rede        = models.CharField("Network", max_length=40) 
    data_1      = models.CharField("First Recorded Date", max_length=26)
    data_2      = models.CharField("Last Recorded Date", max_length=26)
    count       = models.CharField("Count", max_length=10000)

    def __str__(self):
        return self.ip

class Vul(models.Model):
    ip          = models.CharField("IP", max_length=19)
    port        = models.CharField("Port", max_length=10000)
    rede        = models.CharField("Network", max_length=40) 
    data_1      = models.CharField("First Recorded Date", max_length=26)
    data_2      = models.CharField("Last Recorded Date", max_length=26)
    count       = models.CharField("Count", max_length=10000)

    def __str__(self):
        return self.ip

class Mal(models.Model):
    ip          = models.CharField("IP", max_length=19)
    rede        = models.CharField("Network", max_length=40) 
    data_1      = models.CharField("First Recorded Date", max_length=26)
    data_2      = models.CharField("Last Recorded Date", max_length=26)
    count       = models.CharField("Count", max_length=10000)

    def __str__(self):
        return self.ip

class Record(models.Model):
    email       = models.CharField("Email", max_length=100)
    ip          = models.CharField("IP", max_length=19)
    tipo        = models.CharField("Type", max_length=13)
    data      = models.CharField("Date", max_length=26)
    email_sent  = models.CharField("Email Sent Type", max_length=9)
    status      = models.CharField("Status", max_length=11)

    def __str__(self):
        return self.email