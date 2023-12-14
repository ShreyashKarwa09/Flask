import tkinter as tk
from chatbot import bot_message
import speech_recognition as sp
import pyttsx3 as p
import threading as th


BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

f=False
reco = sp.Recognizer()
reco.energy_threshold = 4000
reco.dynamic_energy_threshold = True

class ChatApplication:

    def __init__(self):
        self.window = tk.Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=1000, height=600, bg=BG_COLOR)

        # head label
        head_label = tk.Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome! Enter Your Queries Below!", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)

        # tiny divider
        line = tk.Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # text widget
        self.text_widget = tk.Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=tk.DISABLED)

        # scroll bar
        scrollbar = tk.Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = tk.Label(self.window, bg=BG_GRAY, height=80)
        bottom_label.place(relwidth=1, rely=0.825)

        # message entry box
        self.msg_entry = tk.Entry(bottom_label, bg="#2C3E50", fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.60, relheight=0.05, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)

        # send button
        send_button = tk.Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.62, rely=0.008, relheight=0.05, relwidth=0.20)
        
        #audio button
        
        aud_button = tk.Button(bottom_label, text="🎙", font=FONT_BOLD, width=20, bg=BG_GRAY, command=lambda: self.audio())
        aud_button.place(relx=0.83, rely=0.008, relheight=0.05, relwidth=0.15)
    
    def _on_enter_pressed(self, event):
        f=False
        msg = self.msg_entry.get()
        self._insert_message(msg, "You")
    
    def speak(self):
        spe=""
        with sp.Microphone() as mic :
            try:
                aud = reco.listen(mic,timeout=20)
                text = reco.recognize_google(aud)
                self.text_widget.configure(state=tk.NORMAL)
                self.text_widget.insert(tk.END,f"You : {text}\n\n")
                self.text_widget.configure(state=tk.DISABLED)
                spe = bot_message(text)
                msg2 = f"Bot : {spe}\n\n"
                self.text_widget.configure(state=tk.NORMAL)
                self.text_widget.insert(tk.END,msg2)
                self.text_widget.configure(state=tk.DISABLED)
            except :
                self.text_widget.configure(state=tk.NORMAL)
                spe = "Could not understand the audio"
                self.text_widget.insert(tk.END,"Bot: Could not understand the audio\n\n")
                self.text_widget.configure(state=tk.DISABLED)
            en = p.init()
            en.say(spe)
            en.runAndWait()
    
    def audio(self):
        f=True
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END,"Bot: Start Speaking...\n\n")
        self.text_widget.configure(state=tk.DISABLED)
        thread = th.Thread(target= self.speak())
        thread.start()
        
    def _insert_message(self, msg, sender):
        if not msg:
            return

        self.msg_entry.delete(0, tk.END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg1)
        self.text_widget.configure(state=tk.DISABLED)

        msg2 = f"Bot : {bot_message(msg)}\n\n"
        self.text_widget.configure(state=tk.NORMAL)
        self.text_widget.insert(tk.END, msg2)
        self.text_widget.configure(state=tk.DISABLED)

        self.text_widget.see(tk.END)


if __name__ == "__main__":
    app = ChatApplication()
    app.run()