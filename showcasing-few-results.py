import torch
import torchvision.transforms as transforms
from PIL import Image
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

'''This script relies on predownloaded models, if you do'nt have them then run the following commands to download them-

!kaggle kernels output rajeev86/training-unet-for-image-denoising
!kaggle kernels output rajeev86/training-residual-unet-for-image-denoising
!kaggle kernels output rajeev86/training-unet-with-residuals-and-cbam-layers

Note that you may require kaggle credentials for successfully downloading the models
'''

model1_path = 'models/Script_Unet.pt'
model2_path = 'models/Script_Res-Unet.pt'
model3_path = 'models/Script_Att-Unet.pt'

try:
    model1 = torch.jit.load(model1_path, map_location=device)
    model1.eval()
    model2 = torch.jit.load(model2_path, map_location=device)
    model2.eval()
    model3 = torch.jit.load(model3_path, map_location=device)
    model3.eval()
except Exception as e:
    print(f"Error loading model: {e}")
    model1, model2, model3 = None, None, None

def denoise_image_and_show(image_paths):
    for image_path in image_paths:
        noisy_image = Image.open(image_path).convert('RGB')

        transform = transforms.Compose([transforms.ToTensor()])
        noisy_tensor = transform(noisy_image).unsqueeze(0).to(device)

        denoised_tensor1 = None
        denoised_tensor2 = None
        denoised_tensor3 = None

        with torch.no_grad():
            if model1:
                denoised_tensor1 = model1(noisy_tensor)
            if model2:
                denoised_tensor2 = model2(noisy_tensor)
            if model3:
                denoised_tensor3 = model3(noisy_tensor)

        images_to_show = [noisy_image]
        titles = ['Noisy Image']

        if denoised_tensor1 is not None:
            denoised1_image = transforms.ToPILImage()(denoised_tensor1.squeeze(0).cpu())
            images_to_show.append(denoised1_image)
            titles.append('Unet model')

        if denoised_tensor2 is not None:
            denoised2_image = transforms.ToPILImage()(denoised_tensor2.squeeze(0).cpu())
            images_to_show.append(denoised2_image)
            titles.append('res Unet model')

        if denoised_tensor3 is not None:
            denoised3_image = transforms.ToPILImage()(denoised_tensor3.squeeze(0).cpu())
            images_to_show.append(denoised3_image)
            titles.append('Att model')

        fig, axes = plt.subplots(1, len(images_to_show), figsize=(5 * len(images_to_show), 5))

        if len(images_to_show) == 1:
            axes.imshow(images_to_show[0])
            axes.set_title(titles[0])
            axes.axis('off')
        else:
            for i, img in enumerate(images_to_show):
                axes[i].imshow(img)
                axes[i].set_title(titles[i])
                axes[i].axis('off')

        plt.tight_layout()
        plt.show()

image_list = [
    'images/145079.jpg',
    'images/258089.jpg',
    'images/29030.jpg',
    'images/228076.jpg'
]
denoise_image_and_show(image_list)
