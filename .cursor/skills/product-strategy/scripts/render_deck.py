#!/usr/bin/env python3
"""Render a product-strategy YAML file to a report-out PowerPoint.

Draft and confirmed sections with content become slides. Empty and skipped
sections are listed on the coverage slide, along with blank links. The script
does not invent strategy content.
"""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

import yaml
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt

FONT = "Calibri"
SLIDE_W = 13.333333
SLIDE_H = 7.5

BLACK = "141414"
ORANGE = "F47B20"
INK = "1C1C1C"
MUTED = "5E646C"
PAPER = "F7F5F2"
WHITE = "FFFFFF"
CARD = "FFFFFF"
LINE = "E4DFD6"
BLUE = "2F7EAB"
BLUE_CARD = "E7F3FA"
CHARCOAL = "3A3A3A"
TEAL = "0F6E56"
TEAL_CARD = "E7F4EF"
LIME = "8FCB4A"
LIME_INK = "17330C"
LIME_CARD = "F3FAEA"
SWOT = "2C2C2C"
PALE = "FBFBF9"

ORDER = [
    "frame",
    "vision",
    "where_we_play",
    "needs",
    "how_we_win",
    "pillars",
    "swot",
    "filters",
    "initiatives",
    "roadmap",
]

NAMES = {
    "frame": "Frame",
    "vision": "Vision, mission, and direction",
    "where_we_play": "Where we play",
    "needs": "Customer needs and problems",
    "how_we_win": "How we win",
    "pillars": "Outcome pillars",
    "swot": "SWOT",
    "filters": "Decision filters",
    "initiatives": "Initiatives and operational work",
    "roadmap": "Roadmap",
}

PILLAR_LABELS = {
    "grow": "Grow the business",
    "interoperability": "Establish interoperability",
    "innovation": "Lead industry innovation",
}

SWOT_LABELS = (
    ("strengths", "Strengths we can leverage"),
    ("weaknesses", "Weaknesses to mitigate"),
    ("opportunities", "Opportunities to seize"),
    ("threats", "Threats to counter"),
)


def rgb(hex_color: str) -> RGBColor:
    value = hex_color.lstrip("#")
    return RGBColor(int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


def text_of(value) -> str:
    if value is None:
        return ""
    return str(value).strip()


def as_list(value) -> list:
    if isinstance(value, list):
        return value
    return []


def as_number(value):
    if value is None or value is False or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    cleaned = str(value).strip().rstrip("%")
    try:
        return float(cleaned)
    except ValueError:
        return None


def load_strategy(path: Path) -> dict:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise SystemExit(f"{path} is not a strategy mapping")
    version = data.get("schema_version")
    if version != 1:
        raise SystemExit(
            f"{path} has schema_version {version!r}; this renderer expects 1"
        )
    sections = data.get("sections")
    if not isinstance(sections, dict):
        raise SystemExit(f"{path} is missing sections")
    return data


def section(data: dict, key: str) -> dict:
    raw = data.get("sections", {}).get(key) or {}
    return raw if isinstance(raw, dict) else {}


def status_of(data: dict, key: str) -> str:
    status = text_of(section(data, key).get("status")).lower()
    if status in {"empty", "draft", "confirmed", "skipped"}:
        return status
    return "empty"


def showable(data: dict, key: str) -> bool:
    return status_of(data, key) in {"draft", "confirmed"}


def named_dicts(value, name_key: str = "name") -> list[dict]:
    found = []
    for item in as_list(value):
        if isinstance(item, dict) and text_of(item.get(name_key)):
            found.append(item)
    return found


def strings(value) -> list[str]:
    return [text_of(item) for item in as_list(value) if text_of(item)]


def has_content(data: dict, key: str) -> bool:
    body = section(data, key)
    if key == "frame":
        return any(text_of(body.get(field)) for field in ("product", "horizon", "audience", "decision"))
    if key == "vision":
        return any(text_of(body.get(field)) for field in ("vision", "mission", "direction"))
    if key == "where_we_play":
        return any(
            named_dicts(body.get(field))
            for field in ("regions_and_markets", "segments_and_cohorts", "who_is_out")
        )
    if key == "needs":
        return bool(named_dicts(body.get("items")))
    if key == "how_we_win":
        return bool(named_dicts(body.get("products")) or named_dicts(body.get("value_propositions"), "segment") or named_dicts(body.get("value_propositions"), "statement"))
    if key == "pillars":
        return any(named_dicts(body.get(field), "metric") for field in PILLAR_LABELS)
    if key == "swot":
        return any(named_dicts(body.get(field), "item") for field, _label in SWOT_LABELS)
    if key == "filters":
        return bool(
            strings(body.get("must_haves"))
            or named_dicts(body.get("stop_list"), "item")
            or named_dicts(body.get("resources"), "pillar")
        )
    if key == "initiatives":
        return bool(named_dicts(body.get("product")) or named_dicts(body.get("operational")))
    if key == "roadmap":
        columns = any(named_dicts(body.get(field)) for field in ("now", "next", "later"))
        narrative = any(
            text_of(body.get(field))
            for field in ("dependencies", "reorder_assumption", "delivered_means")
        )
        return columns or narrative
    return False


def open_links(data: dict) -> list[str]:
    links = []
    if showable(data, "how_we_win"):
        for product in named_dicts(section(data, "how_we_win").get("products")):
            if not text_of(product.get("need")):
                links.append(f'Product "{text_of(product.get("name"))}" has no need')
            assumption = text_of(product.get("assumption"))
            if assumption:
                links.append(
                    f'Working assumption on "{text_of(product.get("name"))}": {assumption}'
                )
        for prop in as_list(section(data, "how_we_win").get("value_propositions")):
            if not isinstance(prop, dict):
                continue
            segment = text_of(prop.get("segment")) or "unnamed segment"
            if text_of(prop.get("statement")) and not text_of(prop.get("alternative")):
                links.append(f'Value proposition for "{segment}" has no alternative')
    if showable(data, "initiatives"):
        body = section(data, "initiatives")
        for initiative in named_dicts(body.get("product")):
            name = text_of(initiative.get("name"))
            if not text_of(initiative.get("need")):
                links.append(f'Initiative "{name}" has no need')
            if not text_of(initiative.get("pillar_metric")):
                links.append(f'Initiative "{name}" has no pillar metric')
            if not text_of(initiative.get("must_have")):
                links.append(f'Initiative "{name}" has no must-have')
            assumption = text_of(initiative.get("assumption"))
            if assumption:
                links.append(f'Working assumption on "{name}": {assumption}')
        for action in named_dicts(body.get("operational")):
            name = text_of(action.get("name"))
            if not text_of(action.get("supports")):
                links.append(f'Operational action "{name}" has no support link')
            assumption = text_of(action.get("assumption"))
            if assumption:
                links.append(f'Working assumption on "{name}": {assumption}')
    if showable(data, "roadmap"):
        body = section(data, "roadmap")
        for column in ("now", "next", "later"):
            for item in named_dicts(body.get(column)):
                name = text_of(item.get("name"))
                if not text_of(item.get("traces_to")):
                    links.append(f'Roadmap item "{name}" has no initiative')
                assumption = text_of(item.get("assumption"))
                if assumption:
                    links.append(f'Working assumption on "{name}": {assumption}')
    if showable(data, "swot"):
        for field, _label in SWOT_LABELS:
            for item in named_dicts(section(data, "swot").get(field), "item"):
                if not text_of(item.get("affects")):
                    links.append(f'SWOT item "{text_of(item.get("item"))}" names nothing it affects')
    return links


def prep(text_frame, margin: float = 0.12, top: float = 0.1, bottom: float = 0.08) -> None:
    text_frame.word_wrap = True
    text_frame.auto_size = None
    text_frame.margin_left = Inches(margin)
    text_frame.margin_right = Inches(margin)
    text_frame.margin_top = Inches(top)
    text_frame.margin_bottom = Inches(bottom)
    text_frame._txBody.bodyPr.set("anchor", "t")


def write_blocks(text_frame, blocks: list[tuple]) -> None:
    prep(text_frame)
    wrote = False
    for text, size, color, bold, space_after in blocks:
        if not text:
            continue
        paragraph = text_frame.paragraphs[0] if not wrote else text_frame.add_paragraph()
        wrote = True
        paragraph.alignment = PP_ALIGN.LEFT
        paragraph.space_before = Pt(0)
        paragraph.space_after = Pt(space_after)
        run = paragraph.add_run()
        run.text = text
        run.font.name = FONT
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.color.rgb = rgb(color)
    if not wrote:
        text_frame.paragraphs[0].text = ""


def add_rect(slide, x, y, w, h, fill: str, line: str | None = None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill)
    if line:
        shape.line.color.rgb = rgb(line)
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    # Drop the default outer shadow so cards stay flat.
    effect = shape._element.spPr.find(qn("a:effectLst"))
    if effect is not None:
        shape._element.spPr.remove(effect)
    return shape


def estimate_height(blocks: list[tuple], width: float, pad: float = 0.32) -> float:
    """Rough text-block height in inches, used to keep cards from stretching over empty space."""
    height = pad
    usable = max(1.0, width - 0.4)
    for text, size, _color, _bold, space_after in blocks:
        if not text or not str(text).strip():
            height += 0.08
            continue
        per_line = max(8, int(usable / max(0.06, (size * 0.48) / 72.0)))
        lines = max(1, (len(str(text)) + per_line - 1) // per_line)
        height += lines * (size * 1.32) / 72.0 + space_after / 72.0
    return height


def shared_height(estimates: list[float], minimum: float, maximum: float = 5.78) -> float:
    if not estimates:
        return minimum
    return min(maximum, max([minimum, *estimates]))


def stack_heights(estimates: list[float], available: float = 5.78, gap: float = 0.12, minimum: float = 1.05) -> list[float]:
    natural = [max(minimum, height) for height in estimates]
    if not natural:
        return []
    gaps = gap * (len(natural) - 1)
    if sum(natural) + gaps <= available:
        return natural
    scale = (available - gaps) / sum(natural)
    return [height * scale for height in natural]


def add_text(slide, x, y, w, h, text, size, color, bold=False, align=PP_ALIGN.LEFT, name=None):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    if name:
        shape.name = name
    prep(shape.text_frame, margin=0.02, top=0.02, bottom=0.02)
    paragraph = shape.text_frame.paragraphs[0]
    paragraph.alignment = align
    run = paragraph.add_run()
    run.text = text
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = rgb(color)
    return shape


def set_background(slide, color: str) -> None:
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(color)


def add_header(slide, title: str, fill: str, title_color: str, draft: bool) -> None:
    add_rect(slide, 0, 0, SLIDE_W, 0.98, fill)
    add_text(
        slide,
        0.42,
        0.18,
        10.5 if draft else 12.3,
        0.66,
        title,
        28,
        title_color,
        bold=True,
        name="slide-title",
    )
    if draft:
        chip = add_rect(slide, 11.55, 0.3, 1.32, 0.38, WHITE)
        chip.name = "status-chip"
        prep(chip.text_frame, margin=0.02)
        paragraph = chip.text_frame.paragraphs[0]
        paragraph.alignment = PP_ALIGN.CENTER
        run = paragraph.add_run()
        run.text = "DRAFT"
        run.font.name = FONT
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = rgb(INK)
        chip.text_frame._txBody.bodyPr.set("anchor", "ctr")


def add_footer(slide, product: str) -> None:
    label = product or "Product strategy"
    add_text(slide, 0.42, 7.16, 8.5, 0.28, label, 11, MUTED)
    add_text(
        slide,
        8.4,
        7.16,
        4.5,
        0.28,
        "Product strategy report",
        11,
        MUTED,
        align=PP_ALIGN.RIGHT,
    )


def new_slide(prs, color: str = PAPER):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide, color)
    return slide


def product_name(data: dict) -> str:
    return text_of(section(data, "frame").get("product"))


def add_title_slide(prs, data: dict) -> None:
    frame = section(data, "frame")
    slide = new_slide(prs, BLACK)
    add_rect(slide, 0, 0, SLIDE_W, 0.12, ORANGE)
    add_text(slide, 0.62, 1.7, 11.5, 0.36, "PRODUCT STRATEGY REPORT", 14, ORANGE, bold=True)
    add_text(
        slide,
        0.62,
        2.15,
        11.8,
        1.35,
        product_name(data) or "Product strategy",
        40,
        WHITE,
        bold=True,
        name="cover-product",
    )
    horizon = text_of(frame.get("horizon"))
    if horizon:
        add_text(slide, 0.62, 3.6, 11.5, 0.42, horizon, 20, WHITE)
    decision = text_of(frame.get("decision"))
    if decision:
        add_text(slide, 0.62, 4.35, 11.2, 0.28, "DECISION REQUESTED", 12, ORANGE, bold=True)
        add_text(slide, 0.62, 4.68, 11.2, 0.9, decision, 20, WHITE)
    audience = text_of(frame.get("audience"))
    if audience:
        add_text(slide, 0.62, 6.55, 11.2, 0.36, f"For {audience}", 15, "C8C8C8")
    if status_of(data, "frame") == "draft" and has_content(data, "frame"):
        chip = add_rect(slide, 11.45, 0.4, 1.32, 0.38, WHITE)
        chip.name = "status-chip"
        prep(chip.text_frame, margin=0.02)
        paragraph = chip.text_frame.paragraphs[0]
        paragraph.alignment = PP_ALIGN.CENTER
        run = paragraph.add_run()
        run.text = "DRAFT"
        run.font.name = FONT
        run.font.size = Pt(12)
        run.font.bold = True
        run.font.color.rgb = rgb(INK)


def entry_blocks(heading: str, entries: list[dict], heading_color: str = INK) -> list[tuple]:
    blocks = [(heading, 14, heading_color, True, 8)]
    if not entries:
        return blocks
    for entry in entries:
        blocks.append((text_of(entry.get("name")), 16, INK if heading_color == INK else WHITE, True, 1))
        why = text_of(entry.get("why"))
        if why:
            blocks.append((why, 13, MUTED if heading_color == INK else "D0D0D0", False, 8))
    return blocks


def add_vision(prs, data: dict, included: list[str]) -> None:
    if not (showable(data, "vision") and has_content(data, "vision")):
        return
    body = section(data, "vision")
    parts = [
        ("Vision", text_of(body.get("vision"))),
        ("Mission", text_of(body.get("mission"))),
        ("Direction", text_of(body.get("direction"))),
    ]
    parts = [(label, copy) for label, copy in parts if copy]
    slide = new_slide(prs)
    draft = status_of(data, "vision") == "draft"
    add_header(slide, NAMES["vision"], BLACK, WHITE, draft)
    add_footer(slide, product_name(data))
    gap = 0.14
    block_sets = [
        [(label.upper(), 12, ORANGE, True, 4), (copy, 20, INK, False, 0)]
        for label, copy in parts
    ]
    heights = stack_heights(
        [estimate_height(blocks, 12.5, pad=0.36) for blocks in block_sets],
        gap=gap,
        minimum=1.28,
    )
    top = 1.22
    for blocks, height in zip(block_sets, heights):
        card = add_rect(slide, 0.42, top, 12.5, height, CARD, LINE)
        write_blocks(card.text_frame, blocks)
        top += height + gap
    included.append(NAMES["vision"] + (" (draft)" if draft else ""))


def add_where(prs, data: dict, included: list[str]) -> None:
    if not (showable(data, "where_we_play") and has_content(data, "where_we_play")):
        return
    body = section(data, "where_we_play")
    slide = new_slide(prs)
    draft = status_of(data, "where_we_play") == "draft"
    add_header(slide, NAMES["where_we_play"], ORANGE, WHITE, draft)
    add_footer(slide, product_name(data))
    columns = [
        ("Regions and markets", named_dicts(body.get("regions_and_markets")), CARD, INK),
        ("Customer segments and cohorts", named_dicts(body.get("segments_and_cohorts")), CARD, INK),
        ("Who is out", named_dicts(body.get("who_is_out")), "F4F1EC", INK),
    ]
    width = 4.02
    column_blocks = [entry_blocks(heading, entries, ink) for heading, entries, _fill, ink in columns]
    height = shared_height([estimate_height(blocks, width) for blocks in column_blocks], minimum=2.6)
    x = 0.42
    for (_heading, _entries, fill, _ink), blocks in zip(columns, column_blocks):
        card = add_rect(slide, x, 1.22, width, height, fill, LINE)
        write_blocks(card.text_frame, blocks)
        x += width + 0.18
    included.append(NAMES["where_we_play"] + (" (draft)" if draft else ""))


def add_needs(prs, data: dict, included: list[str]) -> None:
    if not (showable(data, "needs") and has_content(data, "needs")):
        return
    items = named_dicts(section(data, "needs").get("items"))
    slide = new_slide(prs)
    draft = status_of(data, "needs") == "draft"
    add_header(slide, NAMES["needs"], CHARCOAL, WHITE, draft)
    add_footer(slide, product_name(data))
    gap = 0.12
    row_blocks = []
    for item in items:
        blocks = [(text_of(item.get("name")), 18, INK, True, 3)]
        who = " · ".join(
            part for part in (text_of(item.get("who")), text_of(item.get("frequency"))) if part
        )
        if who:
            blocks.append((who, 14, MUTED, False, 2))
        cost = text_of(item.get("cost_of_status_quo"))
        if cost:
            blocks.append((f"Cost of the status quo: {cost}", 14, INK, False, 2))
        evidence = text_of(item.get("evidence"))
        if evidence:
            blocks.append((f"Evidence: {evidence}", 14, INK, False, 0))
        row_blocks.append(blocks)
    heights = stack_heights(
        [estimate_height(blocks, 10.15, pad=0.34) for blocks in row_blocks],
        gap=gap,
        minimum=1.2,
    )
    top = 1.22
    for item, blocks, height in zip(items, row_blocks, heights):
        card = add_rect(slide, 0.42, top, 10.15, height, CARD, LINE)
        stance = text_of(item.get("stance")).lower()
        stance_label = "Own" if stance == "own" else "Acknowledge" if stance == "acknowledge" else ""
        write_blocks(card.text_frame, blocks)
        if stance_label:
            pill_fill = TEAL if stance == "own" else "E6E8EB"
            pill_ink = WHITE if stance == "own" else INK
            pill = add_rect(slide, 10.75, top + max(0.16, (height - 0.36) / 2), 2.15, 0.36, pill_fill)
            prep(pill.text_frame, margin=0.02)
            paragraph = pill.text_frame.paragraphs[0]
            paragraph.alignment = PP_ALIGN.CENTER
            run = paragraph.add_run()
            run.text = stance_label
            run.font.name = FONT
            run.font.size = Pt(12)
            run.font.bold = True
            run.font.color.rgb = rgb(pill_ink)
            pill.text_frame._txBody.bodyPr.set("anchor", "ctr")
        top += height + gap
    included.append(NAMES["needs"] + (" (draft)" if draft else ""))


def add_how(prs, data: dict, included: list[str]) -> None:
    if not (showable(data, "how_we_win") and has_content(data, "how_we_win")):
        return
    body = section(data, "how_we_win")
    slide = new_slide(prs)
    draft = status_of(data, "how_we_win") == "draft"
    add_header(slide, NAMES["how_we_win"], ORANGE, WHITE, draft)
    add_footer(slide, product_name(data))
    products = named_dicts(body.get("products"))
    props = [
        prop
        for prop in as_list(body.get("value_propositions"))
        if isinstance(prop, dict) and (text_of(prop.get("statement")) or text_of(prop.get("segment")))
    ]
    blocks = [("Our products and solutions", 14, ORANGE, True, 10)]
    for product in products:
        blocks.append((text_of(product.get("name")), 18, INK, True, 1))
        need = text_of(product.get("need"))
        if need:
            blocks.append((f"Need: {need}", 14, MUTED, False, 8))
        assumption = text_of(product.get("assumption"))
        if assumption:
            blocks.append((f"Working assumption: {assumption}", 13, TEAL, False, 8))
    prop_blocks = [("Unique value proposition", 14, ORANGE, True, 10)]
    for prop in props:
        segment = text_of(prop.get("segment"))
        if segment:
            prop_blocks.append((segment, 13, MUTED, True, 3))
        statement = text_of(prop.get("statement"))
        if statement:
            prop_blocks.append((statement, 18, INK, False, 6))
        alternative = text_of(prop.get("alternative"))
        if alternative:
            prop_blocks.append((f"Instead of {alternative}", 14, INK, False, 8))
    height = shared_height(
        [estimate_height(blocks, 7.35), estimate_height(prop_blocks, 4.96, pad=0.4)],
        minimum=2.8,
    )
    left = add_rect(slide, 0.42, 1.22, 7.35, height, CARD, LINE)
    write_blocks(left.text_frame, blocks)
    right = add_rect(slide, 7.95, 1.22, 4.96, height, "FFF6EE", ORANGE)
    write_blocks(right.text_frame, prop_blocks)
    included.append(NAMES["how_we_win"] + (" (draft)" if draft else ""))


def metric_blocks(label: str, metrics: list[dict]) -> list[tuple]:
    blocks = [(label, 15, BLUE, True, 10)]
    for metric in metrics:
        blocks.append((text_of(metric.get("metric")), 18, INK, True, 2))
        baseline = text_of(metric.get("baseline"))
        target = text_of(metric.get("target"))
        if baseline and target:
            blocks.append((f"{baseline}  →  {target}", 14, INK, False, 1))
        elif baseline or target:
            blocks.append((baseline or target, 14, INK, False, 1))
        owner = text_of(metric.get("owner"))
        if owner:
            blocks.append((f"Owner: {owner}", 13, MUTED, False, 10))
    return blocks


def add_pillars(prs, data: dict, included: list[str]) -> None:
    if not (showable(data, "pillars") and has_content(data, "pillars")):
        return
    body = section(data, "pillars")
    slide = new_slide(prs)
    draft = status_of(data, "pillars") == "draft"
    add_header(slide, NAMES["pillars"], BLUE, WHITE, draft)
    add_footer(slide, product_name(data))
    width = 4.02
    column_blocks = [
        metric_blocks(label, named_dicts(body.get(key), "metric"))
        for key, label in PILLAR_LABELS.items()
    ]
    height = shared_height([estimate_height(blocks, width) for blocks in column_blocks], minimum=2.5)
    x = 0.42
    for blocks in column_blocks:
        card = add_rect(slide, x, 1.22, width, height, BLUE_CARD, LINE)
        write_blocks(card.text_frame, blocks)
        x += width + 0.18
    included.append(NAMES["pillars"] + (" (draft)" if draft else ""))


def swot_blocks(label: str, items: list[dict]) -> list[tuple]:
    blocks = [(label, 15, WHITE, True, 8)]
    for item in items:
        blocks.append((text_of(item.get("item")), 15, WHITE, False, 1))
        affects = text_of(item.get("affects"))
        if affects:
            blocks.append((affects, 12, "C8C8C8", False, 8))
    return blocks


def add_swot(prs, data: dict, included: list[str]) -> None:
    if not (showable(data, "swot") and has_content(data, "swot")):
        return
    body = section(data, "swot")
    slide = new_slide(prs)
    draft = status_of(data, "swot") == "draft"
    add_header(slide, NAMES["swot"], SWOT, WHITE, draft)
    add_footer(slide, product_name(data))
    width = 6.15
    quads = [swot_blocks(label, named_dicts(body.get(field), "item")) for field, label in SWOT_LABELS]
    height = shared_height([estimate_height(blocks, width) for blocks in quads], minimum=1.7, maximum=2.78)
    coords = [(0.42, 1.22), (6.75, 1.22), (0.42, 1.22 + height + 0.16), (6.75, 1.22 + height + 0.16)]
    for blocks, (x, y) in zip(quads, coords):
        card = add_rect(slide, x, y, width, height, SWOT)
        write_blocks(card.text_frame, blocks)
    included.append(NAMES["swot"] + (" (draft)" if draft else ""))


def add_filters(prs, data: dict, included: list[str]) -> None:
    if not (showable(data, "filters") and has_content(data, "filters")):
        return
    body = section(data, "filters")
    slide = new_slide(prs)
    draft = status_of(data, "filters") == "draft"
    add_header(slide, NAMES["filters"], TEAL, WHITE, draft)
    add_footer(slide, product_name(data))
    width = 4.02
    blocks = [("Must haves", 15, TEAL, True, 8)]
    for item in strings(body.get("must_haves")):
        blocks.append((item, 15, INK, False, 6))
    stop_blocks = [("Won't do (stop list)", 15, TEAL, True, 8)]
    for item in named_dicts(body.get("stop_list"), "item"):
        stop_blocks.append((text_of(item.get("item")), 15, INK, True, 1))
        protects = text_of(item.get("protects"))
        if protects:
            stop_blocks.append((f"Protects: {protects}", 13, MUTED, False, 8))
    resources = named_dicts(body.get("resources"), "pillar")
    resource_rows = []
    total = 0.0
    counted = 0
    for item in resources:
        pillar = text_of(item.get("pillar")).lower()
        label = PILLAR_LABELS.get(pillar, text_of(item.get("pillar")))
        number = as_number(item.get("percent"))
        row_height = 0.96 if len(label) > 24 else 0.74
        resource_rows.append((label, number, row_height))
        if number is not None:
            counted += 1
            total += number
    show_total = counted and abs(total - 100) > 0.01
    resource_height = 0.78 + sum(row[2] for row in resource_rows) + (0.46 if show_total else 0.2)
    height = shared_height(
        [
            estimate_height(blocks, width),
            estimate_height(stop_blocks, width),
            resource_height,
        ],
        minimum=2.6,
    )
    must = add_rect(slide, 0.42, 1.22, width, height, TEAL_CARD, LINE)
    write_blocks(must.text_frame, blocks)
    stops = add_rect(slide, 4.62, 1.22, width, height, CARD, LINE)
    write_blocks(stops.text_frame, stop_blocks)
    add_rect(slide, 8.82, 1.22, width, height, CARD, LINE)
    add_text(slide, 9.0, 1.38, 3.6, 0.32, "Resource allocations", 15, TEAL, bold=True)
    row_y = 1.84
    for label, number, row_height in resource_rows:
        add_text(slide, 9.0, row_y, 2.65, row_height - 0.24, label, 14, INK, bold=True)
        if number is None:
            row_y += row_height
            continue
        shown = str(int(number)) if number.is_integer() else f"{number:g}"
        add_text(slide, 11.65, row_y, 0.9, 0.3, f"{shown}%", 14, INK, bold=True, align=PP_ALIGN.RIGHT)
        bar_y = row_y + row_height - 0.18
        add_rect(slide, 9.0, bar_y, 3.5, 0.1, "E6E6E6")
        width_bar = max(0.08, 3.5 * max(0.0, min(number, 100.0)) / 100.0)
        add_rect(slide, 9.0, bar_y, width_bar, 0.1, TEAL)
        row_y += row_height
    if show_total:
        shown_total = str(int(total)) if total.is_integer() else f"{total:g}"
        add_text(slide, 9.0, row_y + 0.06, 3.5, 0.3, f"Entered total {shown_total}%.", 13, ORANGE)
    included.append(NAMES["filters"] + (" (draft)" if draft else ""))


def initiative_blocks(items: list[dict]) -> list[tuple]:
    blocks = []
    for item in items:
        blocks.append((text_of(item.get("name")), 18, INK, True, 2))
        outcome = text_of(item.get("outcome"))
        if outcome:
            blocks.append((outcome, 15, INK, False, 3))
        meta = []
        if text_of(item.get("need")):
            meta.append(f"Need: {text_of(item.get('need'))}")
        if text_of(item.get("pillar_metric")):
            meta.append(f"Metric: {text_of(item.get('pillar_metric'))}")
        if text_of(item.get("must_have")):
            meta.append(f"Must-have: {text_of(item.get('must_have'))}")
        if text_of(item.get("supports")):
            meta.append(f"Supports: {text_of(item.get('supports'))}")
        if meta:
            blocks.append(("  ·  ".join(meta), 13, MUTED, False, 2))
        assumption = text_of(item.get("assumption"))
        if assumption:
            blocks.append((f"Working assumption: {assumption}", 13, TEAL, False, 8))
        blocks.append((" ", 6, INK, False, 6))
    return blocks


def add_initiatives(prs, data: dict, included: list[str]) -> None:
    if not (showable(data, "initiatives") and has_content(data, "initiatives")):
        return
    body = section(data, "initiatives")
    draft = status_of(data, "initiatives") == "draft"
    suffix = " (draft)" if draft else ""
    product = named_dicts(body.get("product"))
    operational = named_dicts(body.get("operational"))
    if product:
        slide = new_slide(prs)
        add_header(slide, "Product initiatives", ORANGE, WHITE, draft)
        add_footer(slide, product_name(data))
        blocks = initiative_blocks(product)
        height = shared_height([estimate_height(blocks, 12.5)], minimum=1.5)
        card = add_rect(slide, 0.42, 1.22, 12.5, height, CARD, LINE)
        write_blocks(card.text_frame, blocks)
        included.append("Product initiatives" + suffix)
    if operational:
        slide = new_slide(prs)
        add_header(slide, "Operational actions and projects", ORANGE, WHITE, draft)
        add_footer(slide, product_name(data))
        blocks = initiative_blocks(operational)
        height = shared_height([estimate_height(blocks, 12.5)], minimum=1.35)
        card = add_rect(slide, 0.42, 1.22, 12.5, height, CARD, LINE)
        write_blocks(card.text_frame, blocks)
        included.append("Operational actions and projects" + suffix)


def add_roadmap(prs, data: dict, included: list[str]) -> None:
    if not (showable(data, "roadmap") and has_content(data, "roadmap")):
        return
    body = section(data, "roadmap")
    slide = new_slide(prs)
    draft = status_of(data, "roadmap") == "draft"
    add_header(slide, NAMES["roadmap"], LIME, LIME_INK, draft)
    add_footer(slide, product_name(data))
    notes = []
    if text_of(body.get("dependencies")):
        notes.append(("Depends on", text_of(body.get("dependencies"))))
    if text_of(body.get("reorder_assumption")):
        notes.append(("Would reorder if", text_of(body.get("reorder_assumption"))))
    if text_of(body.get("delivered_means")):
        notes.append(("Delivered means", text_of(body.get("delivered_means"))))
    width = 4.02
    column_sets = []
    for key, label in (("now", "Now"), ("next", "Next"), ("later", "Later")):
        blocks = [(label, 15, LIME_INK, True, 8)]
        for item in named_dicts(body.get(key)):
            blocks.append((text_of(item.get("name")), 15, INK, True, 1))
            traces = text_of(item.get("traces_to"))
            if traces:
                blocks.append((traces, 13, MUTED, False, 6))
            assumption = text_of(item.get("assumption"))
            if assumption:
                blocks.append((f"Working assumption: {assumption}", 12, TEAL, False, 6))
        column_sets.append(blocks)
    note_h = 1.2
    max_columns = 5.78 - (note_h + 0.16 if notes else 0)
    height = shared_height(
        [estimate_height(blocks, width) for blocks in column_sets],
        minimum=1.65,
        maximum=max_columns,
    )
    x = 0.42
    for blocks in column_sets:
        card = add_rect(slide, x, 1.22, width, height, LIME_CARD, LINE)
        write_blocks(card.text_frame, blocks)
        x += width + 0.18
    if notes:
        note_w = (12.5 - 0.16 * (len(notes) - 1)) / len(notes)
        nx = 0.42
        note_y = 1.22 + height + 0.16
        for label, copy in notes:
            card = add_rect(slide, nx, note_y, note_w, note_h, CARD, LINE)
            write_blocks(
                card.text_frame,
                [(label.upper(), 11, LIME_INK, True, 2), (copy, 13, INK, False, 0)],
            )
            nx += note_w + 0.16
    included.append(NAMES["roadmap"] + (" (draft)" if draft else ""))


def coverage_lines(data: dict, included: list[str]) -> list[tuple[str, list[str]]]:
    skipped = []
    still_open = []
    produced = set()
    for label in included:
        produced.add(label.replace(" (draft)", ""))
    for key in ORDER:
        status = status_of(data, key)
        name = NAMES[key]
        if key == "initiatives":
            produced_this = "Product initiatives" in produced or "Operational actions and projects" in produced
        else:
            produced_this = name in produced
        if status == "skipped":
            reason = text_of(section(data, key).get("skip_reason"))
            skipped.append(f"{name} — {reason}" if reason else name)
            continue
        if produced_this:
            continue
        if status in {"draft", "confirmed"}:
            still_open.append(f"{name} — marked {status} but empty")
        else:
            still_open.append(name)
    groups = []
    if included:
        groups.append(("In this version", included))
    if still_open:
        groups.append(("Still open", still_open))
    if skipped:
        groups.append(("Skipped", skipped))
    links = open_links(data)
    if links:
        groups.append(("Open links", links))
    if not groups:
        groups.append(("In this version", ["Every section is in this deck."]))
    return groups


def add_coverage(prs, data: dict, included: list[str]) -> None:
    slide = new_slide(prs)
    add_header(slide, "Coverage", BLACK, WHITE, False)
    add_footer(slide, product_name(data))
    groups = coverage_lines(data, included)
    body_size = 15
    head_size = 16
    blocks: list[tuple] = []
    height = 5.78
    while True:
        blocks = []
        for heading, lines in groups:
            blocks.append((heading, head_size, ORANGE, True, 4))
            for line in lines:
                blocks.append((line, body_size, INK, False, 3))
            blocks.append(("", 6, INK, False, 6))
        height = estimate_height(blocks, 12.5, pad=0.36)
        if height <= 5.78 or body_size <= 12:
            break
        body_size -= 1
        head_size -= 1
    card = add_rect(slide, 0.42, 1.22, 12.5, min(5.78, max(2.2, height)), CARD, LINE)
    card.name = "coverage-body"
    write_blocks(card.text_frame, blocks)


def build_presentation(data: dict) -> Presentation:
    prs = Presentation()
    prs.slide_width = Inches(SLIDE_W)
    prs.slide_height = Inches(SLIDE_H)
    prs.core_properties.title = product_name(data) or "Product strategy"
    prs.core_properties.subject = "Product strategy report"
    included: list[str] = []
    add_title_slide(prs, data)
    if showable(data, "frame") and has_content(data, "frame"):
        label = "Frame"
        if status_of(data, "frame") == "draft":
            label += " (draft)"
        included.append(label)
    add_vision(prs, data, included)
    add_where(prs, data, included)
    add_needs(prs, data, included)
    add_how(prs, data, included)
    add_pillars(prs, data, included)
    add_swot(prs, data, included)
    add_filters(prs, data, included)
    add_initiatives(prs, data, included)
    add_roadmap(prs, data, included)
    add_coverage(prs, data, included)
    return prs


def render(path: Path, output: Path) -> int:
    prs = build_presentation(load_strategy(path))
    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(output)
    return len(prs.slides)


def shape_text(shape) -> str:
    if not getattr(shape, "has_text_frame", False):
        return ""
    return shape.text_frame.text


def slide_title(slide) -> str:
    for shape in slide.shapes:
        if shape.name == "slide-title":
            return shape_text(shape).strip()
    return ""


def coverage_text(prs) -> str:
    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.name == "coverage-body":
                return shape_text(shape)
    return ""


def titles(prs) -> list[str]:
    return [slide_title(slide) for slide in prs.slides]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"self-check failed: {message}")


def self_check() -> None:
    root = Path(__file__).resolve().parents[1]
    fixture = root / "fixtures" / "partial-strategy.yml"
    template = root / "templates" / "strategy.yml"
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        out = tmp_path / "partial.pptx"
        count = render(fixture, out)
        prs = Presentation(out)
        found = titles(prs)
        require(count == 10, f"fixture deck has {count} slides, expected 10")
        require(out.stat().st_size > 0, "fixture deck is empty")
        cover = shape_text(next(shape for shape in prs.slides[0].shapes if shape.name == "cover-product"))
        require("Harbor Connect" in cover, "cover is missing the product name")
        for expected in (
            "Vision, mission, and direction",
            "Where we play",
            "Customer needs and problems",
            "How we win",
            "Outcome pillars",
            "Product initiatives",
            "Operational actions and projects",
            "Roadmap",
            "Coverage",
        ):
            require(expected in found, f"missing slide {expected}; got {found}")
        require("SWOT" not in found, "skipped SWOT was rendered as a slide")
        require("Decision filters" not in found, "skipped decision filters were rendered as a slide")
        body = coverage_text(prs)
        require("Evidence review is next week" in body, "SWOT skip reason missing")
        require("Finance owns the capacity conversation Thursday" in body, "filters skip reason missing")
        require('Product "Job record" has no need' in body, "blank product link missing")
        require('Initiative "Audit trail" has no need' in body, "blank initiative need missing")
        require(
            'Initiative "Certified connector program" has no must-have' in body,
            "blank must-have missing",
        )
        require(
            'Roadmap item "Audit packet export" has no initiative' in body,
            "blank roadmap link missing",
        )
        require('Product "Partner API" has no need' not in body, "filled product link listed as open")
        require("Harbor" not in coverage_text(build_presentation(load_strategy(template))), "template deck leaked fixture copy")
        empty = build_presentation(load_strategy(template))
        require(len(empty.slides) == 2, f"empty template rendered {len(empty.slides)} slides")
        empty_titles = titles(empty)
        require(empty_titles == ["", "Coverage"], f"empty template titles were {empty_titles}")
        empty_body = coverage_text(empty)
        for name in NAMES.values():
            require(name in empty_body, f"empty coverage missing {name}")

        draft_only = load_strategy(template)
        draft_only["sections"]["vision"]["status"] = "draft"
        draft_prs = build_presentation(draft_only)
        require("Vision, mission, and direction" not in titles(draft_prs), "empty draft vision rendered a slide")
        require(
            "Vision, mission, and direction — marked draft but empty" in coverage_text(draft_prs),
            "empty draft vision was not listed as open",
        )

        complete = load_strategy(fixture)
        complete["sections"]["swot"] = {
            "status": "confirmed",
            "skip_reason": "",
            "strengths": [{"item": "Dense install base", "affects": "Australia and New Zealand install base"}],
            "weaknesses": [{"item": "Connector setup takes a specialist", "affects": "Integration success"}],
            "opportunities": [{"item": "Design partners want a certified program", "affects": "Time to market"}],
            "threats": [{"item": "Incumbent bundles scheduling and invoicing", "affects": "Operations directors"}],
        }
        complete["sections"]["filters"] = {
            "status": "draft",
            "skip_reason": "",
            "must_haves": ["Moves a pillar metric this horizon"],
            "stop_list": [{"item": "Custom mobile branding", "protects": "Connector focus"}],
            "resources": [
                {"pillar": "grow", "percent": 40},
                {"pillar": "interoperability", "percent": 40},
                {"pillar": "innovation", "percent": 10},
            ],
        }
        full = build_presentation(complete)
        full_titles = titles(full)
        require("SWOT" in full_titles, "SWOT slide did not render when confirmed")
        require("Decision filters" in full_titles, "filters slide did not render when drafted")
        filters_slide = next(slide for slide in full.slides if slide_title(slide) == "Decision filters")
        filters_copy = "\n".join(shape_text(shape) for shape in filters_slide.shapes)
        require("Entered total 90%." in filters_copy, "resource total was corrected or omitted")
        require(any(shape.name == "status-chip" and "DRAFT" in shape_text(shape) for shape in filters_slide.shapes), "draft filters slide has no Draft chip")
        pillar_slide = next(slide for slide in prs.slides if slide_title(slide) == "Outcome pillars")
        require(
            any(shape.name == "status-chip" and shape_text(shape).strip() == "DRAFT" for shape in pillar_slide.shapes),
            "draft pillars slide has no Draft chip",
        )
    print("self-check ok")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Render a product strategy YAML file to PowerPoint.")
    parser.add_argument("strategy", nargs="?", type=Path, help="Path to strategy YAML")
    parser.add_argument("-o", "--output", type=Path, help="Output .pptx path")
    parser.add_argument("--self-check", action="store_true", help="Render the fixture and template and check the deck")
    args = parser.parse_args(argv)
    if args.self_check:
        self_check()
        return 0
    if args.strategy is None or args.output is None:
        parser.error("strategy and --output are required unless --self-check is set")
    count = render(args.strategy, args.output)
    print(f"Wrote {count} slides to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
