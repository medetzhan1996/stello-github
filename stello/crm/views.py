from django.views.generic.base import TemplateResponseMixin, View
from django.contrib.auth.mixins import LoginRequiredMixin


# Страница заказов
class OrderView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'crm/order/list.html'

    def get(self, request, *args, **kwargs):
        return self.render_to_response({})
