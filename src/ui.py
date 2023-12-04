import os
import tkinter as tk
from tkinter import filedialog
import pickle
from datetime import datetime,timedelta
from src.utils import load_object, save_object, save_data

from tkinter import messagebox


PANEL_HEIGHT = 60

FOLDER_WIDTH = 80
FOLDER_HEIGHT = 30

FILE_WIDTH = 80
FILE_HEIGHT = 30

LINE_SPACING = 25

ROW_COUNT = 6
COL_COUNT = 6

WINDOW_WIDTH = 2*LINE_SPACING + COL_COUNT*(FOLDER_WIDTH + LINE_SPACING)
WINDOW_HEIGHT = 2*LINE_SPACING + ROW_COUNT*(FOLDER_HEIGHT + LINE_SPACING) + PANEL_HEIGHT

# WINDOW_WIDTH = 800
# WINDOW_HEIGHT = 600


PIK = os.path.join('metadata','metadata.pkl')

class Finder_window:

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Desktop Replica")
        self.root.geometry("800x600")
        self.root.configure(bg="cyan")

        self.folder_labels = dict()
        self.file_labels = dict()
        
        self.folders, self.folder_metadata, self.files, self.file_metadata = {},{},{},{}
        self.folders, self.folder_metadata, self.files, self.file_metadata = self.initialize_files_and_folders()
        

        B = tk.Button(self.root, text ="Create Folder", command = self.create_Folder)
        B.place(x=WINDOW_WIDTH-400,y=WINDOW_HEIGHT-100)

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        
        self.root.mainloop()

    def initialize_files_and_folders(self):
        folders = None
        folder_metadata = None
        files = None
        file_metadata = None

        PIK_obj = load_object(PIK)
        if PIK_obj != None:
            folders, folder_metadata, files, file_metadata = PIK_obj[0], PIK_obj[1], PIK_obj[2], PIK_obj[3]
        else:
            folders, folder_metadata, files, file_metadata = {},{},{},{}
        self.refresh_display()

        return folders, folder_metadata, files, file_metadata
    
    def refresh_display(self):
        
        for folder in self.folders:
            folder_id = self.folders[folder]
            label = self.folder_labels[folder_id] if folder_id in self.folder_labels else None

            if label != None:
                row, col = self.folder_metadata[folder_id][2][0], self.folder_metadata[folder_id][2][1]
                x_pos, y_pos = self.get_xy(row,col)
                label.place(x=x_pos,y = y_pos, width=FOLDER_WIDTH, height=FOLDER_HEIGHT)
            else:
                row, col = self.folder_metadata[folder_id][2][0], self.folder_metadata[folder_id][2][1]
                x_pos, y_pos = self.get_xy(row,col)
                label = tk.Label(self.root,text=folder, bg="yellow")
                label.place(x=x_pos,y = y_pos, width=FOLDER_WIDTH, height=FOLDER_HEIGHT)
                self.folder_labels[folder_id] = label

        for file in self.files:
            file_id = self.files[file]
            label = self.file_labels[file_id] if file_id in self.file_labels else None
            if label != None:
                row, col = self.file_metadata[file_id][2][0], self.file_metadata[file_id][2][1]
                x_pos, y_pos = self.get_xy(row,col)
                label.place(x=x_pos,y = y_pos, width=FILE_WIDTH, height=FILE_HEIGHT)
            else:
                row, col = self.file_metadata[file_id][2][0], self.file_metadata[file_id][2][1]
                x_pos, y_pos = self.get_xy(row,col)
                label = tk.Label(self.root,text=file, bg="white")
                label.place(x=x_pos,y = y_pos, width=FILE_HEIGHT, height=FILE_HEIGHT)
                self.file_labels[file_id] = label

        self.root.update()


    def get_new_folder_name(self):
        def new_name(name):
            count = 1
            while True:
                count += 1
                yield name +" "+ count.__str__()

        FolderName = "New Folder"
        name = new_name(FolderName)
        while FolderName in self.folders:
            FolderName = next(name)
        # print(FolderName)
        return FolderName

    def get_xy(self, row = 0,col = 0):
        xpos = (row+1)*(LINE_SPACING + FOLDER_WIDTH) - FOLDER_WIDTH/2
        ypos = (col+1)*(LINE_SPACING + FOLDER_HEIGHT) - FOLDER_HEIGHT/2
        return xpos, ypos
    
    def get_row_col(self,x,y):
        row = int((x + FOLDER_WIDTH/2)/(LINE_SPACING + FOLDER_WIDTH))
        col = int((y + FOLDER_HEIGHT/2)/(LINE_SPACING + FOLDER_HEIGHT))
        return row,col

    def get_next_empty_pos(self):
        def next_pos():
            x_initial = 0
            y_initial = 0
            count = 0
            while True:
                row = count % COL_COUNT
                col = int(count / COL_COUNT)
                count += 1
                yield row, col
        pos = next_pos()
        rpos = next(pos)
        rows = [value[-1] for value in self.folder_metadata.values()]
        print(rows)
        while tuple(rpos) in rows:
            rpos = next(pos)
        return rpos


    def create_Folder(self):
        name = self.get_new_folder_name()
        pos = self.get_next_empty_pos()
        folder_id = "FOLDER_"+datetime.now().strftime('%m_%d_%Y_%H_%M_%s')
        self.folders[name] = folder_id
        self.folder_metadata[folder_id] = [[],"close",pos]

        label = tk.Label(self.root, text=name, bg="yellow")
        row, col = pos[0], pos[1]
        x, y = self.get_xy(row,col)
        label.place(x=x, y=y, width=FOLDER_WIDTH, height=FOLDER_HEIGHT)
        label.bind("<Button-1>", lambda event, folder_id=folder_id: self.on_left_click(event, folder_id))
        label.bind("<Double-1>", lambda event, folder_id=folder_id: self.on_double_click(event, folder_id))
        label.bind("<ButtonRelease-1>",lambda event, folder_id=folder_id: self.drag_release(event, folder_id))
        label.bind("<B1-Motion>",self.on_drag)
        
        self.folder_labels[folder_id] = label

        print(self.folder_metadata)
        self.refresh_display()

    def on_left_click(self, event, folder_id):
        label = event.widget
        label.startX = event.x
        label.startY = event.y


    def on_double_click(self, event, folder_id):
        label = event.widget
        folder = label.cget("text")
        start_time = datetime.now()

        self.show_folder_window(folder)

        end_time = datetime.now()
        elapsed_time = end_time - start_time

        self.folder_metadata[self.folders[folder]][0].append(elapsed_time)


    def on_drag(self, event):
        label = event.widget

        x, y = label.winfo_x() - label.startX + event.x , label.winfo_y() - label.startY + event.y

        label.place(x=x, y=y)


    def drag_release(self, event,folder_id):
        # label = event.widget
        # # folder = label.cget("text")
        # x, y = label.winfo_x(), label.winfo_y()
        # # x, y = self.root.x, self.root.y
        # pos = self.get_row_col(x,y)
        # xpos, ypos = self.get_xy(pos[0],pos[1])
        # label.place(x=xpos, y=ypos)
        # self.folder_metadata[folder_id][2] = pos
        pass
        


    def close(self):
        self.save_state()
        self.root.destroy()

    def show_folder_window(self, foldername):
        folder_window = tk.Toplevel(self.root)
        folder_window.title(foldername)
        folder_window.geometry("200x100")

        label = tk.Label(folder_window, text=f"Opened: {foldername}")
        label.pack(padx=10, pady=10)

        close_button = tk.Button(folder_window, text="Close", command=folder_window.destroy)
        close_button.pack(pady=10)



    def save_state(self):
        try:
            save_object(PIK, (self.folders, self.folder_metadata, self.files, self.file_metadata))
        except Exception as e:
            pass





        
if __name__ == "__main__":
    myWindow = Finder_window()

        

