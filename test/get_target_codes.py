import sys, os
import numpy as np
from tqdm import tqdm
from datetime import datetime
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from tools.quotation_api import *
from tools.intereset_checker import InterestChecker

#num_to_choose = 10
formatted_date = datetime.now().strftime("%y%m%d_%H%M%S")


if __name__ == '__main__':
    codes = get_tickers()
#    num = len(codes)
#    selected_integers = np.random.choice(np.arange(0, num + 1), size=num_to_choose, replace=False)

    with open(f"output/interest_stocks_{formatted_date}.txt", "w") as f:
        for code in tqdm(codes):
            checker = InterestChecker(code = code, chart = get_minute_charts(code=code, count=97, unit=60))
            f.write(str(checker)); f.write("\n\n")