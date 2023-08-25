let backgroundColor = '#FFFF00';
let textColor = '#000000';

// Function to highlight instances of the word "the"
function highlightTheInstances() {
    const elements = document.querySelectorAll('*:not(script):not(style)');
    elements.forEach(element => {
        const textNodes = getTextNodes(element);
        textNodes.forEach(node => {
            const text = node.nodeValue;
            const replacedText = text.replace(/the/gi, `<span style="background-color: ${backgroundColor}; color: ${textColor};">$&</span>`);
            if (text !== replacedText) {
                node.parentNode.replaceChild(document.createRange().createContextualFragment(replacedText), node);
            }
        });
    });
}

// Helper function to get text nodes from an element
function getTextNodes(element) {
    const walker = document.createTreeWalker(element, NodeFilter.SHOW_TEXT, null, false);
    const textNodes = [];
    let node;
    while (node = walker.nextNode()) {
        textNodes.push(node);
    }
    return textNodes;
}

// Execute the highlighting function
highlightTheInstances();

// Message listener to handle communication with background script
chrome.runtime.onMessage.addListener(message => {
    if (message.action === 'updateColors') {
        backgroundColor = message.backgroundColor;
        textColor = message.textColor;
        highlightTheInstances();
    }
});
