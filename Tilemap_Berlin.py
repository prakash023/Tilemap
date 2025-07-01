# Installing here all the  necessary libraries
!pip install geopandas shapely pyproj fiona ipywidgets --quiet

# Imports
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import box, Polygon
import math
import os
from ipywidgets import FileUpload, Dropdown, Button, Output, RadioButtons, VBox
from IPython.display import display, clear_output
import ipywidgets as widgets

# Upload widget
upload = FileUpload(accept='.geojson', multiple=False)
label_col_selector = Dropdown(description='Label Column:')
tile_shape_selector = RadioButtons(options=['rectangle', 'hexagon'], description='Tile Shape:')
generate_button = Button(description='Generate Tiles', button_style='success')
#Here we have also defined the tile widget, which generates the tool slider, making it easier to change the desired value.
tile_widget = widgets.FloatSlider(value=0.98, min=0.50, max=2, step=0.01, description='Tilegröße:')

export_button = Button(description='Export GeoJSON', button_style='info')
#output = Output()
output = widgets.Output()


# Global variables for access across functions
bezirke = None
snapped_grid = None
final_grid = None
output_filename = "output_tiles.geojson"
na=None

def handle_upload(change):
    global bezirke
    global na
    if upload.value:
        for filename, fileinfo in upload.value.items():
            with open(filename, 'wb') as f:
                f.write(fileinfo['content'])

            na=filename
            bezirke = gpd.read_file(filename)
            bezirke = bezirke.to_crs(epsg=32633)

            # Populate dropdown with column names
            label_col_selector.options = list(bezirke.columns)

upload.observe(handle_upload, names='value')

def calculate_optimal_tile_size(bounds, target_count):
    minx, miny, maxx, maxy = bounds
    area = (maxx - minx) * (maxy - miny)
    tile_area = area / target_count
    size = math.sqrt(tile_area)
    return size, size

def generate_tiles(b):
    global snapped_grid, final_grid, output_filename
    with output:
      clear_output(wait=True)
      export_button.disabled = True

      if bezirke is None:
          with output:
              print(" upload hier Geojson-File.")
          return

      nam = label_col_selector.value
      tile_shape = tile_shape_selector.value
      label_mode = 'name'

      bezirke["centroid"] = bezirke.geometry.centroid
      minx, miny, maxx, maxy = bezirke.total_bounds
      target_cells = len(bezirke)
      grid_width, grid_height = calculate_optimal_tile_size(bezirke.total_bounds, target_cells)
      grid_size = tile_widget.value

      grid = []
      #the "while" loop here is crucial as it begins with an estimation of the tile size to accommodate all polygons,
      #continuing to create grids until there are sufficient tiles for all generated polygons
      #It halted at 25, which is more than 12 polygons. It corresponds the code to each polygon's
      #closest tile in the larger grid. For this reason, 12 polygons are positioned on 12 out of the 25 available tiles.

      while len(grid) != len(bezirke):  # The size of the grids are defined which results in making the different results.
          if len(grid) < len(bezirke):
              grid_width *= grid_size    #like here change the width and the height to 70 for rectangle, by default we have set on 0.98, or we can go higher( 0.98, 1.02, 1.5 etc!
              grid_height *= grid_size  #the result may vary with the increase or decrease in the width and height.
          else:
              grid_width *= grid_size +0.04
              grid_height *= grid_size + 0.04


          grid_cells = []

          if tile_shape == "rectangle":
              x = minx
              while x < maxx:
                  y = miny
                  while y < maxy:
                      grid_cells.append(box(x, y, x + grid_width, y + grid_height))
                      y += grid_height
                  x += grid_width

          elif tile_shape == "hexagon":
              hex_height = grid_height
              hex_width = math.sqrt(3) / 2 * hex_height
              y = miny
              row = 0
              while y < maxy + hex_height:
                  x = minx - (row % 2) * (hex_width / 2)
                  while x < maxx + hex_width:
                      angles = [math.radians(a) for a in range(-30, 330, 60)]
                      points = [(x + (hex_height / 2) * math.cos(a), y + (hex_height / 2) * math.sin(a)) for a in angles]
                      grid_cells.append(Polygon(points))
                      x += hex_width
                  y += hex_height * 0.75
                  row += 1
          else:
              raise ValueError("Invalid tile")

          grid = gpd.GeoDataFrame({'geometry': grid_cells}, crs=bezirke.crs)
          region_union = bezirke.geometry.union_all()
          grid = grid[grid.intersects(region_union)].reset_index(drop=True)
          grid["grid_centroid"] = grid.geometry.centroid

          if len(grid) >= len(bezirke):
              break

      assigned_geoms = []
      assigned_labels = []
      available_grids = grid.copy()

      for idx, row in bezirke.iterrows():
          centroid = row["centroid"]
          available_grids["distance"] = available_grids["grid_centroid"].distance(centroid)
          candidate_idx = available_grids["distance"].idxmin()
          assigned_geoms.append(available_grids.loc[candidate_idx].geometry)
          assigned_labels.append(row[nam])
          available_grids = available_grids.drop(index=candidate_idx)

      snapped_grid = gpd.GeoDataFrame({
          "geometry": assigned_geoms,
          nam: assigned_labels
      }, crs=bezirke.crs)

      # Combine with original attributes
      final_grid = snapped_grid.copy()
      try:
          final_grid = snapped_grid.drop(columns=[nam]).copy()
      except:
          pass
      attr = bezirke.drop(columns=['geometry', 'centroid']).reset_index(drop=True)
      final_grid = final_grid.join(attr)
      tile_size_str = f"{int(grid_width)}x{int(grid_height)}"



      #output_filename = f"generated_tilemap_{tile_shape}.geojson"
      export_button.disabled = False  # Enable export after generation
      with output:
          print("tiles generated successfully.")
          print("total nr. of Polygons:", len(bezirke))
          print("total nr. of tiles:", len(grid))
          print("Mapped tiles from  Original raster grid:", len(snapped_grid))



      # Plotting
      fig, ax = plt.subplots(figsize=(12, 8))
      snapped_grid.boundary.plot(ax=ax, edgecolor='blue', linewidth=0.8)
      bezirke.boundary.plot(ax=ax, edgecolor='black')
      for idx, row in snapped_grid.iterrows():
          centroid = row.geometry.centroid
          ax.text(centroid.x, centroid.y, str(row[nam])[:10], fontsize=8, ha='center', color='darkred')
      ax.set_title("Tile Map – zugeordnete Kacheln ")
      ax.set_aspect('equal')
      plt.tight_layout()
      plt.show()


def export_geojson(button):
    global output_filename # Make output_filename global to be accessible by check_export_file
    if final_grid is None:
        with output:
            print("Please click on Generate Tiles")
        return

    original_filename_base = os.path.splitext(os.path.basename(na))[0]
    tile_shape = tile_shape_selector.value
    # Generate the output filename here where it is used for saving.
    output_filename = f"{original_filename_base}_{tile_shape}.geojson"

    final_grid.to_file(output_filename, driver='GeoJSON')
    with output:
        print(f"file exported: {output_filename}")
    check_export_file()

def check_export_file():

    print(f"Checking for file: {output_filename}") # Print the filename being checked
    if os.path.exists(output_filename):
        print(f"File '{output_filename}' was successfully created.")
    else:
        print(f"Error: File '{output_filename}' was not created.")


generate_button.on_click(generate_tiles)
export_button.on_click(export_geojson)
display(VBox([upload, label_col_selector,
              tile_shape_selector,tile_widget, generate_button, export_button, output]))