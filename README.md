# 🌤️ Clima Now — v2.0

Web App de previsão do tempo com **mapa interativo de chuva**, interface redesenhada e código organizado por camadas.

## 📁 Estrutura do Projeto

```
weather_app_v2/
├── main.py                    # Entry point FastAPI
├── requirements.txt
├── routers/
│   ├── __init__.py
│   └── weather.py             # Rotas HTTP (GET /, /weather, /api/weather)
├── services/
│   ├── __init__.py
│   └── weather_service.py     # Lógica de negócio (geocoding, clima, regiões)
├── templates/
│   └── index.html             # Interface completa com Leaflet map
└── static/                    # (pasta para futuros assets)
```

## 🚀 Como rodar

```bash
# 1. Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Inicie o servidor
uvicorn main:app --reload

# 4. Acesse
http://localhost:8000
```

## ✨ O que há de novo na v2.0

### Interface
- Design completamente renovado com tema escuro refinado
- Tipografia com DM Serif Display + DM Sans
- Animações suaves e efeito de glow ambiente
- Layout responsivo em grid

### Mapa Interativo (NOVO)
- Mapa Leaflet com tiles OpenStreetMap
- Grade de 9 pontos ao redor da cidade buscada
- Círculos coloridos por condição climática:
  - 🟡 Amarelo — Limpo / Nublado
  - 🔵 Azul — Chuva leve / Garoa
  - 🟣 Roxo — Chuva moderada / Intensa
  - 🩷 Rosa — Tempestade
- Popup com temperatura e precipitação em cada ponto
- Marcador principal animado para a cidade buscada

### Novas métricas
- Pressão atmosférica
- Índice UV
- Visibilidade em km
- Vento máximo diário no forecast
- Horário de nascer/pôr do sol

### Gráfico de precipitação (NOVO)
- Barras hourly de precipitação para as próximas 24h

### Código
- Separação em camadas: `routers/` e `services/`
- Chamadas paralelas com `asyncio.gather` (mais rápido)
- Endpoint JSON `/api/weather?city=...` para uso externo
- Timeout e tratamento de erros por região do mapa

## 🌐 APIs utilizadas

| API | URL | Custo |
|-----|-----|-------|
| Geocoding | geocoding-api.open-meteo.com | Gratuito |
| Previsão | api.open-meteo.com | Gratuito |
| Mapa | tile.openstreetmap.org | Gratuito |

Nenhuma chave de API necessária.

## 📡 Endpoint JSON

```bash
curl "http://localhost:8000/api/weather?city=Goiania"
```

Retorna JSON completo com temperatura, previsão, dados horários e regiões do mapa.
