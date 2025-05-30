import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel
import os

# chargement de CLIP
model_name = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_name)
processor = CLIPProcessor.from_pretrained(model_name)

# chargement des images
image_dir = "./images"
image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir)]
images = [Image.open(p).convert("RGB") for p in image_paths]

# prediction
model.eval()
text_query = "une  photo avec un environement naturel en fond (herbe, arbres ou ciel)"
inputs = processor(text=[text_query], images=images, return_tensors="pt", padding=True)
with torch.no_grad():
    outputs = model(**inputs)
    logits_per_image = outputs.logits_per_image  # [batch_size, 1]
    probs = logits_per_image.softmax(dim=0)       # Normalise les scores

# resultats
print("Scores de similarité pour chaque image :")
for path, prob in zip(image_paths, probs):
    print(f"{path} : {prob}")
