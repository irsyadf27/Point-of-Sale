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
    category = []
    uang_masuk = []
    keuntungan = []
    item = []
    if selisih.days > 365:
        queryset = Invoice.objects.filter(created_at__range=[start_date,end_date]).annotate(category=TruncYear('created_at')).values('category').annotate(uang_masuk=Sum('total') - Sum('discount_size')).annotate(keuntungan=((Sum('total') - Sum('cost_total')) - Sum('discount_size'))).annotate(item=Sum('qty')).values('category', 'uang_masuk', 'keuntungan', 'item')

        for i in queryset:
            category.append(i['category'].year)
            uang_masuk.append(i['uang_masuk'])
            keuntungan.append(i['keuntungan'])
            item.append(i['item'])
    elif selisih.days > 61:
        queryset = Invoice.objects.filter(created_at__range=[start_date,end_date]).annotate(category=TruncMonth('created_at')).values('category').annotate(uang_masuk=Sum('total') - Sum('discount_size')).annotate(keuntungan=((Sum('total') - Sum('cost_total')) - Sum('discount_size'))).annotate(item=Sum('qty')).values('category', 'uang_masuk', 'keuntungan', 'item')

        for i in queryset:
            category.append(datetime.strftime(i['category'], "%b %Y"))
            uang_masuk.append(i['uang_masuk'])
            keuntungan.append(i['keuntungan'])
            item.append(i['item'])
    else:
        queryset = Invoice.objects.filter(created_at__range=[start_date,end_date]).annotate(category=TruncDate('created_at')).values('category').annotate(uang_masuk=Sum('total') - Sum('discount_size')).annotate(keuntungan=((Sum('total') - Sum('cost_total')) - Sum('discount_size'))).annotate(item=Sum('qty')).values('category', 'uang_masuk', 'keuntungan', 'item')

        for i in queryset:
            category.append(i['category'].day)
            uang_masuk.append(i['uang_masuk'])
            keuntungan.append(i['keuntungan'])
            item.append(i['item'])

    res = {'category': category, 'uang_masuk': uang_masuk, 'keuntungan': keuntungan, 'item': item}
    return HttpResponse(json.dumps(res), content_type='application/json')