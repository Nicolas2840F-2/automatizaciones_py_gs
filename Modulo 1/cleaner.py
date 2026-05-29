import pandas as pd # type: ignore
import logging

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def clean_monetary(value):
    try:
        if pd.isna(value):
            return 0.0
        cleaned = str(value).replace('$','').replace(',','').replace(' ','')
        return float(cleaned)
    except:
        return 0.0

def clean_dates(df, date_columns):
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def normalize_status(value, valid_values):
    if pd.isna(value):
        return 'unknown'
    normalized = str(value).strip().lower()
    return normalized if normalized in valid_values else 'unknown'

def remove_duplicates(df, subset=None):
    before = len(df)
    df = df.drop_duplicates(subset=subset)
    after = len(df)
    if before != after:
        logging.warning(f"Se eliminaron {before - after} duplicados")
    return df

def clean_clients(df):
    logging.info("Limpiando clientes...")
    df = remove_duplicates(df, subset=['client_id'])
    df['company_name'] = df['company_name'].str.strip().str.title()
    return df

def clean_invoices(df):
    logging.info("Limpiando facturas...")
    df = remove_duplicates(df, subset=['invoice_id'])
    df = clean_dates(df, ['issue_date', 'due_date'])
    df['total'] = df['total'].apply(clean_monetary)
    df['tax'] = df['tax'].apply(clean_monetary)
    df['status'] = df['status'].apply(
        lambda x: normalize_status(x, ['paid', 'pending', 'overdue', 'cancelled'])
    )
    return df

def clean_payments(df):
    logging.info("Limpiando pagos...")
    df = remove_duplicates(df, subset=['payment_id'])
    df = clean_dates(df, ['payment_date'])
    df['amount'] = df['amount'].apply(clean_monetary)
    return df

def clean_orders(df):
    logging.info("Limpiando órdenes...")
    df = remove_duplicates(df, subset=['order_id'])
    df = clean_dates(df, ['order_date'])
    df['amount'] = df['amount'].apply(clean_monetary)
    return df