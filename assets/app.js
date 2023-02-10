function switchFunction() {
    var button = document.getElementById("card");
    if (button.innerHTML === "Term") {
      button.innerHTML = "Definition";
    } else {
      button.innerHTML = "Term";
    }
  }