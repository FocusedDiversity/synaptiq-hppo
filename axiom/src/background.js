// Store selected colors
let backgroundColor = '#FFFF00';
let textColor = '#000000';

// Listen for messages from popup
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'updateColors') {
        backgroundColor = message.backgroundColor;
        textColor = message.textColor;
        // Send a message to content scripts to update colors
        chrome.tabs.query({ active: true, currentWindow: true }, tabs => {
            chrome.tabs.sendMessage(tabs[0].id, { action: 'updateColors', backgroundColor, textColor });
        });
    }
});
