function clickMainButton(){
	// chack update
	if (document.getElementById("main_button_text").innerText == "Chack update"){
		document.getElementById("main_button_text").innerText = "Chacking..."
		document.getElementById("main_box").style.backgroundColor = "#49adff"
		eel.chackupdate()(adawaystatus_callback)
	}
	// adaway on
	else if (document.getElementById("main_button_text").innerText == "Need update" || document.getElementById("main_button_text").innerText == "Off"){
		document.getElementById("main_button_text").innerText = "Turning on..."
		eel.adawayon()(adawayon_callback)
	}
	// adaway off
	else if (document.getElementById("main_button_text").innerText == "On"){
		document.getElementById("main_button_text").innerText = "Turning off..."
		eel.adawayoff()(adawayoff_callback)
	}
	else{
		alert(document.getElementById("main_button_text").innerText)
	}
}
// for chack update
function adawaystatus_callback(adawaystatus){
	document.getElementById("main_button_text").innerText = adawaystatus
	if (adawaystatus == "Need update"){
		document.getElementById("main_box").style.backgroundColor = "orange"
	}
	else if (adawaystatus == "On"){
		document.getElementById("main_box").style.backgroundColor = "#03bb03"
	}
	else if (adawaystatus == "Off"){
		document.getElementById("main_box").style.backgroundColor = "#ffcccc"
	}
	else{
		document.getElementById("main_box").style.backgroundColor = "black"
	}
}

// for adaway on
function adawayon_callback(adawayon_status){
	if (adawayon_status == "fail"){
		alert("Error: Can't on adaway")
		document.getElementById("main_button_text").innerText = "Chack update"
		document.getElementById("main_box").style.backgroundColor = "gray"
	}
	else{
		document.getElementById("main_button_text").innerText = "On"
		document.getElementById("main_box").style.backgroundColor = "#03bb03"
	}
}

// for adaway off
function adawayon_callback(adawayon_status){
	if (adawayon_status == "fail"){
		alert("Error: Can't off adaway")
		document.getElementById("main_button_text").innerText = "Chack update"
		document.getElementById("main_box").style.backgroundColor = "gray"
	}
	else{
		document.getElementById("main_button_text").innerText = "Off"
		document.getElementById("main_box").style.backgroundColor = "#ffcccc"
	}
}