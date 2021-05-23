from datetime import datetime

def simple_responses(input_text):
    user_message = str(input_text).lower()
    if user_message in ("hello", "hallo", "hi", "guten tag"):
        return "Hey, how are you?"
    elif user_message in ("who are you", "who are you?"):
        return "I am a daily informer bot!"
    elif user_message in ("time", "time?"):
        now = datetime.now()
        date_time = now.strftime("%d/%m/%y, %H:%M")
        return str(date_time)
    else:
        return "I don't understand you."

