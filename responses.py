import random 

def handle_response(message) -> str:
    
    if message == 'hello':
        return 'Hey there!'
    
    if message == 'roll':
        return str(random.randint(1,1000))
    
    if message == '!help':
        return "Help message bro."
    
    return message