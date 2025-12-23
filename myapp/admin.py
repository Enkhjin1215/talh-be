from django.contrib import admin
from .models import Lottery


@admin.register(Lottery)
class LotteryAdmin(admin.ModelAdmin):
    list_display = (
        'buten_ner',
        'utas',
        'email',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
        'hotiin_ner',
    )

    search_fields = (
        'buten_ner',
        'utas',
        'email',
    )

    readonly_fields = ('created_at',)

    ordering = ('-created_at',)

    fieldsets = (
        ("Хувийн мэдээлэл", {
            "fields": (
                'buten_ner',
                'utas',
                'email',
            )
        }),
        ("Хаяг", {
            "fields": (
                'hotiin_ner',
                'sumiin_ner',
                'bagiin_ner',
            )
        }),
        ("Сугалааны мэдээлэл", {
            "fields": (
                'ebarimt_picture',
                'status',
                'letter',
                'created_at',
            )
        }),
    )
