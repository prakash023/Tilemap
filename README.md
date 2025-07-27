# Introduction
This project serves as a repository for the code developed as a part of Master's thesis by Prakash Neupane titled "Conversion of irregular polygons into regular grid geometries - Berlin as an example"

# Abstract
The irregular shapes and sizes of administrative boundaries, regionalization error are a common
problem in the field of spatial analysis. To address this issue, this research paper introduces a new
interactive python based prototype that transforms a irregular polygon geometries into a regular
tile base units forming a hexagonal or rectangular grids. The tool is entirely based developed in
Jupyter Notebook with GeoPandas, Shapely, ipywidgets, and Matplotlib, which ensures smooth
operation in visualization, transformations, and export of geospatial data to a GeoJSON format.
To ensure a one-to-one match between original polygons and generated tiles while preserving
the spatial proximity, a centroid-based greedy assignment approach is employed. Two different
key evaluation metrics, RMS centroid offset and spatial coverage percentage, are used to assess
the quality of the assigned tool.
To test the effectiveness of the tool, a simplified case study was conducted based on Berlins ad-
ministrative Dataset(Prognoseräume, Bezirksregionen and Plannugsregion). The results indicate
that the generated tilemaps enhance spatial uniformity and may improve comparability and in-
terpretability in thematic mapping. While the integrated export function enables the generated
tile to integrate into standard GIS platforms seamlessly. With minimal distortion, the developed
tool can help in the field of thematic mapping and provide support for fairer and more consis-
tent visualizations, assisting urban planners, geospatial analysts, and researchers in their spatial
analysis tasks.

**Keywords**:Tilemap, regular grid, GIS, centroid-based assignment, geospatial analysis, thematic
mapping, spatial visualization, RMS offset, GeoJSON, regionalization error.

# Usage

## Clone / Download the Code
Either download the code as a zip file or clone the code using `git clone https://github.com/prakash023/Tilemap.git`

## Setup / Prerequisites

### Prerequisites
The code can be run using jupyter notebook. Following programs and packages are required:
1. Python3 (version 3.12 tested)
2. Jupyter Notebook


### Running using Jupyter Notebook
** Optional **
Use python virtual environment and ipykernel to select the appropriate virutal environment for jupyter notebook.

1. Make sure the requirements are installed `pip3 install -r requirements.txt`
2. Run jupyter notebook. `jupyter notebook`
3. Click on the file `tilemap_implementation.ipynb`on the jupyter notebook web interface.



## Running Locally

## Upload GeoJSON file to process

## Options
- choose labels, etc.
- Choose scaling factor
- Exporting as GeoJSON after processing

## Visualization



## 
