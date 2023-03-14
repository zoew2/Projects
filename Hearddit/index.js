const Alexa = require('ask-sdk-core');
const Rekognition = require('./rekognition_utils.js');
const Reddit = require('./reddit_utils.js');
const rekognition = new Rekognition();
const reddit = new Reddit();

let lastPostID = 0;
let lastSpeechOutput = message.REPROMT;
const messages = {
    WELCOME: 'Welcome! What would you like to hear about from Reddit?',
    WELCOME_REPROMPT: 'You can ask me for a joke, a quote, a question, a secret, a meme, or a picture.',
    REPROMT: 'Would you like to hear something else?',
    POST_ERROR: 'Oops, there was an error getting posts from Reddit.',
    PICTURE_ERROR: 'Oops there\'s no picture in this post titled ',
    VOTE_SUBMITTED: 'Okay, your vote has been submitted.',
    VOTE_ERROR: 'Oops, there was an error submitting your vote.',
    LINK_ACCOUNT: 'You must have a Reddit account to vote on a post. Please use the Alexa app to link your Amazon account with your Reddit Account.',
    STOP: 'Goodbye!',
    ERROR: `Sorry, I couldn't understand what you said. Please try again.`
};

const LaunchRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'LaunchRequest';
    },
    handle(handlerInput) {
        lastSpeechOutput = messages.WELCOME;
        return handlerInput.responseBuilder
            .speak(messages.WELCOME)
            .reprompt(messages.WELCOME_REPROMPT)
            .getResponse();
    }
};

const VoteHandler = {
    canHandle(handlerInput) {
        let slots = handlerInput.requestEnvelope.request.intent.slots;
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'VoteIntent';
    },
    async handle(handlerInput){
        const accessToken = handlerInput.requestEnvelope.context.System.user.accessToken;

        if (accessToken === undefined) {
            lastSpeechOutput = messages.LINK_ACCOUNT;
            return handlerInput.responseBuilder
                .speak(messages.LINK_ACCOUNT)
                .withLinkAccountCard()
                .getResponse();
        }
        let slots = handlerInput.requestEnvelope.request.intent.slots;
        let direction = slots.subreddit.resolutions.resolutionsPerAuthority[0].values[0].value.id;

        const response = await reddit.vote(direction, accessToken);

        if (response.error) {
            lastSpeechOutput = messages.VOTE_ERROR;
            return handlerInput.responseBuilder
                .speak(messages.VOTE_ERROR)
                .reprompt(messages.REPROMT)
                .getResponse()
        }

        lastSpeechOutput = messages.VOTE_SUBMITTED;
        return handlerInput.responseBuilder
            .speak(messages.VOTE_SUBMITTED)
            .reprompt(messages.REPROMT)
            .getResponse();
    }
};
const PicturesIntentHandler = {
    canHandle(handlerInput) {
        let slots = handlerInput.requestEnvelope.request.intent.slots;
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'GetPostIntent'
            && (slots.subreddit.resolutions.resolutionsPerAuthority[0].values[0].value.id === "pics"
                || slots.subreddit.resolutions.resolutionsPerAuthority[0].values[0].value.id === "memes");
    },
    async handle(handlerInput) {

        let slots = handlerInput.requestEnvelope.request.intent.slots;
        let subreddit = slots.subreddit.resolutions.resolutionsPerAuthority[0].values[0].value.id;
        let sortBy = slots.sortby.value;

        const response = await reddit.getPosts(subreddit, sortBy);

        if (response.error) {
            lastSpeechOutput = messages.POST_ERROR;
            return handlerInput.responseBuilder
                .speak(messages.POST_ERROR)
                .reprompt(messages.REPROMT)
                .getResponse()
        }

        lastPostID = response.id;
        let picURL = response.url;
        let picTitle = response.title;

        if (!(picURL.endsWith(".jpg") || picURL.endsWith(".png"))) {
            lastSpeechOutput = messages.PICTURE_ERROR + picTitle;
            return handlerInput.responseBuilder
                .speak(messages.PICTURE_ERROR + picTitle)
                .reprompt(messages.REPROMT)
                .getResponse();
        }

        let url = picURL.slice(0, 4) + picURL.slice(5, picURL.length);
        let speechOutput = await rekognition.processImage(url, picTitle);

        lastSpeechOutput = speechOutput;
        return handlerInput.responseBuilder
            .speak(speechOutput)
            .reprompt(speechOutput)
            .getResponse();
    }
};
const JokesIntentHandler = {
    canHandle(handlerInput) {
        let slots = handlerInput.requestEnvelope.request.intent.slots;
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'GetPostIntent'
            && slots.subreddit.resolutions.resolutionsPerAuthority[0].values[0].value.id === "DadJokes";
    },
    async handle(handlerInput) {
        let slots = handlerInput.requestEnvelope.request.intent.slots;
        let subreddit = slots.subreddit.resolutions.resolutionsPerAuthority[0].values[0].value.id;
        let sortBy = slots.sortby.value;

        const response = await reddit.getPosts(subreddit, sortBy);

        if (response.error) {
            return handlerInput.responseBuilder
                .speak(messages.POST_ERROR)
                .reprompt(messages.REPROMT)
                .getResponse()
        }

        lastPostID = response.id;
        let jokeTitle = response.title;
        let jokeText = response.selftext;
        let speechOutput = jokeTitle + " <break time='1s'/> " + jokeText;

        lastSpeechOutput = speechOutput;
        return handlerInput.responseBuilder
            .speak(speechOutput)
            .reprompt(messages.REPROMT)
            .getResponse();
    },
};
const QuotesIntentHandler = {
    canHandle(handlerInput) {
        let slots = handlerInput.requestEnvelope.request.intent.slots;
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'GetPostIntent'
            && slots.subreddit.resolutions.resolutionsPerAuthority[0].values[0].value.id === "quotes";
    },
    async handle(handlerInput) {
        let slots = handlerInput.requestEnvelope.request.intent.slots;
        let subreddit = slots.subreddit.resolutions.resolutionsPerAuthority[0].values[0].value.id;
        let sortBy = slots.sortby.value;

        const response = await reddit.getPosts(subreddit, sortBy);

        if (response.error) {
            return handlerInput.responseBuilder
                .speak(messages.POST_ERROR)
                .reprompt(messages.REPROMT)
                .getResponse()
        }

        lastPostID = response.id;
        let quote = response.title;

        lastSpeechOutput = quote;
        return handlerInput.responseBuilder
            .speak(quote)
            .reprompt(messages.REPROMT)
            .getResponse();
    },
};
const QuestionIntentHandler = {
    canHandle(handlerInput) {
        let slots = handlerInput.requestEnvelope.request.intent.slots;
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'GetPostIntent'
            && slots.subreddit.resolutions.resolutionsPerAuthority[0].values[0].value.id === "AskReddit";
    },
    async handle(handlerInput) {
        let slots = handlerInput.requestEnvelope.request.intent.slots;
        let subreddit = slots.subreddit.resolutions.resolutionsPerAuthority[0].values[0].value.id;
        let sortBy = slots.sortby.value;

        const response = await reddit.getPosts(subreddit, sortBy);

        if (response.error) {
            return handlerInput.responseBuilder
                .speak(messages.POST_ERROR)
                .reprompt(messages.REPROMT)
                .getResponse()
        }

        lastPostID = response.id;
        let question = response.title;

        lastSpeechOutput = question;
        return handlerInput.responseBuilder
            .speak(question)
            .reprompt(messages.REPROMT)
            .getResponse();
    },
};
const SecretIntentHandler = {
    canHandle(handlerInput) {
        let slots = handlerInput.requestEnvelope.request.intent.slots;
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'GetPostIntent'
            && slots.subreddit.resolutions.resolutionsPerAuthority[0].values[0].value.id === "ShowerThoughts";
    },
    async handle(handlerInput) {
        let slots = handlerInput.requestEnvelope.request.intent.slots;
        let subreddit = slots.subreddit.resolutions.resolutionsPerAuthority[0].values[0].value.id;
        let sortBy = slots.sortby.value;

        const response = await reddit.getPosts(subreddit, sortBy);

        if (response.error) {
            lastSpeechOutput = messages.POST_ERROR;
            return handlerInput.responseBuilder
                .speak(messages.POST_ERROR)
                .reprompt(messages.REPROMT)
                .getResponse()
        }

        lastPostID = response.id;
        let secret = response.title;
        let speechOutput = '<amazon:effect name="whispered">' + secret + '</amazon:effect>';

        lastSpeechOutput = speechOutput;
        return handlerInput.responseBuilder
            .speak(speechOutput)
            .reprompt(messages.REPROMT)
            .getResponse();
    },
};

const RepeatIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'RepeatIntent'
    },
    handle(handlerInput) {
        return handlerInput.responseBuilder
            .speak(lastSpeechOutput)
            .reprompt(messages.REPROMT)
            .getResponse()
    }
};

const HelpIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && handlerInput.requestEnvelope.request.intent.name === 'AMAZON.HelpIntent';
    },
    handle(handlerInput) {
        lastSpeechOutput = messages.WELCOME_REPROMPT;
        return handlerInput.responseBuilder
            .speak(messages.WELCOME_REPROMPT)
            .reprompt(messages.WELCOME_REPROMPT)
            .getResponse();
    }
};

const CancelAndStopIntentHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest'
            && (handlerInput.requestEnvelope.request.intent.name === 'AMAZON.CancelIntent'
                || handlerInput.requestEnvelope.request.intent.name === 'AMAZON.StopIntent');
    },
    handle(handlerInput) {
        lastSpeechOutput = messages.STOP;
        return handlerInput.responseBuilder
            .speak(messages.STOP)
            .getResponse();
    }
};

const SessionEndedRequestHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'SessionEndedRequest';
    },
    handle(handlerInput) {
        // Any cleanup logic goes here.
        return handlerInput.responseBuilder.getResponse();
    }
};

// repeat the intent the user said for debugging
const IntentReflectorHandler = {
    canHandle(handlerInput) {
        return handlerInput.requestEnvelope.request.type === 'IntentRequest';
    },
    handle(handlerInput) {
        const intentName = handlerInput.requestEnvelope.request.intent.name;
        const speechText = `You just triggered ${intentName}`;

        console.log(JSON.stringify(handlerInput.requestEnvelope.request.intent));

        return handlerInput.responseBuilder
            .speak(speechText)
            .getResponse();
    }
};

// Generic error handling to capture any syntax or routing errors.
const ErrorHandler = {
    canHandle() {
        return true;
    },
    handle(handlerInput, error) {
        console.log(`~~~~ Error handled: ${error.message}`);

        lastSpeechOutput = messages.ERROR;
        return handlerInput.responseBuilder
            .speak(messages.ERROR)
            .reprompt(messages.ERROR)
            .getResponse();
    }
};

exports.handler = Alexa.SkillBuilders.custom()
    .addRequestHandlers(
        LaunchRequestHandler,
        VoteHandler,
        PicturesIntentHandler,
        JokesIntentHandler,
        QuotesIntentHandler,
        QuestionIntentHandler,
        SecretIntentHandler,
        HelpIntentHandler,
        CancelAndStopIntentHandler,
        SessionEndedRequestHandler,
        IntentReflectorHandler)
    .addErrorHandlers(
        ErrorHandler)
    .lambda();
