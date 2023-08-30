import gradio as gr
import json
import torch
import onnxruntime as rt
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("distilroberta-base")

with open("genre_types_encoded_kaggle_onnx.json", "r") as file:
    encode_genre_types = json.load(file)

genres = list(encode_genre_types.keys())

inf_session = rt.InferenceSession("game-classifier-quantized-kaggle.onnx")
input_name = inf_session.get_inputs()[0].name
output_name = inf_session.get_outputs()[0].name


def classify_game_genre(summary):
    input_ids = tokenizer(summary)["input_ids"][:512]
    logits = inf_session.run([output_name], {input_name: [input_ids]})[0]
    logits = torch.FloatTensor(logits)
    probs = torch.sigmoid(logits)[0]
    return dict(zip(genres, map(float, probs)))


examples = [
    ["March Of Soldiers is a real time strategy single player,"
     "It is a military game based on the player's skill and the strength of his financial economy"]
]

labels = gr.outputs.Label(num_top_classes=5)
iface = gr.Interface(fn=classify_game_genre, inputs="text", outputs=labels, examples=examples)
iface.launch(inline=False)
