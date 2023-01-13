"""File to launch application"""

from NbaStatUI import AppUI
from data import *


if __name__ == '__main__':
    nba = NbaDataAnalysis()
    graph = Graph(nba)
    ui = AppUI(nba, graph)
    ui.run()
