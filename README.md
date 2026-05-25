# Mangaba AI · Visão Computacional — GitHub Pages

Landing page estática para o produto **Mangaba CV**, com paleta inspirada na Claude AI
(creme quente, terracota, tipografia serifada).

## Estrutura

```
mangaba-cv/
├─ index.html          # Página principal (PT-BR)
├─ assets/
│  ├─ styles.css       # Tema Claude — variáveis, layout e componentes
│  └─ favicon.svg
└─ README.md
```

## Como publicar no GitHub Pages

1. Crie um repositório (ex.: `mangaba-ai/mangaba-cv` ou `<user>.github.io`).
2. Copie todo o conteúdo da pasta `mangaba-cv/` para a raiz do repositório.
3. No GitHub: **Settings → Pages → Build and deployment**
   - **Source:** Deploy from a branch
   - **Branch:** `main` · pasta `/ (root)`
4. Aguarde o deploy. A URL ficará disponível no painel **Pages**.

### Domínio próprio (opcional)
Adicione um arquivo `CNAME` na raiz com o domínio desejado (ex.: `cv.mangaba.ai`) e
configure o DNS apontando para `<user>.github.io`.

## Como rodar localmente

Qualquer servidor estático funciona. Exemplos:

```bash
# Python
python -m http.server 5173

# Node (npx)
npx serve .
```

Acesse: <http://localhost:5173>

## Seções

- **Hero** — proposta de valor + amostra de detecção
- **Capacidades** — 6 famílias (detecção, OCR, faces, inspeção, vídeo, 3D)
- **Aplicações** — 6 cards de aplicações com imagem e KPIs
- **Vídeo** — 4 demos em loop + callout Edge
- **Cases** — 4 histórias com estatísticas reais
- **Stack** — formas de entrega (API, SDKs, Edge, Dashboard)
- **CTA / Footer**

## Paleta

| Token            | Hex       | Uso                          |
|------------------|-----------|------------------------------|
| `--bg`           | `#FAF9F5` | Fundo principal              |
| `--bg-alt`       | `#F5F1EB` | Seções alternadas            |
| `--ink`          | `#1F1E1B` | Texto principal              |
| `--accent`       | `#D97757` | Terracota Claude             |
| `--accent-dk`    | `#C2624A` | Hover / ênfase               |
| `--accent-soft`  | `#F4E0D5` | Tags, gradientes             |

## Imagens e vídeos

Hospedados via Unsplash (imagens) e Coverr (vídeos demo) — basta substituir as URLs
em `index.html` quando tiver mídia própria do produto.
