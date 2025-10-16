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
     gdown h1vzykr8eH77ypl4R7_AsSb56W9p7LDlKo -O model_store/UNET.mar && \
     gdown 1GdQyPrRn8yH5y7F1jC5Yuu2vWNLUs4K2 -O model_store/R-UNET.mar && \
     gdown 1mw7VbQt9Lrv0TG2LX0Ke3hKp0kyukElA -O model_store/A-R-UNET.mar && \
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