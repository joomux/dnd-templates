#!/usr/bin/env python3
"""
Faction Tracking Template for reMarkable 2
Based on the Game Master's Handbook of Proactive Roleplaying
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


def draw_sword_divider(c, x, y, width):
    """Draw a decorative sword divider."""
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(0.75)
    
    mid = x + width / 2
    
    c.line(x + 20, y, mid - 15, y)
    c.line(mid + 15, y, x + width - 20, y)
    
    c.line(mid - 12, y, mid + 12, y)
    c.line(mid - 3, y - 3, mid - 3, y + 3)
    c.line(mid + 3, y - 3, mid + 3, y + 3)
    c.circle(mid, y, 2, fill=0)


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


def draw_progress_clock(c, x, y, width):
    """Draw a progress track as a horizontal scale (matching disposition style)."""
    scale_width = width - 20
    start_x = x + 10
    
    labels = ["Nascent", "Emerging", "Advancing", "Imminent", "Complete"]
    num_labels = len(labels)
    segment_width = scale_width / (num_labels - 1)
    
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(1)
    c.line(start_x, y, start_x + scale_width, y)
    
    c.setFont("Helvetica", 8)
    c.setFillColor(MED_GRAY)
    
    for i, label in enumerate(labels):
        tick_x = start_x + i * segment_width
        c.line(tick_x, y - 5, tick_x, y + 5)
        
        label_width = c.stringWidth(label, "Helvetica", 8)
        c.drawString(tick_x - label_width/2, y - 16, label)
    
    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(0.5)
    minor_ticks = 3
    for i in range(num_labels - 1):
        for j in range(1, minor_ticks + 1):
            tick_x = start_x + i * segment_width + j * (segment_width / (minor_ticks + 1))
            c.line(tick_x, y - 3, tick_x, y + 3)


def draw_disposition_scale(c, x, y, width):
    """Draw a horizontal disposition scale with tick marks."""
    scale_width = width - 20
    start_x = x + 10
    
    labels = ["Hostile", "Wary", "Neutral", "Friendly", "Allied"]
    num_labels = len(labels)
    segment_width = scale_width / (num_labels - 1)
    
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(1)
    c.line(start_x, y, start_x + scale_width, y)
    
    c.setFont("Helvetica", 8)
    c.setFillColor(MED_GRAY)
    
    for i, label in enumerate(labels):
        tick_x = start_x + i * segment_width
        c.line(tick_x, y - 5, tick_x, y + 5)
        
        label_width = c.stringWidth(label, "Helvetica", 8)
        c.drawString(tick_x - label_width/2, y - 16, label)
    
    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(0.5)
    minor_ticks = 3
    for i in range(num_labels - 1):
        for j in range(1, minor_ticks + 1):
            tick_x = start_x + i * segment_width + j * (segment_width / (minor_ticks + 1))
            c.line(tick_x, y - 3, tick_x, y + 3)


def draw_faction_page(c, page_num):
    """Draw a single faction tracking page."""
    page_width = RM2_WIDTH
    content_width = page_width - 2 * MARGIN
    
    y = RM2_HEIGHT - MARGIN
    
    # === HEADER SECTION ===
    header_height = 35
    draw_decorative_frame(c, MARGIN, y, content_width, header_height)
    
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(DARK_GRAY)
    c.drawString(MARGIN + 10, y - 15, "FACTION:")
    
    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(0.5)
    c.setDash([2, 2])
    c.line(MARGIN + 75, y - 19, content_width - 100, y - 19)
    
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(content_width - 85, y - 15, "Alignment:")
    c.line(content_width - 30, y - 19, content_width + MARGIN - 10, y - 19)
    c.setDash([])
    
    y -= header_height + 15
    
    # === CORE IDENTITY SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Core Identity")
    y -= 5
    
    draw_field_with_label(c, MARGIN + 5, y, "Leader/Key Figure:", 
                          MARGIN + 100, content_width + MARGIN - 5)
    y -= 18
    
    draw_field_with_label(c, MARGIN + 5, y, "Primary Location:", 
                          MARGIN + 95, content_width + MARGIN - 5)
    y -= 18
    
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + 5, y, "Goal (What They Want):")
    y -= 12
    y = draw_ruled_lines(c, MARGIN + 10, y, content_width - 15, 4)
    
    y -= 8
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + 5, y, "Resources:")
    y -= 15
    
    # Resource trackers - 2x2 grid layout
    box_size = 10
    box_spacing = 3
    label_width_max = 55
    col_width = (content_width - 10) / 2
    
    # Row 1: Troops (left) and Magic (right)
    c.setFont("Helvetica", 8)
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + 10, y, "Troops:")
    box_start_x = MARGIN + label_width_max
    for j in range(5):
        c.setStrokeColor(MED_GRAY)
        c.setLineWidth(0.75)
        c.rect(box_start_x + j * (box_size + box_spacing), y - 2, box_size, box_size)
    
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + col_width + 10, y, "Magic:")
    box_start_x_right = MARGIN + col_width + label_width_max - 5
    for j in range(5):
        c.setStrokeColor(MED_GRAY)
        c.setLineWidth(0.75)
        c.rect(box_start_x_right + j * (box_size + box_spacing), y - 2, box_size, box_size)
    
    y -= 16
    
    # Row 2: Money (left) and Influence (right)
    c.setFont("Helvetica", 8)
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + 10, y, "Money:")
    box_start_x = MARGIN + label_width_max
    for j in range(5):
        c.setStrokeColor(MED_GRAY)
        c.setLineWidth(0.75)
        c.rect(box_start_x + j * (box_size + box_spacing), y - 2, box_size, box_size)
    
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + col_width + 10, y, "Influence:")
    box_start_x_right = MARGIN + col_width + label_width_max - 5
    for j in range(5):
        c.setStrokeColor(MED_GRAY)
        c.setLineWidth(0.75)
        c.rect(box_start_x_right + j * (box_size + box_spacing), y - 2, box_size, box_size)
    
    y -= 16
    
    y -= 5
    c.setFont("Helvetica", 8)
    c.setFillColor(LIGHT_GRAY)
    c.drawString(MARGIN + 10, y, "Notes:")
    y -= 10
    y = draw_ruled_lines(c, MARGIN + 10, y, content_width - 15, 3)
    
    y -= 10
    
    # === CURRENT ACTIVITY SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Current Activity")
    y -= 5
    
    frame_height = 65
    draw_decorative_frame(c, MARGIN, y, content_width, frame_height)
    
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + 8, y - 12, "Current Plan/Front:")
    y_inner = draw_ruled_lines(c, MARGIN + 10, y - 22, content_width - 20, 3)
    
    y -= frame_height + 12
    
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + 5, y, "Progress Clock:")
    y -= 22
    draw_progress_clock(c, MARGIN, y, content_width)
    
    y -= 38
    
    # === NOTES SECTION (Page 1) ===
    y = draw_section_header(c, MARGIN, y, content_width, "Notes")
    y -= 5
    
    draw_ruled_lines(c, MARGIN + 5, y, content_width - 10, 5)


def draw_faction_page_2(c):
    """Draw the second page of faction tracking (Relationships and Intelligence)."""
    page_width = RM2_WIDTH
    content_width = page_width - 2 * MARGIN
    
    y = RM2_HEIGHT - MARGIN
    
    # === RELATIONSHIPS SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Relationships")
    y -= 5
    
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + 5, y, "Disposition Toward PCs:")
    y -= 25
    draw_disposition_scale(c, MARGIN, y, content_width)
    
    y -= 35
    
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + 5, y, "Connections to Other Factions:")
    y -= 15
    
    col_width = (content_width - 20) / 2
    for i in range(4):
        c.setFont("Helvetica", 8)
        c.setFillColor(LIGHT_GRAY)
        c.drawString(MARGIN + 10, y, "Faction:")
        c.drawString(MARGIN + col_width + 10, y, "Relationship:")
        
        c.setStrokeColor(LIGHT_GRAY)
        c.setLineWidth(0.5)
        c.setDash([2, 2])
        c.line(MARGIN + 50, y - 3, MARGIN + col_width, y - 3)
        c.line(MARGIN + col_width + 70, y - 3, content_width + MARGIN - 5, y - 3)
        c.setDash([])
        y -= 14
    
    y -= 15
    
    # === INTELLIGENCE SECTION ===
    y = draw_section_header(c, MARGIN, y, content_width, "Intelligence")
    y -= 5
    
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + 5, y, "Known Agents/NPCs:")
    y -= 15
    
    for i in range(5):
        c.setFont("Helvetica", 8)
        c.setFillColor(LIGHT_GRAY)
        c.drawString(MARGIN + 10, y, "Name:")
        c.drawString(MARGIN + col_width - 20, y, "Role:")
        
        c.setStrokeColor(LIGHT_GRAY)
        c.setLineWidth(0.5)
        c.setDash([2, 2])
        c.line(MARGIN + 45, y - 3, MARGIN + col_width - 30, y - 3)
        c.line(MARGIN + col_width + 5, y - 3, content_width + MARGIN - 5, y - 3)
        c.setDash([])
        y -= 14
    
    y -= 10
    
    # Strengths and Weaknesses - 2 columns
    col_width_half = (content_width - 15) / 2
    
    c.setFont("Helvetica", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(MARGIN + 5, y, "Strengths:")
    c.drawString(MARGIN + col_width_half + 15, y, "Weaknesses:")
    y -= 12
    
    # Draw 5 lines for each column
    for i in range(5):
        c.setStrokeColor(LIGHT_GRAY)
        c.setLineWidth(0.5)
        c.setDash([2, 2])
        # Left column (Strengths)
        c.line(MARGIN + 10, y, MARGIN + col_width_half, y)
        # Right column (Weaknesses)
        c.line(MARGIN + col_width_half + 15, y, content_width + MARGIN - 5, y)
        c.setDash([])
        y -= SMALL_LINE_HEIGHT
    
    y -= 10
    
    # === NOTES (Page 2) ===
    y = draw_section_header(c, MARGIN, y, content_width, "Notes")
    y -= 5
    
    remaining_lines = int((y - MARGIN - 10) / SMALL_LINE_HEIGHT)
    draw_ruled_lines(c, MARGIN + 5, y, content_width - 10, remaining_lines)


def create_faction_template(filename="faction_tracking_template.pdf"):
    """Generate the faction tracking template (2 pages for 1 faction)."""
    c = canvas.Canvas(filename, pagesize=(RM2_WIDTH, RM2_HEIGHT))
    
    draw_faction_page(c, 1)
    c.showPage()
    draw_faction_page_2(c)
    
    c.save()
    print(f"Created: {filename}")
    print(f"Page size: {RM2_WIDTH:.1f} x {RM2_HEIGHT:.1f} points")
    print(f"Pages: 2 (1 faction)")
    print(f"Optimized for reMarkable 2 (1404 x 1872 pixels)")


if __name__ == "__main__":
    create_faction_template()
