# OntologyBot

OntologyBot is a bot to query an ontology on how to test machine learning AIs.

## Installation

1.- Install [Python 3.10.4](https://www.python.org/downloads/release/python-3104/) with the .exe file that you can download from their web page.

2.- Install [Anaconda](https://www.anaconda.com/). More info in their web page.

3.- Create an virtual environment:

```bash
$ create –name ENVIRONMENT_NAME python=3
```

4.- To activate the virtual environment use:

```bash
$ conda activate ENVIRONMENT_NAME
```

5.- To deactivate the virtual environment use:

```bash
$ conda deactivate
```

6.- Install requirements.txt in your virtual environment:

```bash
$ pip install -r requirements.txt
```

7.- Create an account on [Ngrok](https://ngrok.com/) and install it downloading the .zip file from their web page and unzipping it in the "Program files" directory.

8.- To configure Ngrok go to the installation directory and type in a Windows shell:

```bash
$ ngrok config add-authtoken TOKEN
```

## Deploy API

1.- First, deploy API in localhost:

```bash
$ uvicorn app:app
```

If you want to activate automatic reloading use:

```bash
$ uvicorn app:app --reload
```

2.- Then, deploy API with Ngrok:

```bash
$ ngrok http LOCALHOST_PORT
```

3.- API will have been deployed

## License
MIT License

Copyright (c) [2022] [Antonio Pérez Vázquez]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
