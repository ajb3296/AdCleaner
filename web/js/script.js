const mainButtonText = document.getElementById('main_button_text');
const loadingElement = document.getElementById('loading');
const mainBox = document.getElementById('main_box');

function clickMainButton() {
  // check update
  if (mainButtonText.dataset.value === 'check_update') {
    // Text disappear
    mainButtonText.style.display = 'none';
    // Loading appear
    loadingElement.style.display = 'block';

    mainButtonText.dataset.value = 'checking';
    mainBox.style.backgroundColor = '#ededed';
    eel.checkupdate()(adawaystatus_callback);
  }
  // adaway on --> off
  else if (
    mainButtonText.dataset.value === 'need_update' ||
    mainButtonText.dataset.value === 'off'
  ) {
    mainButtonText.innerText = 'Turning on...';
    mainButtonText.dataset.value = 'turning_on';
    eel.adawayon()(adawayon_callback);
  }
  // adaway off --> on
  else if (mainButtonText.dataset.value === 'on') {
    mainButtonText.innerText = 'Turning off...';
    mainButtonText.dataset.value = 'turning_off';
    eel.adawayoff()(adawayoff_callback);
  } else {
    alert(mainButtonText.dataset.value);
  }
}
// for check update
function adawaystatus_callback(adawaystatus) {
  let adawaystatus_code = adawaystatus[0]
  let adawaystatus_text = adawaystatus[1]
  mainButtonText.innerText = adawaystatus_text;
  mainButtonText.dataset.value = adawaystatus_code;
  // Text appear
  mainButtonText.style.display = 'block';
  // Loading disappear
  loadingElement.style.display = 'none';

  if (adawaystatus_code === 'need_update') {
    mainBox.style.backgroundColor = 'orange';
  } else if (adawaystatus_code === 'on') {
    mainBox.style.backgroundColor = '#03bb03';
  } else if (adawaystatus_code === 'off') {
    mainBox.style.backgroundColor = '#ffbbbb';
  } else {
    // Check update
    mainBox.style.backgroundColor = '#aaff89';
  }
}

// for adaway on
function adawayon_callback(adawayon_status) {
  if (adawayon_status === 'finish') {
    mainButtonText.innerText = 'On';
    mainButtonText.dataset.value = 'on';
    mainBox.style.backgroundColor = '#03bb03';
  } else {
    alert(adawayon_status);
    mainButtonText.innerText = 'Check update';
    mainButtonText.dataset.value = 'check_update';
    mainBox.style.backgroundColor = '#aaff89';
  }
}

// for adaway off
function adawayoff_callback(adawayoff_status) {
  if (adawayoff_status === 'finish') {
    mainButtonText.innerText = 'Off';
    mainButtonText.dataset.value = 'off';
    mainBox.style.backgroundColor = '#ffbbbb';
  } else {
    alert(adawayoff_status);
    mainButtonText.innerText = 'Check update';
    mainButtonText.dataset.value = 'check_update';
    mainBox.style.backgroundColor = '#aaff89';
  }
}