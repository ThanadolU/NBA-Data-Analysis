import pandas as pd


FILE_NAME = 'NBA Players/all_seasons_modified_csv.csv'


class NbaDataAnalysis:
    """Read file from all_season_modified_csv.csv and create 
    a dataframe for individual player.
    """

    def __init__(self) :
        """Read a csv file and define a columns that 
        I want to use in dataframe.
        """
        self.dataframe = pd.read_csv(FILE_NAME)
        self.columns = ['player_name', 'player_height','age', 'draft_round', 'draft_number', 
                        'season', 'mpg', 'ppg', 'rpg', 'apg', 'spg', 'bpg', 'topg', 'fg_pct', 
                        'fgm_pg', 'fga_pg','fg3_pct', 'fg3m_pg', 'fg3a_pg','ft_pct', 'ftm_pg', 
                        'fta_pg', 'tot_minutes', 'tot_pts', 'tot_fgm', 'tot_fga', 'tot_fg3m', 
                        'tot_fg3a', 'tot_ftm', 'tot_fta', 'tot_oreb', 'tot_dreb', 'tot_reb', 
                        'tot_ast', 'tot_stl', 'tot_blk', 'tot_to', 'plus_minus_pg']

    def get_new_df(self):
        """Create a dataframe of nba players.

        Returns:
            DataFrame: new dataframe of nba players
        """
        return self.dataframe[self.columns]

    def all_player_name(self):
        """Get list of nba players names (unique).

        Returns:
            list: nba players name (unique)
        """
        pname = []
        for name in self.get_new_df()['player_name']:
            if name not in pname:
                pname.append(name)
        return pname

    def get_individual_player_data(self, name, data1, data2):
        """Get dataframe of player that you want to know.

        Args:
            name: key for searh data of that player
            data1: data in x-axis (key for slide dataframe columns)
            data2: data in y-axis (key for slide dataframe columns)

        Returns:
            DataFrame: dataframe of individual player
        """
        players_data = self.get_new_df()
        key_name = self.columns[0]
        individual_player_data = players_data[[key_name, data1, data2]]
        return individual_player_data[individual_player_data[key_name] == name]


class Graph:
    """A graph that you can plot"""

    def __init__(self, nba: NbaDataAnalysis):
        # a constant for each possible state of the Graph
        self.onegraph = OneGraphState(nba)
        self.twograph = TwoGraphState(nba)
        # set a initial state of the graph.
        self.state = self.onegraph
 
    def change_state(self):
        """Change state of the graph.
        If it in to twograph, it will change to onegraph.
        If it in to onegraph, it will change to twograph.
        """
        self.state = self.twograph if self.state == self.onegraph else self.onegraph

    def plotting(self, name1, players, x, y, name2):
        """Plot a graph of player that you want to choose.

        Args:
            name1: key for searh data of that player1
            players: figure that you want to plot on it
            x: data in x-axis (key for slide dataframe columns)
            y: data in y-axis (key for slide dataframe columns)
            name2: key for searh data of that player2
        """
        self.state.plotting(name1, players, x, y, name2)


class GraphState:
    """Super class for Graph States"""
    def __init__(self, nba: NbaDataAnalysis):
        # save a reference to the nba stat.
        self.nba = nba

    def plotting(self):
        pass


class OneGraphState(GraphState):
    """State of onegraph used to player1"""
    def plotting(self, name1, players, x, y, name2=None):
        """Plot a graph of player that you want to choose.

        Args:
            name1: key for searh data of that player1
            players: figure that you want to plot on it
            x: data in x-axis (key for slide dataframe columns)
            y: data in y-axis (key for slide dataframe columns)
            name2(None): Nothing

        Returns:
            matplotlib.axes._subplots.AxesSubplot: ax for plot graph in matplotlib figure 
        """
        dataframe1 = self.nba.get_individual_player_data(name1, x, y)
        return dataframe1.plot.line(x, y, ax=players, color='r', marker='o',
                                    label=name1, grid=True, title=name1)


class TwoGraphState(GraphState):
    """State of twograph used to compare between player1 and player2"""

    def plotting(self, name1, players, x, y, name2):
        """Plot a graph of player that you want to choose.

        Args:
            name1: key for searh data of that player1
            players: figure that you want to plot on it
            x: data in x-axis (key for slide dataframe columns)
            y: data in y-axis (key for slide dataframe columns)
            name2: key for searh data of that player2

        Returns:
            matplotlib.axes._subplots.AxesSubplot: ax for plot graph in matplotlib figure 
        """
        dataframe1 = self.nba.get_individual_player_data(name1, x, y)
        dataframe2 = self.nba.get_individual_player_data(name2, x, y)

        player_1 = dataframe1.plot.line(x, y, ax=players, color='r', marker='o', 
                                        label=name1, grid=True)
        return dataframe2.plot.line(x, y, ax=player_1, color='b', marker='o', label=name2, 
                                    grid=True, title=f'{name1} and {name2}')
