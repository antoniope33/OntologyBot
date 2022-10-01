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

    print(field_dict)

    # Si es uno de los intents finales hago la llamada a la API
    if (nombreIntent == "errorMitigationMechanism" or nombreIntent == "noTMS"):
        r = requests.post(base_url, data=field_dict)

        print(r.text)

        fulfillmentText = r.text

        return {
            "fulfillmentText": fulfillmentText,
            "source": "webhookdata"
        }
