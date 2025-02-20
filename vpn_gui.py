import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

class VPNGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenVPN GUI")

        # Server Configuration Section
        self.server_frame = tk.LabelFrame(root, text="Server Configuration")
        self.server_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        tk.Label(self.server_frame, text="Server Config File:").grid(row=0, column=0, padx=5, pady=5)
        self.server_config_path = tk.Entry(self.server_frame, width=50)
        self.server_config_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.server_frame, text="Browse", command=self.browse_server_config).grid(row=0, column=2, padx=5, pady=5)

        self.start_server_button = tk.Button(self.server_frame, text="Start Server", command=self.start_server)
        self.start_server_button.grid(row=1, column=1, padx=5, pady=5)

        self.stop_server_button = tk.Button(self.server_frame, text="Stop Server", command=self.stop_server)
        self.stop_server_button.grid(row=1, column=2, padx=5, pady=5)

        # Client Configuration Section
        self.client_frame = tk.LabelFrame(root, text="Client Configuration")
        self.client_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        tk.Label(self.client_frame, text="Client Config File:").grid(row=0, column=0, padx=5, pady=5)
        self.client_config_path = tk.Entry(self.client_frame, width=50)
        self.client_config_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.client_frame, text="Browse", command=self.browse_client_config).grid(row=0, column=2, padx=5, pady=5)

        self.connect_client_button = tk.Button(self.client_frame, text="Connect Client", command=self.connect_client)
        self.connect_client_button.grid(row=1, column=1, padx=5, pady=5)

        self.disconnect_client_button = tk.Button(self.client_frame, text="Disconnect Client", command=self.disconnect_client)
        self.disconnect_client_button.grid(row=1, column=2, padx=5, pady=5)

    def browse_server_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("OpenVPN Config", "*.ovpn")])
        self.server_config_path.insert(0, file_path)

    def browse_client_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("OpenVPN Config", "*.ovpn")])
        self.client_config_path.insert(0, file_path)

    def start_server(self):
        config_path = self.server_config_path.get()
        if os.path.isfile(config_path):
            subprocess.Popen(["openvpn", "--config", config_path])
            messagebox.showinfo("Info", "OpenVPN server started.")
        else:
            messagebox.showerror("Error", "Invalid server config file.")

    def stop_server(self):
        subprocess.call(["taskkill", "/F", "/IM", "openvpn.exe"])
        messagebox.showinfo("Info", "OpenVPN server stopped.")

    def connect_client(self):
        config_path = self.client_config_path.get()
        if os.path.isfile(config_path):
            subprocess.Popen(["openvpn", "--config", config_path])
            messagebox.showinfo("Info", "OpenVPN client connected.")
        else:
            messagebox.showerror("Error", "Invalid client config file.")

    def disconnect_client(self):
        subprocess.call(["taskkill", "/F", "/IM", "openvpn.exe"])
        messagebox.showinfo("Info", "OpenVPN client disconnected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VPNGUI(root)
    root.mainloop()
