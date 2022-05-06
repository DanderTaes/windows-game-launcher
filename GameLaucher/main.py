import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import tkinter.font as font
import os.path
from dataFiles import dataTransfer as dT
import math
from itertools import islice
from PIL import Image, ImageTk
import datetime

# pyinstaller --onefile --name GameLauncherv2.0.1BETA --icon=imagenes\app.ico -w main.py

dateLast = datetime.datetime(9999, 12, 31, 23, 59, 59, 999999).strftime('%Y%m%d%H%M%S')  
dateEarlier = datetime.datetime(1, 1, 1, 0, 00, 00, 000000).strftime('%Y%m%d%H%M%S')

# colors: #18191A, #242526, #3A3B3C, #E4E6EB, #B0B3B8
bgColor = "#18191A"
bgTopBarColor = "#242526"
hoverColor = "#3A3B3C"
fgColor = "#E4E6EB"
fgSecondaryColor = "#B0B3B8"
# From left to right: background, card, hover color, primary text, secondary text
ordersHomePage = ["Last Added", "Name", "Last Played"]
ordersNotes = ["Name", "Favorites", "With Notes", "Without Notes"]
tagList=["Steam", "Epic Games", "Origin"]
defaultNewGameProperties = ["imgUrl", "Fav", "gameUrl", dateLast, dateLast, ["Notes"]]
cateoryTuple = (("Stores", "Steam", "Epic", "Origin", "Hacked", "Emulator"),
                ("Genre", "FPS", "Platformer", "Roguelike", "Metroidvania", "Sandbox", "RPG", "Singleplayer", "Multiplayer"),
                ("State of play", "Playing", "Finished", "To Play", "100%", "Waiting For Updates"))

LARGE_FONT=(12)
absPath = os.path.abspath("./")

class GameLauncherApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, absPath + '/imagenes/baseIcon.ico')

        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True, anchor="n")
        self.container.grid_rowconfigure(0, weight=1) # weight = priority
        self.container.grid_columnconfigure(0, weight=1)

        

        self.frames = {}

        for F in (HomePage, Notes):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")


        self.show_frame(HomePage)

    def show_frame(self, controller):
        frame = self.frames[controller]
        frame.tkraise()
    
    
class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controlador = controller
        self.clicked = tk.StringVar()
        self.clicked.set( "Last Played" )
        self.tagSelected = tk.StringVar()
        self.tagSelected.set("Tags")
        self.tagLIST = []

        self.onlyFavsBool = False
        

        self.heartIcon = tk.PhotoImage(file='./imagenes/HeartIcon.png').subsample(50,50)
        self.heartIconOff = tk.PhotoImage(file='./imagenes/HeartIconOff.png').subsample(50,50)

        self.topbar = tk.Frame(self, width=100, height=40, bg=bgTopBarColor)
        self.topbar.pack(side="top", fill="x", anchor="n")
        # main content area
        self.mainarea = tk.Frame(self, width=500, height=200, border=False, bg=bgColor)
        self.mainarea.pack(side="top", fill="both", expand=True)       
        # topbar
        self.favoriteButton = tk.Button(self.topbar, image=self.heartIconOff, command= self.changeOnlyFavs)
        self.favoriteButton.config(bg=bgTopBarColor, border=False, activebackground=hoverColor)
        self.favoriteButton.image = self.heartIconOff
        self.favoriteButton.pack(side="left", padx=10, pady=5)
        allGamesButton = tk.Button(self.topbar, text="All games")
        allGamesButton.config(bg=bgTopBarColor, border=False, fg=fgColor, state="disabled", height=2)
        allGamesButton.pack(side="left", padx=5, pady=5)
        notesButton = tk.Button(self.topbar, text="Notes", command=lambda: controller.show_frame(Notes))
        notesButton.config(bg=bgTopBarColor, border=False, fg=fgColor, height=2, activebackground=hoverColor)
        notesButton.pack(side="left", padx=5, pady=5)
        self.searchBar = tk.Entry(self.topbar, width=20, state="normal")
        self.searchBar.config(bg=bgColor, fg=fgColor, font=LARGE_FONT)
        self.searchBar.pack(side="left", padx=5, pady=5, ipady=3)
        self.searchBar.focus()
        self.searchButton = tk.Button(self.topbar, text="Search", command=lambda searcH=True: self.search(searcH))
        self.searchButton.config(bg=bgTopBarColor, fg=fgColor, activebackground=hoverColor)
        self.searchButton.pack(side="left", padx=3, pady=5)
        self.nosearchButton = tk.Button(self.topbar, text="Reset Search", command=lambda searcH=False: self.search(searcH))
        self.nosearchButton.config(bg=bgTopBarColor, fg=fgColor, activebackground=hoverColor)
        self.nosearchButton.pack(side="left", padx=3, pady=5)
        optionDrop = tk.OptionMenu(self.topbar, self.clicked, *ordersHomePage, command= self.listCreator)
        optionDrop.config(bg=bgTopBarColor, highlightbackground=bgTopBarColor, border=False, fg=fgColor, height=2, activebackground=hoverColor, direction="below")
        optionDrop.pack(side="right", padx=5, pady=5)
        
        # var = tk.StringVar(value="Tags")
        menubutton = tk.Menubutton(self.topbar, text="Tags", indicatoron=True,borderwidth=1, relief="raised", width=20)
        main_menu = tk.Menu(menubutton, tearoff=False)
        menubutton.configure(menu=main_menu, bg=bgTopBarColor, highlightbackground=bgTopBarColor, border=False, fg=fgColor, height=2, activebackground=hoverColor, direction="below")
        for item in cateoryTuple:
            menu = tk.Menu(main_menu, tearoff=False)
            
            main_menu.add_cascade(label=item[0], menu=menu)
            for value in item[1:]:
                var = tk.IntVar()
                menu.add_checkbutton(label=value, variable=var, command=lambda value=value, var=var: self.sortByTag(value, var))
        main_menu.add_command(label='None', command=lambda: self.sortByTag("",0, reset=0))
        menubutton.pack(side="top", padx=5, pady=5)       

        self.mainarea.bind_all("<Return>", (lambda event: self.search(None)))

        self.favImage = Image.open("./imagenes/favoriteTrue.png").resize((20, 20), Image.ANTIALIAS)
        self.favImage = ImageTk.PhotoImage(self.favImage)
        self.notfavImage = Image.open("./imagenes/favoriteFalse.png").resize((20, 20), Image.ANTIALIAS)
        self.notfavImage = ImageTk.PhotoImage(self.notfavImage)
        self.optionsImg = Image.open("./imagenes/optionsIcon.png").resize((20, 20), Image.ANTIALIAS)
        self.optionsImg = ImageTk.PhotoImage(self.optionsImg)

        self.scrollContent()
    
    def sortByTag(self, tag, var, reset=None):
        if reset is not None:
            self.tagLIST.clear()
        else:            
            if var.get() == 1:
                self.tagLIST.append(tag)
            else:
                if tag in self.tagLIST:
                    self.tagLIST.remove(tag)
        
        self.listCreator()
    
    def listCreator(self, game4Change=None, change=None, replaced=None,delete=None, search=None):
        self.canvas.yview_scroll(-100, "units")
        self.listDivided = []
        if game4Change != None and change != None: # detects if it's new or a change
            if replaced != None:
                self.dictFromJson[game4Change] = self.dictFromJson.pop(replaced)
            self.dictFromJson[game4Change] = change
            dT.savetofile(self.dictFromJson)
        elif delete != None:
            del self.dictFromJson[delete]
            dT.savetofile(self.dictFromJson)
        dictFromJsonUnordered = dT.readFile()
        
        self.dictFromJson = dictFromJsonUnordered
       
        
        if self.clicked.get() == "Last Added":
            self.dictFromJson = dict(sorted(dictFromJsonUnordered.items(), reverse=True, key=lambda item: item[1][3]))
        elif self.clicked.get() == "Name":
            self.dictFromJson = dict(sorted(dictFromJsonUnordered.items(), key=lambda x: x[0].lower()))
        elif self.clicked.get() == "Last Played":
            self.dictFromJson = dict(sorted(dictFromJsonUnordered.items(), reverse=True, key=lambda item: item[1][4]))
        
        self.dictPlusAdd = self.dictFromJson.copy()
        if self.tagLIST:
            deleteValues = []
            for value in dict(self.dictPlusAdd).keys():
                for tag in self.tagLIST:
                    if not tag in self.dictFromJson[value][5]:
                        if not value in deleteValues: 
                            deleteValues.append(value)
            for item in deleteValues:
                del self.dictPlusAdd[item]
            deleteValues.clear()
                    
            
        if search != None:
            for value in dict(self.dictPlusAdd).keys():
                if not search.upper() in value.upper():
                    del self.dictPlusAdd[value]
        
        if self.onlyFavsBool:
            for key, value in dict(self.dictPlusAdd).items():
                if value[1] == False:
                    del self.dictPlusAdd[key]
        else:
            self.dictPlusAdd["NuEvO"] = defaultNewGameProperties
        for item in self.chunks(self.dictPlusAdd, 4):
            self.listDivided.append(item)        
        self.organizacionCuadrados()
    
    def search(self, searchY):
        if searchY == True:
            self.listCreator(search=self.searchBar.get())
        elif searchY == False:
            self.searchBar.delete(0,'end')
            self.listCreator()
        elif searchY == None:
            if not self.searchBar.get() == "":
                self.listCreator(search=self.searchBar.get())

    
    def changeOnlyFavs(self):
        if self.onlyFavsBool:
            self.favoriteButton['image'] = self.heartIconOff
            self.onlyFavsBool = False
            self.listCreator()
            
        else:
            self.favoriteButton['image'] = self.heartIcon
            self.onlyFavsBool = True
            self.listCreator()



    def scrollContent(self, *args):
        self.canvas = tk.Canvas(self.mainarea, bg=bgColor, highlightthickness=0)
        self.cframe = tk.Frame(self.canvas, bg=bgColor, border=False)
        self.vsb = tk.Scrollbar(self.mainarea, orient="vertical", command=self.canvas.yview, border=False)
        self.canvas.configure(yscrollcommand=self.vsb.set)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel) # sw


        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.cframe, anchor="nw",tags="self.cframe")

        self.cframe.bind("<Configure>", self.onFrameConfigure)

        self.listCreator()
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units") # scroll wheel

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def chunks(page, data, SIZE=5):
                it = iter(data)
                for i in range(0, len(data), SIZE):
                    yield {k:data[k] for k in islice(it, SIZE)}
    
    def altFav(self, button, info, game, *args):
        if info[1] == False:
            button['image'] = self.favImage
            self.dictFromJson[game][1] = True
            info[1] = True
        else:
            button['image'] = self.notfavImage
            self.dictFromJson[game][1] = False
            info[1] = False
        dT.savetofile(self.dictFromJson)
        
    def optionChanger(self,option, game, *args):
        self.stringExecuted.set("")

        if option == "Edit":
            popup = PopOut(self.controlador)
            popup.setBrother(self)
            popup.formCreate(self.dictFromJson[game],game)
        elif option == "Delete":
            self.listCreator(delete=game)
        elif option == "Notes":
            showinfo(title="Coming soon...", message="This feature is not available yet")
           


    
    def openCreateMode(self, button=None):
        self.newGameImage.config(state='disable')
        popup = PopOut(self.controlador)
        popup.setBrother(self)
        popup.formCreate()
    
    def clear_frame(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()
        
    def openGame(self, gameUrl, game):
        dT.openProgram(gameUrl[2])
        gameUrl[4] = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        self.listCreator(game, gameUrl)


    def organizacionCuadrados(self):

        self.clear_frame(self.cframe)
        gameRows = len(self.listDivided)
        self.stringExecuted = tk.StringVar()
        self.stringExecuted.set("")
        editOptions = ["Edit","Notes", "Delete"]

        for n in range(0,gameRows):
            tempBigFrame = tk.Frame(self.cframe, width=550, height=170)
            tempBigFrame.config(bg=bgColor)
            tempBigFrame.pack(side='top', fill="x", expand=True, anchor='ne', padx=10, pady=10)
            for idx,game in enumerate(self.listDivided[n]):
                tempGameFrame = tk.Frame(tempBigFrame, height=170, width=150)
                tempGameFrame.config(bg=bgColor)
                tempGameFrame.pack(side='left', fill="x", anchor='ne', padx=10)
                # imagenes
                try:
                    image = Image.open(absPath + self.listDivided[n][game][0]).resize((140, 140), Image.ANTIALIAS)
                    currentImage = ImageTk.PhotoImage(image)
                except:
                    image = Image.open("./imagenes/gameImgs/default.png").resize((140, 140), Image.ANTIALIAS)
                    currentImage = ImageTk.PhotoImage(image)       

                if game == "NuEvO":
                    image = Image.open("./imagenes/plus.png").resize((140, 140), Image.ANTIALIAS)
                    currentImage = ImageTk.PhotoImage(image)
                    self.newGameImage = tk.Button(tempGameFrame,image= currentImage, command=lambda: self.openCreateMode())
                    self.newGameImage.config(bg=bgTopBarColor, border=False, activebackground=bgTopBarColor)
                    self.newGameImage.image = currentImage
                    self.newGameImage.pack(side="top", padx=5, pady=0)

                    optionBar = tk.Frame(tempGameFrame, height=23, width=140)
                    optionBar.config(bg="#151617")
                    optionBar.pack(side='top', anchor='s', pady=5)

                    gameName = tk.Label(optionBar, text="New Game", bg="#151617", fg=fgColor)
                    gameName.config(padx=10)
                    gameName.pack(side="left", padx=0, pady=0, anchor="center")
                else:

                    gameImage = tk.Button(tempGameFrame,image= currentImage, command=lambda gameUrl= self.listDivided[n][game], game=game: self.openGame(gameUrl, game))
                    gameImage.config(bg=bgTopBarColor, border=False, activebackground=bgTopBarColor)
                    gameImage.image = currentImage
                    gameImage.pack(side="top", padx=5, pady=0)
                    # barra abajo
                    
                    optionBar = tk.Frame(tempGameFrame, height=23, width=140)
                    optionBar.config(bg="#151617")
                    optionBar.pack(side='top', anchor='s', pady=5)
                    # corazon
                
                    if self.listDivided[n][game][1] == True:
                        corazonEmote = tk.Button(optionBar,image=self.favImage)
                        corazonEmote.image = self.favImage
                    else:
                        corazonEmote = tk.Button(optionBar,image=self.notfavImage)
                        corazonEmote.image = self.notfavImage

                    corazonEmote.config(bg="#151617", border=False, activebackground=hoverColor, command=lambda button = corazonEmote, gamePass = self.listDivided[n][game], gameName=game: self.altFav(button, gamePass, gameName))
                    corazonEmote.grid(row=0, column=0, sticky="w", padx=10)
                                
                 # nombre
                    gameName = tk.Label(optionBar, text=game, bg="#151617", fg=fgColor, width=8)
                    gameName['font'] = font.Font(size=10)
                    optionBar.pack_propagate(0)
                    gameName.grid(row=0, column=1, padx=0)

                    optionsGame = tk.OptionMenu(optionBar, self.stringExecuted,*editOptions, command=lambda option=self.stringExecuted.get(), gameSelected=game:self.optionChanger(option, gameSelected))
                    optionsGame.config(bg="#151617", highlightbackground="#151617", border=False, activebackground=hoverColor)
                    optionsGame.grid(row=0, column=2, sticky="e")

class Notes(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.clicked = tk.StringVar()
        self.clicked.set( "Order" )

        heartIcon = tk.PhotoImage(file='./imagenes/HeartIcon.png').subsample(50,50)

        self.topbar = tk.Frame(self, width=100, height=40, bg=bgTopBarColor, relief='solid')
        self.topbar.pack(side="top", fill="x", anchor="n")
        # main content area
        self.mainarea = tk.Frame(self, width=500, height=200, bg=bgColor)
        self.mainarea.pack(side="top", fill="both", expand=True)
        # topbar       
        favoriteButton = tk.Button(self.topbar, image=heartIcon, command=lambda: controller.show_frame(Favorites))
        favoriteButton.config(bg=bgTopBarColor, border=False, activebackground=hoverColor)
        favoriteButton.image = heartIcon
        favoriteButton.pack(side="left", padx=10, pady=5)
        allGamesButton = tk.Button(self.topbar, text="All games", command=lambda: controller.show_frame(HomePage))
        allGamesButton.config(bg=bgTopBarColor, border=False, fg=fgColor, height=2, activebackground=hoverColor)
        allGamesButton.pack(side="left", padx=10, pady=5)
        notesButton = tk.Button(self.topbar, text="Notes")
        notesButton.config(bg=bgTopBarColor, border=False, fg=fgColor, height=2, state="disabled")
        notesButton.pack(side="left", padx=10, pady=5)
        optionDrop = tk.OptionMenu(self.topbar, self.clicked, *ordersHomePage, command= self.orderChange)
        optionDrop.config(bg=bgTopBarColor,highlightbackground=bgTopBarColor, border=False, fg=fgColor, height=2, activebackground=hoverColor, direction="below")
        optionDrop.pack(side="right", padx=10, pady=5)

        # content
        label = tk.Label(self.mainarea, text="Coming soon...", font=LARGE_FONT, bg='#18191a', fg=fgColor)
        label.pack(pady=10, padx=10)

    def orderChange(self, position, *args):
        print("NOT FINAL")
        print(position)


class PopOut(tk.Toplevel):
    def __init__(self, master, **kwargs):
        tk.Toplevel.__init__(self, master,**kwargs)
        self.geometry('360x350')
        self.wm_title("New Game")
        self.iconbitmap(self, absPath + '/imagenes/baseIcon.ico')
        self.focus_set()
        # master.attributes('-disabled', True)
        self.attributes('-topmost', True)
        self.controller = master

        self.noImage = Image.open(absPath + "/imagenes/addImage.png").resize((100 , 100), Image.ANTIALIAS)
        self.noImage = ImageTk.PhotoImage(self.noImage)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True, anchor="n")
        self.container.config(bg=bgColor)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=3)
        self.imageToPass = None
        self.gameUrlToPass = None
        self.listToPass= None
        self.tagLIST = []

        self.formFrame = tk.Frame(self.container, width=400, height=230, bg=bgColor, relief='solid')
        self.formFrame.pack(side="top", fill="x", expand=True, anchor="n", padx=10, pady=20)

        buttonFrame = tk.Frame(self.container, width=400, height=50, bg=bgColor, relief='solid')
        buttonFrame.pack(side="top", fill="x", expand=True, anchor="s")

        cancelButton = tk.Button(buttonFrame, text="Cancel", command=lambda: self.close())
        cancelButton.config(bg=bgTopBarColor, border=False, fg=fgColor, height=2, width=20)
        cancelButton.pack(side="left", anchor="s", padx=10, pady=10)
        saveButton = tk.Button(buttonFrame, text="Save", command=lambda: self.saveAndExit())
        saveButton.config(bg=bgTopBarColor, border=False, fg=fgColor, height=2, width=20)
        saveButton.pack(side="right", anchor="s", padx=10, pady=10)
        #capture close event
        self.protocol("WM_DELETE_WINDOW", self.close)

    def formCreate(self, game2Edit=None, gameEdited=None):
        self.controller.update()
        if game2Edit is not None and gameEdited is not None:
            if game2Edit[0] == "":
                game2Edit[0] = "./imagenes/gameImgs/default.png"
            self.noImage = Image.open(absPath + game2Edit[0]).resize((100 , 100), Image.ANTIALIAS)
            self.noImage = ImageTk.PhotoImage(self.noImage)
            self.game2Edit = game2Edit
            self.gameEdited = gameEdited

        self.imageButton = tk.Button(self.formFrame, image=self.noImage)
        self.imageButton.config(bg=hoverColor, border=False, activebackground=hoverColor, width=100, height=100, command=lambda: self.select_file("image"))
        self.imageButton.image = self.noImage
        self.imageButton.grid(column=0, row=0, padx=10)



        nameFrame = tk.Frame(self.formFrame)
        nameFrame.config(bg=bgColor, height=100)
        nameFrame.grid(column=1, row=0, sticky="sw", padx=15)

        openableFrame = tk.Frame(self.formFrame)
        openableFrame.config(bg=bgColor, height=100)
        openableFrame.grid(column=0, row=2, columnspan=2, sticky="w", pady=30, padx=10)

        nameLabel = tk.Label(nameFrame, text="Name: ")
        nameLabel.config(fg=fgColor, bg=bgColor, border=False, font=LARGE_FONT)
        nameLabel.pack(side="top", anchor="w", pady=7)
        
        self.nameBox = tk.Entry(nameFrame, width= 20)
        self.nameBox.config(fg=fgColor, bg=hoverColor, font=LARGE_FONT)
        self.nameBox.focus()
        if game2Edit is not None and gameEdited is not None:
            self.nameBox.insert(0,gameEdited)
            self.replaced = self.nameBox.get()
        else:
            self.replaced = ""
        self.nameBox.pack(side="top", anchor="w", pady=3)


        self.exeLabel = tk.Label(openableFrame, text="Executable of the game: ")
        self.exeLabel.config(fg=fgColor, bg=bgColor, border=False, font=LARGE_FONT)
        self.exeLabel.pack(side="left", anchor="w", pady=7)
        
        openGameButton = tk.Button(openableFrame, text="open", command=lambda: self.select_file())
        openGameButton.config(fg=fgColor, bg=hoverColor, font=LARGE_FONT, activebackground=hoverColor, border=False)
        openGameButton.pack(side="left", anchor="center", padx=10)

        menubutton = tk.Menubutton(openableFrame, text="Tags", indicatoron=True,borderwidth=0, relief="raised", width=5)
        main_menu = tk.Menu(menubutton, tearoff=False)
        menubutton.configure(menu=main_menu,font=LARGE_FONT, bg=hoverColor, highlightbackground=bgTopBarColor, border=False, fg=fgColor, height=1, activebackground=hoverColor, direction="below")
        self.tagLIST = game2Edit[5]
        for item in cateoryTuple:
                
            menu = tk.Menu(main_menu, tearoff=False)
            main_menu.add_cascade(label=item[0], menu=menu)
            for value in item[1:]:
                var = tk.IntVar()
                if game2Edit is not None and gameEdited is not None and value in game2Edit[5]:
                    var.set(1)                 
                menu.add_checkbutton(label=value, variable=var, command=lambda value=value, var=var: self.sortByTag(value, var))
        
        menubutton.pack(side="left", anchor="center", padx=5)
        
    
    def sortByTag(self, tag, var):
        if var.get() == 1:
            self.tagLIST.append(tag)
        else:
            if tag in self.tagLIST:
                self.tagLIST.remove(tag)

    
    def setBrother(self, bro):
        self.brother = bro

    def close(self, event=None):
        #re-enable the main window
        self.master.attributes('-disabled', False)
        self.tagLIST.clear()
        #destroy this window
        self.destroy()
        self.brother.newGameImage.config(state="normal")
    def saveAndExit(self):
        if self.nameBox.get() != "":
            if self.gameUrlToPass != None:
                self.gameUrlToPass.replace("/", r"\\")
            try:
                split_url = self.imageToPass.split("/")
                nameOfFile = split_url[-1]
                ruta_nueva =  f".\\imagenes\\gameImgs\\{nameOfFile}" # maybe error xd
                dT.copyImage(self.imageToPass, ruta_nueva)
            except:
                showinfo(title="Error", message="Failed to save new img") 
                ruta_nueva = ""
            if self.replaced != "":
                if self.gameUrlToPass == None:
                    self.gameUrlToPass = self.game2Edit[2]
                if ruta_nueva == "":
                    self.listToPass = [self.game2Edit[0], self.game2Edit[1], self.gameUrlToPass, self.game2Edit[3], self.game2Edit[4], self.tagLIST]
                else:
                    self.listToPass = [ruta_nueva, self.game2Edit[1], self.gameUrlToPass, self.game2Edit[3], self.game2Edit[4], self.tagLIST]
                self.brother.listCreator(self.nameBox.get(), self.listToPass, self.replaced)
                self.replaced = ""
            
            else:
                self.listToPass = [ruta_nueva, False, self.gameUrlToPass, datetime.datetime.now().strftime('%Y%m%d%H%M%S'), dateEarlier, self.tagLIST]
                self.brother.listCreator(self.nameBox.get(), self.listToPass)
            self.close()
        else:
            showinfo(title="Error", message="Failed to save game, try and put a name")
    
    def select_file(self, type=None):
        if type == "image":
            filetypes = (
                ("image", "*.jpeg"),
                ("image", "*.png"),
                ("image", "*.jpg")
            )
            filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
            self.imageToPass = filename
        else:
            filetypes = (
                ('Application files', '*.exe'),
                ('All files', '*.*')
            )
            filename = fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes)
            self.gameUrlToPass = filename

        
        


if __name__ == "__main__":
    app = GameLauncherApp()
    app.geometry("725x500")
    app.resizable(0,1)
    app.wm_title("GameLauncher")
    app.mainloop()

# TODO:
"""
notas
corregir bugs de tags o añadir mas
    bug que se queda check las tags cuando "None"
    añadir:
        Openworld
        To finish
cambiar icono


"""