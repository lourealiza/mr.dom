# Dockerfile para Aplicação Node.js com Puppeteer

Este Dockerfile está configurado para executar aplicações Node.js que utilizam Puppeteer com Chromium em um ambiente Alpine Linux.

## Características

### Base Image
- Utiliza `node:16-alpine` como base, que é leve e ideal para rodar aplicações Node.js

### Instalação de Dependências
- As dependências do Chromium e Puppeteer são instaladas usando `apk add --no-cache` para evitar cache desnecessário e reduzir o tamanho da imagem
- Inclui todas as bibliotecas necessárias para o funcionamento do Chromium

### Variáveis de Ambiente
- `PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true`: Evita o download do Chromium pelo Puppeteer, já que ele será instalado via apk
- `PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser`: Define o caminho do Chromium instalado

### Segurança
- Após instalar as dependências, o usuário é alterado para `node` para evitar executar o aplicativo como root

## Como usar

### Build da imagem
```bash
docker build -f Dockerfile.puppeteer -t puppeteer-alpine .
```

### Executar o container
```bash
docker run --rm puppeteer-alpine
```

### Executar com volume (para desenvolvimento)
```bash
docker run --rm -v $(pwd):/app puppeteer-alpine
```

### Executar interativamente
```bash
docker run --rm -it puppeteer-alpine /bin/bash
```

## Dependências instaladas

- `chromium`: Navegador Chromium
- `nss`: Network Security Services
- `freetype`: Biblioteca de renderização de fontes
- `harfbuzz`: Motor de layout de texto
- `ca-certificates`: Certificados SSL/TLS
- `ttf-freefont`: Fontes TrueType gratuitas
- `bash`: Shell Bash
- `wget`: Utilitário de download
- `udev`: Gerenciador de dispositivos
- `alsa-lib`: Biblioteca de áudio
- `atk`: Accessibility Toolkit
- `cups-libs`: Biblioteca de impressão
- `libxcomposite`: Biblioteca de composição X11
- `libxrandr`: Biblioteca de extensões X11
- `libxss`: Biblioteca de extensões de tela
- `gconf`: Sistema de configuração GNOME
- `ttf-liberation`: Fontes Liberation

## Notas importantes

1. Certifique-se de que seu `package.json` inclui o Puppeteer como dependência
2. O arquivo principal deve ser `index.js` (ou ajuste o CMD conforme necessário)
3. Para aplicações que precisam de acesso à rede, use `--network host` se necessário
4. Para aplicações que geram arquivos, considere usar volumes para persistir dados
