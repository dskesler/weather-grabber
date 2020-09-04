import pandas as pd
import numbers as np
import plotly.express as px
import json as jsn

with open('~/Desktop/weather_bhm.json') as json_file:
    data = jsn.load(json_file)
    for dt in data['list']:
        print(dt)
