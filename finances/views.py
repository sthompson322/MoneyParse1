from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .constants import CATEGORY_CHOICES
from .models import Income, Transaction, Budget
from .forms import IncomeForm, TransactionForm, BudgetForm

@login_required
def income_view(request):
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = request.user
            income.save()
            return redirect('finances.transactions')
    else:
        form = IncomeForm()

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

                    # Check budget if this is an expense (type=False)
                    if not transaction.type:
                        budget = Budget.objects.filter(
                            user=request.user,
                            category=transaction.category
                        ).first()
                        if budget:
                            if budget.spent > budget.limit:
                                messages.warning(
                                    request,
                                    f"You exceeded your {budget.category} budget (${budget.limit})!"
                                )
            return redirect('finances.transactions_display')
    else:
        formset = TransactionFormSet(queryset=Transaction.objects.none())

    return render(request, 'finances/transactions.html', {'formset': formset})


@login_required
def transactions_display(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')

    total_spent = sum(t.amount for t in transactions if not t.type)

    return render(request, 'finances/transactions_display.html', {
        'transactions': transactions,
        'total_spent': total_spent,
    })

@login_required
def budget_view(request):
    if request.method == 'POST':
        if 'delete_id' in request.POST:
            Budget.objects.filter(id=request.POST['delete_id'], user=request.user).delete()
            messages.success(request, "Budget deleted!")
            return redirect('finances.budget')

        elif 'edit_id' in request.POST:
            budget = Budget.objects.get(id=request.POST['edit_id'], user=request.user)
            form = BudgetForm(request.POST, instance=budget)
        else:
            form = BudgetForm(request.POST)

        if form.is_valid():
            budget = form.save(commit=False)
            budget.user = request.user
            budget.save()
            messages.success(request, "Budget saved!")
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

    chart_data = {
        'labels': [b.category for b in budgets],
        'limits': [float(b.limit) for b in budgets],
        'spent': [
            float(Transaction.objects.filter(
                user=request.user,
                category=b.category,
                type=False
            ).aggregate(Sum('amount'))['amount__sum'] or 0)
            for b in budgets
        ]
    }
    budget_data = []
    for budget in budgets:
        spent = Transaction.objects.filter(
            user=request.user,
            category=budget.category,
            type=False
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        budget_data.append({
            'category': budget.category,
            'limit': budget.limit,
            'spent': spent,
            'remaining': budget.limit - spent,
            'percent_used': (spent / budget.limit) * 100 if budget.limit > 0 else 0
        })

    return render(request, 'finances/reports.html', {
        'chart_data': chart_data,
        'budget_data': budget_data,
        'categories': [choice[0] for choice in CATEGORY_CHOICES]
    })