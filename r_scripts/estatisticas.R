# -*- coding: utf-8 -*-
# Lê o CSV exportado pelo Python e calcula estatísticas simples.

# Pacotes base são suficientes
csv_path <- file.path("..", "python_app", "dados_operacoes.csv")

if (!file.exists(csv_path)) {
  stop(paste("Arquivo não encontrado:", csv_path,
             "\nAntes, rode o app Python e exporte o CSV."))
}

dados <- read.csv(csv_path, sep = ",", dec = ".", stringsAsFactors = FALSE)

cat("==== Estatísticas FarmTech ====\n\n")
cat("Registros:", nrow(dados), "\n\n")

# Exemplos de métricas:
metricas <- list(
  area_m2_media = mean(dados$area_m2, na.rm = TRUE),
  area_m2_desvio = sd(dados$area_m2, na.rm = TRUE),
  total_L_media = mean(dados$total_L, na.rm = TRUE),
  total_L_desvio = sd(dados$total_L, na.rm = TRUE),
  dose_mL_por_m_media = mean(dados$dose_mL_por_m, na.rm = TRUE),
  dose_mL_por_m_desvio = sd(dados$dose_mL_por_m, na.rm = TRUE)
)

print(metricas)

# Estatísticas por cultura
cat("\n--- Por Cultura ---\n")
culturas <- unique(dados$cultura)
for (c in culturas) {
  sub <- dados[dados$cultura == c, ]
  cat("\nCultura:", c, "\n")
  cat("  n =", nrow(sub), "\n")
  cat("  Área média (m2):", round(mean(sub$area_m2, na.rm = TRUE), 2), "\n")
  cat("  Total litros médio:", round(mean(sub$total_L, na.rm = TRUE), 2), "\n")
}
