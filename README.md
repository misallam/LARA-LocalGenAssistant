# LARA-LocalGenAssistant
LARA, the Local Arabic Retrieval Augmented Generation Assistant, transforms Arabic data processing with RAG, localized Text2Speech, and Text Generation using Gemma CPP multilingual models, enhancing accessibility and creation for Arabic-speaking communities.

# Installation Guide

### Clone the repo
```shell
git clone https://github.com/misallam/LARA-LocalGenAssistant.git
``` 

### Create Python Environment
```shell
conda create lara python==3.12.2
```

### Activate the environment
```shell
conda activate lara
```

### Install the requirments
```shell
pip install -r requirements.txt
```

### Change the keys in the .env file to include the secret keys of OpenAI & Elevenlabs if you are working with Third-Parties.
```python
ELEVEN_LAPS_KEY = <ELEVEN_LAPS_KEY>
OPEN_AI_API_KEY = <OPEN_AI_API_KEY>
```

### Run the following docker command

```shell
#CHANGE <LARA\store> => to the store location in your hard disk
docker run -p 8000:8000 -e CHROMA_SERVER_AUTH_CREDENTIALS_PROVIDER="chromadb.auth.token.TokenConfigServerAuthCredentialsProvider" -e CHROMA_SERVER_AUTH_PROVIDER="chromadb.auth.token.TokenAuthServerProvider" -e CHROMA_SERVER_AUTH_CREDENTIALS="zed@12345678" -e CHROMA_SERVER_AUTH_TOKEN_TRANSPORT_HEADER="X_CHROMA_TOKEN" -v <LARA\store>:/chroma/chroma -d chromadb/chroma
```

### Download MPV for streaming and put it in the program files
```shell
https://sourceforge.net/projects/mpv-player-windows/
```

### Finally Start the app
```shell
uvicorn main:app --port 8080
```

### You can find PostMan APIs documentation via 
``` shell
https://www.postman.com/satellite-geoscientist-95548148/workspace/lara/collection/33188959-17e24558-26fe-4408-9681-29fa9b17ceb7?action=share&creator=33188959
```
