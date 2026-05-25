"""Reshape index.html to match mangabapixel.online's format:
- centered single-column hero (collapse the 3-card layout)
- new 'Como funciona' 3-step section after the impact band
- update nav with a 'Como funciona' anchor
"""
import os, re
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HTML = os.path.join(ROOT, "index.html")

with open(HTML, "r", encoding="utf-8") as f:
    src = f.read()

# 1) Replace the 3-card hero with a centered single-column hero
NEW_HERO = '''<!-- ============== HERO — centered single column (mangabapixel format) ============== -->
<section class="hero" id="top">
<div class="hero__inner">
<span class="eyebrow">Visão Computacional · pronta para produção</span>
<h1 class="hero__title">
Tire valor das suas câmeras<br/>
em <em>semanas</em>, não em anos.
</h1>
<p class="hero__lede">
  mangaba.ai transforma imagens e vídeos em decisões automáticas:
  defeitos, ruptura de gôndola, EPI, OCR e leitura de placas —
  integrado ao seu ERP, MES ou dashboard em até 6 semanas.
</p>
<div class="hero__cta">
<a class="btn btn--primary btn--lg" href="#contato">Agendar demonstração</a>
<a class="btn btn--ghost btn--lg" href="#cases">Ver casos de uso</a>
</div>
<p class="hero__proof">
sem mudar de câmera · sem refatorar seu ERP · piloto em 6 semanas
</p>
<div class="hero__media">
<img alt="Detecção YOLO de ônibus e pedestres em via urbana" loading="lazy" src="assets/cases/hero.jpg"/>
<div class="hero__hud">
<span class="dot"></span> LIVE · cam-04 · 32 ms · 0 alertas
</div>
</div>
</div>
</section>'''

src, n_hero = re.subn(
    r'<!-- ============== HERO[^>]*-->.*?</section>',
    NEW_HERO,
    src,
    count=1,
    flags=re.DOTALL,
)
print(f"hero replaced: {n_hero}")

# 2) Insert 'Como funciona' section right after the IMPACT STATS band
HOW_HTML = '''<!-- ============== COMO FUNCIONA — 3-step process ============== -->
<section class="section how" id="como-funciona">
<div class="container">
<div class="how__head">
<span class="eyebrow">Como funciona</span>
<h2>Em 3 passos do PoC ao deploy.</h2>
<p>Você manda câmera e contexto. Nós cuidamos do resto — sem hardware novo, sem migração de stack.</p>
</div>
<div class="how__steps">
<article class="how__step">
<div class="how__num">1</div>
<h3>Conecte sua câmera</h3>
<p>RTSP, ONVIF, WebRTC ou upload de vídeo. Reaproveitamos o CFTV que já está no chão de fábrica, na loja ou no CD.</p>
<ul>
<li>Suporte a 80% dos modelos de câmera do mercado</li>
<li>Inferência em nuvem, on-prem ou edge (Jetson/Hailo)</li>
</ul>
</article>
<article class="how__step">
<div class="how__num">2</div>
<h3>Configure seu caso</h3>
<p>Escolha do catálogo de <b>120+ modelos</b> prontos ou treine com seus próprios dados em ambiente isolado.</p>
<ul>
<li>Detecção, segmentação, OCR, pose, tracking, OBB</li>
<li>Auditoria de drift e re-treinamento contínuo</li>
</ul>
</article>
<article class="how__step">
<div class="how__num">3</div>
<h3>Integre o resultado</h3>
<p>Webhook, MQTT, Kafka ou dashboard pronto. Eventos chegam ao seu ERP/MES/WMS em latência de milissegundos.</p>
<ul>
<li>SLA de 99,5% e suporte 12×5 (Scale) ou 24×7 (Enterprise)</li>
<li>Piloto rodando em até <b>6 semanas</b></li>
</ul>
</article>
</div>
</div>
</section>'''

# Find the IMPACT block and inject HOW right after its closing </section>
impact_pattern = re.compile(
    r'(<!-- ============== IMPACT STATS ============== -->.*?</section>)',
    re.DOTALL,
)
src, n_how = impact_pattern.subn(lambda m: m.group(1) + "\n" + HOW_HTML, src, count=1)
print(f"how inserted: {n_how}")

# 3) Add 'Como funciona' link to nav, just before Pacotes
src, n_nav = re.subn(
    r'(<a href="#aplicacoes">Aplicações</a>\s*<a href="#video">Frames</a>\s*)<a href="#pacotes">',
    r'\1<a href="#como-funciona">Como funciona</a>\n<a href="#pacotes">',
    src,
    count=1,
)
print(f"nav link added: {n_nav}")

with open(HTML, "w", encoding="utf-8") as f:
    f.write(src)
print("ok")
