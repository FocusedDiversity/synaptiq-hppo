document.addEventListener('DOMContentLoaded', () => {
    const backgroundColorInput = document.getElementById('backgroundColor');
    const textColorInput = document.getElementById('textColor');

    document.getElementById('saveColors').addEventListener('click', () => {
        const backgroundColor = backgroundColorInput.value;
        const textColor = textColorInput.value;
        chrome.runtime.sendMessage({ action: 'updateColors', backgroundColor, textColor });
    });
});
