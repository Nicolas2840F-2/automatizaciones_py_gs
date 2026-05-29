import pandas as pd  # type: ignore
import os
import logging
from cleaner import clean_clients, clean_invoices, clean_payments, clean_orders
from validator import detect_anomalies
from reporter import generate_financial_summary

logging.basicConfig(level=logging.INFO)


DATA_PATH = "data/"
OUTPUT_PATH = "output/"
CLEAN_PATH = OUTPUT_PATH + "clean_data/"

os.makedirs(CLEAN_PATH, exist_ok=True)
os.makedirs(OUTPUT_PATH, exist_ok=True)

def load_data():
    clients = pd.read_csv(f"{DATA_PATH}clients.csv")
    orders = pd.read_csv(f"{DATA_PATH}orders.csv")
    invoices = pd.read_csv(f"{DATA_PATH}invoices.csv")
    payments = pd.read_csv(f"{DATA_PATH}payments.csv")
    return clients, orders, invoices, payments

def run_pipeline():
    logging.info("=== INICIANDO PIPELINE ===")
    
    
    clients, orders, invoices, payments = load_data()
    
    clients = clean_clients(clients)
    orders = clean_orders(orders)
    invoices = clean_invoices(invoices)
    payments = clean_payments(payments)
    
    clients.to_csv(f"{CLEAN_PATH}clients_clean.csv", index=False)
    orders.to_csv(f"{CLEAN_PATH}orders_clean.csv", index=False)
    invoices.to_csv(f"{CLEAN_PATH}invoices_clean.csv", index=False)
    payments.to_csv(f"{CLEAN_PATH}payments_clean.csv", index=False)
    
    anomalies = detect_anomalies(clients, orders, invoices, payments)
    anomalies.to_csv(f"{OUTPUT_PATH}anomalies_report.csv", index=False)
    
    summary, debt = generate_financial_summary(invoices, payments)
    summary.to_csv(f"{OUTPUT_PATH}financial_summary.csv", index=False)
    
    logging.info("=== PIPELINE COMPLETADO ===")
    logging.info(f"Anomalías encontradas: {len(anomalies)}")
    logging.info(f"Resumen financiero generado")

if __name__ == "__main__":
    run_pipeline()