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

function readDefinition(id) {
    var definition = document.getElementById("definition-" + id).querySelector(".definition");
    var text = definition.innerText;
    const speech = new SpeechSynthesisUtterance();
    speech.text = text;
    window.speechSynthesis.speak(speech);
}

function showHint(id, self) {
    var definitionElement = document.getElementById("definition-" + id).querySelector(".definition");

    const words = definitionElement.textContent.split(' ');
    let hint = '';
    
    if (words.length > 0) {
        hint = words[0].charAt(0);
    }

    var hint_e = "First letter: " + hint;

    if (self.textContent === "Show Hint") {
        self.textContent = "Hide Hint";
        self.originalDefinition = definitionElement.textContent; // store the original definition
        definitionElement.textContent = hint_e;
        definitionElement.style.display = "block";
    } else {
        self.textContent = "Show Hint";
        definitionElement.textContent = self.originalDefinition; // restore the original definition
        definitionElement.style.display = "none";
    }
}