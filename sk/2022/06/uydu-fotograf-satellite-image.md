# Uydu Fotograflarina Erismek

```python
from pystac_client import Client
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import rioxarray

api_url = "https://earth-search.aws.element84.com/v0"
client = Client.open(api_url)

# collection: Sentinel-2, Level 2A, COGs
collection = "sentinel-s2-l2a-cogs"

# AMS coordinates
lat, lon = 52.37, 4.90
geometry = {"type": "Point", "coordinates": (lon, lat)}

mysearch = client.search(
    collections=[collection],
    intersects=geometry,
    max_items=10,
)

for item in mysearch.items():
   print (item)
   print(item.assets["thumbnail"].href)
   visual_href = item.assets["visual"].href
   break
```

```text
<Item id=S2A_31UFU_20220629_0_L2A>
https://roda.sentinel-hub.com/sentinel-s2-l1c/tiles/31/U/FU/2022/6/29/0/preview.jpg
```




```python
visual = rioxarray.open_rasterio(visual_href)
print(visual)
visual_clip = visual.rio.clip_box(
    minx=627000,
    maxx=631000,
    miny=5802000,
    maxy=5806000
)
visual_clip.plot.imshow(figsize=(10,10))
plt.savefig('uydu_01.png')
```

```text
<xarray.DataArray (band: 3, y: 10980, x: 10980)>
[361681200 values with dtype=uint8]
Coordinates:
  * band         (band) int64 1 2 3
  * y            (y) float64 5.9e+06 5.9e+06 5.9e+06 ... 5.79e+06 5.79e+06
  * x            (x) float64 6e+05 6e+05 6e+05 ... 7.098e+05 7.098e+05 7.098e+05
    spatial_ref  int64 0
Attributes:
    _FillValue:    0.0
    scale_factor:  1.0
    add_offset:    0.0
    grid_mapping:  spatial_ref
```

![](uydu_01.png)

Kaynaklar

[1] [The Carpentries Incubator](https://carpentries-incubator.github.io/geospatial-python/19-access-data/index.html)

