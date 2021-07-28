import json
import requests
import tkinter as tk
import tkinter.ttk as ttk
import urllib.request

# Requirements
from PIL import Image, ImageTk # pillow

# Request patch version and items data from Data Dragon
version = requests.get('https://ddragon.leagueoflegends.com/api/versions.json').json()[0]
items = requests.get(f'https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json').json()


class Application(tk.Frame):
    def __init__(self, master: tk.Tk = None) -> None:
        """
        This function creates an instance of the application.
        
        :param master: The Tkinter root instance.
        """
        super().__init__(master)
        self.master = master
        self.master.title('Live client reader by Vianpyro')
        self.reading = False
        self.initialized = False

        self.master.wm_iconphoto(False, ImageTk.PhotoImage(Image.open('league_of_help_favicon.ico')))

        self.grid()
        self.create_widgets()

    def create_widgets(self) -> None:
        """
        This function create the 'constant' widgets.
        """
        self.start_button = tk.Button(self.master, text='Start', command=self.start, fg='red', bg='lightgray')
        self.stop_button = tk.Button(self.master, text='Stop', command=self.stop, fg='blue', bg='lightgray')

        self.start_button.grid(row=0, column=0, ipadx=20, ipady=10)
        self.stop_button.grid(row=0, column=1, ipadx=20, ipady=10)

    def stop(self) -> None:
        """
        This function ends the reading processus.
        """
        if self.reading:
            self.reading = False
            print([champion['championName'] for champion in self.data['allPlayers']])
            print('Successfully stopped reading live client data.')
        else:
            print('Already not reading live client data.')

    def start(self) -> None:
        """
        This function starts the reading processus.
        """
        if not self.reading:
            self.reading = True
            print('Successfully started reading live client data.')
            self.read_live_client_data()
        else:
            print('Already reading live client data.')

    def read_live_client_data(self) -> None:
        """
        This function reads the data from the league client.
        """
        if self.reading:
            try:
                self.data = requests.get('https://localhost:2999/liveclientdata/allgamedata', verify=False).json()
            except:
                try:
                    with open('active_client.json') as json_file:
                        self.data = json.load(json_file)
                except Exception as e:
                    print('Unable to read data from the live client:', e)
                    if len(self.master.winfo_children()) > 2:
                        for widget in self.master.winfo_children()[3:]:
                            widget.destroy()

            if self.initialized:
                self.update()
            else:
                self.initialization()

            # After 3000 mili-seconds (3 sec) restart this function (loop).
            self.after(3000, self.read_live_client_data)

    def initialization(self) -> None:
        """
        Initialize every information to be displayed on the application.
        """
        # Find the active player's champion
        for e in self.data['allPlayers']:
            if self.data['activePlayer']['summonerName'] == e['summonerName']:
                all_active_player = e

        # Player's champion icon
        urllib.request.urlretrieve(
            f"https://ddragon.leagueoflegends.com/cdn/{version}/img/champion/{all_active_player['championName']}.png",
            'active_player_champion_icon.png'
        )
        
        self.image = tk.PhotoImage(file='active_player_champion_icon.png')
        self.champion_icon = tk.Label(master=self.master, image=self.image)
        self.champion_icon.grid(row=1, column=0, rowspan=4)

        # Player and champion name
        self.active_player_label = tk.Label(master=self.master, text=f"{all_active_player['championName']} (You)")
        self.active_player_label.grid(row=1, column=1)

        # K/D/A
        kda_separator = '/'

        self.active_player_kda_label = tk.Label(master=self.master, text='KDA:')
        self.active_player_kda_label.grid(row=1, column=3)
        
        self.active_player_kills_entry = tk.Entry(master=self.master, width=4)
        self.active_player_kills_entry.insert(tk.END, f"{all_active_player['scores']['kills']:>4}")
        self.active_player_kills_entry['state'] = 'readonly'
        self.active_player_kills_entry.grid(row=1, column=4)

        self.active_player_kd_sep = tk.Label(master=self.master, text=kda_separator)
        self.active_player_kd_sep.grid(row=1, column=5)

        self.active_player_deaths_entry = tk.Entry(master=self.master, width=4)
        self.active_player_deaths_entry.insert(tk.END, f"{all_active_player['scores']['deaths']:>4}")
        self.active_player_deaths_entry['state'] = 'readonly'
        self.active_player_deaths_entry.grid(row=1, column=6)

        self.active_player_da_sep = tk.Label(master=self.master, text=kda_separator)
        self.active_player_da_sep.grid(row=1, column=7)

        self.active_player_assists_entry = tk.Entry(master=self.master, width=4)
        self.active_player_assists_entry.insert(tk.END, f"{all_active_player['scores']['assists']:>4}")
        self.active_player_assists_entry['state'] = 'readonly'
        self.active_player_assists_entry.grid(row=1, column=8)

        self.active_player_kda_ratio = tk.Label(master=self.master, text=':')
        self.active_player_kda_ratio.grid(row=1, column=9)

        self.active_player_kda_ratio_entry = tk.Entry(master=self.master, width=6)
        self.active_player_kda_ratio_entry.insert(tk.END, 
            f"{round(((all_active_player['scores']['kills'] + all_active_player['scores']['assists']) / max(1, all_active_player['scores']['deaths'])), 2):>6}"
        )
        self.active_player_kda_ratio_entry['state'] = 'readonly'
        self.active_player_kda_ratio_entry.grid(row=1, column=10)

        # Level
        self.active_player_level_label = tk.Label(master=self.master, text='Level:')
        self.active_player_level_label.grid(row=2, column=1)

        self.active_player_level_entry = tk.Entry(master=self.master, width=2)
        self.active_player_level_entry.insert(tk.END, f"{self.data['activePlayer']['level']:>2}")
        self.active_player_level_entry['state'] = 'readonly'
        self.active_player_level_entry.grid(row=2, column=2)

        # Creep score
        self.active_player_cs_label = tk.Label(master=self.master, text='CS:')
        self.active_player_cs_label.grid(row=2, column=3)
        
        self.active_player_cs_entry = tk.Entry(master=self.master, width=5)
        self.active_player_cs_entry.insert(tk.END, f"{all_active_player['scores']['creepScore']:>5}")
        self.active_player_cs_entry['state'] = 'readonly'
        self.active_player_cs_entry.grid(row=2, column=4, columnspan=2)

        # Vision score
        self.active_player_vision_label = tk.Label(master=self.master, text='Vision:')
        self.active_player_vision_label.grid(row=2, column=6, columnspan=2)

        self.active_player_vision_entry = tk.Entry(master=self.master, width=4)
        self.active_player_vision_entry.insert(tk.END, f"{all_active_player['scores']['wardScore']:>4}")
        self.active_player_vision_entry['state'] = 'readonly'
        self.active_player_vision_entry.grid(row=2, column=8)

        # Gold efficiency
        gold_efficiency = 0
        for item in all_active_player['items']:
            if items['data'][str(item['itemID'])]['gold']['purchasable'] and items['data'][str(item['itemID'])]['gold']['total']:
                gold_efficiency += items['data'][str(item['itemID'])]['gold']['total'] * item['count']

        self.active_player_total_gold_label = tk.Label(master=self.master, text='Gold efficiency:')
        self.active_player_total_gold_label.grid(row=3, column=3, columnspan=4)

        self.active_player_total_gold_entry = tk.Entry(master=self.master, width=5)
        self.active_player_total_gold_entry.insert(tk.END, f"{gold_efficiency:>5}")
        self.active_player_total_gold_entry['state'] = 'readonly'
        self.active_player_total_gold_entry.grid(row=3, column=8)

        # Once everything is ready ones want to update the data without regenerating it each turn.
        self.team = {'order': [], 'chaos': []}
        self.all_champions_grid_row_start = self.master.grid_size()[1]
        for i in range(len(self.data['allPlayers'])):
            if all_active_player['summonerName'] != self.data['allPlayers'][i]['summonerName']:
                self.add_champion(i)

        self.initialized = True

    def add_champion(self, id: int = 0) -> None:
        """
        This function creates a champion's slot depending on its id.
        
        :param id: The index of the champion in the champions list.
        """
        # Add the players to teams lists to detect which team they're in with their widgets.
        self.team[self.data['allPlayers'][id]['team'].lower()].append({'id': id, 'champion': self.data['allPlayers'][id], 'widgets': [
            tk.Label(
                text=f"{self.data['allPlayers'][id]['championName']} ({self.data['allPlayers'][id]['summonerName']})",
                fg=['blue', 'red'][int(self.data['allPlayers'][id]['team'] == 'CHAOS')]
            )
        ]})
        
        # Add a separator above the new line if necessary
        if len(self.team[self.data['allPlayers'][id]['team'].lower()]) == max(len(self.team['order']), len(self.team['chaos'])):
            ttk.Separator(master=self.master, orient='horizontal').grid(row=self.master.grid_size()[1], column=0, columnspan=self.master.grid_size()[0], sticky='we')
        
        if id % 2 == 0:
            ttk.Separator(master=self.master, orient='vertical').grid(row=self.master.grid_size()[1], column=5, rowspan=2, sticky='ns')

        # Grid every widget
        for index, widget in enumerate(self.team[self.data['allPlayers'][id]['team'].lower()][-1]['widgets']):
            widget.grid(
                row=self.all_champions_grid_row_start + (2 * len(self.team[self.data['allPlayers'][id]['team'].lower()])),
                column=int(self.data['allPlayers'][id]['team'] == 'CHAOS') * 6
            )

    def update(self) -> None:
        """
        TODO: Rework the whole function.
        This function updates every information displayed on the application.
        """
        if len(self.master.winfo_children()) > 2:
            for widget in self.master.winfo_children()[3:]:
                widget.destroy()

        # Active player
        active_player = self.data['activePlayer']
        self.active_player_button = tk.Button(self.master, text=active_player['summonerName'])
        self.active_player_button.grid(row=2, column=0)

        # All players
        players_list = [player for player in self.data['allPlayers'] if player['summonerName'] != active_player['summonerName']]
        self.champions_list = [
            tk.Button(self.master, text=f"{champion['championName']}")
            for champion in players_list
        ]

        for index, champion in enumerate(self.champions_list):
            gold_efficiency = 0
            for item in players_list[index]['items']:
                if items['data'][str(item['itemID'])]['gold']['purchasable'] and items['data'][str(item['itemID'])]['gold']['total']:
                    gold_efficiency += items['data'][str(item['itemID'])]['gold']['total'] * item['count']
            
            champion['text'] = f"{players_list[index]['championName']} ({players_list[index]['summonerName']}) [{gold_efficiency} GE]"
            champion['fg'] = 'blue' if players_list[index]['team'] == 'ORDER' else 'red'
                
            # If 1v1
            # if len(self.champions_list) == 2:
            #     champion.grid(row=(3 * index) + 2, column=1, ipadx=20, ipady=10, sticky='nesw')
            # else:
            #     champion.grid(row=(3 * index) + 2, column=0)
            champion.grid(row=index + 3, column=int(champion['fg'] == 'red'))

root = tk.Tk()
app = Application(master=root)
app.mainloop()
