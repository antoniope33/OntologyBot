from encodings import normalize_encoding
from os import system
from re import I
from urllib import request
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from typing import Optional, Text, Any, Dict
import requests
import json

##URL BASE PARA HACER LAS LLAMADAS A LA API DE ANNE##
base_url = "http://rationale.kereval.com/api/request/"

field_dict = {
    "question": "",

    # SUT
    "task": "",
    "data_type": "",
    "dataset": "",
    "model_type": "",
    "ml_method": "",
    "access": "",

    # THREAT
    "threat_type": "",
    "failure_type": "",
    "intentional_threat": "",
    "vulnerability": "",
    "fault": "",

    # TESTING APPROACH
    "verified_requirement": "",
    "security_req": "",
    "safety_req": "",
    "perf_metric": "",
    "safety_metric": "",
    "test_oracle_type": "",
    "specified_oracle": "",
    "derived_oracle": "",
    "test_case_generator": "",
    "test_adequacy": "",

    # ADVERSARIAL MODEL
    "targeted_phase": "",
    "adversarial_knowledge": "",
    "adversarial_capability": "",
    "adversarial_goal": "",
    "adversarial_strategy": "",

    # THREAT MITIGATION STRATEGY
    "evaluation_mechanism": "",
    "security_defense": "",
    "proactive_defense": "",
    "reactive_defense": "",
    "error_mitigation_mechanism": "",
}

# FIELD MODEL


class FieldModel(BaseModel):
    question: Text = ""

    # SUT
    task: Text = ""
    data_type: Text = ""
    dataset: Text = ""
    model_type: Text = ""
    ml_method: Text = ""
    access: Text = ""

    # THREAT
    threat_type: Text = ""
    failure_type: Text = ""
    intentional_threat: Text = ""
    vulnerability: Text = ""
    fault: Text = ""

    # TESTING APPROACH
    verified_requirement: Text = ""
    security_req: Text = ""
    safety_req: Text = ""
    perf_metric: Text = ""
    safety_metric: Text = ""
    test_oracle_type: Text = ""
    specified_oracle: Text = ""
    derived_oracle: Text = ""
    test_case_generator: Text = ""
    test_adequacy: Text = ""

    # ADVERSARIAL MODEL
    targeted_phase: Text = ""
    adversarial_knowledge: Text = ""
    adversarial_capability: Text = ""
    adversarial_goal: Text = ""
    adversarial_strategy: Text = ""

    # THREAT MITIGATION STRATEGY
    evaluation_mechanism: Text = ""
    security_defense: Text = ""
    proactive_defense: Text = ""
    reactive_defense: Text = ""
    error_mitigation_mechanism: Text = ""


app = FastAPI(
    title="OntologyBot API")


@app.get('/')
def read_root():
    return {"welcome": "Welcome to OntologyBot API",
            "author": "Mr. Antonio Pérez"}


@app.post('/query_ontology_api')
def query_ontology_api(dataField: FieldModel):

    r = requests.post(base_url, data=dataField.dict())

    return r.text


@app.post('/query_ontology_api_dialogflow')
def query_ontology_api_dialogflow(request: Dict[Any, Any]):

    # print(request)

    # CONVIERTO JSON A DICCIONARIO
    #diccionario = json.loads(request)

    # print(diccionario)

    # OBTENGO DICCIONARIO QUERYRESULT PARA OBTENER LA INFO
    queryResult = request['queryResult']

    # OBTENGO INFO INTENT
    intentInfo = queryResult['intent']

    # OBTENGO NOMBRE DEL INTENT
    nombreIntent = intentInfo['displayName']

    # SI ES EL DEFAULT WELCOME INTENT VACIO EL DICCIONARIO
    if nombreIntent == "useOntology":
        for entidad in field_dict:
            field_dict[entidad] = ''

        title = "Hi, I'm the bot who will help you to know all about testing of machine learning AIs! Are you looking for Attack, Threat Mitigation Strategy or Testing Approach??"
        quickReplies = [
            "Attack", "Threat Mitigation Strategy", "Testing Approach"]
        fulfillmentText = "Hi, I'm the bot who will help you to know all about testing of machine learning AIs! Are you looking for Attack, Threat Mitigation Strategy or Testing Approach??"

    elif nombreIntent == "Default Welcome Intent":
        for entidad in field_dict:
            field_dict[entidad] = ''

        return {"fulfillmentMessages": [
            {
                "card": {
                    "title": "Hello! What do you want to do?",
                    "buttons": [
                        {
                            "text": "Use ontology",
                            "postback": "Use ontology"
                        },
                        {
                            "text": "Help",
                            "postback": "Help"
                        },
                        {
                            "text": "Contact",
                            "postback": "Contact"
                        },
                        {
                            "text": "Bug",
                            "postback": "Error"
                        }
                    ]
                },
                "platform": "TELEGRAM"
            },
            {"quickReplies": {
                "quickReplies": ["New query"]
            },
                "platform": "TELEGRAM"}]}

    # OBTENGO LISTA OUTPUTCONTEXTS PARA OBTENER POSTERIORMENTE LOS PARAMETROS
    outputContexts = queryResult['outputContexts']

    # ACCEDO AL DICCIONARIO DE OUTPUTCONTEXTS
    outputContextsDict = outputContexts[0]

    # ACCEDO AL DICCIONARIO DE PARAMETROS SI EXISTE LA CLAVE (ALGUNOS INTENTS NO TIENEN PARAMETERS)
    if "parameters" in outputContextsDict:
        parameters = outputContextsDict['parameters']

    # ESTABLEZCO PRIMERO LOS PARAMETROS QUE NO TIENEN ENTIDADES EN DIALOGFLOW
    if nombreIntent == "datasetSUT":
        if (parameters['any'] == 'Skip' or parameters['any'] == 'skip'):
            field_dict['dataset'] = ""
        else:
            field_dict['dataset'] = parameters['any']

    elif nombreIntent == "vulnerability":
        if (parameters['any'] == 'Skip' or parameters['any'] == 'skip'):
            field_dict['vulnerability'] = ""
        else:
            field_dict['vulnerability'] = parameters['any']

    elif nombreIntent == "errorMitigationMechanism":
        if (parameters['any'] == 'Skip' or parameters['any'] == 'skip'):
            field_dict['error_mitigation_mechanism'] = ""
        else:
            field_dict['error_mitigation_mechanism'] = parameters['any']

    # RECORRO EL DICCIONARIO (ESTO ES PARA PONER LOS VALORES EN EL DICCIONARIO)
    if "parameters" in locals():
        for parametro in parameters:

            # RECORRO EL DICCIONARIO VACIO PARA HACER LA LLAMADA FINAL
            for entidad in field_dict:

                # SI COINCIDEN LAS CLAVES PONGO EL VALOR DEL JSON EN EL DICCIONARIO PARA LA LLAMADA
                if parametro == entidad:

                    # Si recibe skip lo deja vacio porque el usuario ha saltado la pregunta. Si no pone el valor
                    if parameters[parametro] == 'Skip':
                        field_dict[entidad] = ''
                    else:
                        field_dict[entidad] = parameters[parametro]

    # Si es uno de los intents finales hago la llamada a la API
    if (nombreIntent == "errorMitigationMechanism" or nombreIntent == "noTMS"):
        r = requests.post(base_url, data=field_dict)

        print(r.status_code)

        if r.status_code != 200:

            title = "Oops❗ :(\n\nThere was an error. Try again later"
            quickReplies = ["New query"]
            fulfillmentText = "Oops❗ :(\n\nThere was an error. Try again later"
        else:
            if r.text == '{}':
                title = "😕​ I have not been able to find an answer to your query. Please try again"
                quickReplies = ["New query"]
                fulfillmentText = "😕​ I have not been able to find an answer to your query. Please try again"
            else:

                # CONVIERTO RESPUESTA A DICCIONARIO
                dictResponse = json.loads(r.text)
                response = ""

                # RECORRO EL DICCIONARIO PARA OBTENER LOS VALORES
                for i in dictResponse:
                    value = dictResponse[i]

                    # NOMBRE
                    response = response + value[0] + ": "

                    # SI ESTÁ VACÍO MUESTRO QUE NO HAY INFO
                    if value[2] == "":
                        response = response + "No info\n\n"

                    # SI TIENE CONTENIDO LO MUESTRO
                    else:
                        response = response + value[2] + "\n\n"

                # RESPUESTA
                title = response
                quickReplies = ["New query"]
                fulfillmentText = response

    # RESPUESTA PARA CADA INTENT
    # Access
    if nombreIntent == 'access':
        title = "Nice, thanks! Now, It would be interesting if you answered the questions about the Threats"
        quickReplies = ["Yes", "No"]
        fulfillmentText = "Nice, thanks! Now, do you want to answer some questions about the Threats"

    elif nombreIntent == 'adversarialCapability':
        title = "Very good! Now, tell me what is the adversarial goal of your system. Availability violation, Confidentiality violation, Integrity violation or Privacy violation?"
        quickReplies = ["Availabilty",
                        "Confidentiality", "Integrity", "Privacy"]
        fulfillmentText = "Very good! Now, tell me what is the adversarial goal of your system. Availability violation, Confidentiality violation, Integrity violation or Privacy violation?"

    elif nombreIntent == 'adversarialGoal':
        title = "All rigth! What is the adversarial strategy? Iterative strategy or One-shot strategy?"
        quickReplies = ["Iterative", "One-shot"]
        fulfillmentText = "All rigth! What is the adversarial strategy? Iterative strategy or One-shot strategy?"

    elif nombreIntent == 'adversarialKnowledge':
        title = "Okey! What is the adversarial capability? Pipeline, Model, Architecture, Parameters, Reading, Injection, Modification or Logic Corruption?"
        quickReplies = ["Pipeline", "Model", "Architecture", "Parameters",
                        "Reading", "Injection", "Modification", "Logic Corruption"]
        fulfillmentText = "Okey! What is the adversarial capability? Pipeline, Model, Architecture, Parameters, Reading, Injection, Modification or Logic Corruption?"

    elif nombreIntent == 'adversarialStrategy':
        title = "Perfect, thanks! Now, do you answer some questions of the Threat Mitigation Strategy?"
        quickReplies = ["Yes", "No"]
        fulfillmentText = "Perfect, thanks! Now, do you answer some questions of the Threat Mitigation Strategy?"

    elif nombreIntent == 'datasetSUT':
        title = "Ok. Tell me the type of ML algorithm that trained the model of your system under test. Supervised Learning, Unsupervised Learning or Reinforcement Learning?"
        quickReplies = ["Supervised", "Unsupervised", "Reinforcement"]
        fulfillmentText = "Ok. Tell me the type of ML algorithm that trained the model of your system under test. Supervised Learning, Unsupervised Learning or Reinforcement Learning?"

    elif nombreIntent == 'dataTypeSUT':
        title = "Nice. Tell me the name of  the dataset used for training. For example, MINIST, ImageNet, IMDb Movie Reviews, etc."
        quickReplies = ["Skip"]
        fulfillmentText = "Nice. Tell me the name of  the dataset used for training. For example, MINIST, ImageNet, IMDb Movie Reviews, etc."

    elif nombreIntent == 'defenseStrategy':
        title = "Nice! Finally, list or name error mitigations mechanism"
        quickReplies = ["Skip"]
        fulfillmentText = "Nice! Finally, list or name error mitigations mechanism"

    elif nombreIntent == 'evaluationMechanism':
        title = "Okey! Tell me what type of defense strategy use your system. Proactive Defense or Reactive Defense?"
        quickReplies = ["Proactive", "Reactive"]
        fulfillmentText = "Okey! Tell me what type of defense strategy use your system. Proactive Defense or Reactive Defense?"

    elif nombreIntent == 'fault':
        title = "Nice, thanks! It would be interesting if you answered the questions about the Testing Approach"
        quickReplies = ["Yes", "No"]
        fulfillmentText = "Nice, thanks! Do you want to answer some questions about the Testing Approach?"

    elif nombreIntent == "mlAlgorithmSUT":
        title = "Ok, thanks. Now, what is the model type of your system under test? Autoencoder, CNN, FFNN, RNN/LSTM, Other NN, Decision Tree, Linear Regression, Multi-Layer Perceptron, Support Vector Machine or other?"
        quickReplies = ["Autoencoder", "CNN", "FFNN", "RNN/LSTM",
                        "Oter NN", "Decision Tree", "Regression", "Multi-Layer", "SVM", "Other"]
        fulfillmentText = "Ok, thanks. Now, what is the model type of your system under test? Autoencoder, CNN, FFNN, RNN/LSTM, Other NN, Decision Tree, Linear Regression, Multi-Layer Perceptron, Support Vector Machine or other?"

    elif nombreIntent == 'mlModelType':
        title = "Very nice! Tell me the way in which your system feature is accessed. Black-box access or White-box access?"
        quickReplies = ["Black-box", "White-box"]
        fulfillmentText = "Very nice! Tell me the way in which your system feature is accessed. Black-box access or White-box access?"

    elif nombreIntent == 'noAdversarialModel':
        title = "Got it! It would be interesting if you answered the questions about the Threat Mitigation Strategy of your system under test"
        quickReplies = ["Yes", "No"]
        fulfillmentText = "Got it! Do you want to answer some questions about the Threat Mitigation Strategy of your system under test?"

    elif nombreIntent == 'noSUT':
        title = "Ok, It would be interesting if you answered the questions about the Threats"
        quickReplies = ["Yes", "No"]
        fulfillmentText = "Ok, do you want to answer some questions about the Threats?"

    elif nombreIntent == 'noTesting':
        title = "Okey! It would be interesting if you answered the questions about the Adversarial Model of your system"
        quickReplies = ["Yes", "No"]
        fulfillmentText = "Okey! Do you want to answer some questions about the Adversarial Model of your system?"

    elif nombreIntent == 'noThreats':
        title = "Ok, It would be interesting if you answered the questions about the Testing Approach"
        quickReplies = ["Yes", "No"]
        fulfillmentText = "Ok, do you want to answer some questions about the Testing Approach?"

    elif nombreIntent == 'siAdversarialModel':
        title = "Perfect! What is the targeted phase of your system? Training or Testing/Inference?"
        quickReplies = ["Training", "Testing/Interference"]
        fulfillmentText = "Perfect! What is the targeted phase of your system? Training or Testing/Inference?"

    elif nombreIntent == 'siSUT':
        title = "Nice! What is the task of your system under test? Classification, Clustering Analysis, Controlling and Scheming, Dimensionality Reduction or Regression?"
        quickReplies = ["Classification", "Clustering",
                        "Controlling and Scheming", "Reduction", "Regression"]
        fulfillmentText = "Nice! What is the task of your system under test? Classification, Clustering Analysis, Controlling and Scheming, Dimensionality Reduction or Regression?"

    elif nombreIntent == 'siTesting':
        title = "Nice! What is the verified requirement of your system under test? Functional Requirement, Performance Requirement, Safety Requirement or Security Requirement?"
        quickReplies = ["Functional", "Performance", "Safety", "Security"]
        fulfillmentText = "Nice! What is the verified requirement of your system under test? Functional Requirement, Performance Requirement, Safety Requirement or Security Requirement?"

    elif nombreIntent == 'siThreats':
        title = "Let's go! What is the threat type? Accidental Threat or Intentional Threat?"
        quickReplies = ["Accidental", "Intentional"]
        fulfillmentText = "Let's go! What is the threat type? Accidental Threat or Intentional Threat?"

    elif nombreIntent == 'siTMS':
        title = "Got it! What is the evaluation mechanism of your system under test? Holdout method, Cross-validation, k-fold cross-validation, Leave-one-out cross-validation or other?"
        quickReplies = ["Holdout", "Cross-validation",
                        "k-fold", "Leave-one-out", "Other"]
        fulfillmentText = "Got it! What is the evaluation mechanism of your system under test? Holdout method, Cross-validation, k-fold cross-validation, Leave-one-out cross-validation or other?"

    elif nombreIntent == 'targetedPhase':
        title = "Good! What is the adversarial knowledge? Complete knowledge or Partial/Constrained knowledge?"
        quickReplies = ["Complete", "Partial/Constrained"]
        fulfillmentText = "Good! What is the adversarial knowledge? Complete knowledge or Partial/Constrained knowledge?"

    elif nombreIntent == 'taskSUT':
        title = "Ok. What is the data type of your system under test? Numerical data, Categorical data, Time series data, Image, Audio or Text?"
        quickReplies = ["Numerical", "Categorical",
                        "Time series", "Image", "Audio", "Text"]
        fulfillmentText = "Ok. What is the data type of your system under test? Numerical data, Categorical data, Time series data, Image, Audio or Text?"

    elif nombreIntent == 'testAdequacyMetric':
        title = "Good! Now, it would be interesting if you answered the questions about the Adversarial Model"
        quickReplies = ["Yes", "No"]
        fulfillmentText = "Good! Now, do you want to answer some questions about the Adversarial Model?"

    elif nombreIntent == 'testCaseGeneratorType':
        title = "Okey! What is the test adequacy metric? Coverage, Distance, Mutation score, other or none?"
        quickReplies = ["Coverage", "Distance", "Mutation", "Other", "None"]
        fulfillmentText = "Okey! What is the test adequacy metric? Coverage, Distance, Mutation score, other or none?"

    elif nombreIntent == 'testOracleType':
        title = "Thanks! What is the test case generator type? Adversarial Input Generator, Combinatorial Generator, Input Mutation Generator, Manual Generator, Random Generator or Search-based Generator?"
        quickReplies = ["Adversarial", "Combinatorial",
                        "Input Mutation", "Manual", "Random", "Search-based"]
        fulfillmentText = "Thanks! What is the test case generator type? Adversarial Input Generator, Combinatorial Generator, Input Mutation Generator, Manual Generator, Random Generator or Search-based Generator?"

    elif nombreIntent == 'threatType':
        title = "Good! Now, list known vulnerabilities of your system."
        quickReplies = ["Skip"]
        fulfillmentText = "Good! Now, list known vulnerabilities of your system."

    elif nombreIntent == 'verifiedRequirement':
        title = "Perfect! Now, what is the test oracle type of your system under test? Derived, Human, Implicit or Specified?"
        quickReplies = ["Derived", "Human", "Implicit", "Specified"]
        fulfillmentText = "Perfect! Now, what is the test oracle type of your system under test? Derived, Human, Implicit or Specified?"

    elif nombreIntent == 'vulnerability':
        title = "Good! What is the fault of your system under test? Misclassification, Underfitting, Overfitting, Bias, Negative side effects, Reward hacking or other?"
        quickReplies = ["Missclassification", "Underfitting", "Overfitting",
                        "Bias", "Negative side effects", "Reward hacking", "Other"]
        fulfillmentText = "Good! What is the fault of your system under test? Misclassification, Underfitting, Overfitting, Bias, Negative side effects, Reward hacking or other?"

    elif nombreIntent == "Looking for Intent":
        title = "Great! It would be interesting if you answered the questions about your system under test"
        quickReplies = ["Yes", "No"]
        fulfillmentText = "Great! Do you want to answer some questions about your system under test??"

    elif nombreIntent == "help":
        title = "Here you have the help you need to talk with me:\n\n💬 𝐔𝐬𝐞 𝐨𝐧𝐭𝐨𝐥𝐨𝐠𝐲: To use the ontology you only have to write 'Hi', 'Use ontology' or 'New query' and answer the questions that I will ask you\n\n​📧​​ 𝐂𝐨𝐧𝐭𝐚𝐜𝐭: If you want to know the contact information you just have to write 'Contact' and I will show you all information\n\n⚠️ 𝐄𝐫𝐫𝐨𝐫: If you want to report some error you just have to write 'Report error' or 'Error' and I will show how you can report it\n\n🆘​ 𝐇𝐞𝐥𝐩: If you want to consult this information you just have to write 'Help' and I will show it you\n\n⁉️​ 𝐔𝐬𝐞𝐟𝐮𝐥 𝐜𝐨𝐧𝐜𝐞𝐩𝐭𝐬: For information about the concepts of the questions see this link http://rationale.kereval.com"
        quickReplies = ["New query"]
        fulfillmentText = "Here you have the help you need to talk with me:\n\n💬 𝐔𝐬𝐞 𝐨𝐧𝐭𝐨𝐥𝐨𝐠𝐲: To use the ontology you only have to write 'Hi', 'Use ontology' or 'New query' and answer the questions that I will ask you\n\n​📧​ 𝐂𝐨𝐧𝐭𝐚𝐜𝐭: If you want to know the contact information you just have to write 'Contact' and I will show you all information\n\n⚠️ 𝐄𝐫𝐫𝐨𝐫: If you want to report some error you just have to write 'Report error' or 'Error' and I will show how you can report it\n\n🆘​ 𝐇𝐞𝐥𝐩: If you want to consult this information you just have to write 'Help' and I will show it you\n\n⁉️​ 𝐔𝐬𝐞𝐟𝐮𝐥 𝐜𝐨𝐧𝐜𝐞𝐩𝐭𝐬: For information about the concepts of the questions see this link http://rationale.kereval.com"

    elif nombreIntent == "contact":
        title = "Here you have all contact information:\n\nYou can contact us to give feedback or to contribute.\n\n🤝​ If you want to 𝐜𝐨𝐧𝐭𝐫𝐢𝐛𝐮𝐭𝐞, write to this email address (ontology.cotribute@gmail.com) indicating the type of component in the subject and explain this component in the body\n\n🤔 If you want to give 𝐟𝐞𝐞𝐝𝐛𝐚𝐜𝐤, you can write to this email address (ontology.feedback@gmail.com) whatever you want\n\nThank you for contacting us ❤️!"
        quickReplies = ["New query"]
        fulfillmentText = "Here you have all contact information:\n\nYou can contact us to give feedback or to contribute.\n\n🤝​ If you want to 𝐜𝐨𝐧𝐭𝐫𝐢𝐛𝐮𝐭𝐞, write to this email address (ontology.cotribute@gmail.com) indicating the type of component in the subject and explain this component in the body\n\n🤔 If you want to give 𝐟𝐞𝐞𝐝𝐛𝐚𝐜𝐤, you can write to this email address (ontology.feedback@gmail.com) whatever you want\n\nThank you for contacting us ❤️!"

    elif nombreIntent == "errorReport":
        title = "𝗢𝗼𝗽𝘀❗ :(\n\nIf you have found an error about me, you can write to this email address and explain to my creators what is wrong. Thanks for helping me!\n\n📧 𝐄𝐦𝐚𝐢𝐥 𝐚𝐝𝐝𝐫𝐞𝐬𝐬: ontologybot.error@gmail.com"
        quickReplies = ["New query"]
        fulfillmentText = "𝗢𝗼𝗽𝘀❗ :(\n\nIf you have found an error about me, you can write to this email address and explain to my creators what is wrong. Thanks for helping me!\n\n📧 𝐄𝐦𝐚𝐢𝐥 𝐚𝐝𝐝𝐫𝐞𝐬𝐬: ontologybot.error@gmail.com"

    print(field_dict)

    return {"fulfillmentText": fulfillmentText,
            "fulfillmentMessages": [{"quickReplies": {
                "title": title,
                "quickReplies": quickReplies
            },
                "platform": "TELEGRAM"}]
            }
