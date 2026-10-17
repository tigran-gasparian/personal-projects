# Functions within `AsphaltPacks.py`

`get_3_car_hunt_pack`, `get_10_pack_distribution` and `get_10_multi_pack_distribution` convolve probability functions of opening a single pack into probability functions of opening the whole bundle.

`run_simulation` use one of the previous functions to simulate players opening the bundles until they reach a goal. 

Its output is a probability function on amount of bundles to open before obtaining X blueprints

This project uses the following libraries:
* `math`
* `numpy`
* `matplotlib`
