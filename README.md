# Aplicativo de Clima ☀️🌧️

Aplicativo web para consultar a previsão do tempo de qualquer cidade, utilizando Python (Flask) no backend e HTML/CSS/JS no frontend. O backend consome a API Open-Meteo e o frontend pode ser hospedado no Vercel.

## Funcionalidades

- Busca de cidade por nome.
- Exibe temperatura atual, vento e condição do tempo.
- Mostra previsão de 5 dias (máxima, mínima, vento, precipitação).
- Interface responsiva e moderna.
- Backend com cache em memória para otimizar requisições.

## Tecnologias

- **Backend:** Python, Flask, Flask-CORS, requests
- **Frontend:** HTML, CSS puro, JavaScript (fetch)
- **APIs:** Open-Meteo, Nominatim (OpenStreetMap)

## Como rodar localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repo.git
   cd seu-repo/weather_app
   ```

2. Instale as dependências:
   ```bash
   pip install flask flask-cors requests
   ```

3. Inicie o backend:
   ```bash
   python backend.py
   ```
   O backend estará disponível em `http://localhost:5000`.

4. Abra o `index.html` no navegador (ou use uma extensão como Live Server).

## Link do App Online

Acesse o app hospedado em: [https://app-clima-m51l0te38-la1sa0s-projects.vercel.app](https://app-clima-m51l0te38-la1sa0s-projects.vercel.app)


## Observações

- O backend utiliza cache em memória para previsões (expira em 1 hora).
- O frontend faz requisições para o backend via fetch.
- Para produção, sempre use a URL pública do backend no frontend.
