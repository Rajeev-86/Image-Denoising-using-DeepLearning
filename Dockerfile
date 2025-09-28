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
     gdown 1h0N5fQtWwzdn4TEH_CJZDlE5xBI7-7X_ -O model_store/UNET.mar && \
     gdown 1ozPgC_Cha99D5yYl4ES90LOd_Jo6p_fQ -O model_store/R-UNET.mar && \
     gdown 1dr0Oe5mkpb_o7rarXGcolXgobqL5T9S0 -O model_store/A-R-UNET.mar && \
     pip uninstall gdown -y

USER model-server

# 4. Start TorchServe with all models
CMD ["torchserve", \
     "--start", \
     "--ncs", \
     "--model-store", "/home/model-server/model_store", \
     "--models", "model_unet=UNET.mar,model_runet=R-UNET.mar,model_arunet=A-R-UNET.mar", \
     "--disable-token-auth"]