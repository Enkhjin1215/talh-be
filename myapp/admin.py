from django.contrib import admin
from .models import Lottery

import pandas as pd
from django.http import HttpResponse
from django.utils.timezone import localtime


def export_lottery_to_excel(modeladmin, request, queryset):
    data = []

    for obj in queryset:
        data.append({
            'Утас': obj.utas,
            'И-мэйл': obj.email,
            'Бүтэн нэр': obj.buten_ner,
            'Хотын нэр': obj.hotiin_ner,
            'Сумын нэр': obj.sumiin_ner,
            'Багийн нэр': obj.bagiin_ner,
            'Захидал': obj.letter,
            'Статус': obj.status,
            'Бүртгэгдсэн огноо': localtime(obj.created_at).replace(tzinfo=None),
            'Е-баримтын зураг': obj.ebarimt_picture.url if obj.ebarimt_picture else '',
        })

    df = pd.DataFrame(data)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=lottery.xlsx'

    df.to_excel(response, index=False)
    return response






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
    actions = [export_lottery_to_excel]
