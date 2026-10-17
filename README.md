# Functions within `AsphaltPacks.py`

`get_3_car_hunt_pack`, `get_10_pack_distribution` and `get_10_multi_pack_distribution` convolve probability functions of opening a single pack into probability functions of opening the whole bundle.

`run_simulation` use one of the previous functions and vectorisation to simulate players opening the bundles until they reach a goal. 

`cumulative_probability_plot` outputs a probability function on amount of bundles to open before obtaining X blueprints

<img width="1289" height="718" alt="high_res_graph" src="https://github.com/user-attachments/assets/fb31dab4-2ea7-494e-8156-c8619213371b" />

This project uses the following libraries:
* `math`
* `numpy`
* `matplotlib`
