import sys
from bs4 import BeautifulSoup as sp
import re
import json
from datetime import datetime
import os
import math
import numpy as np


# with open('../static/conproba.json') as f:
#     data = json.load(f)

a = 3
b={'hoax':5,'valid':7}
c=90



print(max(b.values()))
# import pandas as pd
# to_csv = pd.DataFrame(data)
# print(to_csv)
# to_csv.to_csv('../offData/contoh.csv',encoding='utf-8-sig')

print("Program start at = ", datetime.now().time())
