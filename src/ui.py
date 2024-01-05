import os
import tkinter as tk
from tkinter import filedialog
import pickle
from datetime import datetime,timedelta
from src.utils import load_object, save_object, save_data
from src.components.model_predict import Model

from tkinter import messagebox


PANEL_HEIGHT = 60

FOLDER_WIDTH = 80
FOLDER_HEIGHT = 30

FILE_WIDTH = 80
FILE_HEIGHT = 30

LINE_SPACING = 25

ROW_COUNT = 6
COL_COUNT = 6

WINDOW_WIDTH = 2*LINE_SPACING + COL_COUNT*(FOLDER_WIDTH + LINE_SPACING) + 100
WINDOW_HEIGHT = 2*LINE_SPACING + ROW_COUNT*(FOLDER_HEIGHT + LINE_SPACING) + PANEL_HEIGHT + 100

PRIORITY_ROW_MARGIN = 3
PRIORITY_COL_MARGIN = 1

PRIORITY_ROW_COUNT = 1
PRIORITY_COL_COUNT = 3
THRESHHOLD = PRIORITY_ROW_COUNT*PRIORITY_COL_COUNT
# WINDOW_WIDTH = 800
# WINDOW_HEIGHT = 600

TOP_WINDOW_HEIGHT = 300
TOP_WINDOW_WIDTH = 200


PIK = os.path.join('metadata','metadata.pkl')

class Finder_window:

    folder_count = 0

    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Desktop Replica")
        self.root.geometry(WINDOW_WIDTH.__str__()+"x"+WINDOW_HEIGHT.__str__())
        self.root.configure(bg="cyan")


        self.tipwindow = None
        self.folder_labels = dict()
        self.file_labels = dict()
        
        self.folders, self.folder_metadata, self.files, self.file_metadata = {},{},{},{}
        self.folders, self.folder_metadata, self.files, self.file_metadata = self.initialize_files_and_folders()
        
        self.rearrange()

        self.generate_all_labels()

        Finder_window.folder_count = len(self.folders)

        B = tk.Button(self.root, text ="Create Folder", command = self.create_Folder)
        B.place(x=WINDOW_WIDTH-400,y=WINDOW_HEIGHT-100)

        self.root.protocol("WM_DELETE_WINDOW", self.close)
        
        self.root.mainloop()

    def initialize_files_and_folders(self):
        """
        Defining an empty data structure to store the metadata of the files. 
        If the metadata exists, it is taken from the pickle file.
        """
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
        """
         Updates the display as per the current state values by changing the labels.
        """
        for folder in self.folders:
            folder_id = self.folders[folder]
            label = self.folder_labels[folder_id] 
            # if folder_id in self.folder_labels else None

            if label != None:
                label.destroy()
                # row, col = self.folder_metadata[folder_id][2][0], self.folder_metadata[folder_id][2][1]
                # x_pos, y_pos = self.get_xy(row,col)
                # label.place(x=x_pos,y = y_pos, width=FOLDER_WIDTH, height=FOLDER_HEIGHT)
            # else:
            pos = self.folder_metadata[folder_id][2]
            self.create_label(folder,pos)

        for file in self.files:
            file_id = self.files[file]
            label = self.file_labels[file_id] 
            # if file_id in self.file_labels else None
            if label != None:
                label.destroy()
                # row, col = self.file_metadata[file_id][2][0], self.file_metadata[file_id][2][1]
                # x_pos, y_pos = self.get_xy(row,col)
                # label.place(x=x_pos,y = y_pos, width=FILE_WIDTH, height=FILE_HEIGHT)
            # else:
            pos = self.file_metadata[folder_id][2]
            self.create_label(file,pos)

        self.root.update()


    def get_new_folder_name(self):
        """
        Gives name to the new folder created by the user
        """
        def new_name(name):
            count = 1
            while True:
                count += 1
                yield name +" "+ count.__str__()

        FolderName = "New Folder"
        name = new_name(FolderName)
        while FolderName in self.folders:
            FolderName = next(name)
        return FolderName

    def get_xy(self, row = 0,col = 0):
        """To get the coordinates from the row and column position"""
        xpos = (row+1)*(LINE_SPACING + FOLDER_WIDTH) - FOLDER_WIDTH/2
        ypos = (col+1)*(LINE_SPACING + FOLDER_HEIGHT) - FOLDER_HEIGHT/2
        return xpos, ypos
    
    def get_row_col(self,x,y):
        """To get the row and column position from the coordinates"""
        row = int((x + FOLDER_WIDTH/2)/(LINE_SPACING + FOLDER_WIDTH))
        col = int((y + FOLDER_HEIGHT/2)/(LINE_SPACING + FOLDER_HEIGHT))
        return row,col

    def get_next_empty_pos(self):
        """"Gives the next empty position on the window"""
        def next_pos():
            # x_initial = 0
            # y_initial = 0
            count = 0
            while True:
                row = count % COL_COUNT
                col = int(count / COL_COUNT)
                count += 1
                yield row, col
        pos = next_pos()
        rpos = next(pos)
        rows = [value[-1] for value in self.folder_metadata.values()]
        
        
        while tuple(rpos) in rows:
            rpos = next(pos)
        return rpos

    def get_next_empty_priority_pos(self,df_dic):
        """Gives the next empty position on the window within the priority area"""
        def next_pos():
            # x_initial = 0
            # y_initial = 0
            count = 0
            while True:
                row = count % PRIORITY_COL_COUNT
                col = int(count / PRIORITY_COL_COUNT)
                count += 1
                yield row + PRIORITY_COL_MARGIN, col + PRIORITY_ROW_MARGIN
        pos = next_pos()
        rpos = next(pos)
        rows = [value[-1] for value in self.folder_metadata.values()]
        
        
        while tuple(rpos) in rows:
            rpos = next(pos)
        return rpos

    def create_Folder(self):
        """Creates a new folder"""
        name = self.get_new_folder_name()
        pos = self.get_next_empty_pos()
        folder_id = "FOLDER_"+datetime.now().strftime('%m_%d_%Y_%H_%M_%S_').replace(':','_') + Finder_window.folder_count.__str__()
        self.folders[name] = folder_id
        self.folder_metadata[folder_id] = [[],"close",pos]
        Finder_window.folder_count = len(self.folders)
        self.create_label(name,pos)
        print(self.folder_metadata)
        self.refresh_display()

    def showtip(self,event, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.root.bbox("insert")
        x = x + event.widget.winfo_rootx() + 57
        y = y + cy + event.widget.winfo_rooty() +27
        self.tipwindow = tw = tk.Toplevel(self.root)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                      background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                      font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self, event):
        """To make the information disappear when the cursor moves away from the folder"""
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

    def create_label(self,name,pos):
        """Creates new labels"""
        folder_id = self.folders[name]
        label = tk.Label(self.root, text=name, bg="yellow")
        row, col = pos[0], pos[1]
        x, y = self.get_xy(row,col)
        label.place(x=x, y=y, width=FOLDER_WIDTH, height=FOLDER_HEIGHT)
        label.bind("<Button-1>", lambda event, foldername=name: self.on_left_click(event, foldername))
        label.bind("<Double-1>", lambda event, foldername=name: self.on_double_click(event,foldername))
        label.bind("<ButtonRelease-1>",lambda event, foldername=name: self.drag_release(event, foldername))
        label.bind("<B1-Motion>",self.on_drag)
        metadata = self.folder_metadata[folder_id]
        label.bind('<Enter>', lambda event, text = metadata: self.showtip(event, text))
        label.bind('<Leave>',  lambda event: self.hidetip(event))
        self.folder_labels[folder_id] = label


    def generate_all_labels(self):
        """Generates labels for all the folders"""
        for folder in self.folders:
            folder_id = self.folders[folder]
            pos = self.folder_metadata[folder_id][-1]
            self.create_label(folder,pos)



    def on_left_click(self, event, foldername):
        """Keeps track of the current position of the folder"""
        label = event.widget
        label.startX = event.x
        label.startY = event.y


    def on_double_click(self,event, foldername):
        """Opens the folder and takes log of the time of access"""
        # label = event.widget
        # folder = label.cget("text")
        # start_time = datetime.now()
        # foldername = self.folders[folder_id]

        self.show_folder_window(foldername)

        # end_time = datetime.now()
        # elapsed_time = end_time - start_time

        # self.folder_metadata[self.folders[folder]][0].append(elapsed_time)


    def on_drag(self, event):
        """Repositions the folders"""
        label = event.widget

        x, y = label.winfo_x() - label.startX + event.x , label.winfo_y() - label.startY + event.y

        label.place(x=x, y=y)


    def drag_release(self, event,foldername):
        # label = event.widget
        # # folder = label.cget("text")
        # x, y = label.winfo_x(), label.winfo_y()
        # # x, y = self.root.x, self.root.y
        # pos = self.get_row_col(x,y)
        # xpos, ypos = self.get_xy(pos[0],pos[1])
        # label.place(x=xpos, y=ypos)
        # self.folder_metadata[folder_id][2] = pos
        pass
        

    def close_toplevel(self,folder_window,folder_id,creation_time):
        """To close the open folder and store the time in metadata"""
        destruction_time = datetime.now()
        elapsed_time = destruction_time - creation_time
        self.folder_metadata[folder_id][0].append(elapsed_time)
        folder_window.destroy()

    def show_folder_window(self, foldername):
        """Opens the folder and takes log of the time of access"""
        folder_window = tk.Toplevel(self.root)
        folder_window.title(foldername)
        folder_window.geometry(TOP_WINDOW_HEIGHT.__str__()+"x"+TOP_WINDOW_WIDTH.__str__())

        label = tk.Label(folder_window, text=f"Opened: {foldername}")
        label.pack(padx=10, pady=10)

        folder_id = self.folders[foldername]

        close_button = tk.Button(folder_window, text="Close", command=lambda folder_window=folder_window,folder_id = folder_id, creation_time = datetime.now() : self.close_toplevel(folder_window, folder_id, creation_time))
        close_button.pack(pady=10)


        folder_window.protocol("WM_DELETE_WINDOW", lambda folder_window=folder_window,folder_id = folder_id, creation_time = datetime.now() : self.close_toplevel(folder_window, folder_id, creation_time))



    def save_state(self):
        """Save the current state of desktop including metadata"""
        try:
            save_object(PIK, (self.folders, self.folder_metadata, self.files, self.file_metadata))
        except Exception as e:
            pass

    def close(self):
        """Saves the state of desktop and destroys the window"""
        self.save_state()
        self.root.destroy()

    def rearrange(self):
        """Rearranges the folders after calling the model to get priorities and labels"""
        try:
            kmeans = Model()
            df_dic = kmeans.fit_predict()
            lst = sorted(df_dic.items(),key = lambda x : x[1][-2],reverse=True)
            count = 0
            prev = lst[0][1][-1]
            for column in lst:
                if count > THRESHHOLD or column[1][-1] != prev:
                    break
                pos = self.get_next_empty_priority_pos(df_dic)
                print(column[0],'\t',pos)
                self.folder_metadata[column[0]] = [[],"close",pos]
            self.refresh_display()
        except Exception as e:
            pass
            




        
if __name__ == "__main__":
    myWindow = Finder_window()

        

