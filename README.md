# GPConnect

ChatGPT is pretty awesome, but there should be an API interface to the website. GPConnect is such an interface. It's two simple bits of code. One is a Chrome extension, the other a Django project.

The extension is activated on the ChatGPT website, monitoring the chat and posting prompts. The Django project provides an API endpoint that can be used to send prompts and receive answers.

### Notes
This is very experimental and might stop working if ChatGPT changes anything. I made it so I could use ChatGPT-4 for some learning, testing and experimentation. 

# The Extension
Install the extension as a regular unpacked Chrome extension. This enables the extension, to use it, on the ChatGPT site, after starting a conversation, use "Load Plugin" to activate the plugin and the "Start" and "Stop" button to start and stop the listening and posting process.

In the extension options page the server and port for the endpoint can be configured. Default is port 7500 and localhost.

# The API
The Django project provides a number of endpoints to facilitate interactions with the ChatGPT. The API is Dockerized, and can be started with:

`docker-compose up`

On the ChatGPT side, for the Chrome extension to receive command send responses.

* http://127.0.0.1:7500/chatapi/command/
* http://127.0.0.1:7500/chatapi/response/

On the user side, for a application to give a command and read a response

* http://127.0.0.1:7500/chatapi/set_command/
* http://127.0.0.1:7500/chatapi/get_response/

The format for these are to set a command

    url_base = "http://127.0.0.1:7500/"

    # Define the request payload
    payload = {
        'command': prompt,
    }

    # Make the POST request
    response = requests.post(url_base + 'chatapi/set_command/', json=payload)

    # Extract the nonce from the JSON response
    nonce = response.json()['nonce']

The nonce can than be used to get a response

    url_base = "http://127.0.0.1:7500/"

    # Define the request payload
    payload = {
        'nonce': nonce,
    }

    # Make the POST request
    response = requests.post(url_base + 'chatapi/get_response/', json=payload)

In addition, for testing the URL http://127.0.0.1:7500 can be used to see previous commands and responses and to submit new prompts to ChatGPT.