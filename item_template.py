#!/usr/bin/env python3
"""
Item Template for reMarkable 2
"""

from reportlab.lib.units import mm
from reportlab.lib.colors import Color, black, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter

# reMarkable 2 native resolution: 1404 x 1872 pixels at 226 DPI
RM2_WIDTH = 1404 * 72 / 226  # ~446.5 points
RM2_HEIGHT = 1872 * 72 / 226  # ~595.6 points

# Colors
LIGHT_GRAY = Color(0.8, 0.8, 0.8)
MED_GRAY = Color(0.6, 0.6, 0.6)
DARK_GRAY = Color(0.3, 0.3, 0.3)

# Spacing
MARGIN = 20
LINE_HEIGHT = 14
SMALL_LINE_HEIGHT = 12


def draw_corner_flourish(c, x, y, position):
    """Draw a small Celtic-style corner flourish."""
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(0.75)
    size = 8

    if position == "tl":
        c.line(x, y, x + size, y)
        c.line(x, y, x, y - size)
        c.arc(x, y - size, x + size, y, 90, 90)
    elif position == "tr":
        c.line(x, y, x - size, y)
        c.line(x, y, x, y - size)
        c.arc(x - size, y - size, x, y, 0, 90)
    elif position == "bl":
        c.line(x, y, x + size, y)
        c.line(x, y, x, y + size)
        c.arc(x, y, x + size, y + size, 180, 90)
    elif position == "br":
        c.line(x, y, x - size, y)
        c.line(x, y, x, y + size)
        c.arc(x - size, y, x, y + size, 270, 90)


def draw_decorative_frame(c, x, y, width, height):
    """Draw a decorative frame around a section."""
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(1)
    c.rect(x, y - height, width, height)

    draw_corner_flourish(c, x, y, "tl")
    draw_corner_flourish(c, x + width, y, "tr")
    draw_corner_flourish(c, x, y - height, "bl")
    draw_corner_flourish(c, x + width, y - height, "br")


def draw_section_header(c, x, y, width, title):
    """Draw a decorated section header."""
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(DARK_GRAY)
    c.drawString(x + 12, y, title)

    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(1.5)
    c.line(x, y - 5, x + width, y - 5)

    draw_corner_flourish(c, x, y + 5, "tl")
    draw_corner_flourish(c, x + width, y + 5, "tr")

    return y - 15


def draw_ruled_lines(c, x, y, width, num_lines, line_height=SMALL_LINE_HEIGHT):
    """Draw light gray ruled lines for writing."""
    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(0.5)
    c.setDash([2, 2])

    for i in range(num_lines):
        line_y = y - (i * line_height)
        c.line(x, line_y, x + width, line_y)

    c.setDash([])
    return y - (num_lines * line_height)


def draw_field_with_label(c, x, y, label, line_start, line_end):
    """Draw a labeled field with underline."""
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(x, y, label)
    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(0.5)
    c.setDash([2, 2])
    c.line(line_start, y - 3, line_end, y - 3)
    c.setDash([])


def draw_item_page_1(c):
    """Draw the first page of item tracking."""
    page_width = RM2_WIDTH
    content_width = page_width - 2 * MARGIN

    y = RM2_HEIGHT - MARGIN

    # === HEADER SECTION ===
    header_height = 35
    draw_decorative_frame(c, MARGIN, y, content_width, header_height)

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(DARK_GRAY)
    c.drawString(MARGIN + 10, y - 15, "ITEM NAME:")

    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(0.5)
    c.setDash([2, 2])
    c.line(MARGIN + 120, y - 19, content_width - 120, y - 19)

    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(content_width - 110, y - 15, "Type:")
    c.line(content_width - 70, y - 19, content_width + MARGIN - 10, y - 19)
    c.setDash([])

    y -= header_height + 15

    # === CORE INFORMATION SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Core Information")
    y -= 5

    draw_field_with_label(c, MARGIN + 5, y, "Description:",
                          MARGIN + 100, content_width + MARGIN - 5)
    y -= 18

    y -= 8
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + 5, y, "Properties:")
    y -= 12
    y = draw_ruled_lines(c, MARGIN + 10, y, content_width - 15, 4)

    y -= 8
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + 5, y, "Magical Nature (Y/N):")
    y -= 12
    y = draw_ruled_lines(c, MARGIN + 10, y, content_width - 15, 1)

    draw_field_with_label(c, MARGIN + 10, y, "Conditions/Attunement:",
                          MARGIN + 140, content_width + MARGIN - 5)
    y -= 18

    y -= 8
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + 5, y, "History:")
    y -= 12
    y = draw_ruled_lines(c, MARGIN + 10, y, content_width - 15, 4)

    y -= 10

    # === STORY INTEGRATION SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Story Integration")
    y -= 5

    draw_field_with_label(c, MARGIN + 5, y, "Sessions Used In:",
                          MARGIN + 160, content_width + MARGIN - 5)
    y -= 18

    draw_field_with_label(c, MARGIN + 5, y, "Current Ownership:",
                          MARGIN + 140, content_width + MARGIN - 5)
    y -= 18

    y -= 8
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + 5, y, "Notable Events:")
    y -= 12
    y = draw_ruled_lines(c, MARGIN + 10, y, content_width - 15, 4)

    y -= 10

    # === PAGE 1 NOTES SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Notes")
    y -= 5
    y = draw_ruled_lines(c, MARGIN + 5, y, content_width - 10, 4)

    return y


def draw_item_page_2(c):
    """Draw the second page of item tracking (extended notes)."""
    page_width = RM2_WIDTH
    content_width = page_width - 2 * MARGIN

    y = RM2_HEIGHT - MARGIN

    # === HEADER SECTION ===
    header_height = 35
    draw_decorative_frame(c, MARGIN, y, content_width, header_height)

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(DARK_GRAY)
    c.drawString(MARGIN + 10, y - 15, "ITEM NAME (continued):")

    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(0.5)
    c.setDash([2, 2])
    c.line(MARGIN + 200, y - 19, content_width - 100, y - 19)
    c.setDash([])

    y -= header_height + 15

    # === ORIGINAL PURPOSE & CREATORS SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Original Purpose & Creators")
    y -= 5
    y = draw_ruled_lines(c, MARGIN + 5, y, content_width - 10, 6)

    y -= 10

    # === UNIQUE FEATURES SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Unique Features")
    y -= 5
    y = draw_ruled_lines(c, MARGIN + 5, y, content_width - 10, 6)

    y -= 10

    # === FUTURE PLOT HOOKS & UPGRADES SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Future Plot Hooks & Upgrades")
    y -= 5
    y = draw_ruled_lines(c, MARGIN + 5, y, content_width - 10, 6)

    y -= 10

    # === UNRESOLVED MYSTERIES SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Unresolved Mysteries")
    y -= 5
    y = draw_ruled_lines(c, MARGIN + 5, y, content_width - 10, 6)

    y -= 10

    # === ADDITIONAL NOTES SECTION (Page 2) ===
    y = draw_section_header(c, MARGIN, y, content_width, "Additional Notes")
    y -= 5
    remaining_lines = int((y - MARGIN - 10) / SMALL_LINE_HEIGHT)
    draw_ruled_lines(c, MARGIN + 5, y, content_width - 10, remaining_lines)


def create_item_template(filename="item_template.pdf"):
    """Generate the item tracking template (2 pages)."""
    c = canvas.Canvas(filename, pagesize=(RM2_WIDTH, RM2_HEIGHT))

    draw_item_page_1(c)
    c.showPage()
    draw_item_page_2(c)

    c.save()
    print(f"Created: {filename}")
    print(f"Page size: {RM2_WIDTH:.1f} x {RM2_HEIGHT:.1f} points")
    print(f"Pages: 2")
    print(f"Optimized for reMarkable 2 (1404 x 1872 pixels)")


if __name__ == "__main__":
    create_item_template()