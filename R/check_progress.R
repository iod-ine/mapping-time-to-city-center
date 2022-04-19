library(sf)
library(tmap)
library(here)
library(dplyr)

dd <- read_sf(here("data", "shp", "st_petersburg_times.shp"))

dd |>
  mutate(has_time = !is.na(best_time)) |>
  tm_shape() +
  tm_symbols(size = 0.1, col = "has_time")
