const AWS = require('aws-sdk');
const axios = require('axios');

let rekognition = new AWS.Rekognition();

class RekognitionUtils {

    static rekognizeLabels(imageData) {
        let params = {
            Image: {
                Bytes: imageData
            },
            MaxLabels: 3,
            MinConfidence: 80
        };

        return rekognition.detectLabels(params).promise()
    }

    static rekognizeFaces(imageData) {
        let params = {
            Attributes: ["ALL"],
            Image: {
                Bytes: imageData
            }
        };

        return rekognition.detectFaces(params).promise()
    }

    static rekognizeText(imageData) {
        let params = {
            Image: {
                Bytes: imageData
            }
        };

        return rekognition.detectText(params).promise()
    }

    static addLabelInfo(labelData, speechOutput) {
        let labels = [];
        let names = Object.keys(labelData.Labels);
        for (let i = 0; i < names.length; i++) {
            labels.push(labelData.Labels[names[i]].Name);
        }
        speechOutput += "The top three words I would use to describe this picture are ";
        speechOutput += labels[0] + ", " + labels[1] + " and " + labels[2] + ".";
        return speechOutput;
    }

    static addFaceInfo(faceData, speechOutput) {
        let confidentFaces = [];
        for (let i = 0; i < faceData.FaceDetails.length; i++) {
            if (faceData.FaceDetails[i].Confidence > 90) {
                confidentFaces.push(faceData.FaceDetails[i]);
            }
        }
        if (confidentFaces.length > 0) {
            speechOutput += " I see "
                + confidentFaces.length
                + " face"
                + (confidentFaces > 1 ? "s" : "")
                + " in this picture.  <break time='1s'/> ";
            speechOutput = RekognitionUtils.getFaceInfo(confidentFaces, speechOutput);
        } else {
            speechOutput += " I don't see any faces in this picture."
        }
        return speechOutput;
    }

    static addTextInfo(textData, speechOutput) {
        let isText = textData.TextDetections.length > 0;
        if (isText) {
            let message = [];
            for (let t = 0; t < textData.TextDetections.length; t++) {
                if (textData.TextDetections[t].Type === "WORD") {
                    message.push(textData.TextDetections[t].DetectedText);
                }
            }
            speechOutput += " Also, the picture says " + message.join(" ") + "."
        }
        return speechOutput;
    }

    static getTopEmotion(emotions) {
        let emotion = "";
        let bestEmotionScore = 0;
        for (let k = 0; k < emotions; k++) {
            if (emotions[k].Confidence > bestEmotionScore) {
                emotion = emotions[k].Type;
                bestEmotionScore = emotions[k].Confidence;
            }
        }
        return emotion;
    }

    static getFaceInfo(confidentFaces, speechOutput) {
        for (let j = 0; j < confidentFaces.length; j++) {
            let faceNum = j + 1;
            let lowAge = confidentFaces[j].AgeRange.Low;
            let highAge = confidentFaces[j].AgeRange.High;
            let gender = confidentFaces[j].Gender;

            let emotion = RekognitionUtils.getTopEmotion(confidentFaces[j].Emotions);
            let pronoun = gender.Value === "Female" ? " She" : " He";
            speechOutput += gender.Confidence < 90 ? " I'm not certain, but " : "";
            speechOutput += " Face number " + faceNum + " appears to be a " + emotion + " " + gender.Value;
            speechOutput += " between " + lowAge + " and " + highAge + ".";

            let smile = confidentFaces[j].Smile;
            let smileComment = pronoun + (Boolean(smile.Value) ? " is " : " isn't ") + " smiling.";
            speechOutput += smile.Confidence > 90 ? smileComment : "";

            let eyeglasses = confidentFaces[j].Eyeglasses;
            let glassesComment = pronoun + (Boolean(eyeglasses.Value) ? " is " : " isn't ") + " wearing glasses.";
            speechOutput += eyeglasses.Confidence > 90 ? glassesComment : "";

            let sunglasses = confidentFaces[j].Sunglasses;
            let sunglassesComment = pronoun + (Boolean(sunglasses.Value) ? " is " : " isn't ") + " wearing sunglasses.";
            speechOutput += sunglasses.Confidence > 90 ? sunglassesComment : "";

            let beard = confidentFaces[j].Beard;
            let beardComment = pronoun + (Boolean(beard.Value) ? " has " : " doesn't have ") + " a beard.";
            speechOutput += (beard.Confidence > 90 && gender.Value === "Male") ? beardComment : "";

            let mustache = confidentFaces[j].Mustache;
            let mustacheComment = pronoun + (Boolean(mustache.Value) ? " has " : " doesn't have ") + " a mustache.";
            speechOutput += (mustache.Confidence > 90 && gender.Value === "Male") ? mustacheComment : "";
        }
        return speechOutput;
    }

    async processImage(picURL, picTitle) {
        let speechOutput = "This picture is titled " + picTitle + ".   <break time=\'1s\'/> ";
        return await axios({
            method: 'GET',
            url,
            responseType: 'arraybuffer'
        }).then(response => {
            return RekognitionUtils.rekognizeLabels(response.data)
                .then(function (labelData) {
                    speechOutput = RekognitionUtils.addLabelInfo(labelData, speechOutput);
                    return RekognitionUtils.rekognizeFaces(response.data);
                }).then(function (faceData) {
                    speechOutput = RekognitionUtils.addFaceInfo(faceData, speechOutput);
                    return RekognitionUtils.rekognizeText(response.data);
                }).then(function (textData) {
                    speechOutput = RekognitionUtils.addTextInfo(textData, speechOutput);
                    return speechOutput
                }).catch(err => console.log(err));

        }).catch(err => console.log(err));
    }
}

module.exports = RekognitionUtils;