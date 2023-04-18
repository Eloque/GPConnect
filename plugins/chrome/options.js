const defaultConfig = {
    serverUrl: 'http://localhost',
    serverPort: 7500
};

function saveConfig() {
    const serverUrlInput = document.getElementById('server-url');
    const serverPortInput = document.getElementById('server-port');

    const config = {
        serverUrl: serverUrlInput.value,
        serverPort: serverPortInput.valueAsNumber
    };

    chrome.storage.local.set(config, () => {
        console.log(config);
        console.log('Configuration saved');
    });
}

function loadConfig() {

    console.log("Attempting to load config");

    chrome.storage.local.get(defaultConfig, (config) => {

        console.log(config);

        const serverUrlInput = document.getElementById('server-url');
        const serverPortInput = document.getElementById('server-port');

        serverUrlInput.value = config.serverUrl;
        serverPortInput.value = config.serverPort;
    });
}

chrome.storage.sync.get(defaultConfig, (config) => {
    // Use the configuration values
    //const serverUrlInput = document.getElementById('server-url');
    // const serverPortInput = document.getElementById('server-port');
    let serverUrlInput //  = document.getElementById('server-url');
    let serverPortInput // = document.getElementById('server-port');

    //serverUrlInput.value = config.serverUrl;
    //serverPortInput.value = config.serverPort;
});

document.getElementById('save-btn').addEventListener('click', saveConfig);
document.getElementById('load-btn').addEventListener('click', loadConfig);
