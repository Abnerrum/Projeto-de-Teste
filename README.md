# 🌤️ Previsão do Clima

Web App de previsão do tempo feito com **FastAPI** + **Jinja2**.  
Usa a API gratuita [Open-Meteo](https://open-meteo.com/) — sem necessidade de cadastro ou chave de API.

## 📁 Estrutura

```
weather_app/
├── main.py              # Aplicação FastAPI
├── requirements.txt     # Dependências
└── templates/
    └── index.html       # Interface web
```

## 🚀 Como rodar

### 1. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv
source venv/bin/activate        # Linux/Mac
venv\Scripts\activate           # Windows
```

### 2. Instale as dependências
```bash
pip install -r requirements.txt
```

### 3. Inicie o servidor
```bash
uvicorn main:app --reload
```

### 4. Acesse no navegador
```
http://localhost:8000
```

## ✨ Funcionalidades

- 🔍 Busca por qualquer cidade do mundo
- 🌡️ Temperatura atual e sensação térmica
- 💧 Umidade relativa do ar
- 💨 Velocidade do vento
- 📅 Previsão para os próximos 7 dias
- 🌧️ Precipitação diária

## 🛠️ Tecnologias

| Tecnologia | Uso |
|---|---|
| FastAPI | Backend / rotas |
| Jinja2 | Templates HTML |
| HTTPX | Requisições HTTP assíncronas |
| Open-Meteo | Dados climáticos (gratuito) |
| Uvicorn | Servidor ASGI |

## 🌐 APIs utilizadas

- **Geocoding**: `https://geocoding-api.open-meteo.com/v1/search`
- **Clima**: `https://api.open-meteo.com/v1/forecast`

Ambas são gratuitas, sem limite de uso para projetos pessoais.
