import random 

def handle_response(message) -> str:
    p_message = 'hello'
    
    if p_message == 'hello':
        return 'Hey there!'
    
    if p_message == 'roll':
        return str(random.randint(1,6))
    
    if p_message == '!help':
        return "Help message bro."
    
    return "I don't know how to response to that shit"