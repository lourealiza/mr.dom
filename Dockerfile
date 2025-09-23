FROM atendai/evolution-api:latest

USER root

# Instala dependências do Chromium/Puppeteer no Alpine
RUN apk update && apk add --no-cache \
    chromium \
    nss \
    freetype \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    bash \
    wget \
    udev \
    alsa-lib \
    atk \
    cups-libs \
    libxcomposite \
    libxrandr \
    libxss \
    gconf \
    ttf-liberation

# Variáveis de ambiente para o Puppeteer usar o Chromium instalado
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

USER node   # ou o usuário padrão da imagem
