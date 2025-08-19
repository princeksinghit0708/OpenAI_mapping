import os
import subprocess
from openai import AzureOpenAI, OpenAI
from google.oauth2.credentials import Credentials

# Optional imports for Google Cloud services
try:
    from vertexai.generative_models import GenerativeModel
    import vertexai
    VERTEX_AI_AVAILABLE = True
except ImportError:
    VERTEX_AI_AVAILABLE = False
    GenerativeModel = None
    vertexai = None

import dotenv

import logging

from typing import List, Union, Generator, Any

import json

import dotenv

from pymongo import MongoClient

import sys

from anthropic import AnthropicVertex

import httpx

http_client = httpx.Client()

# Centralized configuration

HTTP_PROXY = os.getenv("HTTP_PROXY", "")

HTTPS_PROXY = os.getenv("HTTPS_PROXY", "")

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

# Make BASE_URL optional for demo purposes
if not BASE_URL:
    BASE_URL = "http://localhost:8000"

os.environ["HTTP_PROXY"] = HTTP_PROXY

os.environ["HTTPS_PROXY"] = HTTPS_PROXY

# Constants

AZURE_API_VERSION = "2023-05-15"

VERTEX_PROJECT = "prj-gen-ai-9571"

# Configure logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_token_from_mongo():

    mongo_user = os.getenv('DEV_MONGO_USER')
    mongo_key = os.getenv('DEV_MONGO_KEY')

    mongo_url = f'mongodb://{mongo_user}:{mongo_key}@maas-mw-d284-u2090.nam.nsroot.net:37017/?authSource=admin&readPreference=primary&tls=true&tlsInsecure-true'

    client = MongoClient(mongo_url)

    db = client['AI_POC']

    collection = db["token"]

    """

    Retrieve the token from MongoDB.

    Returns:

    str: The authentication token if found, None otherwise.

    """

    token_doc = collection.find_one({"_id": "coin_token"})

    if token_doc and "token" in token_doc:

        return token_doc["token"]

    return None

# print(get_token_from_mongo()) # Debugging line to check token retrieval

# exit()

def get_coin_token() -> str:

    """

Retrieve the authentication token using a shell command.

Returns:

    str: The authentication token if found, None otherwise.
    """

    command = "helix auth access-token print -a"

    try:

        result = subprocess.check_output(command, shell=True)

        return result.decode().strip()

    except subprocess.CalledProcessError as e:

            logging.error("Failed to retrieve token: %s", e)

            raise RuntimeError("Failed to retrieve token. Ensure 'helix' is installed and configured.")

class LLMService:
    """

Unified class for handling OpenAI, Gemini, Stellar, and Anthropic streaming services.

    """

    def __init__(self):
        """


        Initialize the LLMService with necessary endpoints and project details.
        """

        self.openai_url = f"{BASE_URL}/azure"

        self.stellar_url = f"{BASE_URL}/stellar/v1"

        self.gemini_url = f"{BASE_URL}/vertex"

        self.claude_url = f"{BASE_URL}/vertex/v1/"



    def _get_fresh_token(self) -> str:  # noqa: N802
        """
        Get a fresh token from the MongoDB database.

        Returns:
            str: The authentication token if found, None otherwise.
        """
        return get_coin_token()

    def output(
        self,
        client: Any,
        model: str,
        messages: List[dict],
        temperature: float = 0.2,
        is_gemini: bool = False,
        stream: bool = False,
        raw_response: bool = False,
    ) -> Union[str, Generator[str, None, None]]:
        """
        Generic method to handle streaming and non-streaming responses from different clients.

        Args:
            client (Any): The client instance (AzureOpenAI, OpenAI, or GenerativeModel).
            model (str): The model to use for chat completion.
            messages (List[dict]): List of messages to send to the model. 
            temperature (float, optional): Sampling temperature. Defaults to False
            stream (bool, optional): Whether to stream the response. Defaults to True.

        Returns:
            Union[str, Generator[str, None, None]]: The response from the model.
        """
        # Validate messages
        if not messages or not isinstance(messages, list) or not all("role" in msg and "content" in msg for msg in messages):
            raise ValueError("Invalid 'messages.' parameter: Each message must contain 'role' and 'content' fields.")

        try:
            if is_gemini:
                # Prepend system message to user message for Gemini
                system_message = next((msg["content"] for msg in messages if msg["role"] == "system"), "")
                user_message = next((msg["content"] for msg in messages if msg["role"] == "user"), "")
                combined_message = f"{system_message}\n\n{user_message}"
                response = client.generate_content(contents=combined_message, stream=stream)
            else:
                response = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    stream=stream,
                )

            if stream:
                return response if raw_response else self.format_stream(response, is_gemini)

            return response if raw_response else self._process_non_streaming_response(response, is_gemini)

        except Exception as e:
            logging.error("Error in response handling: %s", e)
            raise RuntimeError(f"Error in response handling.check logs for details:{e}")

    def format_stream(self, response: Any, is_gemini: bool) -> Generator[str, None, None]:
        """
        Format a streaming response from the model.

        Args: 

        response (Any): The response from the model.

        is_gemini (bool): Whether the response is from Gemini.


        Yields: 

        str: The content chunks from the streaming response.

        Returns:

        Generator[str, None, None]: The formatted response.
        """
        if is_gemini:
            for chunk in response:
                content = chunk.text
                if content:
                    yield content
        else:
            for chunk in response:
                if not chunk.choices or not chunk.choices[0].delta or not chunk.choices[0].delta.content:
                    continue
                content = chunk.choices[0].delta.content
                if content:
                    yield content

    def _process_non_streaming_response(self, response: Any, is_gemini: bool) -> str:
        """
        Process a non-streaming response from the model.

        Args:

        response (Any): The response from the model.

        is_gemini (bool): Whether the response is from Gemini.

        Returns:

        str: The processed response.

        Raises:

        RuntimeError: If the response is not from Gemini or OpenAI or Claude.
        """

        """
        various response stratergies for different models
        1.response.candidates[0].content.parts[0].text.strip()#gemini
        2.response.choices[0].message.content.strip()#openai/stellar
        3.response.choices[0].message.content.strip()#anthropic
        4.response.choices[0].message.content.strip()#claude
        5.response.choices[0].message.content.strip()#groq
        6.response.choices[0].message.content.strip()#groq
        7.response.choices[0].message.content.strip()#groq
        8.response.choices[0].message.content.strip()#groq
        """

        response_text = ""

        try:
            #various strategies for different models
            response_text = response.candidates[0].content.parts[0].text.strip() if is_gemini else response.choices[0].message.content.strip()
        except (AttributeError, IndexError,KeyError) as e:
            try:
                response_text = response.choices[0].message.content.strip()
            except (AttributeError, IndexError,KeyError) as e:
                try:
                    response_text = response.choices[0].message.content.strip()
                except (AttributeError, IndexError,KeyError) as e:
                    logging.error("Error processing response: %s", e)
                    raise RuntimeError(f"Error processing response.check logs for details: {e}")
        
        return response_text
    
    def _process_streaming_response(self, response: Any, is_gemini: bool) -> Generator[str, None, None]:
        """
        Process a streaming response from the model.

        Args:

        response (Any): The response from the model.

        is_gemini (bool): Whether the response is from Gemini.

        Yields:

        str: The content chunks from the streaming response.
        """

        if is_gemini:                   
            for chunk in response:  
                content = chunk.text
                if content:
                    yield content
        else:
            for chunk in response:
                if not chunk.choices or not chunk.choices[0].delta or not chunk.choices[0].delta.content:   
                    continue
                content = chunk.choices[0].delta.content
                if content:
                    yield content
    
    def query_llm(self, model: str, messages: List[dict], temperature: float = 0.2, stream: bool = False, raw_response: bool = False, max_tokens: int = 32000, llm_provider: str = "azure") -> Union[str, Generator[str, None, None]]:
        """
        Query the LLM with the given model, messages, temperature, stream, raw_response, and max_tokens.
        Args:

        model (str): The model to use for chat completion.

        messages (List[dict]): List of messages to send to the model.

        temperature (float, optional): Sampling temperature. Defaults to False  

        stream (bool, optional): Whether to stream the response. Defaults to True.

        raw_response (bool, optional): Whether to return the raw response. Defaults to False.

        max_tokens (int, optional): The maximum number of tokens to generate. Defaults to 32000.

        Returns:

        Union[str, Generator[str, None, None]]: The response from the model.
        """

        """         
        Supported models:
        - openai/azure
        - openai/gemini
        - openai/stellar
        - openai/claude
        - openai/groq
        """

        self.token = self._get_fresh_token()
        credentials = Credentials(self.token)

        if not messages or len(messages) <2:

            raise ValueError("messages must be a list of at least 2 messages.")

        if not self.token :


            raise ValueError("Token is required.")
        conbined_messages = f"{messages[0]['content']}\n\n{messages[1]['content']}"

        if llm_provider == "gemini":
            if not VERTEX_AI_AVAILABLE:
                raise ImportError("vertexai is not available. Please install it with: pip install google-cloud-aiplatform")
            
            vertexai.init(project=VERTEX_PROJECT, 
            api_transport="rest",
            api_endpoint=self.gemini_url,
            credentials=credentials,
            )
            llm=GenerativeModel(model)
            return llm.generate_content(conbined_messages).text.strip()

        elif llm_provider == "claude":
            messages_formatted = [{"role": "user", "content": conbined_messages}]
            credentials = Credentials(self._get_fresh_token())
            http_client = httpx.Client()
            client = AnthropicVertex(
                region="us-east5",
                project_id=VERTEX_PROJECT,
                http_client=http_client,
                credentials=credentials,
                base_url=self.claude_url)
            response =client.messages.create(
            model=model,
            messages=messages,
            temperature=temperature,
            stream=stream,
            )
            return response.choices[0].message.content.strip()

        elif llm_provider == "stellar":
            client = OpenAI(
                api_key=self.token,
                base_url=self.stellar_url,
            )
            response = client.chat.completions.create(model=model, messages=messages, temperature=temperature, stream=stream)
            return response.choices[0].message.content.strip()

        else:
            client = AzureOpenAI(
                azure_endpoint=self.openai_url,
                api_key=self.token,
                api_version=AZURE_API_VERSION,
            )
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                stream=stream,
            )
            return response.choices[0].message.content.strip()

    def call_default_llm(self, messages: List[dict], model: str = "claude-3-7-sonnet@20250219", temperature: float = 0.2, stream: bool = False, raw_response: bool = False, max_tokens: int = 32000) -> Union[str, Generator[str, None, None]]:
        """
        Call the default LLM with the given messages and optional parameters.
        
        Args:
            messages (List[dict]): List of messages to send to the model.
            model (str, optional): The model to use. Defaults to "claude-3-7-sonnet@20250219".
            temperature (float, optional): Sampling temperature. Defaults to 0.2.
            stream (bool, optional): Whether to stream the response. Defaults to False.
            raw_response (bool, optional): Whether to return raw response. Defaults to False.
            max_tokens (int, optional): Maximum tokens to generate. Defaults to 32000.
            
        Returns:
            Union[str, Generator[str, None, None]]: Response from the LLM.
        """
        
        # You can uncomment and modify these lines based on which provider you want to use:
        # return self.query_llm("claude-3-7-sonnet@20250219", messages=messages, llm_provider="claude")
        # return self.query_llm("Meta-Llama-3.3-70B-Instruct", messages, llm_provider="stellar")
        # return self.query_llm("Citi-GPT4-o", messages, llm_provider="openai")
        
        # Currently using Gemini as default
        return self.query_llm("gemini-2.5-pro", messages, llm_provider="gemini")

    def get_response(self, prompt: str, model: str = "claude-3-7-sonnet@20250219", temperature: float = 0.2) -> str:
        """
        Get a response from the LLM for a simple prompt.
        
        Args:
            prompt (str): The prompt to send to the LLM.
            model (str, optional): The model to use. Defaults to "claude-3-7-sonnet@20250219".
            temperature (float, optional): Sampling temperature. Defaults to 0.2.
            
        Returns:
            str: Response from the LLM.
        """
        messages = [{"role": "user", "content": prompt}]
        return self.call_default_llm(messages=messages, model=model, temperature=temperature)


llm_service = LLMService()
logging.info("LLM Service initialized")

if __name__ == "__main__":
        messages = [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "what is the meaning of life? with less than 100 words "},
        ]
        response = llm_service.call_default_llm(messages=messages,temperature=0.2,stream=False,raw_response=False,max_tokens=100)
        print(response)

        providers = ["gemini","claude","stellar","azure"]
        default_models = [ "claude-3-7-sonnet@20250219","gemini-2.5-pro","Meta-Llama-3.2-90B-Vision-Instruct"]
        for provider,model in zip(providers,default_models):
            try:
                response = llm_service.query_llm(model=model, messages=messages, llm_provider=provider)
                print(f"Provider: {provider}, Model: {model}, Response: {response}")
            except Exception as e:
                logging.error(f"Error calling {provider} {model}: {e}")
                
                
                
                
                
                











