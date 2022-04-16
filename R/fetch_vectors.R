library(sf)
library(dplyr)
library(tmap)
library(here)

russia <- geodata::gadm("Russia", path = here::here("data"), level = 2)
russia <- st_as_sf(russia)

moscow <- russia |>
  filter(NAME_1 == "Moscow City") |>
  st_transform(crs = 32637)

moscow |>
  qtm()

grid <- st_make_grid(moscow, cellsize = 500, what = "centers")
grid <- grid[moscow]

# tmap_mode("plot")

tm_shape(moscow) +
  tm_polygons() +
  tm_shape(centroid) +
  tm_symbols(col = "red", size = 0.5) +
  tm_shape(grid) +
  tm_symbols(size = 0.01) +
  tm_scale_bar()

centroid <- moscow |>
  st_geometry() |>
  st_union() |>
  st_centroid()

# transform to WGS84 and export
grid |>
  st_transform(crs = 4326) |>
  write_sf(here("data", "shp", "moscow_grid.shp"))
