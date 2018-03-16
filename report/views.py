from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.db.models.functions import TruncMonth, TruncYear, TruncDate
from django.db.models import Sum
from cashier.models import Invoice
from datetime import datetime
import json
# Create your views here.
@login_required
def home(request):
    return render(request, 'report/report.html')

@login_required
def get_json(request):
    start_date = request.GET.get(u'start_date', '2018-03-10') + " 00:00:00"
    end_date = request.GET.get(u'end_date', '2018-03-16') + " 23:59:59"

    a = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
    b = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    selisih = b - a
    if selisih.days > 365:
        total_uang_masuk = Invoice.objects.filter(created_at__range=[start_date,end_date]).annotate(tahun=TruncMonth('created_at')).values('tahun').annotate(jml=Sum('total')).values('tahun', 'jml')
        total_keuntungan = Invoice.objects.filter(created_at__range=[start_date,end_date]).annotate(tahun=TruncMonth('created_at')).values('tahun').annotate(jml=(Sum('total') - Sum('cost_total'))).values('jml')
        total_item = Invoice.objects.filter(created_at__range=[start_date,end_date]).annotate(tahun=TruncMonth('created_at')).values('tahun').annotate(jml=Sum('qty')).values('jml')

        hari = [i['tahun'].year for i in total_uang_masuk]
        uang_masuk = [i['jml'] for i in total_uang_masuk]
        keuntungan = [i['jml'] for i in total_keuntungan]
        item = [i['jml'] for i in total_item]
    elif selisih.days > 61:
        total_uang_masuk = Invoice.objects.filter(created_at__range=[start_date,end_date]).annotate(bulan=TruncMonth('created_at')).values('bulan').annotate(jml=Sum('total')).values('bulan', 'jml')
        total_keuntungan = Invoice.objects.filter(created_at__range=[start_date,end_date]).annotate(bulan=TruncMonth('created_at')).values('bulan').annotate(jml=(Sum('total') - Sum('cost_total'))).values('jml')
        total_item = Invoice.objects.filter(created_at__range=[start_date,end_date]).annotate(bulan=TruncMonth('created_at')).values('bulan').annotate(jml=Sum('qty')).values('jml')

        hari = [datetime.strftime(i['bulan'], "%b %Y") for i in total_uang_masuk]
        uang_masuk = [i['jml'] for i in total_uang_masuk]
        keuntungan = [i['jml'] for i in total_keuntungan]
        item = [i['jml'] for i in total_item]
    else:
        total_uang_masuk = Invoice.objects.filter(created_at__range=[start_date,end_date]).annotate(hari=TruncDate('created_at')).values('hari').annotate(jml=Sum('total')).values('hari', 'jml')
        total_keuntungan = Invoice.objects.filter(created_at__range=[start_date,end_date]).annotate(hari=TruncDate('created_at')).values('hari').annotate(jml=(Sum('total') - Sum('cost_total'))).values('jml')
        total_item = Invoice.objects.filter(created_at__range=[start_date,end_date]).annotate(hari=TruncDate('created_at')).values('hari').annotate(jml=Sum('qty')).values('jml')

        hari = [i['hari'].day for i in total_uang_masuk]
        uang_masuk = [i['jml'] for i in total_uang_masuk]
        keuntungan = [i['jml'] for i in total_keuntungan]
        item = [i['jml'] for i in total_item]
    res = {'category': hari, 'uang_masuk': uang_masuk, 'keuntungan': keuntungan, 'item': item}
    return HttpResponse(json.dumps(res), content_type='application/json')