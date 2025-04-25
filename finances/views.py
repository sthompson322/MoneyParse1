from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .constants import CATEGORY_CHOICES
from .models import Income, Transaction, Budget
from .forms import IncomeForm, TransactionForm, BudgetForm
from .models import Ticket
from .forms import TicketForm
from django.db.models import Sum
from decimal import Decimal

@login_required
def income_view(request):
    existing_income = Income.objects.filter(user=request.user).first()

    if request.method == 'POST':
        form = IncomeForm(request.POST, instance=existing_income)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('finances.transactions')
    else:
        form = IncomeForm(instance=existing_income)

    return render(request, 'finances/income.html', {'form': form})

@login_required
def transactions_view(request):
    TransactionFormSet = modelformset_factory(
        Transaction, form=TransactionForm, extra=1, can_delete=True
    )

    if request.method == 'POST':
        formset = TransactionFormSet(request.POST, queryset=Transaction.objects.none())
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                    transaction = form.save(commit=False)
                    transaction.user = request.user
                    transaction.amount = form.cleaned_data.get('amount')
                    transaction.save()

            return redirect('finances.transactions_display')
    else:
        formset = TransactionFormSet(queryset=Transaction.objects.none())

    return render(request, 'finances/transactions.html', {'formset': formset})


@login_required
def transactions_display(request):
    annual_income = Income.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or Decimal("0.00")
    monthly_budgeted_income = (annual_income / 12).quantize(Decimal('0.01')) if annual_income else Decimal("0.00")

    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    total_spent = sum(t.amount for t in transactions if not t.type)
    total_income = sum(t.amount for t in transactions if t.type)
    net_balance = total_income - total_spent

    return render(request, 'finances/transactions_display.html', {
        'transactions': transactions,
        'total_spent': total_spent,
        'total_income': total_income,
        'net_balance': net_balance,
        'annual_income': annual_income,
        'monthly_budgeted_income': monthly_budgeted_income,
    })

@login_required
def budget_view(request):
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            Budget.objects.filter(id=request.POST['delete_id'], user=request.user).delete()
            messages.success(request, "Budget deleted!")
            return redirect('finances.budget')
        else:
            form = BudgetForm(request.POST)

        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, "Budget created!")
            return redirect('finances.budget')
    else:
        form = BudgetForm()

    budgets = Budget.objects.filter(user=request.user)
    for b in budgets:
        print(b.category, b.percent_used, b.remaining)
    return render(request, 'finances/budget.html', {
        'form': form,
        'budgets': budgets,
        'categories': CATEGORY_CHOICES,
    })

def delete_budget(request, budget_id):
    Budget.objects.filter(id=budget_id, user=request.user).delete()
    return redirect('finances.budget')


@login_required
def reports_view(request):
    budgets = Budget.objects.filter(user=request.user)

    # Prepare data for template
    budget_data = []
    for budget in budgets:
        spent = Transaction.objects.filter(
            user=request.user,
            category=budget.category,
            type=False
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        budget_data.append({
            'category': budget.category,
            'limit': float(budget.limit),
            'spent': float(spent),
            'remaining': float(budget.limit - spent),
            'percent_used': (float(spent) / float(budget.limit)) * 100 if budget.limit > 0 else 0
        })

    return render(request, 'finances/reports.html', {
        'budget_data': budget_data,
        'categories': [choice[0] for choice in CATEGORY_CHOICES]
    })

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            messages.success(request, "Your ticket has been submitted successfully!")
            return redirect('finances.profile')
    else:
        form = TicketForm()

    user_tickets = Ticket.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'finances/profile.html', {
        'form': form,
        'tickets': user_tickets
    })


@login_required
def update_ticket_status(request, ticket_id):
    if not request.user.is_staff:
        return redirect('finances.profile')

    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [choice[0] for choice in Ticket.STATUS_CHOICES]:
            ticket.status = new_status
            ticket.save()
            messages.success(request, f"Ticket #{ticket_id} status updated to {new_status}")
    return redirect('finances.admin_tickets')

@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)

    if request.method == 'POST':
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket updated successfully!")
            return redirect('finances.profile')
    else:
        form = TicketForm(instance=ticket)

    return render(request, 'finances/edit_ticket.html', {
        'form': form,
        'ticket': ticket
    })

@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id, user=request.user)
    if request.method == 'POST':
        ticket.delete()
        messages.success(request, "Ticket deleted successfully!")
    return redirect('finances.profile')