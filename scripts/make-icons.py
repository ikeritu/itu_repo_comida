from pathlib import Path
from PIL import Image, ImageDraw

out = Path(__file__).resolve().parent.parent / 'assets' / 'icons'
out.mkdir(parents=True, exist_ok=True)
for size, name in [(192, 'icon-192.png'), (512, 'icon-512.png'), (512, 'maskable-512.png')]:
    scale = 4
    im = Image.new('RGB', (size * scale, size * scale), '#37533d')
    draw = ImageDraw.Draw(im)
    def box(values):
        return tuple(int(x*size*scale) for x in values)
    # Pan centered inside the maskable safe area.
    draw.ellipse(box((.22,.25,.7,.73)), fill='#fff9e9')
    draw.rounded_rectangle(box((.59,.58,.81,.67)), radius=int(.045*size*scale), fill='#fff9e9')
    draw.ellipse(box((.36,.39,.56,.59)), fill='#d99b4a')
    im.resize((size, size), Image.Resampling.LANCZOS).save(out / name)
