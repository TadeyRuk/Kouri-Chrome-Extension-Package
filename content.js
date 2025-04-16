// Stores the last selected text and sends it to the extension when updated
document.addEventListener("mouseup", () => {
    const selectedText = window.getSelection().toString().trim();
    
    if (selectedText) {
      chrome.runtime.sendMessage({ selectedText });
    }
  });
  