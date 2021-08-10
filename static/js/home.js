document.getElementById('toggle').checked = false;

function classToggle(){
  const navs = document.querySelectorAll('.rmenu')
  navs.forEach(nav => nav.classList.toggle('ToggleShow'));
  if (document.getElementById('toggle').checked == true) {
    document.getElementById('toggl_label').innerHTML="&#10799;";
  } 
  else {
    document.getElementById('toggl_label').innerHTML="&#9776;";
  }
}