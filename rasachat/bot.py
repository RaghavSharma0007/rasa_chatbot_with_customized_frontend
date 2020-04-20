from rasa_core.agent import Agent
from rasa_core.channels.socketio import SocketIOInput
from rasa_core.agent import Agent
from rasa_core.utils import EndpointConfig
# load your trained agent
action_endpoint = EndpointConfig(url="http://localhost:5055/webhook")
agent = Agent.load('models/dialogue', interpreter='models/current/nlu', action_endpoint=action_endpoint)

input_channel = SocketIOInput(
	# event name for messages sent from the user
	user_message_evt="user_uttered",
	
	# event name for messages sent from the bot
	bot_message_evt="bot_uttered",
	# socket.io namespace to use for the messages
	namespace=None
)

# set serve_forever=False if you want to keep the server running
s = agent.handle_channels([input_channel], 5500, serve_forever=True )

#@socketio.on('user_message_evt')
#def handle_message(message):
 #   emit('bot_message_evt', {"text": "hello"}, room=session_id)s
