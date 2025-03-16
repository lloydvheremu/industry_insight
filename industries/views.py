from django.views.generic import UpdateView, CreateView, DeleteView, DetailView, ListView

from .models import Industry

class IndustryCreateView(CreateView):
    model = Industry
    template_name = 'industries/industry_create.html'

