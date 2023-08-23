console.log("Loading chatapi.js");

let url, port;
let commandUrl, responseUrl;

const defaultConfig = {
    serverUrl: 'http://localhost',
    serverPort: 7500
};

chrome.storage.local.get(defaultConfig, (config) => {
  url = config.serverUrl;
  port = config.serverPort;

  console.log(`Server URL: ${url}:${port}`);
  commandUrl = `${url}:${port}/chatapi/command/`;
  console.log(`Command URL: ${commandUrl}`);

  responseUrl = `${url}:${port}/chatapi/response/`;
  console.log(`Response URL: ${responseUrl}`);
});


// Define a listener to start and stop the interval timer
chrome.runtime.onMessage.addListener(function(message, sender, sendResponse) {
  if (message === 'startInterval') {
    startInterval();
  } else if (message === 'stopInterval') {
    stopInterval();
  }
});

// Define the startInterval function
function startInterval() {
  // Start the interval timer to call the CheckCommand function every 3 seconds
  console.log("Starting interval timer");
  console.log(`Server URL: ${url}:${port}`);

  intervalId = setInterval(checkCommand, 3000);
}

// Define the stopInterval function
function stopInterval() {
  // Stop the interval timer
  console.log("Stopping interval timer");
  clearInterval(intervalId);
}

var lastNonce = 0;
var waitingForResponse = false;

function checkCommand() {

    console.log("Checking for command");

    // Check if the previous command has been processed
    if ( CheckIfCommandProcessed() == true )
    {
        let xhr = new XMLHttpRequest();
        xhr.open('GET', commandUrl);
        xhr.onload = function () {
            if (xhr.status === 200) {
                let response = JSON.parse(xhr.responseText);
                let nonce = response.nonce;
                let command = response.command;
                let answered = response.answered;

                if (!answered)
                {
                    if (nonce > lastNonce) {
                        giveCommand(command);
                        lastNonce = nonce;
                    }
                }

                // console.log("Checking for command again in 3 seconds");

            }
        };
        xhr.send();
    }
}

function giveCommand(command) {
    // console.log("Received command: " + command);

    // Get a list of all the buttons on a page
    var buttons = document.getElementsByTagName('button');

    // the last button is the one we want to click
    submitButton = buttons[buttons.length - 1];

    // Get the previous sibling of the submit button
    // This is the text input field
    var input = submitButton.previousSibling;

    input = document.getElementById('prompt-textarea');

    // Clear the input field
    input.value = '';

    // Select the input field as the active element
    input.focus();
    document.execCommand('insertText', false, command);

    clickSubmit()

}


function clickSubmit() {
  // Get a list of all the buttons on a page
  var buttons = document.getElementsByTagName('button');

  waitingForResponse = true;

  // the last button is the one we want to click
  buttons[buttons.length - 2].click();

}

function CheckIfCommandProcessed() {
    var buttons = document.getElementsByTagName('button');
    var text = buttons[buttons.length - 1].innerText;
    // console.log("Generate button text is: " + text);
    var ready = false

    // loop through all the buttons
    for (var i = 0; i < buttons.length; i++) {
        if ( buttons[i].innerText == "Regenerate" ){
            ready = true;
        }

    }


    if (ready== true){
        // console.log("Response is done, going back...");

        if (waitingForResponse === true) {
            ReturnResponse();
        }

        waitingForResponse = false;
        return true;
    }
    else
    {
        // console.log("Response is pending, waiting..");
        return false;
    }
}

function ReturnResponse() {

    // console.log("JSONifying response");

    // Get all elements with class "group w-full text-gray-800"
    const elements = document.getElementsByClassName("group w-full text-token-text-primary border-b");

    // Get the last element
    const lastElement = elements[elements.length - 1];

    // Get the text of the last element
    const text = lastElement.innerText;

    // Stick the inner text in a JSON object together with the nonce
    const response = {  "nonce": lastNonce, "response": text };

    // Convert the data object to a JSON string
    var json = JSON.stringify(response);

    var xhr = new XMLHttpRequest();

    // Set the request type to POST and the content type to JSON
    xhr.open("POST", responseUrl, true);
    xhr.setRequestHeader('Content-type','application/json');

    // Send the JSON data
    xhr.send(json);

    // console.log("Sending response: " + json);
}