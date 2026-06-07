from flask import Flask, request, render_template_string
from textblob import TextBlob

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Mental Health Chatbot</title>
    <style>
        body{
            font-family: Arial, sans-serif;
            background:#f4f4f4;
            padding:40px;
        }

        .container{
            max-width:700px;
            margin:auto;
            background:white;
            padding:20px;
            border-radius:10px;
            box-shadow:0px 0px 10px rgba(0,0,0,0.1);
        }

        h1{
            text-align:center;
            color:#333;
        }

        textarea{
            width:100%;
            height:120px;
            padding:10px;
            margin-top:10px;
        }

        button{
            margin-top:10px;
            padding:10px 20px;
            background:#007BFF;
            color:white;
            border:none;
            cursor:pointer;
            border-radius:5px;
        }

        .result{
            margin-top:20px;
            padding:15px;
            background:#eef;
            border-radius:5px;
        }
    </style>
</head>
<body>

<div class="container">
    <h1>AI Mental Health Chatbot</h1>

    <form method="POST">
        <textarea name="message"
        placeholder="How are you feeling today?"></textarea>

        <br>

        <button type="submit">
            Analyze Emotion
        </button>
    </form>

    {% if emotion %}
    <div class="result">
        <h3>Detected Emotion: {{ emotion }}</h3>
        <p>{{ response }}</p>
    </div>
    {% endif %}

</div>

</body>
</html>
"""

def detect_emotion(text):

    polarity = TextBlob(text).sentiment.polarity

    if polarity > 0.2:
        return "Happy"

    elif polarity < -0.2:
        return "Sad"

    return "Neutral"


def chatbot_response(emotion):

    responses = {
        "Happy":
        "That's wonderful to hear! Keep doing the things that bring you joy and positivity.",

        "Sad":
        "I'm sorry you're feeling this way. Consider talking with someone you trust and taking care of yourself today.",

        "Neutral":
        "Thank you for sharing. Would you like to tell me more about how your day is going?"
    }

    return responses[emotion]


@app.route("/", methods=["GET", "POST"])
def home():

    emotion = None
    response = None

    if request.method == "POST":

        message = request.form["message"]

        emotion = detect_emotion(message)

        response = chatbot_response(emotion)

    return render_template_string(
        HTML,
        emotion=emotion,
        response=response
    )


if __name__ == "__main__":
    app.run(debug=True)
