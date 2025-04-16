chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.selectedText) {
      chrome.storage.local.set({ selectedText: message.selectedText });
    }
  });
  