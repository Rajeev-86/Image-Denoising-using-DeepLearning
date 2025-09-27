from ts.torch_handler.base_handler import BaseHandler
import torch
import torchvision.transforms as transforms
from PIL import Image
import io

class ImageHandler(BaseHandler):
    def __init__(self):
        super(ImageHandler, self).__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.transform = transforms.Compose([transforms.ToTensor()])

    def preprocess(self, data):
        # TorchServe sends input as bytes → we decode into PIL image
        image_bytes = data[0].get("body")
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = self.transform(image).unsqueeze(0).to(self.device)
        return tensor

    def inference(self, data, *args, **kwargs):
        with torch.no_grad():
            output = self.model(data)
        return output

    def postprocess(self, data):
        output_tensor = data.squeeze(0).cpu().clamp(0, 1)  # ensure valid range
        output_image = transforms.ToPILImage()(output_tensor)

        buf = io.BytesIO()
        output_image.save(buf, format="PNG")
        return [buf.getvalue()]