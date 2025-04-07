from django.shortcuts import render, redirect
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from .models import Income, Transaction
from .forms import IncomeForm, TransactionForm

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
                    transaction.save()
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
    return render(request, 'finances/budget.html')

@login_required
def reports_view(request):
    return render(request, 'finances/reports.html')
