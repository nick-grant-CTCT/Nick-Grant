# Site Contractor — cumulative extra sales

Companion stacked-column slide for the Site Contractor Roadmap Options
line chart. Extra = Added − Current. Values are rough estimates digitised
from that chart, not a new forecast.

## Published deck

https://docs.google.com/presentation/d/1SeSqbcX0fWwj6AgI1_Tjl01hkRU5TFHwxURwlh7dN2I/edit

Same Drive folder as Roadmap Options. Original Options deck is unchanged.

Source numbers also live in sibling Sheet
https://docs.google.com/spreadsheets/d/1awX4ILI_EZNkzWo4zO0x29Ju933fw_NXYAQT1Mk12os/edit

## Rebuild locally

```bash
python3 render_preview.py
python3 build_companion_slide.py          # native stacked bars (python-pptx)
python3 build_google_picture_pptx.py      # Drive-importable picture slide
```
