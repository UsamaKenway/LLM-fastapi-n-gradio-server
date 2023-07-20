import gradio as gr
import random
import time
from gradio.chatbot import ChatBot
import gradio as gr
import requests
from fastapi import FastAPI
from fastapi.routing import APIRouter
from LLMApp.core.event_handler import start_app_handler
from LLMApp.api.api import predict


class ChatBotApp:
    def __init__(self):
        self.bot = ChatBot()

    def run(self, message, chatbot):
        response = self.bot.respond(message)
        chatbot.append((message, response))
        return "", chatbot


def main():
    app = FastAPI()
    app.add_event_handler("startup", start_app_handler(
        app, "usamakenway/Wizard-Vicuna-13B-Uncensored-AutoGPTQ"))

    router = APIRouter()
    router.include_router(predict)
    app.include_router(router)

    bot_app = ChatBotApp()

    with gr.Blocks() as demo:
        no = gr.Label("title here")
        chatbot = gr.Chatbot()

        msg = gr.Textbox()
        clear = gr.ClearButton([msg, chatbot])

        msg.submit(bot_app.run, [msg, chatbot], [msg, chatbot])

    demo.launch(share=True)


if __name__ == "__main__":
    import threading
    import uvicorn

    server_thread = threading.Thread(target=lambda: uvicorn.run("main:app", host="0.0.0.0", port=8080, log_level="info"))
    server_thread.start()

    main()
