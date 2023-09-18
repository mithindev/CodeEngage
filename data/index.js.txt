const btnEl = document.getElementById("btn");
const appEl = document.getElementById("app");
const clearAllBtnEl = document.getElementById("clear-all-btn");
const changeNameBtnEl = document.getElementById("change-name-btn");

// Load notes from local storage
let notes = getNotes();

// Render existing notes
notes.forEach((note) => {
  const noteEl = createNoteEl(note.id, note.content);
  appEl.insertBefore(noteEl, btnEl);
});

// Create a new note element
function createNoteEl(id, content) {
  const element = document.createElement("textarea");
  element.classList.add("note");
  element.placeholder = "Empty Note";
  element.value = content;

  element.addEventListener("dblclick", () => {
    const confirmation = confirm(localStorage.getItem("name") + ", Do you want to delete this note?😊");
    if (confirmation) {
      deleteNote(id, element);
    }
  });

  element.addEventListener("input", () => {
    updateNote(id, element.value);
  });

  return element;
}

// Delete a note
function deleteNote(id, element) {
  notes = notes.filter((note) => note.id !== id);
  saveNotes();
  appEl.removeChild(element);
}

// Update a note
function updateNote(id, content) {
  const note = notes.find((note) => note.id === id);
  if (note) {
    note.content = content;
    saveNotes();
  }
}

// Add a new note
function addNote() {
  const noteObj = {
    id: Math.floor(Math.random() * 100000),
    content: "",
  };

  const noteEl = createNoteEl(noteObj.id, noteObj.content);
  appEl.insertBefore(noteEl, btnEl);

  notes.push(noteObj);
  saveNotes();
}

// Save notes to local storage
function saveNotes() {
  localStorage.setItem("note-app", JSON.stringify(notes));
}

// Retrieve notes from local storage
function getNotes() {
  return JSON.parse(localStorage.getItem("note-app")) || [];
}

// Clear all notes
function clearAllNotes() {
  notes = [];
  saveNotes();
  appEl.innerHTML = '';
}

// Change name
function changeName() {
  const newName = prompt("Please enter a new username");
  if (newName) {
    localStorage.setItem("name", newName);
    document.getElementById("name").textContent = newName;
    document.title = newName + "'s Notes📝";
  }
}

// Event listener for adding a new note
btnEl.addEventListener("click", addNote);

// Event listener for clearing all notes
clearAllBtnEl.addEventListener("click", clearAllNotes);

// Event listener for changing name
changeNameBtnEl.addEventListener("click", changeName);

// Personalization
if (!localStorage.getItem("hasLoadedBefore")) {
  const name = prompt("Please enter a username");
  localStorage.setItem("name", name);
  localStorage.setItem("hasLoadedBefore", true);
  location.reload();
} else {
  const name = localStorage.getItem("name");
  document.getElementById("name").textContent = name;
  document.title = name + "'s Notes📝";
}
