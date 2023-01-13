import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from tkinter import filedialog as fd
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from data import *
from threading import Thread


class ProgressBar(tk.Toplevel):
    """Toplevel for a Progress bar."""
    def __init__(self, parent):
        super().__init__(parent)
        self.title('Change State')
        self.progressbar()

    def progressbar(self):
        """Create a label frame and progress bar"""
        self.label = ttk.LabelFrame(self, text="Please Wait")
        self.label.grid(row=0, column=0, sticky="news", padx=5, pady=5)
        self.label.rowconfigure(0, weight=1)
        self.label.rowconfigure(1, weight=1)
        self.label.columnconfigure(0, weight=1)
        self.bar = ttk.Progressbar(self.label, length=500, mode="indeterminate")
        self.status = ttk.Label(self.label, text="Running")

        # Grid label frame, progress bar and status
        self.label.grid(row=0, column=0, sticky='nsew', padx=10)
        self.bar.grid(row=1, column=0, sticky="sew", padx=10)
        self.status.grid(row=2, column=0, sticky="wn", padx=10)


class AppUI(tk.Tk):
    """Use Interface for nba stat.

    The UI displays a graph of each players
    """
    def __init__(self, data: NbaDataAnalysis, graph: Graph):
        super().__init__()
        # save a reference to the nba stat
        self.data = data 
        # save a reference to the graph
        self.graph = graph
        # save a reference to the list of players name
        self.name = self.data.all_player_name()
        self.options = {'padx': 10, 'pady': 10, 'sticky': tk.NSEW}
        self.init_components()

    def init_components(self):
        """Create components and layout the UI."""

        # Components
        self.title("NBA Data Analysis")
        self.create_label_frame()
        self.compare_two_player()
        self.create_inside_label_frame()
        self.create_combobox()
        self.load_player_name
        self.load_column_name()
        self.create_button()
        self.forget(self.player2)
        self.forget(self.label4)
        
        # Rows configure
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        
        # Columns configure
        self.columnconfigure(0, weight=1)

    def create_label_frame(self):
        """Create all label frames"""
        self.label_frame_1 = ttk.LabelFrame(self, text='Player Data')
        self.label_frame_2 = ttk.LabelFrame(self, text='Command')
        
        self.label_frame_1.grid(row=2, column=0)
        self.label_frame_2.grid(row=0, column=0)

    def create_inside_label_frame(self):
        """Create label inside label frame1"""
        self.label1 = tk.Label(self.label_frame_1, text='Player-1')
        self.label2 = tk.Label(self.label_frame_1, text='x-axis')
        self.label3 = tk.Label(self.label_frame_1, text='y-axis')
        self.label4 = tk.Label(self.label_frame_1, text='Player-2')
        
        self.label1.grid(row=1, column=0, **self.options)
        self.label2.grid(row=1, column=1, **self.options)
        self.label3.grid(row=1, column=2, **self.options)
        self.label4.grid(row=1, column=3, **self.options)

    def create_combobox(self):
        """Create combo box inside label frame1"""
        self.all_name1 = tk.StringVar()
        self.all_name2 = tk.StringVar()
        self.x_data = tk.StringVar()
        self.y_data = tk.StringVar()
        self.player1 = ttk.Combobox(self.label_frame_1, textvariable=self.all_name1)
        self.player2 = ttk.Combobox(self.label_frame_1, textvariable=self.all_name2)
        self.x_axis = ttk.Combobox(self.label_frame_1, state='readonly', textvariable=self.x_data)
        self.y_axis = ttk.Combobox(self.label_frame_1, state='readonly', textvariable=self.y_data)
        
        # load players name inside combo box (player1)
        self.player1['values'] = self.name
        self.player1.bind('<KeyRelease>', self.load_player_name)
        self.player1.grid(row=0, column=0, **self.options)

        # load players name inside combo box (player2)
        self.player2['values'] = self.name
        self.player2.bind('<KeyRelease>', self.load_player_name)
        self.player2.grid(row=0, column=3, **self.options)

        self.x_axis.grid(row=0, column=1, **self.options)
        self.y_axis.grid(row=0, column=2, **self.options)

    def create_button(self):
        """Create all command button inside label frame2"""
        self.switch = ttk.Button(self.label_frame_2, text='State', command=self.progressbar)
        self.plot = ttk.Button(self.label_frame_2, text='Plot', command=self.show_first_second_player)
        self.save = ttk.Button(self.label_frame_2, text='Save', command=self.save_figure)
        self.clear = ttk.Button(self.label_frame_2, text='Clear', command=self.clear_handler)
        self.btn_quit = ttk.Button(self.label_frame_2, text='Quit', command=self.destroy)
        
        self.switch.grid(row=0, column=0, **self.options)
        self.plot.grid(row=0, column=1, **self.options)
        self.save.grid(row=0, column=2, **self.options)
        self.clear.grid(row=0, column=3, **self.options)
        self.btn_quit.grid(row=0, column=4, **self.options)

    def error_box(self):
        """Create error message"""
        messagebox.showerror(title='Error', message="You can't plot a graph without any data inside Combo box")
        
    def warning_box1(self):
        """Create warning message1"""
        messagebox.showwarning(title='Warning', message="You can't plot a graph because you didn't select x and y axes")

    def warning_box2(self):
        """Create warning message2"""
        messagebox.showwarning(title='Warning', message="You can't compare the same player")

    def forget(self, widget):
        """Forget grid"""
        widget.grid_forget()
        
    def retrieve1(self, widget):
        """Retrieve combo box for player2"""
        widget.grid(row=0, column=3)
    
    def retrieve2(self, widget):
        """Retrieve label for player2"""
        widget.grid(row=1, column=3)

    def have_grid(self, widget):
        return bool(widget.grid_info())

    def compare_two_player(self):
        """Figure (graph) of player1 and player2"""
        self.fig_players = Figure()
        self.players = self.fig_players.add_subplot()

        self.fig_canvas = FigureCanvasTkAgg(self.fig_players, master=self)
        self.fig_canvas.get_tk_widget().grid(row=1, column=0,
                                              sticky="news", padx=10, pady=10)

    def load_player_name(self, event):
        """Load players name to combo box and search players name"""
        all_name_1 = event.widget.get()
        all_name_2 = event.widget.get()
        if all_name_1 == '' or all_name_2 == '':
            self.player1['values'] = self.name
            self.player2['values'] = self.name
        else:
            data = [item for item in self.name 
                    if (all_name_1 in item) or (all_name_2 in item)]
            self.player1['values'] = data
            self.player2['values'] = data

    def load_column_name(self):
        """Load player data of x and y axes"""
        x_data = ['age', 'player_height', 'season', 'mpg', 'plus_minus_pg']
        y_data = ['mpg', 'ppg', 'rpg', 'apg', 'spg', 'bpg', 'topg', 'fg_pct', 
                    'fgm_pg', 'fga_pg','fg3_pct', 'fg3m_pg', 'fg3a_pg','ft_pct', 'ftm_pg', 
                    'fta_pg', 'tot_minutes', 'tot_pts', 'tot_fgm', 'tot_fga', 'tot_fg3m', 
                    'tot_fg3a', 'tot_ftm', 'tot_fta', 'tot_oreb', 'tot_dreb', 'tot_reb', 
                    'tot_ast', 'tot_stl', 'tot_blk', 'tot_to']
        self.x_axis['values'] = x_data
        self.y_axis['values'] = y_data

    def show_first_second_player(self):
        """Figure (graph) of player1 and player2 
        [depend on state at that time]
        """
        all_name_1 = self.all_name1.get()
        all_name_2 = self.all_name2.get()
        x_data = self.x_data.get()
        y_data = self.y_data.get()

        self.fig_players.subplots_adjust(bottom=0.15)
        try:
            if all_name_1 != all_name_2 and x_data == '' and y_data == '':
                self.warning_box1()
            elif all_name_1 == all_name_2 and x_data != '' and y_data != '':
                self.warning_box2()
            else:
                self.players.clear()
                self.figure = self.graph.plotting(all_name_1, self.players, x_data, y_data, 
                                                  all_name_2)
        except KeyError:
            self.error_box()

        self.fig_canvas.draw()

    def save_figure(self):
        """Save image of figure"""
        save_file = fd.asksaveasfilename(title='Save File', filetypes=(("PNG file", "*.png"),))
        if save_file != '':
            self.players.get_figure().savefig(save_file)

    def clear_handler(self):
        """Clear figure and all combo boxes"""
        self.all_name1.set('')
        self.x_data.set('')
        self.y_data.set('')
        self.all_name2.set('')
        self.players.clear()
        self.fig_canvas.draw()

    def progressbar(self):
        """Show progress bar and change state"""
        window = ProgressBar(self)
        window.grab_set()
        self.run_task(window)
        if self.have_grid(self.player2):
            self.forget(self.player2)
            self.forget(self.label4)
        else:
            self.retrieve1(self.player2)
            self.retrieve2(self.label4)

    def run_task(self, window: ProgressBar):
        self.task_thread = Thread(target=self.graph.change_state)
        self.task_thread.start()
        window.bar.start()
        self.after(10, lambda: self.check_task(window))

    def check_task(self, window: ProgressBar):
        """Check task regularly whether it has completed"""
        if self.task_thread.is_alive():
            self.after(10, lambda: self.check_task(window))
        else:
            window.status.config(text='Done')
            window.bar.stop()
            window.destroy()

    def run(self):
        # start the app, wait for events
        self.mainloop()
