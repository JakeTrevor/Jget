function copy(id) {
  let copyText = document.getElementById(id).innerText;
  navigator.clipboard.writeText(copyText);
}
