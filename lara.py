from memory import create_memory, create_context, create_history
from embedding import load_and_embedd, encode
from audio import get_audio_stream
from args import Args
from llm import openai_llm

import elevenlabs
from langchain.prompts import PromptTemplate
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()


class Lara:

    def __init__(self):
        self.g_vars = {}
        self.client = OpenAI(api_key=os.getenv('OPEN_AI_API_KEY'))
        self.memo = []

        elevenlabs.set_api_key(os.getenv('ELEVEN_LAPS_KEY'))

    def get_the_prompt(self, question):
        results = self.g_vars['dp'].max_marginal_relevance_search(
            question, k=1)
        template = self.g_vars['config']['prompts']['course_propmt']
        context = create_context(results)
        history = create_history(self.g_vars['memory'].chat_memory.messages)

        new_template = template.format(
            context=context,
            history=history,
            question=question
        )
        prompt = PromptTemplate(
            input_variables=["context", "history", "question"],
            template=new_template
        )

        return prompt

    def stream_text(self, question):
        prompt = self.get_the_prompt(question)
        return self.openai_llm(prompt, question)

    def stream_audio(self, question):
        prompt = self.get_the_prompt(question)
        return get_audio_stream(self.openai_llm(prompt, question))

    async def stream_text_audio_ws(self, question):
        prompt = self.get_the_prompt(question)

        audio_stream = elevenlabs.generate(
            text=self.openai_llm_with_memmory(prompt, question), voice="Alice", model="eleven_multilingual_v2", stream=True)
        for chunk in audio_stream:
            if chunk:
                yield chunk

    def openai_llm_with_memmory(self, prompt, question):

        messages = [
            {"role": "system", "content": prompt.template}
        ]

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            temperature=0,
            messages=messages,
            stream=True,
        )
        
        res = ""

        for chunk in response:
            txt = chunk.choices[0].delta.content
            if txt:
                res += txt
                self.memo.append(txt)

                yield txt

        self.g_vars['memory'].chat_memory.messages = []
        self.g_vars['memory'].save_context(
            {"input": question}, {"output": res})

    def openai_llm(self, prompt, question):

        messages = [
            {"role": "system", "content": prompt.template}
        ]

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            temperature=0,
            messages=messages,
            stream=True,
        )

        res = ""

        for chunk in response:
            txt = chunk.choices[0].delta.content
            if txt:
                res += txt

                yield txt

        self.g_vars['memory'].chat_memory.messages = []
        self.g_vars['memory'].save_context(
            {"input": question}, {"output": res})
