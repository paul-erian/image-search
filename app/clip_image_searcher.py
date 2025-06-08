import torch

class ClipImageSearcher:
    def __init__(self, model, processor, image_features, s3_image_paths):
        self.model = model
        self.processor = processor
        self.image_features = image_features
        self.s3_image_paths = s3_image_paths

    def search(self, text_query, top_k=12, treshold=0.2):
        with torch.no_grad():
            text_inputs = self.processor(text=[text_query], return_tensors="pt")
            text_features = self.model.get_text_features(**text_inputs).half()
            text_features /= text_features.norm(dim=-1, keepdim=True)

            logits = self.image_features @ text_features.T
            logits = logits.squeeze(1)

            top_indices = logits.topk(top_k).indices.tolist()
            results = [
                (self.s3_image_paths[i], logits[i].item())
                for i in top_indices if logits[i] >= treshold
            ]
            return results