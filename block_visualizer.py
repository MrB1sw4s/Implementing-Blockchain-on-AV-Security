import tkinter as tk
from tkinter import scrolledtext, font
import requests
import json

class BlockchainVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Block Visualizer")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        self.root.tk_setPalette(background='#212121', foreground='white')

        self.blocks_text = scrolledtext.ScrolledText(self.root, width=60, height=20, bg='#212121', fg='white',
                                                     selectbackground='#1565C0', selectforeground='white')
        self.blocks_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.blocks_text.grid_rowconfigure(0, weight=1)
        self.blocks_text.grid_columnconfigure(0, weight=1)

        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_blocks, bg='#424242', fg='white')
        self.refresh_button.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

        self.blocks_text.bind("<Control-plus>", self.increase_font_size)
        self.blocks_text.bind("<Control-minus>", self.decrease_font_size)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.font_size = 10
        self.update_font_size()

    def increase_font_size(self, event):
        self.font_size += 1
        self.update_font_size()

    def decrease_font_size(self, event):
        if (self.font_size > 1):
            self.font_size -= 1
            self.update_font_size()

    def update_font_size(self):
        updated_font = font.Font(family="TkDefaultFont", size=self.font_size)
        self.blocks_text.configure(font=updated_font)

    def refresh_blocks(self):
        try:
            response = requests.get("http://localhost:5000/chain")
            if response.status_code == 200:
                chain = response.json()["chain"]
                self.blocks_text.delete(1.0, tk.END)
                for block in chain:
                    self.blocks_text.insert(tk.END, f"Block Index: {block['index']}\n")
                    self.blocks_text.insert(tk.END, f"Current Hash: {block['current_hash']}\n")
                    self.blocks_text.insert(tk.END, f"Timestamp: {block['timestamp']}\n")
                    self.blocks_text.insert(tk.END, f"Transactions: {json.dumps(block['transactions'])}\n")
                    self.blocks_text.insert(tk.END, f"Proof: {block['proof']}\n")
                    self.blocks_text.insert(tk.END, f"Previous Hash: {block['previous_hash']}\n\n")
            else:
                self.blocks_text.insert(tk.END, f"Failed to retrieve blockchain data: {response.text}\n")
        except requests.RequestException as e:
            self.blocks_text.insert(tk.END, f"Error communicating with blockchain: {e}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainVisualizerApp(root)
    root.mainloop()
