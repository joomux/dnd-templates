#!/usr/bin/env python3
"""
NPC Template for reMarkable 2
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
COL_GAP = 8


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


def draw_col_label(c, x, y, label):
    """Draw a bold column sub-header label."""
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(x, y, label)


def draw_npc_continued_header(c, y):
    """Draw the NPC continuation header (pages 2+)."""
    content_width = RM2_WIDTH - 2 * MARGIN
    header_height = 35
    draw_decorative_frame(c, MARGIN, y, content_width, header_height)

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(DARK_GRAY)
    c.drawString(MARGIN + 10, y - 15, "NPC NAME (continued):")

    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(0.5)
    c.setDash([2, 2])
    c.line(MARGIN + 200, y - 19, content_width - 100, y - 19)
    c.setDash([])

    return y - header_height - 15


def draw_npc_page_1(c):
    """Draw page 1: Header, Core Identity, Relationships."""
    content_width = RM2_WIDTH - 2 * MARGIN
    col_width = (content_width - COL_GAP) / 2
    left_x = MARGIN + 5
    right_col_start = MARGIN + col_width + COL_GAP
    right_x = right_col_start + 5

    y = RM2_HEIGHT - MARGIN

    # === HEADER ===
    header_height = 52
    draw_decorative_frame(c, MARGIN, y, content_width, header_height)

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(DARK_GRAY)
    c.drawString(MARGIN + 10, y - 15, "NPC NAME:")

    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(0.5)
    c.setDash([2, 2])
    c.line(MARGIN + 100, y - 19, content_width - 100, y - 19)

    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(content_width - 85, y - 15, "Race:")
    c.line(content_width - 30, y - 19, content_width + MARGIN - 10, y - 19)
    c.setDash([])

    # Row 2: Faction and Current Location
    draw_field_with_label(c, MARGIN + 10, y - 33, "Faction:", MARGIN + 58, MARGIN + col_width - 5)
    draw_field_with_label(c, MARGIN + col_width + COL_GAP + 5, y - 33, "Current Location:", MARGIN + col_width + COL_GAP + 115, MARGIN + content_width - 5)

    y -= header_height + 15

    # === CORE IDENTITY SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Core Identity")
    y -= 5

    # 2-column row: Appearance (left) | Voice/Quirks (right)
    col_top_y = y
    draw_col_label(c, left_x, col_top_y, "Appearance")
    draw_col_label(c, right_x, col_top_y, "Voice / Quirks")

    y_col = col_top_y - 5
    draw_ruled_lines(c, left_x, y_col, col_width - 10, 5)
    draw_ruled_lines(c, right_x, y_col, col_width - 10, 5)

    y = y_col - 5 * SMALL_LINE_HEIGHT - 8

    # Other Details (formerly Notes)
    draw_col_label(c, left_x, y, "Other Details:")
    y -= 8
    y = draw_ruled_lines(c, left_x, y, content_width - 10, 5)

    y -= 12

    # === RELATIONSHIPS SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Relationships")
    y -= 5

    # 2-column row: Friends (left) | Foes (right)
    col_top_y = y
    draw_col_label(c, left_x, col_top_y, "Friends")
    draw_col_label(c, right_x, col_top_y, "Foes")

    # Draw a subtle vertical divider between the columns
    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(0.5)
    c.setDash([3, 3])
    c.line(MARGIN + col_width + COL_GAP / 2, col_top_y + 4, MARGIN + col_width + COL_GAP / 2, MARGIN + 5)
    c.setDash([])

    # Fill remaining page space with lines in both columns
    y_start = col_top_y - 5
    remaining_lines = int((y_start - MARGIN - 5) / SMALL_LINE_HEIGHT)
    draw_ruled_lines(c, left_x, y_start, col_width - 10, remaining_lines)
    draw_ruled_lines(c, right_x, y_start, col_width - 10, remaining_lines)


def draw_npc_page_2(c):
    """Draw page 2: Previous Locations and Campaign Tracking."""
    content_width = RM2_WIDTH - 2 * MARGIN
    col_width = (content_width - COL_GAP) / 2
    left_x = MARGIN + 5
    right_x = MARGIN + col_width + COL_GAP + 5

    y = RM2_HEIGHT - MARGIN

    y = draw_npc_continued_header(c, y)

    # === PREVIOUS LOCATIONS SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Previous Locations")
    y -= 5

    # 3 location entries: location name field + notes lines
    for _ in range(3):
        draw_field_with_label(c, left_x, y, "Location:", left_x + 58, MARGIN + content_width - 5)
        y -= 16
        y = draw_ruled_lines(c, left_x + 10, y, content_width - 15, 3)
        y -= 8

    y -= 10

    # === CAMPAIGN TRACKING SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Campaign Tracking")
    y -= 5

    # Each entry: Session name + Date (side by side), then context lines
    entry_height = 16 + 3 * SMALL_LINE_HEIGHT + 10
    entries_fit = int((y - MARGIN - 5) / entry_height)
    num_entries = max(3, entries_fit)

    for _ in range(num_entries):
        if y < MARGIN + 40:
            break
        draw_field_with_label(c, left_x, y, "Session:", left_x + 55, MARGIN + col_width - 5)
        draw_field_with_label(c, right_x, y, "Date:", right_x + 32, MARGIN + content_width - 5)
        y -= 16
        y = draw_ruled_lines(c, left_x + 10, y, content_width - 15, 3)
        y -= 10


def draw_npc_additional_notes_page(c, page_num):
    """Draw a full additional notes page (pages 3 and 4)."""
    content_width = RM2_WIDTH - 2 * MARGIN

    y = RM2_HEIGHT - MARGIN

    y = draw_npc_continued_header(c, y)

    # Section title distinguishes the two pages
    title = "Additional Notes" if page_num == 1 else "Additional Notes (continued)"
    y = draw_section_header(c, MARGIN, y, content_width, title)
    y -= 5

    remaining_lines = int((y - MARGIN - 5) / SMALL_LINE_HEIGHT)
    draw_ruled_lines(c, MARGIN + 5, y, content_width - 10, remaining_lines)


def create_npc_template(filename="npc_template.pdf"):
    """Generate the NPC template (4 pages)."""
    c = canvas.Canvas(filename, pagesize=(RM2_WIDTH, RM2_HEIGHT))

    # Page 1: Core Identity + Relationships
    draw_npc_page_1(c)
    c.showPage()

    # Page 2: Previous Locations + Campaign Tracking
    draw_npc_page_2(c)
    c.showPage()

    # Pages 3 & 4: Additional Notes (2 full pages)
    draw_npc_additional_notes_page(c, 1)
    c.showPage()
    draw_npc_additional_notes_page(c, 2)

    c.save()
    print(f"Created: {filename}")
    print(f"Page size: {RM2_WIDTH:.1f} x {RM2_HEIGHT:.1f} points")
    print(f"Pages: 4")
    print(f"Optimized for reMarkable 2 (1404 x 1872 pixels)")


if __name__ == "__main__":
    create_npc_template()
