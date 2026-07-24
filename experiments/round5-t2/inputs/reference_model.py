from pathlib import Path
import cadquery as cq

OUT = Path(__file__).parent
CAP_OD_NOMINAL = 63.0
BAR_LENGTH_X = 62.0
BAR_WIDTH_Y = 11.7
BAR_HEIGHT_Z = 24.0
D0_Z = 0.0

bar = cq.Workplane("XY").box(BAR_LENGTH_X, BAR_WIDTH_Y, BAR_HEIGHT_Z, centered=(True, True, False))

def write_svg(name: str, body: str, width=900, height=620):
    (OUT / name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
        '<rect width="100%" height="100%" fill="#f8f8f5"/>'
        '<style>.cap{fill:#d9dde2;stroke:#20262d;stroke-width:3}.bar{fill:#8f9aa6;stroke:#20262d;stroke-width:3}.ref{fill:#155e75;fill-opacity:.45;stroke:#0e7490;stroke-width:4}.datum{stroke:#bf3b2b;stroke-width:2;stroke-dasharray:8 7}.t{font:20px Arial;fill:#20262d}.s{font:15px Arial;fill:#4b5560}</style>'
        + body + '</svg>', encoding='utf-8')

def views():
    write_svg('reference_top.svg', '''
<text x="40" y="42" class="t">Blind reference — top view (D0 / D1 / D2)</text>
<circle cx="340" cy="330" r="220.5" class="cap"/><rect x="123" y="289.05" width="434" height="81.9" class="bar"/>
<line x1="40" y1="330" x2="640" y2="330" class="datum"/><line x1="340" y1="90" x2="340" y2="570" class="datum"/>
<text x="45" y="600" class="s">F01 shown only as nominal D0 envelope Ø63.0; thickness/rim unknown and not exported.</text>
<text x="45" y="575" class="s">F02 export: 62.0 × 11.7, centred at D1/D2.</text>''')
    write_svg('reference_side.svg', '''
<text x="40" y="42" class="t">Blind reference — side section through D1/D2</text>
<line x1="70" y1="450" x2="780" y2="450" class="datum"/><text x="80" y="475" class="s">D0 cap face (unknown cap body below)</text>
<rect x="183" y="282" width="434" height="168" class="bar"/>
<line x1="400" y1="100" x2="400" y2="510" class="datum"/><text x="415" y="120" class="s">D3 / Z</text>
<text x="80" y="545" class="s">F04 root fillet/ramp unknown: square bounded F02 envelope intentionally retained.</text>''')
    write_svg('reference_isometric.svg', '''
<text x="40" y="42" class="t">Blind reference — isometric</text>
<ellipse cx="420" cy="445" rx="260" ry="85" fill="none" stroke="#20262d" stroke-width="3"/>
<path d="M190 393 L570 295 L650 335 L270 433 Z" class="bar"/><path d="M270 433 L650 335 L650 167 L270 265 Z" fill="#73808d" stroke="#20262d" stroke-width="3"/><path d="M570 295 L650 335 L650 167 L570 127 Z" fill="#65717d" stroke="#20262d" stroke-width="3"/>
<text x="60" y="565" class="s">Cap ellipse is a nominal D0 visual envelope only; exported solid is F02 bar.</text>''')
    write_svg('reference_overlay_top.svg', '''
<text x="40" y="42" class="t">Aligned overlay — fixture top view / blind F02 reference</text>
<text x="40" y="68" class="s">Alignment: D3=(325,350), D1/D2; 5 px/mm. Gray fixture, cyan reference.</text>
<circle cx="325" cy="350" r="157.5" fill="#d9dde2" fill-opacity=".48" stroke="#20262d" stroke-width="3"/>
<rect x="170" y="321" width="310" height="58.5" fill="#8f9aa6" fill-opacity=".4" stroke="#20262d" stroke-width="3"/>
<rect x="170" y="321" width="310" height="58.5" class="ref"/>
<line x1="70" y1="350" x2="580" y2="350" class="datum"/><line x1="325" y1="160" x2="325" y2="560" class="datum"/>
<text x="40" y="600" class="s">Exact coincidence of specified F02 top envelope; F03 corner and F04 root treatment remain unknown/bounded.</text>''')
    write_svg('reference_overlay_side.svg', '''
<text x="40" y="42" class="t">Aligned overlay — fixture side section / blind F02 reference</text>
<text x="40" y="68" class="s">Alignment: D0=y475, D3=x875; 10 px/mm. Gray fixture, cyan reference.</text>
<rect x="665" y="475" width="420" height="40" rx="18" fill="#d9dde2" fill-opacity=".48" stroke="#20262d" stroke-width="3"/>
<rect x="565" y="235" width="620" height="240" fill="#8f9aa6" fill-opacity=".40" stroke="#20262d" stroke-width="3"/>
<rect x="565" y="235" width="620" height="240" class="ref"/>
<line x1="450" y1="475" x2="1180" y2="475" class="datum"/><line x1="875" y1="130" x2="875" y2="540" class="datum"/>
<text x="40" y="600" class="s">Exact 24.0 mm F02 height on D0. Cap thickness and F04 transition are deliberately not reconstructed.</text>''', 1200, 620)

if __name__ == '__main__':
    cq.exporters.export(bar, str(OUT / 'reference_bar.stl'), tolerance=0.05, angularTolerance=0.1)
    cq.exporters.export(bar, str(OUT / 'reference_bar.step'))
    views()
