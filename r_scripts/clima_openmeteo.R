# -*- coding: utf-8 -*-
# Consome a API pública Open-Meteo e imprime previsão simples no terminal.
# Ajuste latitude/longitude para sua região (Fortaleza como exemplo).

library(httr)
library(jsonlite)

lat <- -3.7327    # Fortaleza-CE
lon <- -38.5267

url <- paste0(
  "https://api.open-meteo.com/v1/forecast?",
  "latitude=", lat,
  "&longitude=", lon,
  "&hourly=temperature_2m,relative_humidity_2m,precipitation",
  "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum",
  "&timezone=auto"
)

resp <- GET(url)
stop_for_status(resp)

dados <- content(resp, as = "text", encoding = "UTF-8")
j <- fromJSON(dados)

cat("==== Clima - Open-Meteo ====\n")
cat("Local (lat,lon):", lat, lon, "\n\n")

# Resumo diário (hoje)
daily <- j$daily
if (!is.null(daily)) {
  cat("Previsão diária (próximos dias):\n")
  for (i in seq_along(daily$time)) {
    dia <- daily$time[i]
    tmin <- daily$temperature_2m_min[i]
    tmax <- daily$temperature_2m_max[i]
    prcp <- daily$precipitation_sum[i]
    cat(sprintf("  %s | Tmin: %.1f°C  Tmax: %.1f°C  Precipitação: %.1f mm\n",
                dia, tmin, tmax, prcp))
  }
} else {
  cat("Sem dados diários.\n")
}
