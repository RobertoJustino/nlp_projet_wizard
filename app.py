import gradio as gr
import requests

demo = gr.Blocks()

# Code Gradio pour la tab 1

# requête API sur le model bart-large-cnn de Facebook
def query(payload):
    api_url = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": "Bearer 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"}
    response = requests.post(api_url, headers=headers, json=payload)
    result =  response.json()
    return result[0]['summary_text']


# Code Gradio pour la tab 2

# requête API sur le model opus-mt-en-fr de Helsinki-NLP
def query1(payload):
    api_url1 = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt-en-fr"
    headers1 = {"Authorization": "Bearer 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"}
    response = requests.post(api_url1, headers=headers1, json=payload)
    result =  response.json()
    return result[0]['translation_text']

# combinaison des 2 pour traduire le résumé d'un article
def combineSummarizeAndTranslate(text):
    summarizedText = query(text)
    translatedText = query1(summarizedText)
    return translatedText

# découpage de chaque partie en Tab pour sélectionner la fonction voulu
with demo:
    gr.Markdown("Summarize an article or Translate text")
    with gr.Tabs():
        with gr.TabItem("Summarize Text"):
            with gr.Row():
                article_input = gr.inputs.Textbox(label="Please paste your article:", lines=30)
                summary_output = gr.outputs.Textbox(label="Summary")
            text_button = gr.Button("Summarize")
        with gr.TabItem("Translate Text"):
            gr.Markdown("Long text not supported")
            with gr.Row():
                text_input = gr.inputs.Textbox(label="Please write your text:", lines=10)
                translation_output = gr.outputs.Textbox(label="Translation")
            text_button1 = gr.Button("Translate")
        with gr.TabItem("Summarize and Translate"):
            with gr.Row():
                article_input1 = gr.inputs.Textbox(label="Please paste your article:", lines=30)
                summary_output1 = gr.outputs.Textbox(label="Translated Summary")
            text_button2 = gr.Button("Summarize and translate text in French")

    text_button.click(query, inputs=article_input, outputs=summary_output)
    text_button1.click(query1, inputs=text_input, outputs=translation_output)
    text_button2.click(combineSummarizeAndTranslate, inputs=article_input1, outputs=summary_output1)

demo.launch()