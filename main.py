import os # it permits to use operating systems command

import tkinter  # it permits to create a window
from tkinter import filedialog  # it permits to create a button to browse folders
from time import sleep  # it permits to wait
from watchdog.observers import Observer  # it permits to add a watcher on windows
from watchdog.events import PatternMatchingEventHandler  # it permits to define caracteristics of a watcher on windows

from PIL import Image  # it permits to use an image in python


mode_to_bpp = {'1':1, 'L':8, 'P':8, 'RGB':24, 'RGBA':32, 'CMYK':32, 'YCbCr':24, 'I':32, 'F':32}  # BITS too choose


def on_created(event):  # Create a function called "on_created" with a parameter called "event" to watch every file created on Windows
    sleep(1)  # wait 1 second for the file to be created
    file_created = event.src_path  # get the filename using event object defined on https://pythonhosted.org/watchdog/api.html
    #DEBUG print("file_created", file_created)
    suffix = "_ORG.tif"  # get the suffix on a variable called "suffix"
    val = len(suffix)  # get the length of the word on variable suffix on variable "val"

    if file_created[-val:] == suffix:  # if the suffix of the filename correspond to the suffix on variable "suffix" we did the process indented
        file_location = os.getcwd() + event.src_path[1:]  # TODO maybe remove /we get the full path of the file using method getcwd() (https://www.tutorialspoint.com/python/os_getcwd.htm) from library os and let it on variable "file_location"
        file_location = file_created  # we get the full path of the file using method getcwd() (https://www.tutorialspoint.com/python/os_getcwd.htm) from library os and let it on variable "file_location"
        try:  # if there was an error during the lines indented go to line with "except:"
            data = Image.open(file_location)  # we open a connection and get the data of the file and let it on variable "data"
            bpp = mode_to_bpp[data.mode]  # we stock the number of bits of the image from "file_location" on variable "bpp"
            data.close()  # we close the file
            if bpp < 16:  # check number of bits before remove
                print("Delete file", file_location, bpp)  # print on console "Delete file" with variable "file_location" and variable "bpp"
                os.unlink(file_location)  # remove file on "file_location" variable
        except:  # if an error occured in previous indented lines to the process on indented lines below
            print("Can't delete file", file_location)  # print on console with variable "file_location"


def create_observer(path_directory_to_clean=""):  # Create a function called "create_observer" with parameter path_directory_to_clean which take by default value "" to launch a watcher
    patterns = "*"  # define a variable called "patterns" with "*"
    ignore_patterns = ""  # define a variable called "ignore_patterns" with ""
    ignore_directories = False  # define a variable called "ignore_directories" with "False"
    case_sensitive = True  # define a variable called "case_sensitive" with "True"
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)  # call a function called PatternMatchingEventHandler (https://pythonhosted.org/watchdog/api.html) with variables defined before and get the result on object "my_event_handler"
    my_event_handler.on_created = on_created  # Put the function called "on_created" on attribute called "on_created" on object "my_event_handler"

    if path_directory_to_clean == "":  # case that we don't define a directory
        path = "."  # the AutoRemover will be active on AutoRemover directory and subdirectories
    else:
        path = path_directory_to_clean  # the AutoRemover will be active on text on variable "path_directory_to_clean"
    go_recursively = True  # define a variable called "go_recursively" and put it boolean "True"
    my_observer = Observer()  # create an object Observer (https://pypi.org/project/watchdog/) and put it on variable my_observer
    #DEBUG print("path", path, "Cut")
    my_observer.schedule(event_handler=my_event_handler, path=path, recursive=go_recursively)  # activate the watcher on directory given on variable "path" using object "my_observer"
    return my_observer  # return the object "my_observer" when the function end the lines above


class App:  # create an object called "App"
    def __init__(self):  # initialise the variables of the object
        self.root = tkinter.Tk()  # the attribute "root" of the object will contains the object Tk() which is a window
        self.my_observer = create_observer() # the variable "my_observer" will contains the result of the called function "created_observer" created above
        self.my_observer.start()  # the function "start()" of the object will be used on object called "my_oberserver" to start the watcher

        def on_closing():  # this function will be called when we click on button "close" on the window
            print("Close AutoRemove")  # print on the console
            self.my_observer.stop()  # it will stop the watcher
            self.my_observer.join()  # it will wait the process to stop the watcher
            self.root.destroy()  # it will end the process of the object called "App" so it will close the window

        def browsefunc():  # this function will be called when we click on button "browse directory to clean"
            path_directory = filedialog.askdirectory()  # it will create a variable and fufill it with the directory we choose
            pathlabel.config(text="Directory to clean " + path_directory)  # it will show a label with the text "Directory to clean " and the text of the variable path_directory
            #TODO Update observer

            self.my_observer.stop()  # it will stop the watcher
            self.my_observer.join()  # it will wait the process to stop the watcher
            self.my_observer = create_observer(path_directory)  # the variable "my_observer" will contains the result of the called function "created_observer" created above
            self.my_observer.start()  # the function "start()" of the object will be used on object called "my_oberserver" to start the watcher

        browsebutton = tkinter.Button(self.root, text="Browse directory to clean", command=browsefunc)  # it will add the button called "Browse directory to clean" that will use the function browseFunc
        browsebutton.pack()  # it will manage the display of the button on the windows

        pathlabel = tkinter.Label(self.root)  # it will add a label to display text
        pathlabel.pack()  # it will manage the display of the text on the windows

        self.root.protocol("WM_DELETE_WINDOW", on_closing)  # it will use the function "on_closing" above to add it process on the button "close window"
        self.root.mainloop()  # it will launch the window


if __name__ == '__main__':  # it will launch this line after line beginning with "mode_to_bpp = {[...]"
    app = App()  # it will create the window


