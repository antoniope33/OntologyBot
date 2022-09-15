from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from typing import Optional, Text, Any, Dict

import requests

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
def consulta_api(dataField: FieldModel):

    r = requests.post(base_url, data=dataField.dict())

    return r.text
