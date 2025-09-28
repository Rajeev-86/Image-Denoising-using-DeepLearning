from ts.torch_handler.base_handler import BaseHandler
import torch
import torchvision.transforms as transforms
from PIL import Image
import io
import time
import logging
import torch.nn.functional as F

logger = logging.getLogger(__name__)

class ImageHandler(BaseHandler):
    def __init__(self):
        super(ImageHandler, self).__init__()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.transform = transforms.Compose([transforms.ToTensor()])
        self.input_tensor_for_metrics = None
        self.start_time = 0

    def preprocess(self, data):
        self.start_time = time.time()

        image_bytes = data[0].get("body")
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        width, height = image.size
        logger.info(f"DATA_QUALITY: resolution={width}x{height}, format={image.format}")
        tensor = self.transform(image).unsqueeze(0).to(self.device)
        self.input_tensor_for_metrics = tensor.clone().detach()
        return tensor

    def inference(self, data, *args, **kwargs):
        with torch.no_grad():
            output = self.model(data)
        return output

    def postprocess(self, data):
        output_batched = data
        input_batched = self.input_tensor_for_metrics
        output_tensor = output_batched.squeeze(0).cpu().clamp(0, 1)
        input_tensor = input_batched.squeeze(0).cpu()
        output_tensor_resized = output_tensor
        if output_tensor.shape != input_tensor.shape:
             output_tensor_resized = F.interpolate(
                 output_tensor.unsqueeze(0), 
                 size=input_tensor.shape[-2:],
                 mode='bilinear', 
                 align_corners=False
             ).squeeze(0)
        
        pixel_difference = torch.mean(torch.abs(input_tensor - output_tensor_resized)).item()
        logger.info(f"OUTPUT_QUALITY: denoising_intensity={pixel_difference:.4f}")

        end_time = time.time()
        latency_ms = (end_time - self.start_time) * 1000
        logger.info(f"OPERATIONAL_HEALTH: total_latency={latency_ms:.2f}ms")

        output_image = transforms.ToPILImage()(output_tensor)
        buf = io.BytesIO()
        output_image.save(buf, format="PNG")
        return [buf.getvalue()]