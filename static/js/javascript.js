function showdefinition(id, self) {
    var definition = document.getElementById("definition-" + id).querySelector(".definition");
    if (definition.style.display === "none") {
        self.innerHTML = "Hide definition";
        definition.style.display = "block";
    } else {
        self.innerHTML = "Show definition";
        definition.style.display = "none";
    }
}