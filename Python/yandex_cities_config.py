from collections import namedtuple

City = namedtuple("City", ["shp_stem", "center_coords"])

city_grids_and_center_coords = {
    "moscow": City("moscow_grid", "55.749435, 37.629416"),
    "st_petersburg": City("st_petersburg_grid", "59.938996, 30.315482"),
}
