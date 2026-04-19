# 🌤️ Clima Now

Aplicação web de previsão do tempo em tempo real, desenvolvida com **FastAPI** e **Python**.  
Busque qualquer cidade do mundo e visualize temperatura, previsão dos próximos 7 dias e um mapa interativo de chuva por região.

---

## 🚀 Tecnologias utilizadas

- **FastAPI** — framework web moderno e assíncrono
- **Uvicorn** — servidor ASGI de alta performance
- **HTTPX** — requisições HTTP assíncronas
- **Jinja2** — renderização de templates HTML
- **Leaflet.js** — mapa interativo no frontend
- **Open-Meteo API** — dados climáticos gratuitos, sem necessidade de cadastro

---

## 📁 Estrutura do projeto
weather_app_v2/
├── main.py                      # Ponto de entrada da aplicação
├── requirements.txt             # Dependências do projeto
├── README.md                    # Documentação
├── routers/
│   └── weather.py               # Rotas HTTP da aplicação
├── services/
│   └── weather_service.py       # Lógica de negócio e integração com APIs
├── templates/
│   └── index.html               # Interface web completa
└── static/                      # Arquivos estáticos (CSS, JS futuros)
---

## ⚙️ Como executar o projeto

### Pré-requisitos
- Python 3.10 ou superior instalado
- Terminal (PowerShell, CMD ou Bash)

### Passo a passo

**1. Entre na pasta do projeto:**
```bash
cd weather_app_v2
```

**2. Crie o ambiente virtual:**
```bash
python -m venv venv
```

**3. Ative o ambiente virtual:**
```bash
# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

**4. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**5. Inicie o servidor:**
```bash
uvicorn main:app --reload
```

**6. Acesse no navegador:**
http://localhost:8000


---

## ✨ Funcionalidades

- 🔍 Busca por qualquer cidade do mundo
- 🌡️ Temperatura atual e sensação térmica
- 💧 Umidade relativa do ar
- 💨 Velocidade do vento
- 🌧️ Precipitação atual em mm
- 🌡️ Pressão atmosférica
- ☀️ Índice UV
- 👁️ Visibilidade em km
- 🌅 Horário de nascer e pôr do sol
- 📅 Previsão detalhada para os próximos 7 dias
- 📊 Gráfico de precipitação hora a hora (24h)
- 🗺️ Mapa interativo com condição climática por região

---

## 🗺️ Como funciona o mapa de chuva

Ao buscar uma cidade, o sistema consulta automaticamente 9 pontos geográficos ao redor da localização e exibe círculos coloridos no mapa indicando a condição climática de cada ponto:

| Cor | Condição |
|-----|----------|
| 🟡 Amarelo | Céu limpo ou nublado |
| 🔵 Azul | Garoa ou chuva leve |
| 🟣 Roxo | Chuva moderada ou intensa |
| 🩷 Rosa | Tempestade |

Clique em qualquer círculo para ver a temperatura e precipitação daquele ponto.

---

## 📡 API JSON

O projeto expõe um endpoint JSON para uso externo:
GET /api/weather?city=NomeDaCidade


Exemplo:
```bash
curl "http://localhost:8000/api/weather?city=Goiania"
```

---

## 🌐 APIs utilizadas

| Serviço | Endpoint | Custo |
|---------|----------|-------|
| Geocoding | geocoding-api.open-meteo.com | Gratuito |
| Previsão do tempo | api.open-meteo.com | Gratuito |
| Mapa | tile.openstreetmap.org | Gratuito |

Nenhuma chave de API é necessária.

---

## 👨‍💻 Autor

Desenvolvido como projeto pessoal de estudo em Python e desenvolvimento web.


