# -*- coding: utf-8 -*-
"""Internship.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Z9a2mNgRxeZ7qpqs9B2HERWtyAu7jJOG
"""

import nltk
import re
import numpy as np
import json

# Check if 'punkt' is already installed
if not nltk.download('punkt', quiet=True):
    print("'punkt' is already installed.")

# Text Preprocessing
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    tokens = nltk.word_tokenize(text)
    return tokens

# Read data from file
with open('/content/drive/MyDrive/human_chat.txt', 'r') as file:
    # Read the contents of the file
    contents = file.read()

# Split the contents into sentences
data = contents.split('\n')

# Preprocess each sentence
preprocessed_data = [preprocess_text(sentence) for sentence in data if sentence.strip()]

intents = {
    "greeting": ["hi", "hello", "hey"],
    "question": ["what", "which", "do", "how"],
    "statement": ["one", "hard", "i", "not", "yea", "i", "wow", "there", "so", "my", "thats", "should", "cool"],
    "appreciation": ["thank", "thanks", "appreciate", "grateful", "gratitude"],
    "farewell": ["goodbye", "bye", "see you", "farewell"],
    "agreement": ["yes", "yeah", "definitely", "absolutely", "agree"],
    "disagreement": ["no", "not really", "disagree", "not sure"],
    "request": ["please", "could you", "would you mind", "can you"],
    "confusion": ["confused", "uncertain", "not understand", "explain"],
    "excitement": ["awesome", "amazing", "fantastic", "exciting"],
    "concern": ["worried", "concerned", "anxious", "troubled"],
    "interest": ["curious", "interested", "intrigued", "want to know"],
    "clarification": ["clarify", "explain", "elaborate", "details"],
    "acknowledgment": ["got it", "understood", "acknowledge", "gotcha"],
    "negation": ["nope", "nah", "not really", "not exactly"],
    "affirmation": ["yes", "yeah", "yep", "absolutely", "indeed"],
    "invitation": ["join", "come over", "attend", "participate"],
    "suggestion": ["suggest", "recommend", "advice", "propose"],
    "confirmation": ["confirm", "verification", "validate", "verify"],
    "denial": ["deny", "refuse", "reject", "decline"],
    "acceptance": ["yes", "okay", "sure", "alright"],
    "reject": ["no", "not", "decline", "refuse"],
    "apology": ["sorry", "apologize", "regret", "forgive"],
    "thanks": ["thank you", "thanks a lot", "much appreciated", "grateful"],
    "encouragement": ["you can do it", "keep going", "don't give up", "stay strong"],
    "disbelief": ["really?", "are you serious?", "you can't be serious", "no way"],
    "surprise": ["wow", "unbelievable", "no way", "really?"],
    "compliment": ["good job", "well done", "great work", "awesome"],
    "regret": ["wish", "regret", "if only", "should have"],
    "blame": ["your fault", "you did this", "because of you", "you caused this"],
    "request for information": ["can you tell me", "I need to know", "what is", "where can I find"],
    "disappointment": ["disappointed", "let down", "not what I expected", "upset"],
    "suspicion": ["suspicious", "doubt", "not sure about", "questionable"],
    "shock": ["shocked", "stunned", "can't believe", "speechless"],
    "comfort": ["it's okay", "don't worry", "I'm here for you", "it'll be alright"],
    "humor": ["that's funny", "lol", "haha", "you're hilarious"],
    "encouragement to try": ["give it a try", "go for it", "take a chance", "try it out"],
    "confirmation of understanding": ["I see", "understood", "got it", "makes sense"],
    "disinterest": ["not interested", "don't care", "whatever", "meh"],
    "preference": ["prefer", "like better", "would rather", "favorite"],
    "excuse": ["because", "since", "due to", "the reason is"],
    "realization": ["I see", "now I understand", "that makes sense", "aha"],
    "hypothetical": ["if", "suppose", "imagine", "what if"],
    "contradiction": ["however", "but", "on the contrary", "although"],
    "willingness": ["willing", "happy to", "glad to", "prepared to"],
    "reluctance": ["reluctant", "hesitant", "not sure about", "unwilling"],
    "inquiry": ["question", "ask", "wonder", "inquire"],
    "permission": ["may I", "can I", "is it okay", "do you mind if"],
    "instruction": ["please", "you should", "it’s best to", "I recommend"],
    "condition": ["if", "provided that", "on the condition that", "as long as"],
    "comparison": ["more than", "less than", "better than", "worse than"],
    "reason": ["because", "since", "as", "due to"],
    "encouragement to stop": ["stop", "don't", "cease", "give up"],
    "motivation": ["you can do it", "keep going", "don't give up", "stay strong"]
}


responses = {
    "greeting": ["Hello! How can I assist you today?", "Hi there! How are you?"],
    "question": ["Can you please clarify your question?", "That's an interesting question!", "I'm not sure, can you tell me more?"],
    "statement": ["I see. Can you elaborate?", "That's fascinating!", "Wow, that's interesting!"],
    "appreciation": ["You're welcome! Is there anything else I can help you with?", "Glad I could assist! Let me know if there's anything else you need."],
    "farewell": ["Goodbye! Have a great day!", "Until next time! Take care!"],
    "agreement": ["I completely agree with you!", "That's spot on!"],
    "disagreement": ["I respectfully disagree.", "I see your point, but I have a different perspective."],
    "request": ["Sure thing! What would you like me to do?", "Of course, how can I assist you?"],
    "confusion": ["I'm a bit confused. Could you provide more context?", "I'm not sure I follow. Can you explain that again?"],
    "excitement": ["That's amazing! Tell me more!", "Wow, that's fantastic news!"],
    "concern": ["I understand your concern. Let's see how we can address it.", "I hear you. Let's figure this out together."],
    "interest": ["I'm intrigued! Tell me all about it.", "That sounds interesting! Could you share more details?"],
    "clarification": ["Sure, I'd be happy to clarify. What specifically would you like to know?", "Of course! Let me provide some clarification."],
    "acknowledgment": ["Got it!", "Understood!", "Acknowledged!"],
    "negation": ["No problem.", "That's okay.", "Noted."],
    "affirmation": ["Absolutely!", "Indeed!", "Yes, that's correct."],
    "invitation": ["We'd love to have you join us!", "Sure, you're welcome to come over!", "You're invited to attend!"],
    "suggestion": ["I suggest you try...", "How about...", "My advice would be to..."],
    "confirmation": ["Confirmed!", "Verification successful!", "Yes, that's verified."],
    "denial": ["I'm sorry, but I can't comply with that request.", "I'm afraid I have to decline.", "I must refuse that proposition."],
    "acceptance": ["Great!", "Okay, let's proceed.", "Sure thing!"],
    "reject": ["I'm sorry, but I can't comply with that request.", "I must respectfully decline.", "Unfortunately, I cannot agree to that."],
    "apology": ["I'm sorry for any inconvenience caused.", "My apologies for the confusion.", "I apologize for the misunderstanding."],
    "thanks": ["You're welcome!", "No problem at all!", "It was my pleasure to assist!"],
    "encouragement": ["You can do it!", "Keep going!", "Don't give up!"],
    "disbelief": ["Really?", "Are you serious?", "You can't be serious."],
    "surprise": ["Wow!", "Unbelievable!", "Really?"],
    "compliment": ["Good job!", "Well done!", "Great work!"],
    "regret": ["I wish it was different.", "I regret that.", "If only things were different."],
    "blame": ["It's your fault.", "You did this.", "Because of you."],
    "request for information": ["Can you tell me more?", "I need to know more details.", "Where can I find this information?"],
    "disappointment": ["I'm disappointed.", "You let me down.", "Not what I expected."],
    "suspicion": ["I'm suspicious.", "I doubt it.", "Not sure about this."],
    "shock": ["I'm shocked!", "I can't believe it!", "Speechless!"],
    "comfort": ["It's okay.", "Don't worry.", "I'm here for you."],
    "humor": ["That's funny!", "LOL!", "You're hilarious!"],
    "encouragement to try": ["Give it a try.", "Go for it!", "Take a chance."],
    "confirmation of understanding": ["I see.", "Understood.", "Makes sense."],
  "disinterest": ["I'm not interested.", "I don't care.", "Whatever."],
  "preference": ["I prefer this.", "I like this better.", "I would rather do this."],
  "excuse": ["Because of that.", "Since this happened.", "Due to these reasons."],
  "realization": ["I see now.", "Now I understand.", "That makes sense."],
  "hypothetical": ["If that's the case.", "Suppose we did this.", "Imagine that happened."],
  "contradiction": ["However, this is different.", "But that's not the case.", "On the contrary."],
  "willingness": ["I'm willing to do that.", "Happy to help.", "I'm prepared for that."],
  "reluctance": ["I'm reluctant to agree.", "I'm hesitant about that.", "Not sure I can do that."],
  "inquiry": ["I have a question.", "I wonder about this.", "Can you explain this?"],
  "permission": ["May I do this?", "Can I go?", "Is it okay if I do this?"],
  "instruction": ["Please follow this.", "You should do this.", "It’s best to try this."],
  "condition": ["If you do this.", "Provided that this happens.", "On the condition that."],
  "comparison": ["This is better than that.", "This is worse than the other.", "More than this, less than that."],
  "reason": ["Because of this.", "Since this is the case.", "Due to these circumstances."],
  "encouragement to stop": ["Stop that.", "Don't do that.", "Cease this activity."],
  "motivation": ["You can do it!", "Keep going!", "Don't give up!", "Stay strong!"]
    # Add more responses for each intent here
}

def recognize_intent(tokens):
    for token in tokens:
        for intent, keywords in intents.items():
            if token in keywords:
                return intent
    return "unknown"

def generate_response(intent):
    if intent in responses:
        return np.random.choice(responses[intent])
    else:
        return "I'm sorry, I didn't understand that."

def log_interaction(user_input, tokens, intent, response, feedback=None):
    interaction = {
        "user_input": user_input,
        "tokens": tokens,
        "intent": intent,
        "response": response,
        "feedback": feedback
    }
    with open("/content/drive/MyDrive/logs.json", "a") as log_file:
        log_file.write(json.dumps(interaction) + "\n")

def load_logs():
    interactions = []
    try:
        with open("logs.json", "r") as log_file:
            for line in log_file:
                interactions.append(json.loads(line))
    except FileNotFoundError:
        pass
    return interactions

def update_model_from_logs():
    interactions = load_logs()
    feedback_counts = {}

    for interaction in interactions:
        intent = interaction["intent"]
        feedback = interaction["feedback"]
        if feedback == "no":
            if intent not in feedback_counts:
                feedback_counts[intent] = 0
            feedback_counts[intent] += 1

    for intent, count in feedback_counts.items():
        print(f"Intent '{intent}' had {count} negative feedback(s). Consider updating the model.")

# Simple text-based interaction with learning mechanism
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Chatbot: Okay, Goodbye!")
        break

    tokens = preprocess_text(user_input)
    intent = recognize_intent(tokens)
    response = generate_response(intent)

    print(f"Chatbot: {response}")

    feedback = input("Was this response helpful? (yes/no): ").strip().lower()
    log_interaction(user_input, tokens, intent, response, feedback)

    if feedback == "no":
        # Potentially ask for more details and refine response/intents
        print("Chatbot: I'm sorry about that. How can I improve?")

    # Periodically update the model (for simplicity, we call it every time here)
    update_model_from_logs()

from google.colab import drive
drive.mount('/content/drive')