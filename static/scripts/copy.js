function copy(id) {
  console.log(id);
  let copyText = document.getElementById(id).innerText;
  navigator.clipboard.writeText(copyText);
}
