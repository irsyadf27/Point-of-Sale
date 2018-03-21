from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, HttpResponse
from django.db.models.functions import TruncMonth, TruncYear, TruncDate
from django.db.models import Sum
from cashier.models import Invoice
from datetime import datetime
import json
import xlwt

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

@login_required
def export_report_xls(request):
    start_date = request.GET.get(u'start_date', '2018-03-10') + " 00:00:00"
    end_date = request.GET.get(u'end_date', '2018-03-25') + " 23:59:59"

    filename = "Laporan %s - %s.xls" % (start_date[:10], end_date[:10])

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Invoice')

    # Sheet header, first row
    row_num = 0

    font_bold = xlwt.XFStyle()
    font_bold.font.bold = True
    font_bold.borders.left = xlwt.Formatting.Borders.THIN
    font_bold.borders.right = xlwt.Formatting.Borders.THIN
    font_bold.borders.top = xlwt.Formatting.Borders.THIN
    font_bold.borders.bottom = xlwt.Formatting.Borders.THIN


    font_style = xlwt.XFStyle()
    font_style.borders.left = xlwt.Formatting.Borders.THIN
    font_style.borders.right = xlwt.Formatting.Borders.THIN
    font_style.borders.top = xlwt.Formatting.Borders.THIN
    font_style.borders.bottom = xlwt.Formatting.Borders.THIN

    font_kanan = xlwt.XFStyle()
    font_kanan.font.bold = True
    font_kanan.alignment.horz = xlwt.Formatting.Alignment.HORZ_RIGHT
    font_kanan.borders.left = xlwt.Formatting.Borders.THIN
    font_kanan.borders.right = xlwt.Formatting.Borders.THIN
    font_kanan.borders.top = xlwt.Formatting.Borders.THIN
    font_kanan.borders.bottom = xlwt.Formatting.Borders.THIN

    font_tengah = xlwt.XFStyle()
    font_tengah.font.bold = True
    font_tengah.alignment.horz = xlwt.Formatting.Alignment.HORZ_CENTER
    font_tengah.borders.left = xlwt.Formatting.Borders.THIN
    font_tengah.borders.right = xlwt.Formatting.Borders.THIN
    font_tengah.borders.top = xlwt.Formatting.Borders.THIN
    font_tengah.borders.bottom = xlwt.Formatting.Borders.THIN

    invoice = Invoice.objects.filter(created_at__range=[start_date,end_date])

    kol1 = ws.col(0)
    kol1.width = 256 * 30

    kol2 = ws.col(1)
    kol2.width = 256 * 20

    kol3 = ws.col(3)
    kol3.width = 256 * 20
    for idx in range(len(invoice)):
        ws.write(row_num, 0, "No. Invoice", font_bold)
        ws.write_merge(row_num, row_num, 1, 3, invoice[idx].invoice_number, font_style)
        row_num += 1
        ws.write(row_num, 0, "Tanggal", font_bold)
        ws.write_merge(row_num, row_num, 1, 3, datetime.strftime(invoice[idx].created_at, "%Y-%m-%d %H:%M:%S"), font_style)
        row_num += 1
        ws.write(row_num, 0, "Pembeli", font_bold)
        ws.write_merge(row_num, row_num, 1, 3, invoice[idx].customer.name, font_style)
        row_num += 1

        kolom = ['Produk', 'Harga', 'Qty', 'Subtotal']
        for i in range(len(kolom)):
            ws.write(row_num, i, kolom[i], font_tengah)

        row_num += 1

        for detail in invoice[idx].details.all():
            ws.write(row_num, 0, detail.product_warehouse.product.name, font_style)
            ws.write(row_num, 1, detail.selling_price, font_style)
            ws.write(row_num, 2, detail.qty, font_style)
            ws.write(row_num, 3, detail.subtotal, font_style)
            row_num += 1

        ws.write_merge(row_num, row_num, 0, 2, "Diskon", font_kanan)
        ws.write(row_num, 3, invoice[idx].discount_size, font_style)
        row_num += 1
        ws.write_merge(row_num, row_num, 0, 2, "Total", font_kanan)
        ws.write(row_num, 3, invoice[idx].total, font_style)
        row_num += 2

    wb.save(response)
    return response
