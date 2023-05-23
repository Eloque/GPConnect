from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
import time

from apichat.models import ChatMessage

def chat(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt')
        nonce = int(time.time())
        chat_message = ChatMessage(prompt=prompt, nonce=nonce)
        chat_message.save()

        # We should wait for the response to be updated
        while chat_message.response == '':
            time.sleep(1)
            chat_message = ChatMessage.objects.get(nonce=nonce)

    else:
        prompt = ''

    # Return a list of 10 chats, in reverse order
    chats = ChatMessage.objects.all().order_by('-id')[:10]

    return render(request, 'apichat/chat.html', {'prompt': prompt, 'chats': chats})


# This is the command that is about to be send to ChatPlug
@csrf_exempt
def command(request):

    # Get the most recent ChatMessage
    chat_message = ChatMessage.objects.last()

    # check if it's answered
    if len(chat_message.response) != 0:
        answered = True
    else:
        answered = False

    response_data = {
        'nonce': chat_message.nonce,
        'command': chat_message.prompt,
        'answered': answered
    }

    json_response = JsonResponse(response_data)

    return json_response


@csrf_exempt
def response(request):
    # create your response

    response = HttpResponse()

    if request.method == 'POST':
        data = json.loads(request.body)

        # Get the nonce from the request
        nonce = data['nonce']

        # Get the ChatMessage with the matching nonce
        chat_message = ChatMessage.objects.get(nonce=nonce)

        # Update the ChatMessage with the response
        chat_message.response = data['response']
        chat_message.save()

    return response


@csrf_exempt
def set_command(request):

    if request.method == 'POST':

        # Load the JSON data from the request
        data = json.loads(request.body)
        # Get the nonce from the request
        command = data['command']

        chat_message = ChatMessage(prompt=command)
        chat_message.save()

        nonce = chat_message.nonce
        json_response = JsonResponse({'nonce': nonce})

    else:
        
        json_response = JsonResponse({'error': 'This is a POST request only.'})

    return json_response


@csrf_exempt
def get_response(request):

    if request.method == 'POST':

        # Load the JSON data from the request
        data = json.loads(request.body)
        # Get the nonce from the request
        nonce = data['nonce']

        # Get the ChatMessage with the matching nonce
        try:
            chat_message = ChatMessage.objects.get(nonce=nonce)
            json_response = JsonResponse(chat_message.response, safe=False)

        except ChatMessage.DoesNotExist:
            json_response = JsonResponse({'error': "Nonce not found"})

    else:
        chat_message = ChatMessage.objects.last()
        nonce = chat_message.nonce
        json_response = JsonResponse({'error': 'This is a POST request only.',
                                      "nonce": nonce})

    return json_response


@csrf_exempt
def update_chat_message(request):
    # Get the ChatMessage object to update
    chat_message = ChatMessage.objects.last()

    if request.method == 'POST':
        # If the form has been submitted, update the ChatMessage object with the form data
        chat_message.prompt = request.POST.get('prompt')
        chat_message.response = request.POST.get('response')
        chat_message.nonce = request.POST.get('nonce')
        chat_message.save()
        # return redirect('chat_message_detail', chat_message_id=chat_message.id)

    # Render the chat message update form with the existing data pre-populated
    form = {
        'prompt': chat_message.prompt,
        'response': chat_message.response,
        'nonce': chat_message.nonce,
    }

    return render(request, 'apichat/update_chat_message.html', {'form': form})



