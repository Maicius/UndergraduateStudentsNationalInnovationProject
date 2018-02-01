import pandas as pd
from USNIP import USNIP
if __name__ == '__main__':
    usnip = USNIP()
    _2015_data = pd.read_excel('2015.xls', header=None)
    usnip._2015_data = _2015_data.iloc[3:]
    usnip.calculate_keyword(_2015_data.iloc[3:, 3:4])
    pass