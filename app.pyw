import asyncio
import keyboard
import pygame
import json
import async_eel

from random import randint
import os


#--------------------------------------------------------------------- ETAPA DE CONFIGURACIONES ---------------------------------------------------------------------------#
pygame.init()
pygame.mixer.init()

max_volume = 5

def update_tracks_n_keys():
    return os.listdir("Songs"), os.listdir("keySounds")
pistas, key_sets = update_tracks_n_keys()

def configuration_phase(selected_track,selected_key_set):
    with open(os.path.join("Songs",pistas[selected_track],"config.json"),"r") as config:
        tracks = {
                "config":json.loads(config.read()),
                "song":[pygame.mixer.Sound(os.path.join("Songs",pistas[selected_track],track)) for track in os.listdir(os.path.join("Songs",pistas[selected_track])) if track != "config.json"],
                "pistas":[track for track in os.listdir(os.path.join("Songs",pistas[selected_track])) if track != "config.json"]
            }
        for index, pista in enumerate(tracks["pistas"]):
            track = tracks["song"][index]
            if pista in tracks["config"]["low"] : track.set_volume(max_volume/10)
            else: track.set_volume(0)

    keys = [pygame.mixer.Sound(os.path.join("keySounds",key_sets[selected_key_set],key)) for key in os.listdir(os.path.join("keySounds",key_sets[selected_key_set]))]
    for key in keys: key.set_volume(0.5)
    return tracks, keys

tracks, keys = configuration_phase(0,0)

typing_intensity = 0
intensity_level = "low"

##############################################################################################################################################################################

# ----------------------------------------------------------------- FUNCIONES ------------------------------------------------------------------ #

async def change_intensity(intensity):
    global intensity_level

    intensity_level = "high" if intensity else "low"
    for i in range(max_volume + 1):
        i_inverso = max_volume-i
        for pista_index, pista in enumerate(tracks["pistas"]):
            if pista in tracks["config"][intensity_level]: 
                if tracks["song"][pista_index].get_volume() < i/10:
                    tracks["song"][pista_index].set_volume(i/10)
            else: 
                if tracks["song"][pista_index].get_volume() > i_inverso/10:
                    tracks["song"][pista_index].set_volume(i_inverso/10)
        await asyncio.sleep(0.5)
    
def press_key(event):
    global typing_intensity
    if typing_intensity < 15 :typing_intensity += 1
    for key in keys: key.stop()
    keys[randint(0,len(keys)-1)].play()
keyboard.on_press(press_key)

playing_song = False
song_loop_task = None
async def song_loop():
    global song_task_delay
    while playing_song:
        for track in tracks["song"]: 
            track.stop()
            track.play()
        await asyncio.sleep(tracks["song"][0].get_length())

#--------------------------------------------------------------------------- GUI --------------------------------------------------------------#
async def gui_loop():
    # ------------- Funciones de los botones ------------- #

    @async_eel.expose
    def start_stop_loop():# <--------------- BOTÓN DE START/MUTE
        global playing_song, song_loop_task, tracks

        if playing_song:
            song_loop_task.cancel()
            playing_song = False
            for track in tracks["song"]: track.stop()

        elif not playing_song:
            playing_song = True
            song_loop_task = asyncio.create_task(song_loop())

    @async_eel.expose# <------------- SELECTOR DE CANCIONES
    def getSongs():return pistas
    @async_eel.expose
    def changeSong(song_index):
        global tracks
        tracks , _ = configuration_phase(int(song_index),0)

    @async_eel.expose# <------------ SELECTOR DE TECLAS
    def getKeySounds():return key_sets
    @async_eel.expose
    def changeKeySound(keySound_index):
        global keys
        _ , keys = configuration_phase(0,int(keySound_index))

    @async_eel.expose
    def change_background_volume(value):# <----------- VOLUMEN DE LA MUSICA
        global max_volume
        max_volume = int(value)
        for track in tracks["song"]:
            if track.get_volume() != 0:
                track.set_volume(max_volume/10)

    @async_eel.expose# <---------- VOLUMEN DE LAS TECLAS
    def change_key_volume(value):
        for key in keys:
            key.set_volume(int(value)/10)

    @async_eel.expose# <----------- BOTON DE REFRESCAMIENTO
    def refresh_sources():
        global pistas, key_sets
        pistas, key_sets = update_tracks_n_keys()

    @async_eel.expose
    def importSongs():os.system("explorer " + os.path.join(os.getcwd(),"Songs"))
    @async_eel.expose
    def importKeys():os.system("explorer " + os.path.join(os.getcwd(),"keySounds"))

    def close_callback(_,__):
        print("closing...")
        os._exit(1)

    async_eel.init('web')
    await async_eel.start('index.html',close_callback=close_callback,size=(410,584))

    # ----------------------- Loop ----------------------- #
    while True:
        await asyncio.sleep(5)

#-----------------------------------------------------------------------------------------------------------------------------------------------

async def main_loop():
    global typing_intensity
    while True:
        if typing_intensity > 0: typing_intensity -= 1
        if playing_song:
            if typing_intensity >= 5 and intensity_level == "low": 
                asyncio.create_task(change_intensity(True))
            if typing_intensity < 5 and intensity_level == "high": 
                asyncio.create_task(change_intensity(False))
        await asyncio.sleep(0.5)

async def main():
    main_loop_task = asyncio.create_task(main_loop())
    gui_loop_task = asyncio.create_task(gui_loop())
    await gui_loop_task
asyncio.run(main())

