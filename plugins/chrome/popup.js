async function getCurrentTab() {
  let queryOptions = { active: true, lastFocusedWindow: true };
  // `tab` will either be a `tabs.Tab` instance or `undefined`.
  let [tab] = await chrome.tabs.query(queryOptions);
  return tab;
}

let clicked = true;
async function injectScript() {

    let currentTab = await getCurrentTab();
    console.log(currentTab);

    chrome.scripting.executeScript({
        target: {tabId: currentTab.id, allFrames: false},
        files: ['chatapi.js'],
    });

}

document.getElementById('btLoadPlugin').onclick = () => {
    injectScript();
}

document.getElementById('btStart').onclick = () => {

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs)
    {
        chrome.tabs.sendMessage(tabs[0].id, 'startInterval');
    });
};

document.getElementById('btStop').onclick = () => {

    chrome.tabs.query({active: true, currentWindow: true}, function(tabs)
    {
        chrome.tabs.sendMessage(tabs[0].id, 'stopInterval');
    });
};

