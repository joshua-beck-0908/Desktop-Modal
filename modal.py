import json
import os
import sys
import requests
import time
import threading
import queue
import keyboard
from tkinter import Tk, ttk, StringVar
import pywinctl as pwc

uiOpen = False

nameSubs = {'f': 'firefox', 'c': 'chrome', 'e': 'explorer', 't': 'terminal', 'n': 'notepad', 'v': 'visual studio code', 'p': 'powershell', 's': 'spotify', 'm': 'microsoft teams', 'd': 'discord', 'w': 'whatsapp', 'a': 'android studio'}

class KeyboardListener(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def runCmd(self, cmd):
        cmd = cmd.lower()
        if cmd.startswith('g'):
            if len(cmd) == 2:
                try:
                    name = nameSubs[cmd[1]]
                except KeyError:
                    name = cmd[1:]
            # go to a specific window
            windows = pwc.getWindowsWithTitle(name, condition=pwc.Re.CONTAINS, flags=pwc.Re.IGNORECASE)
            try:
                windows[0].activate()
            except IndexError:
                pass
        elif cmd == 'q':
            # quit
            self.queue.put('quit')


    def run(self):
        while True:
            cmd = self.queue.get()
            if cmd == 'quit':
                root.destroy()
                break
            elif cmd.startswith('run:'):
                self.runCmd(cmd[4:])

def initUI():
    global root, cmdText, cmdEntry, uiOpen
    root = Tk()
    cmdText = StringVar()
    root.title('Modal Keyboard')
    ttk.Label(root, text='Enter a command').pack(side='left')
    cmdEntry = ttk.Entry(root, textvariable=cmdText)
    cmdEntry.pack(side='left')
    cmdEntry.focus()
    cmdEntry.bind('<Return>', runCmd)
    cmdEntry.bind('<Escape>', hotkey)
    # set always on top
    root.wm_attributes('-topmost', 1)
    root.withdraw()

def runCmd(event):
    global uiOpen
    cmd = cmdText.get()
    workerQueue.put(f'run:{cmd}')
    cmdText.set('')
    root.withdraw()
    uiOpen = False

def hotkey(event):
    global uiOpen
    if uiOpen:
        root.withdraw()
    else:
        root.deiconify()
        cmdEntry.focus()
    uiOpen = not uiOpen

def main():
    global workerQueue
    initUI()
    #keyboard.add_hotkey('caps lock', hotkey)
    #keyboard.hook_key('caps lock', hotkey)
    keyboard.remap_hotkey('caps lock', 'F24')
    keyboard.on_press_key('caps lock', hotkey)
    workerQueue = queue.Queue()
    KeyboardListener(workerQueue).start() 
    root.mainloop()
    

if __name__ == '__main__':
    main()
