import tkinter as tk
import subprocess
import ctypes
import os
import sys
import threading
import winreg
import psutil
import atexit
import webbrowser 

# ==========================================
# ⚙️ OPTIMIZER ENGINE (Same as before)
# ==========================================
class OptimizerCore:
    @staticmethod
    def run_cmd(cmd):
        try:
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except:
            pass

    @staticmethod
    def optimize_network():
        commands = [
            "netsh int tcp set global congestionprovider=ctcp",
            "netsh int tcp set global rss=enabled",
            "netsh int tcp set heuristics disabled",
            "netsh int ip set global taskoffload=enabled",
            "ipconfig /flushdns"
        ]
        for cmd in commands:
            OptimizerCore.run_cmd(cmd)

    @staticmethod
    def optimize_system():
        OptimizerCore.run_cmd("powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"System\GameConfigStore", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "GameDVR_Enabled", 0, winreg.REG_DWORD, 0)
            winreg.CloseKey(key)
        except:
            pass

    @staticmethod
    def smart_ram_clean():
        psapi = ctypes.windll.psapi
        current_pid = os.getpid()
        cleaned_count = 0
        for proc in psutil.process_iter():
            try:
                pid = proc.pid
                if pid == current_pid: continue 
                h_process = ctypes.windll.kernel32.OpenProcess(0x001F0FFF, False, pid)
                if h_process:
                    psapi.EmptyWorkingSet(h_process)
                    ctypes.windll.kernel32.CloseProcess(h_process)
                    cleaned_count += 1
            except:
                pass
        return cleaned_count

    @staticmethod
    def restore_defaults():
        OptimizerCore.run_cmd("netsh int tcp set global congestionprovider=default")
        OptimizerCore.run_cmd("netsh int tcp set heuristics enabled")
        OptimizerCore.run_cmd("powercfg /setactive 381b4222-f694-41f0-9685-ff5bb260df2e")
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"System\GameConfigStore", 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "GameDVR_Enabled", 0, winreg.REG_DWORD, 1)
            winreg.CloseKey(key)
        except:
            pass

# ==========================================
# 🎮 FREEWARE UI
# ==========================================
class FixPingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fix Ping (Free Edition)")
        self.root.geometry("380x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#111111")
        self.is_boosted = False

        atexit.register(self.safe_exit)

        # TITLE
        tk.Label(root, text="FIX PING", font=("Impact", 30), bg="#111111", fg="#00FF7F").pack(pady=(30, 0))
        tk.Label(root, text="Community Edition | Free Forever", font=("Segoe UI", 8), bg="#111111", fg="#666").pack(pady=(0, 20))

        # STATUS CIRCLE
        self.status_canvas = tk.Canvas(root, width=140, height=140, bg="#111111", highlightthickness=0)
        self.status_canvas.pack(pady=10)
        self.draw_status_circle("#333", "OFF")

        # MAIN BUTTON
        self.btn_action = tk.Button(root, text="ACTIVATE BOOST", font=("Segoe UI", 12, "bold"), 
                                    bg="#00AA00", fg="white", relief="flat", cursor="hand2", 
                                    command=self.toggle_boost, width=20, height=2)
        self.btn_action.pack(pady=20)

        # INFO TEXT
        self.info_lbl = tk.Label(root, text="Ready to optimize", font=("Consolas", 9), bg="#111111", fg="#555")
        self.info_lbl.pack(pady=5)

        # FOOTER (The "Free" Guarantee)
        f_frame = tk.Frame(root, bg="#1a1a1a", pady=10)
        f_frame.pack(side="bottom", fill="x")
        
        tk.Label(f_frame, text="✅ 100% Free & Open Source", font=("Segoe UI", 8, "bold"), bg="#1a1a1a", fg="#888").pack()
        
        # Optional: Link to your GitHub or Site
        link = tk.Label(f_frame, text="View Source Code / GitHub", font=("Segoe UI", 8, "underline"), bg="#1a1a1a", fg="#00AA00", cursor="hand2")
        link.pack(pady=2)
        link.bind("<Button-1>", lambda e: self.open_link())

    def draw_status_circle(self, color, text):
        self.status_canvas.delete("all")
        self.status_canvas.create_oval(10, 10, 130, 130, outline=color, width=3)
        self.status_canvas.create_text(70, 70, text=text, fill=color, font=("Segoe UI", 20, "bold"))

    def toggle_boost(self):
        if not self.is_boosted:
            self.info_lbl.config(text="Applying Tweaks...", fg="yellow")
            threading.Thread(target=self.run_boost, daemon=True).start()
        else:
            self.info_lbl.config(text="Restoring defaults...", fg="yellow")
            threading.Thread(target=self.run_restore, daemon=True).start()

    def run_boost(self):
        time.sleep(0.5)
        OptimizerCore.optimize_network()
        OptimizerCore.optimize_system()
        cleaned = OptimizerCore.smart_ram_clean()
        self.root.after(0, lambda: self.finish_boost(cleaned))

    def run_restore(self):
        time.sleep(0.5)
        OptimizerCore.restore_defaults()
        self.root.after(0, self.finish_restore)

    def finish_boost(self, cleaned):
        self.is_boosted = True
        self.btn_action.config(text="DEACTIVATE", bg="#CC0000", activebackground="#990000")
        self.draw_status_circle("#00FF7F", "ON")
        self.info_lbl.config(text=f"Optimization Active\nFreed RAM from {cleaned} apps", fg="#00FF7F")

    def finish_restore(self):
        self.is_boosted = False
        self.btn_action.config(text="ACTIVATE BOOST", bg="#00AA00", activebackground="#008800")
        self.draw_status_circle("#333", "OFF")
        self.info_lbl.config(text="System Normal", fg="#555")

    def open_link(self):
        # Change this link to your actual GitHub or website
        webbrowser.open("https://github.com/your-username/fix-ping")

    def safe_exit(self):
        pass

if __name__ == "__main__":
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    
    if not is_admin:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()

    root = tk.Tk()
    app = FixPingApp(root)
    root.mainloop()