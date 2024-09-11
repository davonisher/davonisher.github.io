// js/util_buttons.js

// Functie om een knop te maken
function createButton(text, onClick) {
    const button = document.createElement('button');
    button.innerText = text;
    button.addEventListener('click', onClick);
    return button;
  }
  
  // Functie om een knop toe te voegen aan een element
  function addButtonToElement(elementId, buttonText, onClick) {
    const element = document.getElementById(elementId);
    if (element) {
      const button = createButton(buttonText, onClick);
      element.appendChild(button);
    }
  }
  
  // Voorbeeld gebruik
  document.addEventListener('DOMContentLoaded', () => {
    addButtonToElement('display-projects', 'Click Me', () => {
      alert('Button Clicked!');
    });
  });