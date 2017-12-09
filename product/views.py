from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import CreateView, DetailView, UpdateView, ListView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django_datatables_view.base_datatable_view import BaseDatatableView
from product.models import Product, ProductWarehouse
from product.forms import ProductForm
from warehouse.models import Warehouse
import json

# Create your views here.
@login_required
def home(request):
    return render(request, 'product/product.html')

@login_required
def list_json(request):
    result = []
    search = request.GET.get(u'term', None)
    if search:
        qs = Product.objects.filter(name__contains=search)
    else:
        qs = Product.objects.all()

    for data in qs:
        result.append({'id': data.pk, 'text': str(data)})

    result = json.dumps({'results': result})
    return HttpResponse(result, content_type='application/json')

@login_required
def qrcode(request, pk):
    data = get_object_or_404(Product, pk=pk)
    nama = "%s (%s) %s" % (data.name, data.size, data.color)
    return HttpResponse('<img src="data:image/png;base64,%s" class="download-qrcode"/><div class="clearfix"></div><div class="ln_solid"></div><div class="text-center"><a href="data:image/png;base64,%s" download="%s.png" class="btn btn-sm btn-primary"><i class="fa fa-download"></i> Download</a>' % (data.generate_qrcode, data.generate_qrcode, nama))

class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/detail.html'

class ProductCreateView(CreateView):
    form_class = ProductForm
    model = Product
    #success_url = reverse_lazy('product')
    template_name = 'product/create.html'
    #fields = ['name', 'merk', 'serial_number', 'size', 'color', 'price', ]
    def get_success_url(self):
        return reverse('detail_product',args=(self.object.id,))

class ProductEditView(UpdateView):
    form_class = ProductForm
    model = Product
    success_url = reverse_lazy('product')
    template_name = 'product/update.html'
    #fields = ['name', 'merk', 'serial_number', 'size', 'color', 'price', ]

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('product')
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

class ModalProductCreateView(CreateView):
    #form_class = ProductForm
    model = Product
    success_url = reverse_lazy('receiving_product')
    template_name = 'product/modal/create.html'
    fields = ['name', 'merk', 'serial_number', 'size', 'color', 'cost_price', 'selling_price']

class ProductListJson(BaseDatatableView):
    model = Product
    columns = ['name', 'merk', 'serial_number', 'size', 'color', 'cost_price', 'selling_price']
    order_columns = ['name', 'merk', 'serial_number', 'size', 'color', 'cost_price', 'selling_price']
    max_display_length = 500

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                "<u><a href='%s' class='text-primary'>%s</a></u>" % (reverse('detail_product',args=(item.id,)), item.name),
                item.merk.name,
                item.serial_number,
                item.size,
                item.color,
                item.cost_price,
                item.selling_price,
                "<a href='#' onclick='javascript: get_qrcode(%s);' class='btn btn-sm btn-default'><i class='fa fa-qrcode'></i> QR Code</a> <a href='%s' class='btn btn-sm btn-default'><i class='fa fa-pencil-square-o'></i> Ubah</a> <a href='#' onclick='javascript: hapus_produk(%s);' class='btn btn-sm btn-danger'><i class='fa fa-trash'></i> Hapus</a>" % (item.id, reverse('update_product', kwargs = {'pk' : item.id, }), item.id)
            ])
        return json_data
        
    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(name__contains=search)

        return qs

class MappingListJson(BaseDatatableView):
    model = ProductWarehouse
    columns = ['product', 'warehouse', 'stock']
    order_columns = ['product', 'warehouse', 'stock']
    max_display_length = 500

    def get_initial_queryset(self):
        qs = ProductWarehouse.objects.filter(product=self.kwargs['pk'])
        return qs

    def prepare_results(self, qs):
        json_data = []
        for item in qs:
            json_data.append([
                str(item.product),
                str(item.warehouse),
                item.stock
            ])
        return json_data
        
    def filter_queryset(self, qs):
        search = self.request.GET.get(u'search[value]', None)
        if search:
            qs = qs.filter(product__name__contains=search)

        return qs
