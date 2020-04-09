function disableButton() {
    elt = document.getElementById('submit-words')
    elt.style.display='none'
}

function insertWords() {
    entries = document.getElementById('descriptor-entry').querySelectorAll('.word-input')
    story = getParagraph()
    i = 0
    newStory = ""
    for (word of story.split(" ")) {
        if (word[0] === '[') {
            newStory = newStory + "<span class='descriptor'>" + entries[i].value + "</span> "
            i++
        } else {
            newStory = newStory + word + " "
        }
    }
    elt = document.getElementById('story')
    console.log(newStory)
    elt.innerHTML = newStory
    elt.style.color = 'black'
    disableButton()
}

function getParagraph() {
    elt = document.getElementById('story')
    return elt.innerText
}

function watchClick() {
    elt = document.getElementById('submit-descriptors')
    elt.onclick = insertWords
}

window.onload = watchClick;
