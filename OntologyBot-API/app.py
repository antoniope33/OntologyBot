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


app = FastAPI()


@app.get('/')
def read_root():
    return {"welcome": "Welcome to OntologyBot API",
            "author": "Mr. Antonio Pérez"}


@app.post('/consulta_api')
def query_ontology_api(dataField: FieldModel):

    r = requests.post(base_url, data=dataField.dict())

    return r.text


@app.post('/consulta_api_dialog')
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
    if nombreIntent == "Default Welcome Intent":
        for entidad in field_dict:
            field_dict[entidad] = ''

        fulfillmentText = "Hi, I'm the bot who will help you to know all about testing of machine learning IAs! Are you looking for Attack, Threat Mitigation Strategy or Testing Approach??"

    # OBTENGO LISTA OUTPUTCONTEXTS PARA OBTENER POSTERIORMENTE LOS PARAMETROS
    outputContexts = queryResult['outputContexts']

    # ACCEDO AL DICCIONARIO DE OUTPUTCONTEXTS
    outputContextsDict = outputContexts[0]

    # ACCEDO AL DICCIONARIO DE PARAMETROS SI EXISTE LA CLAVE (ALGUNOS INTENTS NO TIENEN PARAMETERS)
    if "parameters" in outputContextsDict:
        parameters = outputContextsDict['parameters']

    # ESTABLEZCO PRIMERO LOS PARAMETROS QUE NO TIENEN ENTIDADES EN DIALOGFLOW
    if nombreIntent == "datasetSUT":
        field_dict['dataset'] = parameters['any']

    elif nombreIntent == "vulnerability":
        field_dict['vulnerability'] = parameters['any']

    elif nombreIntent == "errorMitigationMechanism":
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

        fulfillmentText = r.text

    # RESPUESTA PARA CADA INTENT
    # Access
    if nombreIntent == 'access':
        fulfillmentText = "Nice, thanks! Now, do you want to answer some questions about the Threats"

    elif nombreIntent == 'adversarialCapability':
        fulfillmentText = "Very good! Now, tell me what is the adversarial goal of your system. Availability violation, Confidentiality violation, Integrity violation or Privacy violation?"

    elif nombreIntent == 'adversarialGoal':
        fulfillmentText = "All rigth! What is the adversarial strategy? Iterative strategy or One-shot strategy?"

    elif nombreIntent == 'adversarialKnowledge':
        fulfillmentText = "Okey! What is the adversarial capability? Pipeline, Model, Architecture, Parameters, Reading, Injection, Modification or Logic Corruption?"

    elif nombreIntent == 'adversarialStrategy':
        fulfillmentText = "Perfect, thanks! Now, do you answer some questions of the Threat Mitigation Strategy?"

    elif nombreIntent == 'datasetSUT':
        fulfillmentText = "Ok. Tell me the type of ML algorithm that trained the model of your system under test. Supervised Learning, Unsupervised Learning or Reinforcement Learning?"

    elif nombreIntent == 'dataTypeSUT':
        fulfillmentText = "Nice. Tell me the name of  the dataset used for training. For example, MINIST, ImageNet, IMDb Movie Reviews, etc."

    elif nombreIntent == 'defenseStrategy':
        fulfillmentText = "Nice! Finally, list or name error mitigations mechanism"

    elif nombreIntent == 'evaluationMechanism':
        fulfillmentText = "Okey! Tell me what type of defense strategy use your system. Proactive Defense or Reactive Defense?"

    elif nombreIntent == 'fault':
        fulfillmentText = "Nice, thanks! Do you want to answer some questions about the Testing Approach?"

    elif nombreIntent == "mlAlgorithmSUT":
        fulfillmentText = "Ok, thanks. Now, what is the model type of your system under test? Autoencoder, CNN, FFNN, RNN/LSTM, Other NN, Decision Tree, Linear Regresion, Multi-Layer Perceptron, Support Vector Machine or other?"

    elif nombreIntent == 'mlModelType':
        fulfillmentText = "Very nice! Tell me the way in which your system feature is accessed. Black-box access or White-box access?"

    elif nombreIntent == 'noAdversarialModel':
        fulfillmentText = "Got it! Do you want to answer some questions about the Threat Mitigation Strategy of your system under test?"

    elif nombreIntent == 'noSUT':
        fulfillmentText = "Ok, do you want to answer some questions about threats?"

    elif nombreIntent == 'noTesting':
        fulfillmentText = "Okey! Do you want to answer some questions about the Adversarial Model of your system?"

    elif nombreIntent == 'noThreats':
        fulfillmentText = "Ok, do you want to answer some questions about the Testing Approach?"

    elif nombreIntent == 'siAdversarialModel':
        fulfillmentText = "Perfect! What is the targeted phase of your system? Training or Testing/Inference?"

    elif nombreIntent == 'siSUT':
        fulfillmentText = "Nice! What is the task of your system under test? Classification, Clustering Analysis, Controlling and Scheming, Dimensionality Reduction or Regression?"

    elif nombreIntent == 'siTesting':
        fulfillmentText = "Nice! What is the verified requierement of your system under test? Functional Requirement, Performance Requirement, Safety Requirement or Security Requirement?"

    elif nombreIntent == 'siThreats':
        fulfillmentText = "Let's go! What is the threat type? Accidental Threat or Intentional Threat?"

    elif nombreIntent == 'siTMS':
        fulfillmentText = "Got it! What is the evaluation mechanism of your system under test? Holdout method, Cross-validation, k-fold cross-validation, Leave-one-out cross-validation or other?"

    elif nombreIntent == 'targetedPhase':
        fulfillmentText = "Good! What is the adversarial knowledge? Complete knowledge or Partial/Constrained knowledge?"

    elif nombreIntent == 'taskSUT':
        fulfillmentText = "Ok. What is the data type of your system under test? Numerical data, Categorical data, Time series data, Image, Audio or Text?"

    elif nombreIntent == 'testAdequacyMetric':
        fulfillmentText = "Good! Now, do you want to answer some questions about the Adversarial Model?"

    elif nombreIntent == 'testCaseGeneratorType':
        fulfillmentText = "Okey! What is the test adequacy metric? Coverage, Distance, Mutation score, other or none?"

    elif nombreIntent == 'testOracleType':
        fulfillmentText = "Thanks! What is the test case generator type? Adversarial Input Generator, Combinatorial Generator, Input Mutation Generator, Manual Generator, Random Generator or Search-based Generator?"

    elif nombreIntent == 'threatType':
        fulfillmentText = "Good! Now, list known vulnerabilities of your system."

    elif nombreIntent == 'verifiedRequirement':
        fulfillmentText = "Perfect! Now, what is the test oracle type of your system under test? Derived, Human, Implicit or Specified?"

    elif nombreIntent == 'vulnerability':
        fulfillmentText = "Good! What is the fault of your system under test? Misclassification, Underfitting, Overfitting, Bias, Negative side effects, Reward hacking or other?"

    elif nombreIntent == "Looking for Intent":
        fulfillmentText = "Great! Do you want to answer some questions about your system under test??"

    print(field_dict)

    return {
        "fulfillmentText": fulfillmentText,
        "source": "webhookdata"
    }
