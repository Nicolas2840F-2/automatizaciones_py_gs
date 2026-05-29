# Quark.i — AI Automation Developer — Prueba Técnica

## Descripción general
Solución a los dos módulos de la prueba técnica.

## Estructura del proyecto
modulo1/ → pipeline Python de limpieza financiera
modulo2/ → sistema Apps Script de monitoreo de KPIs

## MÓDULO 1 — Instalación y ejecución
### Requisitos
- Python instalado
- pip install pandas

### Cómo correr
cd modulo1
python main.py

### Outputs generados
- output/clean_data/ → CSVs limpios
- output/financial_summary.csv → resumen financiero
- output/anomalies_report.csv → anomalías detectadas

## MÓDULO 2 — Instrucciones
1. Abrir el Google Sheet
2. Ir a Extensiones → Apps Script
3. Pegar el código de Code.gs
4. Configurar TELEGRAM_TOKEN y TELEGRAM_CHAT_ID
5. Ejecutar run o runKPIMonitor()

## Supuestos que asimile
- Los formatos monetarios con coma se asumen como separador de miles
- Fechas inválidas se convierten a NaT y se reportan como anomalía
- Un KPI sin threshold se reporta como alerta MEDIUM

## Decisiones técnicas
- Se eligió modularidad sobre un script único para facilitar mantenimiento
- Se usó logging en lugar de print para trazabilidad
- Apps Script separado por funciones para permitir cambios aislados

## Limitaciones
- El limpiador asume que los IDs son únicos por definición del negocio
- La integración con Telegram requiere bot creado manualmente
