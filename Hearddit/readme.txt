How to use Hearddit

Model JSON is included in the file model.json which can be pasted into the Alexa Developer Console.

The code for the endpoints is included in the file index.js. The code can be zipped and uploaded to an AWS Lambda Endpoint.
Code to include in the zipped folder:
    - index.js
    - reddit_utils.js
    - rekognition_utils.js
    - node_modules directory (not included here since this is mainly the Alexa Skills Kit and this branch is just my code samples)

To use the skill in the Alexa simulator:

    Start the skill by using the invocation name - "talking reddit"

    You can ask for any of the following: joke, quote, question, secret, picture, meme
    With any of the following sort criteria: top, hot, rising, new, controversial
        examples: "Tell me a joke", "Show me new pictures", "Ask me a controversial question"

    You can continue to ask for the same type of post or a new type.

    To exit you can say "Cancel", "Exit" or "Goodbye"
