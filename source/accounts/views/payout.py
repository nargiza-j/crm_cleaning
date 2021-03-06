from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from accounts.forms import PayoutForm
from accounts.models import Payout, Staff
from crmapp.models import CashManager
from crmapp.forms import ManagerCashForm
from tgbot.handlers.orders.tg_order_staff import staff_salary_alert


class PayoutListView(PermissionRequiredMixin, ListView):
    model = Payout
    context_object_name = 'payouts'
    template_name = 'account/payout_list.html'
    ordering = ['-date_payout', ]
    permission_required = "accounts.view_payout"


class PayoutCreateView(PermissionRequiredMixin, CreateView):
    model = Payout
    form_class = PayoutForm
    template_name = 'account/payout_add.html'
    success_url = reverse_lazy('accounts:staff-list')
    context_object_name = 'staff_payout'
    permission_required = "accounts.add_payout"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        context['staff'] = staff
        return context

    def post(self, request, *args, **kwargs):
        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        if staff.balance > 0:
            try:
                with transaction.atomic():
                    Payout.objects.create(staff=staff, salary=staff.balance)
                    staff_salary_alert(staff)
                    staff.nullify_salary()
                    messages.success(self.request,
                                     f'Баланс сотрудника {staff.first_name} {staff.last_name} успешно списан!')
            except:
                messages.warning(self.request,
                                 f'Операция отменена, попробуйте снова')
        else:
            messages.warning(self.request,
                             f'Баланс сотрудника {staff.first_name} {staff.last_name} составляет {staff.balance} cом! Операция невозможна! ')
        return HttpResponseRedirect(self.success_url)


class CashManagerCreateView(PermissionRequiredMixin, CreateView):
    model = CashManager
    form_class = ManagerCashForm
    template_name = 'account/cash_add.html'
    success_url = reverse_lazy('crmapp:manager_cash_list')
    permission_required = "crmapp.add_cashmanager"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        manager = get_object_or_404(Staff, pk=self.kwargs['pk'])
        context['manager'] = manager
        return context

    def post(self, request, *args, **kwargs):
        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        group = Group(name="Manager")
        if staff.groups.filter(name=group):
            if staff.cash > 0:
                try:
                    with transaction.atomic():
                        staff.nullify_cash()
                        messages.success(self.request,
                                         f'Касса менеджера {staff.first_name} {staff.last_name} успешно анулирован!')
                except:
                    messages.warning(self.request,
                                     f'Операция отменена, попробуйте снова')
            else:
                messages.warning(self.request,
                                 f'Касса менеджера {staff.first_name} {staff.last_name} составляет {staff.cash} cом! Операция невозможна! ')
        return HttpResponseRedirect(self.success_url)

    def has_permission(self):
        return self.request.user.is_staff
