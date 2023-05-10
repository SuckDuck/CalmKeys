// ---------------------------- REPRODUCIR O PARAR LA CANCION ----------------------------- //
document.querySelector("#start_btn").onclick = function(){ 
    document.querySelector("#song_choicer").setAttribute("disabled",false)
    this.innerText = this.innerText == "START" ? "STOP" : "START"
    if(this.innerText == "STOP") this.classList.add("music_playing")
    else this.classList.remove("music_playing")
    document.querySelector("#song_choicer").disabled = this.innerText == "START" ? false:true
    document.querySelector("#refresh").disabled = this.innerText == "START" ? false:true
    eel.start_stop_loop()
}

function call_eel(eel_function){
    return new Promise(function(resolve){
        eel_function()(function(data){
            resolve(data)
        })
    })
}


// --------------------------- ACTUALIZAR LA LISTA DE CANCIONES --------------------------- //
// ------------------------------- Y SELECCIONAR LA CANCIÓN ------------------------------- //
function update_songs(){
    call_eel(eel.getSongs).then(function(songs){
        document.querySelector("#song_choicer").innerHTML = ""
        for(let index = 0; index < songs.length; index++){
            let song = songs[index]
            document.querySelector("#song_choicer").innerHTML += (
                `<option value='${index}'>${song}</option>`)
        }
    })}
update_songs()

document.querySelector("#song_choicer").onchange = function(){
    eel.changeSong(this.value)
}


// --------------------------- ACTUALIZAR LA LISTA DE KEY SOUNDS --------------------------- //
// -------------------------------- Y SELECCIONAR EL SONIDO -------------------------------- //
function update_keySounds(){
    call_eel(eel.getKeySounds).then(function(keySounds){
        document.querySelector("#keySound_choicer").innerHTML = ""
        for(let index = 0; index < keySounds.length; index++){
            keySound = keySounds[index]
            document.querySelector("#keySound_choicer").innerHTML += (
                `<option value='${index}'>${keySound}</option>`)
        }
    })}
update_keySounds()

document.querySelector("#keySound_choicer").onchange = function(){
    eel.changeKeySound(this.value)
}


// -------------------------------- VOLUMEN POR CANCIÓN ---------------------------------- //
document.querySelector("#song_volume").oninput = function(){
    value = parseInt(this.value/10) == 0 ? 1 : parseInt(this.value/10)
    eel.change_background_volume(value)
}

// -------------------------------- VOLUMEN POR CANCIÓN ---------------------------------- //
document.querySelector("#keySound_volume").oninput = function(){
    value = parseInt(this.value/10)
    eel.change_key_volume(value)
}

// ---------------------------------- REFRESCA FUENTES ----------------------------------- //
document.querySelector("#refresh").onclick = function(){
    eel.refresh_sources()
    update_songs()
    update_keySounds()
}

// ------------------------------------ IMPORTACIONES ------------------------------------ //
document.querySelector("#importsongs").onclick = function(){eel.importSongs()}
document.querySelector("#importkeys").onclick = function(){eel.importKeys()}