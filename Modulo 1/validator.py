import pandas as pd # type: ignore
import logging

def detect_anomalies(clients, orders, invoices, payments):
    anomalies = []

    valid_invoice_ids = set(invoices['invoice_id'].dropna())
    orphan_payments = payments[~payments['invoice_id'].isin(valid_invoice_ids)]
    for _, row in orphan_payments.iterrows():
        anomalies.append({
            'type': 'orphan_payment',
            'severity': 'HIGH',
            'detail': f"Pago {row.get('payment_id')} sin factura válida"
        })

    dup_invoices = invoices[invoices.duplicated(subset=['invoice_id'], keep=False)]
    if not dup_invoices.empty:
        anomalies.append({
            'type': 'duplicate_invoice',
            'severity': 'HIGH',
            'detail': f"{len(dup_invoices)} facturas duplicadas detectadas"
        })

    valid_client_ids = set(clients['client_id'].dropna())
    if 'client_id' in orders.columns:
        invalid_orders = orders[~orders['client_id'].isin(valid_client_ids)]
        for _, row in invalid_orders.iterrows():
            anomalies.append({
                'type': 'order_invalid_client',
                'severity': 'MEDIUM',
                'detail': f"Orden {row.get('order_id')} con cliente inválido"
            })

    if 'invoice_id' in payments.columns:
        merged = payments.merge(
            invoices[['invoice_id', 'total']], 
            on='invoice_id', how='left'
        )
        overpaid = merged[merged['amount'] > merged['total']]
        for _, row in overpaid.iterrows():
            anomalies.append({
                'type': 'overpayment',
                'severity': 'HIGH',
                'detail': f"Pago {row.get('payment_id')} supera el valor de factura"
            })

    if 'invoice_id' in payments.columns and 'issue_date' in invoices.columns:
        merged2 = payments.merge(
            invoices[['invoice_id', 'issue_date']],
            on='invoice_id', how='left'
        )
        if 'payment_date' in merged2.columns:
            bad_dates = merged2[
                merged2['payment_date'] < merged2['issue_date']
            ]
            for _, row in bad_dates.iterrows():
                anomalies.append({
                    'type': 'illogical_date',
                    'severity': 'MEDIUM',
                    'detail': f"Pago {row.get('payment_id')} anterior a fecha de factura"
                })

    logging.info(f"Total anomalías detectadas: {len(anomalies)}")
    return pd.DataFrame(anomalies)