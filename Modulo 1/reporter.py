import pandas as pd  # type: ignore
from datetime import date

def generate_financial_summary(invoices, payments):
    total_invoiced = invoices['total'].sum()
    total_paid = payments['amount'].sum()
    balance_pending = total_invoiced - total_paid

    if 'client_id' in invoices.columns:
        debt_by_client = invoices.groupby('client_id')['total'].sum().reset_index()
        debt_by_client.columns = ['client_id', 'total_invoiced']
        debt_by_client = debt_by_client.sort_values('total_invoiced', ascending=False)
    else:
        debt_by_client = pd.DataFrame()

    total = len(invoices)
    overdue = len(invoices[invoices['status'] == 'overdue'])
    pct_overdue = round((overdue / total * 100), 2) if total > 0 else 0

    summary = pd.DataFrame([{
        'total_invoiced': round(total_invoiced, 2),
        'total_paid': round(total_paid, 2),
        'balance_pending': round(balance_pending, 2),
        'pct_overdue_invoices': pct_overdue,
        'generated_at': date.today()
    }])

    return summary, debt_by_client