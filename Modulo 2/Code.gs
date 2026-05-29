const TELEGRAM_TOKEN = "TOKEN_BOT";
const TELEGRAM_CHAT_ID = "CHAT_ID";
const SPREADSHEET_ID = SpreadsheetApp.getActiveSpreadsheet().getId();

function runKPIMonitor() {
  try {
    logProcess("KPI_MONITOR", "STARTED", "Iniciando monitoreo de KPIs");
    
    const kpis = readKPIs();
    const alerts = [];
    
    kpis.forEach(kpi => {
      const result = evaluateKPI(kpi);
      if (result.hasAlert) {
        alerts.push(result);
        registerAlert(result);
      }
    });
    
    if (alerts.length > 0) {
      sendTelegramSummary(alerts);
    } else {
      sendTelegram("✅ Todos los KPIs están dentro del rango esperado.");
    }
    
    logProcess("KPI_MONITOR", "SUCCESS", `${alerts.length} alertas generadas`);
    
  } catch (error) {
    logProcess("KPI_MONITOR", "ERROR", error.toString());
    sendTelegram(`❌ Error en monitoreo: ${error.toString()}`);
  }
}

function readKPIs() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("KPIs");
  if (!sheet) throw new Error("Hoja 'KPIs' no encontrada");
  
  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  const kpis = [];
  
  for (let i = 1; i < data.length; i++) {
    const row = data[i];
    
    if (!row[0]) continue;
    
    const kpi = {};
    headers.forEach((header, index) => {
      kpi[header] = row[index];
    });
    
    kpis.push(kpi);
  }
  
  return kpis;
}

function evaluateKPI(kpi) {
  const result = {
    kpi_id: kpi.kpi_id || "unknown",
    team: kpi.team || "unknown",
    hasAlert: false,
    severity: "LOW",
    message: ""
  };
  
  if (!kpi.current_value && kpi.current_value !== 0) {
    result.hasAlert = true;
    result.severity = "HIGH";
    result.message = `KPI ${result.kpi_id} sin valor actual registrado`;
    return result;
  }
  
  if (!kpi.threshold && kpi.threshold !== 0) {
    result.hasAlert = true;
    result.severity = "MEDIUM";
    result.message = `KPI ${result.kpi_id} sin threshold definido`;
    return result;
  }
  
  const current = parseFloat(kpi.current_value);
  const threshold = parseFloat(kpi.threshold);
  const target = parseFloat(kpi.target) || threshold;
  
  if (current < threshold) {
    const pct = target > 0 ? Math.round((current / target) * 100) : 0;
    result.hasAlert = true;
    result.severity = pct < 50 ? "CRITICAL" : "HIGH";
    result.message = `KPI ${result.kpi_id} (${result.team}): valor ${current} bajo threshold ${threshold} (${pct}% del objetivo)`;
  }
  
  return result;
}

function sendTelegram(message) {
  try {
    const url = `https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`;
    const payload = {
      chat_id: TELEGRAM_CHAT_ID,
      text: message,
      parse_mode: "HTML"
    };
    
    UrlFetchApp.fetch(url, {
      method: "POST",
      contentType: "application/json",
      payload: JSON.stringify(payload),
      muteHttpExceptions: true
    });
    
  } catch (error) {
    logProcess("TELEGRAM", "ERROR", error.toString());
  }
}

function sendTelegramSummary(alerts) {
  const critical = alerts.filter(a => a.severity === "CRITICAL").length;
  const high = alerts.filter(a => a.severity === "HIGH").length;
  
  let message = `🚨 <b>ALERTA DE KPIs — Quark.i</b>\n\n`;
  message += `📊 Total alertas: ${alerts.length}\n`;
  message += `🔴 Críticas: ${critical}\n`;
  message += `🟠 Altas: ${high}\n\n`;
  message += `<b>Detalle:</b>\n`;
  
  alerts.forEach(alert => {
    const icon = alert.severity === "CRITICAL" ? "🔴" : 
                 alert.severity === "HIGH" ? "🟠" : "🟡";
    message += `${icon} ${alert.message}\n`;
  });
  
  message += `\n⏰ ${new Date().toLocaleString()}`;
  sendTelegram(message);
}

function registerAlert(alert) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Alerts");
  if (!sheet) return;
  
  sheet.appendRow([
    new Date(),
    alert.kpi_id,
    alert.severity,
    alert.message
  ]);
}

function logProcess(process, status, detail) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet()
                                .getSheetByName("Logs");
    if (!sheet) return;
    
    sheet.appendRow([new Date(), process, status, detail]);
  } catch (e) {
    console.log("Error en log:", e);
  }
}