import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import subprocess

class VPNGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenVPN GUI")

        self.tab_control = ttk.Notebook(root)
        self.tab_control.pack(expand=1, fill="both")

        self.server_tab = tk.Frame(self.tab_control)
        self.client_tab = tk.Frame(self.tab_control)

        self.tab_control.add(self.server_tab, text="Server Configuration")
        self.tab_control.add(self.client_tab, text="Client Configuration")

        self.create_server_config()
        self.create_client_config()

    def create_server_config(self):
        self.server_frame = tk.LabelFrame(self.server_tab, text="Server Configuration")
        self.server_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        tk.Label(self.server_frame, text="Server Config File:").grid(row=0, column=0, padx=5, pady=5)
        self.server_config_path = tk.Entry(self.server_frame, width=50)
        self.server_config_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.server_frame, text="Browse", command=self.browse_server_config).grid(row=0, column=2, padx=5, pady=5)

        self.start_server_button = tk.Button(self.server_frame, text="Start Server", command=self.start_server)
        self.start_server_button.grid(row=1, column=1, padx=5, pady=5)

        self.stop_server_button = tk.Button(self.server_frame, text="Stop Server", command=self.stop_server)
        self.stop_server_button.grid(row=1, column=2, padx=5, pady=5)

    def create_client_config(self):
        self.client_frame = tk.LabelFrame(self.client_tab, text="Client Configuration")
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
        file_path = filedialog.askopenfilename(filetypes=[("OpenVPN Config", "server.ovpn")])
        self.server_config_path.delete(0, tk.END)
        self.server_config_path.insert(0, file_path)

    def browse_client_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("OpenVPN Config", "client.ovpn")])
        self.client_config_path.delete(0, tk.END)
        self.client_config_path.insert(0, file_path)

    def start_server(self):
        config_path = self.server_config_path.get()
        if os.path.isfile(config_path):
            self.server_process = subprocess.Popen(["openvpn", "--config", config_path])
            messagebox.showinfo("Info", "OpenVPN server started.")
        else:
            messagebox.showerror("Error", "Invalid server config file.")

    def stop_server(self):
        if hasattr(self, 'server_process') and self.server_process:
            self.server_process.terminate()
            self.server_process = None
            messagebox.showinfo("Info", "OpenVPN server stopped.")
        else:
            subprocess.call(["taskkill", "/F", "/IM", "openvpn.exe"])
            messagebox.showinfo("Info", "OpenVPN server stopped.")

    def connect_client(self):
        config_path = self.client_config_path.get()
        if os.path.isfile(config_path):
            self.client_process = subprocess.Popen(["openvpn", "--config", config_path])
            messagebox.showinfo("Info", "OpenVPN client connected.")
        else:
            messagebox.showerror("Error", "Invalid client config file.")

    def disconnect_client(self):
        if hasattr(self, 'client_process') and self.client_process:
            self.client_process.terminate()
            self.client_process = None
            messagebox.showinfo("Info", "OpenVPN client disconnected.")
        else:
            subprocess.call(["taskkill", "/F", "/IM", "openvpn.exe"])
            messagebox.showinfo("Info", "OpenVPN client disconnected.")

if __name__ == "__main__":
    root = tk.Tk()
    app = VPNGUI(root)
    root.mainloop()
