import requests
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master: tk.Tk = None):
        super().__init__(master)
        self.master = master
        self.reading = False

        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.start_button = tk.Button(self, text='Start', command=self.start, fg='red', bg='lightgray')
        self.stop_button = tk.Button(self, text='Stop', command=self.stop, fg='blue', bg='lightgray')

        self.start_button.grid(row=0, column=0, ipadx=20, ipady=10)
        self.stop_button.grid(row=0, column=1, ipadx=20, ipady=10)

    def stop(self):
        if self.reading:
            self.reading = False
            print([champion['championName'] for champion in self.data['allPlayers']])
            print('Successfully stopped reading live client data.')
        else:
            print('Already not reading live client data.')

    def start(self):
        if not self.reading:
            self.reading = True
            print('Successfully started reading live client data.')
            self.read_live_client_data()
        else:
            print('Already reading live client data.')

    def read_live_client_data(self):
        if self.reading:
            try:
                self.data = requests.get('https://localhost:2999/liveclientdata/allgamedata', verify=False).json()
                self.update()
            except Exception as e:
                print('Unable to read data from the live client:', e)
                for widget in self.master.winfo_children()[2:]:
                    widget.destroy()

        # After 3000 mili-seconds (3 sec) restart this function (loop).
        self.after(3000, self.read_live_client_data)

    def update(self):
        for widget in self.master.winfo_children()[2:]:
            widget.destroy()

        self.champions_list = [
            tk.Button(self, text=f"{champion['championName']}")
            for champion in [champion for champion in self.data['allPlayers']]
        ]

        for index, champion in enumerate(self.champions_list):
            champion['text'] = f"{self.data['allPlayers'][index]['championName']} ({self.data['allPlayers'][index]['summonerName']})"
            champion['fg'] = 'blue' if self.data['allPlayers'][index]['team'] == 'ORDER' else 'red'
            tk.Label(self, text='')
                
            # If 1v1
            if len(self.champions_list) == 2:
                champion.grid(row=(3 * index) + 2, column=1, ipadx=20, ipady=10, sticky='nesw')
            else:
                champion.grid(row=(3 * index) + 2, column=0)

root = tk.Tk()
app = Application(master=root)
app.mainloop()
