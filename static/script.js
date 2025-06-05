const myModal = document.getElementById('loginModal')
const myInput = document.getElementById('myInput')

// Autofocus on modal.
myModal.addEventListener('shown.bs.modal', () => {
  myInput.focus()
})