from django.db import models

class Tender(models.Model):
    org_chain = models.CharField(max_length=255)
    ref_no = models.CharField(max_length=100)
    tender_id = models.CharField(max_length=100)
    zip_url = models.URLField(null=True)

    def __str__(self):
        return f"{self.tender_reference_number} - {self.tender_id}"
