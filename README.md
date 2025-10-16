---
title: Denoiser-Server
emoji: 🚀
colorFrom: indigo
colorTo: purple
sdk: docker
app_port: 8080
app_file: Dockerfile 
pinned: false
---

#Image Denoising using UNET and it's variants
_A Deep Learning approach to remove noise from images._

##1. Project Problem Statement: The Critical Need for Image Denoising
Digital images are indispensable data sources across numerous high-stakes industries, yet they are universally susceptible to noise corruption introduced during acquisition, transmission, or processing. This noise, whether Gaussian, Poisson, or Speckle, degrades images in two critical ways:

Impairing Human Perception: Noise obscures subtle features and textures, significantly lowering the visual fidelity required for accurate human interpretation.

Compromising Machine Reliability: Noise introduces spurious data points that confuse downstream Computer Vision tasks, drastically reducing the accuracy of algorithms used for analysis and automation.

The challenge is magnified across essential fields:

In Medical Imaging (e.g., MRI, CT), noise threatens the ability to identify critical, life-saving diagnostic features.

In Industrial Quality Control, noise leads to costly false positives or false negatives during automated inspection.

In Remote Sensing and Astronomy, noise prevents the reliable extraction of scientific data from satellite and telescopic imagery.

The objective of this project is to develop and evaluate a robust image denoising solution capable of effectively suppressing varied noise types while preserving crucial structural details, thereby elevating the reliability and precision of visual data for both human experts and advanced Machine Learning systems.

##2. Few Results

![Showcasing few test results](images/test-collage.png)

##3. Project Structure

├── .gitignore \
├── .gitattributes \
├── .github/workflows \
│ ├── sync_to_hf.yml \
├── Dockerfile \
├── api-test.py  
├── handler.py \
├── requirements.txt \
├── images \
└── README.md 

- [Dataset Preparation](https://drive.google.com/file/d/1hY0OBv0TI8dsP5Y2Le6IT9kFwPM_t8_V/view?usp=sharing) 
- [UNET_training](https://www.kaggle.com/code/rajeev86/training-unet-for-image-denoising)
- [Residual-UNET_training](https://www.kaggle.com/code/rajeev86/training-residual-unet-for-image-denoising)
- [CBAM-Residual-UNET_training](https://www.kaggle.com/code/rajeev86/training-unet-with-residuals-and-cbam-layers)
- [TorchScript_comparison](https://drive.google.com/file/d/1JC6WIi59fppT78v5kl26VSD4tX73ikgg/view?usp=sharing)
[- Model Archiving](https://drive.google.com/file/d/1X4lMJYiC8ps3170X-Jj5-YvnaIDDvnbx/view?usp=sharing)

##4. Dataset Used

The model was trained on an augmented dataset of 32,000 clean/noisy patch pairs derived from the BSD500 dataset, utilizing a 128×128 patch size with dynamic D4 geometric augmentation. To ensure robustness against real-world degradation, we employed a hybrid noise model incorporating four components:

Mixed Sensor Noise: A combination of Additive White Gaussian Noise (σstd ∈[0,30]) and Signal-Dependent Poisson Noise (a∈[0,0.05]).

Impulse Noise: Sparse Salt-and-Pepper noise (∈[0.001,0.005]).

Structured Artifacts: JPEG compression with randomized quality (∈[70,95]).

Due to the complex, non-linear nature of this hybrid noise model, we quantified the overall degradation using the Effective Noise Level (σ eff), defined as the Standard Deviation of the entire noise residual (y−x) across the validation set. The measured effective noise level for the challenging dataset was σeff =79.32 (scaled to 0-255). All performance metrics (PSNR, SSIM) presented below are reported against this highly degraded baseline.

- [Original Berkeley Segmentation Dataset 500 (BSDS500)](https://data.vision.ee.ethz.ch/cvl/DIV2K/) \
- [GDrive link for our modified Dataset](https://drive.google.com/drive/folders/1AObLCZGTHvtcv-lZFGPBA8k8xgC1k4_w?usp=sharing)

##5. Model Architectures

| Model                 | Description                                          | Key Features                            |
| --------------------- | ---------------------------------------------------- | --------------------------------------- |
| U-Net                 | Baseline architecture for image-to-image restoration | Encoder-decoder skip connections        |
| Residual U-Net        | Adds residual blocks to improve feature flow         | Residual connections within U-net blocks|
| Residual U-Net + CBAM | Incorporates Convolutional Block Attention Module    | focuses noise removal on key locations  |

##6. Training Setup

| Platform     | Purpose                        | Notes                          |
| ------------ | ------------------------------ | ------------------------------ |
| Google Colab | Dataset prep + initial testing | Limited GPU runtime            |
| Kaggle       | Model training                 | Used for high-performance GPUs |
| Google Drive | Model & dataset storage        | For cross-platform access      |

##7. Optimization
Comparing ordinary serlialization vs TorchScript inference time

| Model                    | Speedup |
| -------------------------| ------------------------ |
| U-Net                    | 39.18 %                  |
| Residual U-Net           | 43.77 %                  |
| Attention Residual U-Net | 30.72 %                  |

##8. Deployment (Backend)

Backend Framework: TorchServe

Containerization: Docker

Deployment Platform: Hugging Face Spaces

HuggingFace Space link: [here](https://huggingface.co/spaces/Rexy-3d/Denoiser-Server)

Artifacts: .mar model files stored [here](https://drive.google.com/drive/folders/1Arnlrjdxqd0zBaIC4ECigDxxSrgqyAHX?usp=sharing)

##8. Frontend (Next.js)

Repo: [Frontend Repo Link](https://github.com/Rajeev-86/Denoiser_-Frontend-)

Platform: Vercel

Provides a simple web interface for uploading noisy images and visualizing denoised outputs.

Open Web Frontend [here](https://denoiserbyrajeev.vercel.app/)

##9. Results:

| Model                 | PSNR         | SSIM        | Notes                   |
| --------------------- | ------------ | ------------| ----------------------- |
| U-Net                 | 28.7583      | 0.8444      | Baseline                |
| Residual U-Net        | 28.7630      | 0.8415      | Better texture recovery |
| Residual U-Net + CBAM | **29.0086**  | **0.8485**  | Best performance        |

##10. References

[1] [U-Net: Convolutional Networks for Biomedical Image Segmentation](https://arxiv.org/abs/1505.04597)\
[2] [Recurrent Residual Convolutional Neural Network based on U-Net (R2U-Net) for Medical Image Segmentation](https://arxiv.org/pdf/1802.06955)\
[3] [Layer Normalization](https://arxiv.org/abs/1607.06450)\
[CBAM: Convolutional Block Attention Module](https://arxiv.org/abs/1807.06521)\
[4] [Attention-based UNet enabled Lightweight Image Semantic Communication System over Internet of Things](https://arxiv.org/html/2401.07329v1)\
[5] [Application of ResUNet-CBAM in Thin-Section Image Segmentation of Rocks](https://www.mdpi.com/2078-2489/15/12/788)

##11. Author

Rajeev Ahirwar

[Linkedin](https://www.linkedin.com/in/86thrajeev/)\
[GitHub](https://github.com/Rajeev-86)