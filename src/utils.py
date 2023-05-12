

BUNDESTAG_DATA_PATH = "data/Bundestag/"
BUNDESTAG_GRAPH_PATH = "graphs/Bundestag/"
YEAR_TO_LEG_ID = {"2021": 132, "2017": 111, "2013": 97, "2009": 83, "2005": 67}


def year_to_period(year):
    return f'{year}-{int(year)+4}'