import gradio as gr
import torch
import torch.nn.functional as F
from PIL import Image
import torchvision.transforms as transforms
from models.autoencoder import Autoencoder
from models.cnn import CNN
from constants.constants import Constants

class Classifier:
    def __init__(self,autoencoder_path,cnn_path):
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        self.autoencoder = self._load_model(Autoencoder(),autoencoder_path)
        self.cnn = self._load_model(CNN(),cnn_path)

        self.transform = transforms.Compose([
            transforms.Resize((256,256)),
            transforms.Grayscale(num_output_channels=1),
            transforms.ToTensor(),
        ])

        self.classes = Constants.CLASSES

    def _load_model(self, model, path):
        model.load_state_dict(torch.load(path, map_location=self.device))
        model.to(self.device)
        model.eval()
        return model

    def add_noise(self,img,noise_factor=0.3):
        noise = torch.randn_like(img) * noise_factor
        noisy_img = img + noise
        return torch.clamp(noisy_img, 0, 3)

    def predict(self, image, noise_factor=0.3):
        if isinstance(image,str):
            img = Image.open(image).convert('L')
        img = self.transform(image).unsqueeze(0).to(self.device)

        noisy_img = self.add_noise(img, noise_factor)

        with torch.no_grad():
            denoised = self.autoencoder(noisy_img)
            outputs = self.cnn(denoised)
            probs = F.softmax(outputs,dim=1)

        probs = probs.cpu().numpy()[0]
        
        return {
            'Original': self._prepare_image_for_display(image),
            'Noisy': self._prepare_image_for_display(noisy_img),
            'Denoised': self._prepare_image_for_display(denoised),
            'Prediction': {self.classes[i]: float(probs[i]) for i in range(len(self.classes))},
        }
    
    def _prepare_image_for_display(self,tensor):
        return tensor.cpu().squeeze().numpy()

def create_interface(autoencoder_path, cnn_path):
    classifier = Classifier(autoencoder_path,cnn_path)

    def process_image(image, noise_factor=0.3):
        if image is None:
            return None,None,None,"please upload an image"
        try:
            results = classifier.predict(image, noise_factor)

            pred_html = "<div style='text-align: center;'>"

            for cls, prob in results['Prediction'].items():
                bar_length = int(prob*100)
                pred_html += f"<p>{cls}: {prob:.4f}</p>"
                pred_html += f"<div style='margin: 5px 0;'>"
                pred_html += f"<div style='font-weight: bold;'>{cls}: {prob:.2%}</div>"
                pred_html += f"<div style='background: #ddd; height: 20px; border-radius: 5px;'>"
                pred_html += f"<div style='background: {'#4CAF50' if prob == max(results['Prediction'].values()) else '#2196F3'}; "
                pred_html += f"width: {bar_length}%; height: 100%; border-radius: 5px;'></div></div></div>"
            pred_html += "</div>"

            return (
                    results['Original'],
                    results['Noisy'],
                    results['Denoised'],
                    pred_html
                )
        except Exception as e:
            return None,None,None,f"Error processing image: {str(e)}"

    with gr.Blocks(theme = gr.themes.Soft()) as iface:
        gr.Markdown("# Image Denoising and Classification")
        gr.Markdown("Upload an image to see the denoising process and classification results.")

        with gr.Row():
            with gr.Column(scale=1):
                image_input = gr.Image(type="pil", label="Upload Image",sources=["upload","clipboard"])
                noise_slider = gr.Slider(minimum=0, maximum=1, value=0.3, step=0.01, label="Noise Factor")
                submit_button = gr.Button("Analyze", variant="primary")

            with gr.Column(scale=2):
                original_output = gr.Image(label="Original Image")
                noisy_output = gr.Image(label="Noisy Image")
                denoised_output = gr.Image(label="Denoised Image")
                prediction_output = gr.HTML(label="Prediction")

        gr.Examples(
            examples=[
                ["examples/covid.jpeg", 0.3],
                ["examples/normal.jpeg", 0.3],
                ["examples/pneumonia.jpeg", 0.3]
            ],
            inputs=[image_input,noise_slider],
            outputs=[original_output,noisy_output,denoised_output,prediction_output],
            fn=process_image,
            cache_examples=True
        )

        submit_button.click(
            fn=process_image,
            inputs=[image_input, noise_slider],
            outputs=[original_output, noisy_output, denoised_output, prediction_output]
        )

    return iface
 
if __name__ == "__main__":
    import argparse
    import os

    parser = argparse.ArgumentParser(description='x-ray classification and denoising app')

    parser.add_argument(
        '--autoencoder_path', type=str,required=True,default="results/autoencoder/checkpoints/best_model.pth"
    )

    parser.add_argument(
        '--cnn_path', type=str,required=True,default="results/cnn/checkpoints/best_model.pth"
    )

    parser.add_argument(
        '--port', type=int, default=7860,help="Port to run the Gradio app on"
    )

    parser.add_argument(
        '--example_dir',type=str,default='examples',help="Directory containing example images"
    )

    args = parser.parse_args()

    os.makedirs(args.example_dir, exist_ok=True)

    interface = create_interface(args.autoencoder_path,args.cnn_path)

    interface.launch(
        server_port=args.port,
        share=True,
        server_name="0.0.0.0"
    )

