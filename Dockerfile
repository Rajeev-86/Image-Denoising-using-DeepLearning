# 1. Pinned Base Image
FROM pytorch/torchserve:0.12.0-cpu

USER root 

# 2. Install other dependencies and clean up
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

WORKDIR /home/model-server
RUN mkdir model_store

EXPOSE 8080

# 3. Installing gdown, downloading models and immediately uninstalling it for a smaller image
RUN pip install --no-cache-dir gdown && \
     gdown 1yZfaeCagywUGfObCyhwNvd9hYVdXH84t -O model_store/UNET.mar && \
     gdown 1632np236SU0ZFM9Li4EbcwpNyLPcio9A -O model_store/R-UNET.mar && \
     gdown 1LyE6FQzY6wQI0nWwj3s1O29jseiF5-xo -O model_store/A-R-UNET.mar && \
     pip uninstall gdown -y && \
     rm -rf /root/.cache/pip && \
     rm -rf /var/lib/apt/lists/*

USER model-server

# 4. Start TorchServe with all models
CMD ["torchserve", \
     "--start", \
     "--ncs", \
     "--model-store", "/home/model-server/model_store", \
     "--models", "model_unet=UNET.mar,model_runet=R-UNET.mar,model_arunet=A-R-UNET.mar", \
     "--disable-token-auth"]