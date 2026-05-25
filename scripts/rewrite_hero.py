"""Replace the hero block with a 3-card layout (brand identity)."""
import re, os
HTML = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "index.html")

NEW = '''<!-- ============== HERO — 3-card row (brand identity layout) ============== -->
<section class="hero" id="top">
<div class="hero__inner">

  <article class="hero-card hero-card--text">
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
      <a class="btn btn--primary" href="#contato">Agendar demonstração</a>
      <a class="btn btn--ghost" href="https://wa.me/5500000000000?text=Quero%20saber%20mais%20sobre%20mangaba.ai" rel="noopener" target="_blank">Falar no WhatsApp</a>
    </div>
    <p class="hero__proof">
      <span>✓</span> +40 deploys em produção · ROI médio em <b>5 meses</b> · compatível com sua câmera
    </p>
  </article>

  <article class="hero-card hero-card--media">
    <div class="hero__media">
      <img alt="Detecção YOLO de ônibus e pedestres em via urbana" loading="lazy" src="assets/cases/hero.jpg"/>
      <div class="hero__hud">
        <span class="dot"></span> LIVE · cam-04 · 32 ms · 0 alertas
      </div>
    </div>
  </article>

  <article class="hero-card hero-card--side">
    <ul class="hero__kpi">
      <li><b>+40</b><span>deploys em produção</span></li>
      <li><b>32 ms</b><span>latência por frame</span></li>
      <li><b>99,2%</b><span>precisão em QC industrial</span></li>
      <li><b>14</b><span>setores atendidos</span></li>
    </ul>
    <div class="hero__chips">
      <span class="chip">◐ Detecção</span>
      <span class="chip chip--ok">◍ Segmentação</span>
      <span class="chip">▶ Tracking</span>
      <span class="chip chip--ink">◇ OCR</span>
    </div>
  </article>

</div>
</section>'''

with open(HTML, 'r', encoding='utf-8') as f:
    src = f.read()

pattern = re.compile(r'<!-- ============== HERO ============== -->.*?</section>', re.DOTALL)
new_src, n = pattern.subn(NEW, src)
print(f"hero replacements: {n}")

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(new_src)
print('written')
