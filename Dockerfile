# 1. Pinned Base Image
FROM pytorch/torchserve:0.12.0-cpu

USER root 

# 2. Install gdown and immediately uninstall it for a smaller image
RUN pip install --no-cache-dir gdown && pip uninstall gdown -y

# 3. Install other dependencies and clean up
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR /home/model-server
RUN mkdir model_store

# 4. Download models using gdown
RUN gdown 1x9lGntRiYsNb-dYf1SugGGwnoGa_oQes -O model_store/UNET.mar
RUN gdown 1Y_P77RtNnC1StUeBGlONuNGAW5rFq02S -O model_store/R-UNET.mar
RUN gdown 1VYvAh5S5MQICbqmQkNJ1Epdmcm5VgVWb -O model_store/A-R-UNET.mar

USER model-server

# 5. Start TorchServe with all models
CMD ["torchserve", \
     "--start", \
     "--ncs", \
     "--model-store", "/home/model-server/model_store", \
     "--models", "model_unet=UNET.mar,model_runet=R-UNET.mar,model_arunet=A-R-UNET.mar"]