from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.forms.models import modelformset_factory
from django.views.generic import DeleteView

from crmapp.forms import BaseStaffAddFormSet, OrderStaffForm
from crmapp.models import StaffOrder, Order

User = get_user_model()


class OrderStaffCreateView(FormView):
    model = StaffOrder
    formset = BaseStaffAddFormSet
    form_class = OrderStaffForm
    template_name = "staff/create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        staff_filter = User.objects.filter(is_staff=False, is_active=True, black_list=False)
        StaffOrderFormset = modelformset_factory(StaffOrder, form=self.form_class, formset=self.formset, extra=5)
        formset = StaffOrderFormset(prefix="staff")
        for forms in formset:
            forms.fields["staff"].queryset = staff_filter
        context["formset"] = formset
        return context

    def post(self, request, *args, **kwargs):
        StaffOrderFormset = modelformset_factory(StaffOrder, form=self.form_class, formset=self.formset, extra=5)
        formset = StaffOrderFormset(request.POST, prefix="staff")
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        order = get_object_or_404(Order, pk=self.kwargs.get("pk"))
        form = formset.save(commit=False)
        for obj in form:
            obj.order = order
            obj.save()
        return redirect("crmapp:order_detail", pk=order.pk)


class OrderStaffDeleteView(DeleteView):
    model = StaffOrder
    template_name = 'staff/delete.html'
    context_object_name = 'staff'

    def get_success_url(self):
        return reverse('crmapp:order_detail', kwargs={'pk': self.object.order.pk})