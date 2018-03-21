from django.shortcuts import render
from django.views.generic import UpdateView
from django.core.urlresolvers import reverse_lazy
from config.models import Config
from config.forms import ConfigForm

# Create your views here.
def home(request):
    conf = Config.objects.first()
    form = ConfigForm(request.POST or None, instance=conf)
    if form.is_valid():
        form.save()
    return render(request, 'config/update.html', {'form': form})