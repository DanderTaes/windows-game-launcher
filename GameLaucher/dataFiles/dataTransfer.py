import json
import subprocess
import os
import io
import shutil
from tkinter.messagebox import showinfo

dictionary = {
    "Minecra": ["/imagenes/gameImgs/minecraft.png", False, r"C:\Users\Ander\Documents\Juegos\MultiMC\MultiMC.exe",
    "Notes", "dateAdded", "dateLastPlayed"],
    "HK": ["/imagenes/gameImgs/hk.jpg", False, r"C:\Users\Ander\Documents\Juegos\Hollow.Knight.Godmaster.v1.4.3.2\Hollow.Knight.v1.5.75.11827\Hollow.Knight.v1.5.75.11827\Hollow Knight.exe", "Notes2", "dateAdded2", "dateLastPlayed2"],
    "Shapez.io": ["/imagenes/gameImgs/HeartIcon.png", True, "C:\Program Files (x86)\Steam\Steam.exe -applaunch 1318690", "Notes3", "dateAdded3", "dateLastPlayed3"],
    "deltarune": ["/imagenes/big-chungus.png", True, r"C:\Program Files (x86)\Steam\steamapps\common\DELTARUNEdemo\DELTARUNE.exe", "Notes4", "dateAdded4", "dateLastPlayed4"],
    "isaac": ["/imagenes/gameImgs/default.png", False, r"C:\Users\Ander\Documents\Juegos\The.Binding.of.Isaac.Repentance.v4.0.4\The Binding of Isaac Rebirth Repentance\isaac-ng.exe", "Notes", "dateAdded", "dateLastPlayed"],
    "Axiom Verge": ["/imagenes/gameImgs/default.png", False, r"C:\Users\Ander\Documents\Juegos\Axiom.Verge.v1.43\Axiom.Verge.v1.43\AxiomVerge.exe", "Notes2", "dateAdded2", "dateLastPlayed2"],
    "game7": ["", False, "gameUrl3", "Notes3", "dateAdded3", "dateLastPlayed3"]
    }
# "game1" : ["imgUrl", favoriteBool, r"gameUrl", "dateAdded", "dateLastPlayed", ["tags"], ["notes"]]



def savetofile(data):
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)
        outfile.close()

def readFile():
    if os.path.isfile('data.json') and os.access('data.json', os.R_OK):
        with open('data.json') as json_file:
            data = json.load(json_file)
            json_file.close()
            return data
    else:
        with io.open(os.path.join('data.json'), 'w') as db_file:
            db_file.write(json.dumps({}))

def openProgram(program):
    print(program)
    try:
        subprocess.run(program)
    except:
        showinfo(title="Error", message="Can't open program") 
    
def copyImage(ruta_image, ruta_nueva):

    try:
        shutil.copyfile(ruta_image, ruta_nueva)
    except shutil.SameFileError:
        print("file already exists")
    








    

