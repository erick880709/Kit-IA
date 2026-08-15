# Convierte NHAMCS ED (XPT v8) a CSV usando haven
.libPaths(c("C:/Users/ELITEBOOK/Rlib", .libPaths()))
library(haven)

base <- "c:/Users/ELITEBOOK/OneDrive/Documentos/Repositorio/Trabajo/kit-ia/datasets"
pares <- list(
  c("nhamcs_ED2018/ED2018", "nhamcs_ed2018.csv"),
  c("nhamcs_ED2019/ed2019", "nhamcs_ed2019.csv"),
  c("nhamcs_ed2020/ed2020", "nhamcs_ed2020.csv"),
  c("nhamcs_ed2021/ed2021", "nhamcs_ed2021.csv"),
  c("nhamcs_ed2022/ed2022", "nhamcs_ed2022.csv")
)
for (p in pares) {
  entrada <- file.path(base, p[1])
  salida <- file.path(base, p[2])
  d <- read_xpt(entrada)
  write.csv(d, salida, row.names = FALSE, na = "")
  cat("OK", p[2], nrow(d), "filas\n")
}
