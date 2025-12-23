from django.db import models

class Lottery(models.Model):
    utas = models.CharField(max_length=20, verbose_name="Утасны дугаар")
    email = models.EmailField(blank=True, null=True)
    buten_ner = models.CharField(max_length=100, verbose_name="Бүтэн нэр")
    hotiin_ner = models.CharField(max_length=50, blank=True, null=True)
    sumiin_ner = models.CharField(max_length=50, blank=True, null=True)
    bagiin_ner = models.CharField(max_length=50, blank=True, null=True)
    letter = models.TextField(verbose_name="Захидал", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    ebarimt_picture = models.FileField(upload_to='ebarimt_pictures/')
    status = models.CharField(max_length=50, default='draft', verbose_name="Status")

    def __str__(self):
        return f"{self.buten_ner}"

    class Meta:
        db_table = 'lottery'  # Table нэрийг explicit зааж өгч байна
        verbose_name = 'Lottery'
        verbose_name_plural = 'Lotteries'
        ordering = ['-created_at']  # Default order
