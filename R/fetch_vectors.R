library(sf)
library(dplyr)
library(tmap)
library(here)

# Fetch vectors for Russia
russia <- geodata::gadm("Russia", path = here::here("data"), level = 2)
russia <- st_as_sf(russia)

# Extract Moscow
moscow <- russia |>
  filter(NAME_1 == "Moscow City") |>
  st_transform(crs = 32637)

moscow |>
  qtm()

# Generate a grid of point for Moscow
grid <- st_make_grid(moscow, cellsize = 500, what = "centers")
grid <- grid[moscow]

tm_shape(moscow) +
  tm_polygons() +
  tm_shape(grid) +
  tm_symbols(size = 0.01) +
  tm_scale_bar()

# Transform to WGS84 and export
if (!file.exists(here("data", "shp", "moscow_grid.shp"))) {
  grid |>
    st_as_sf() |>
    mutate(public = NA, car = NA, walk = NA, cycle = NA, date = NA) |>
    st_transform(crs = 4326) |>
    write_sf(here("data", "shp", "moscow_grid.shp"))
}

# Extract Saint Petersburg
st_petersburg <- russia |>
  filter(NAME_1 == "City of St. Petersburg") |>
  st_transform(crs = 32637)

st_petersburg |>
  qtm()

# Generate a grid of point for Moscow
grid <- st_make_grid(st_petersburg, cellsize = 500, what = "centers")
grid <- grid[st_petersburg]

tm_shape(st_petersburg) +
  tm_polygons() +
  tm_shape(grid) +
  tm_symbols(size = 0.01) +
  tm_scale_bar()

# Transform to WGS84 and export
if (!file.exists(here("data", "shp", "st_petersburg_grid.shp"))) {
  grid |>
    st_as_sf() |>
    mutate(public = NA, car = NA, walk = NA, cycle = NA, date = NA) |>
    st_transform(crs = 4326) |>
    write_sf(here("data", "shp", "st_petersburg_grid.shp"))
}
