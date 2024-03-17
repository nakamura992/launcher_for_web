import tkinter as tk
from tkinter import messagebox
import webbrowser

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("WebサイトLauncher")
        self.geometry("300x100")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_tray_icon()
        self.tray_icon.run()

    def create_tray_icon(self):
        self.tray_icon = TrayIcon(self)

    def on_closing(self):
        if messagebox.askyesno("確認", "アプリケーションを終了しますか?"):
            self.tray_icon.stop()
            self.quit()

class TrayIcon(tk.Label):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.icon = tk.PhotoImage(file="icon.png")
        self.config(image=self.icon)
        self.bind("<Button-1>", self.open_website)
        self.master.overrideredirect(True)
        self.master.withdraw()
        self.master.after(300, self.place_window)

    def place_window(self):
        x = self.master.winfo_pointerx() - 16
        y = self.master.winfo_pointery() - 16
        self.master.geometry(f"+{x}+{y}")
        self.lift()
        self.master.after(10, self.place_window)

    def open_website(self, event):
        webbrowser.open("https://claude.ai/chat/")

    def stop(self):
        self.master.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()