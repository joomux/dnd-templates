#!/usr/bin/env python3
"""
Lazy DM Session Prep Template for reMarkable 2
Based on Sly Flourish's "Return of the Lazy Dungeon Master" method
"""

from reportlab.lib.units import mm
from reportlab.lib.colors import Color, black, white
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter

# reMarkable 2 native resolution: 1404 x 1872 pixels at 226 DPI
# Converting to points (72 DPI): 
RM2_WIDTH = 1404 * 72 / 226  # ~446.5 points
RM2_HEIGHT = 1872 * 72 / 226  # ~595.6 points

# Colors
LIGHT_GRAY = Color(0.8, 0.8, 0.8)  # For lines
MED_GRAY = Color(0.6, 0.6, 0.6)    # For decorative elements
DARK_GRAY = Color(0.3, 0.3, 0.3)  # For headers

# Spacing
MARGIN = 20
LINE_HEIGHT = 14
SMALL_LINE_HEIGHT = 12
NAV_HEIGHT = 25
HEADER_HEIGHT = 18

# Page names for navigation
PAGES = ["Overview", "Scenes", "Locations", "Secrets", "NPCs", "Combat", "Notes"]


def draw_nav_bar(c, page_width, current_page_idx):
    """Draw navigation bar at top of page with links."""
    y = RM2_HEIGHT - MARGIN - 15
    
    # Draw decorative bar background
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(1)
    c.line(MARGIN, y - 8, page_width - MARGIN, y - 8)
    c.line(MARGIN, y + 12, page_width - MARGIN, y + 12)
    
    # Calculate link positions
    link_width = (page_width - 2 * MARGIN) / len(PAGES)
    
    for i, page_name in enumerate(PAGES):
        x = MARGIN + i * link_width + link_width / 2
        
        # Highlight current page
        if i == current_page_idx:
            c.setFillColor(DARK_GRAY)
            c.setFont("Helvetica-Bold", 10)
        else:
            c.setFillColor(MED_GRAY)
            c.setFont("Helvetica", 10)
        
        c.drawCentredString(x, y, page_name)
        
        # Create clickable link area
        link_rect = (x - link_width/2 + 5, y - 5, x + link_width/2 - 5, y + 12)
        c.linkRect("", f"page{i+1}", link_rect, Border="[0 0 0]")
    
    return y - 20  # Return Y position below nav bar


def draw_section_header(c, x, y, width, title, icon=None):
    """Draw a decorated section header."""
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(DARK_GRAY)
    c.drawString(x + 12, y, title)  # Moved right to avoid corner flourish
    
    # Decorative line under header
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(1.5)
    c.line(x, y - 5, x + width, y - 5)
    
    # Corner flourishes
    draw_corner_flourish(c, x, y + 5, "tl")
    draw_corner_flourish(c, x + width, y + 5, "tr")
    
    return y - 15


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


def draw_ruled_lines(c, x, y, width, num_lines, line_height=SMALL_LINE_HEIGHT):
    """Draw light gray ruled lines for writing."""
    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(0.5)
    c.setDash([2, 2])  # Dotted line
    
    for i in range(num_lines):
        line_y = y - (i * line_height)
        c.line(x, line_y, x + width, line_y)
    
    c.setDash([])  # Reset to solid
    return y - (num_lines * line_height)


def draw_checkbox(c, x, y, size=8):
    """Draw a checkbox square."""
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(0.75)
    c.rect(x, y - size + 2, size, size)


def draw_decorative_frame(c, x, y, width, height, style="parchment"):
    """Draw a decorative frame around a section."""
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(1)
    
    # Main rectangle
    c.rect(x, y - height, width, height)
    
    # Corner decorations
    draw_corner_flourish(c, x, y, "tl")
    draw_corner_flourish(c, x + width, y, "tr")
    draw_corner_flourish(c, x, y - height, "bl")
    draw_corner_flourish(c, x + width, y - height, "br")


def draw_sword_divider(c, x, y, width):
    """Draw a decorative sword divider."""
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(0.75)
    
    mid = x + width / 2
    
    # Main line
    c.line(x + 20, y, mid - 15, y)
    c.line(mid + 15, y, x + width - 20, y)
    
    # Sword shape in middle
    c.line(mid - 12, y, mid + 12, y)  # Blade
    c.line(mid - 3, y - 3, mid - 3, y + 3)  # Guard
    c.line(mid + 3, y - 3, mid + 3, y + 3)  # Guard
    c.circle(mid, y, 2, fill=0)  # Pommel hint


# ============ PAGE 1: OVERVIEW ============

def draw_page1_overview(c):
    """Draw Page 1: Overview with header, characters, strong start, story beats."""
    page_width = RM2_WIDTH
    content_width = page_width - 2 * MARGIN
    
    # Add bookmark/destination for navigation
    c.bookmarkPage("page1")
    
    # Navigation bar
    y = draw_nav_bar(c, page_width, 0)
    
    # === HEADER BLOCK ===
    y -= 10
    draw_decorative_frame(c, MARGIN, y, content_width, 45, "banner")
    
    # Campaign field spans full width on top row
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(DARK_GRAY)
    c.drawString(MARGIN + 10, y - 12, "Campaign:")
    
    # Underline for campaign
    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(0.5)
    c.line(MARGIN + 70, y - 16, content_width + MARGIN - 10, y - 16)
    
    # Session # and Date on second row, smaller
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN + 10, y - 35, "Session #")
    c.drawString(MARGIN + 150, y - 35, "Date:")
    
    # Underlines for session and date
    c.line(MARGIN + 65, y - 39, MARGIN + 130, y - 39)
    c.line(MARGIN + 180, y - 39, MARGIN + 280, y - 39)
    
    y -= 60
    
    # === TWO COLUMN SECTION: Characters (left) and Session Recap (right) ===
    col_width = (content_width - 10) / 2
    section_start_y = y
    
    # Left column: Review the Characters
    y = draw_section_header(c, MARGIN, y, col_width, "Review the Characters")
    y -= 5
    
    # 4 character slots (removed PC 5)
    for i in range(4):
        c.setFont("Helvetica", 9)
        c.setFillColor(MED_GRAY)
        c.drawString(MARGIN + 5, y, f"PC {i+1}:")
        y = draw_ruled_lines(c, MARGIN + 35, y, col_width - 35, 2)
        y -= 5
    
    left_col_end_y = y
    
    # Right column: Session Recap
    right_col_x = MARGIN + col_width + 10
    y = section_start_y
    y = draw_section_header(c, right_col_x, y, col_width, "Session Recap")
    y -= 5
    
    # Ruled lines for recap
    y = draw_ruled_lines(c, right_col_x + 5, y, col_width - 10, 9)
    
    # Use the lower of the two columns
    y = min(left_col_end_y, y)
    
    y -= 10
    
    # === STRONG START ===
    y = draw_section_header(c, MARGIN, y, content_width, "Strong Start")
    y -= 5
    
    frame_height = 140
    draw_decorative_frame(c, MARGIN, y, content_width, frame_height)
    y = draw_ruled_lines(c, MARGIN + 10, y - 15, content_width - 20, 10)
    
    y -= 20
    
    # === STORY BEATS (3 columns) ===
    y = draw_section_header(c, MARGIN, y, content_width, "Story Beats")
    y -= 5
    
    # Calculate remaining space and fill with 3 columns
    remaining_height = y - MARGIN - 10
    num_lines = int(remaining_height / SMALL_LINE_HEIGHT)
    
    col3_width = (content_width - 20) / 3
    
    for i in range(num_lines):
        c.setStrokeColor(LIGHT_GRAY)
        c.setLineWidth(0.5)
        c.setDash([2, 2])
        
        # Left column
        c.line(MARGIN + 5, y, MARGIN + col3_width - 5, y)
        
        # Middle column
        c.line(MARGIN + col3_width + 10, y, MARGIN + 2 * col3_width + 5, y)
        
        # Right column
        c.line(MARGIN + 2 * col3_width + 15, y, MARGIN + content_width - 5, y)
        
        y -= SMALL_LINE_HEIGHT
    
    c.setDash([])


# ============ PAGE 2: SCENES ============

def draw_page2_scenes(c):
    """Draw Page 2: Potential Scenes (full page)."""
    page_width = RM2_WIDTH
    content_width = page_width - 2 * MARGIN
    
    c.bookmarkPage("page2")
    y = draw_nav_bar(c, page_width, 1)
    
    # === POTENTIAL SCENES ===
    y -= 10
    y = draw_section_header(c, MARGIN, y, content_width, "Potential Scenes")
    y -= 5
    
    # 7 scene blocks to fill the page
    for i in range(7):
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(MED_GRAY)
        c.drawString(MARGIN + 5, y, f"Scene {i+1}:")
        c.setStrokeColor(LIGHT_GRAY)
        c.line(MARGIN + 50, y - 3, content_width + MARGIN, y - 3)
        y -= 15  # Space before first dotted line
        y = draw_ruled_lines(c, MARGIN + 10, y, content_width - 10, 4)
        y -= 8


# ============ PAGE 3: LOCATIONS ============

def draw_page3_locations(c):
    """Draw Page 3: Fantastic Locations (full page)."""
    page_width = RM2_WIDTH
    content_width = page_width - 2 * MARGIN
    
    c.bookmarkPage("page3")
    y = draw_nav_bar(c, page_width, 2)
    
    # === FANTASTIC LOCATIONS ===
    y -= 10
    y = draw_section_header(c, MARGIN, y, content_width, "Fantastic Locations")
    y -= 5
    
    # 8 location blocks to fill the page
    for i in range(8):
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(MED_GRAY)
        c.drawString(MARGIN + 5, y, f"Location {i+1}:")
        c.setStrokeColor(LIGHT_GRAY)
        c.line(MARGIN + 65, y - 3, content_width + MARGIN, y - 3)
        y -= 15  # Space before Features
        
        c.setFont("Helvetica", 8)
        c.setFillColor(LIGHT_GRAY)
        c.drawString(MARGIN + 10, y, "Features:")
        y = draw_ruled_lines(c, MARGIN + 55, y, content_width - 55, 3)
        y -= 8


# ============ PAGE 4: SECRETS & LOOT ============

def draw_page4_secrets(c):
    """Draw Page 4: Secrets/Clues and Loot & Rewards."""
    page_width = RM2_WIDTH
    content_width = page_width - 2 * MARGIN
    
    c.bookmarkPage("page4")
    y = draw_nav_bar(c, page_width, 3)
    
    # === SECRETS AND CLUES ===
    y -= 10
    y = draw_section_header(c, MARGIN, y, content_width, "Secrets and Clues")
    y -= 5
    
    # 10 secrets with checkboxes
    for i in range(10):
        draw_checkbox(c, MARGIN + 5, y)
        c.setFont("Helvetica", 9)
        c.setFillColor(MED_GRAY)
        c.drawString(MARGIN + 18, y - 6, f"{i+1}.")
        y = draw_ruled_lines(c, MARGIN + 30, y - 6, content_width - 30, 2)
        y -= 5
    
    y -= 5
    
    # === LOOT & REWARDS (2 columns, fill remainder of page) ===
    y = draw_section_header(c, MARGIN, y, content_width, "Loot & Rewards")
    y -= 5
    
    col_width = (content_width - 10) / 2
    remaining_height = y - MARGIN - 10
    num_rows = int(remaining_height / SMALL_LINE_HEIGHT) + 1
    
    # Draw lines for both columns
    for i in range(num_rows):
        c.setStrokeColor(LIGHT_GRAY)
        c.setLineWidth(0.5)
        c.setDash([2, 2])
        
        # Left column
        c.line(MARGIN + 5, y, MARGIN + col_width - 5, y)
        
        # Right column
        c.line(MARGIN + col_width + 15, y, MARGIN + content_width - 5, y)
        
        y -= SMALL_LINE_HEIGHT
    
    c.setDash([])


# ============ PAGE 5: NPCs ============

def draw_page5_npcs(c):
    """Draw Page 5: Important NPCs (full page)."""
    page_width = RM2_WIDTH
    content_width = page_width - 2 * MARGIN
    
    c.bookmarkPage("page5")
    y = draw_nav_bar(c, page_width, 4)
    
    # === IMPORTANT NPCs ===
    y -= 10
    y = draw_section_header(c, MARGIN, y, content_width, "Important NPCs")
    y -= 5
    
    # 4 NPC blocks with Notes field (reduced from 5 to fit with Notes)
    for i in range(4):
        # NPC frame - taller to fit all fields including Notes
        frame_height = 105
        draw_decorative_frame(c, MARGIN, y, content_width, frame_height)
        
        inner_y = y - 14
        c.setFont("Helvetica-Bold", 9)
        c.setFillColor(MED_GRAY)
        c.drawString(MARGIN + 8, inner_y, "Name:")
        c.setStrokeColor(LIGHT_GRAY)
        c.setLineWidth(0.5)
        c.setDash([2, 2])
        c.line(MARGIN + 40, inner_y - 3, MARGIN + 200, inner_y - 3)
        
        # Faction field on same line as name
        c.setFont("Helvetica", 8)
        c.setFillColor(MED_GRAY)
        c.drawString(MARGIN + 210, inner_y, "Faction:")
        c.setStrokeColor(LIGHT_GRAY)
        c.line(MARGIN + 250, inner_y - 3, content_width + MARGIN - 10, inner_y - 3)
        
        inner_y -= 16
        c.drawString(MARGIN + 8, inner_y, "Appearance:")
        c.line(MARGIN + 60, inner_y - 3, content_width + MARGIN - 10, inner_y - 3)
        
        inner_y -= 16
        c.drawString(MARGIN + 8, inner_y, "Motivation:")
        c.line(MARGIN + 55, inner_y - 3, content_width + MARGIN - 10, inner_y - 3)
        
        inner_y -= 16
        c.drawString(MARGIN + 8, inner_y, "Voice/Quirk:")
        c.line(MARGIN + 58, inner_y - 3, content_width + MARGIN - 10, inner_y - 3)
        
        inner_y -= 16
        c.drawString(MARGIN + 8, inner_y, "Notes:")
        c.line(MARGIN + 40, inner_y - 3, content_width + MARGIN - 10, inner_y - 3)
        # Second notes line
        inner_y -= 12
        c.line(MARGIN + 10, inner_y - 3, content_width + MARGIN - 10, inner_y - 3)
        
        c.setDash([])
        y -= frame_height + 12


# ============ PAGE 6: COMBAT ============

def draw_initiative_tracker(c, x, y, width, height, tracker_num):
    """Draw a single initiative tracker box."""
    draw_decorative_frame(c, x, y, width, height)
    
    inner_y = y - 12
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(MED_GRAY)
    c.drawString(x + 5, inner_y, f"Encounter {tracker_num}:")
    c.setStrokeColor(LIGHT_GRAY)
    c.line(x + 70, inner_y - 3, x + width - 10, inner_y - 3)
    
    inner_y -= 18
    
    # Column headers
    c.setFont("Helvetica", 7)
    c.setFillColor(LIGHT_GRAY)
    c.drawString(x + 5, inner_y, "Init")
    c.drawString(x + 30, inner_y, "Name")
    c.drawString(x + width - 70, inner_y, "HP")
    c.drawString(x + width - 30, inner_y, "Notes")
    
    inner_y -= 10
    
    # 12 rows for combatants (increased from 8)
    for i in range(12):
        c.setStrokeColor(LIGHT_GRAY)
        c.setLineWidth(0.5)
        c.setDash([1, 2])
        
        # Init box
        c.rect(x + 5, inner_y - 10, 18, 12)
        
        # Name line
        c.line(x + 28, inner_y - 8, x + width - 75, inner_y - 8)
        
        # HP boxes (5 small boxes)
        for j in range(5):
            c.rect(x + width - 70 + (j * 10), inner_y - 10, 8, 10)
        
        # Notes line
        c.line(x + width - 18, inner_y - 8, x + width - 5, inner_y - 8)
        
        inner_y -= 12
    
    c.setDash([])


def draw_page6_combat(c):
    """Draw Page 6: Combat with 2x2 initiative trackers and monster reference."""
    page_width = RM2_WIDTH
    content_width = page_width - 2 * MARGIN
    
    c.bookmarkPage("page6")
    y = draw_nav_bar(c, page_width, 5)
    
    # === INITIATIVE TRACKERS (2x2) ===
    y -= 10
    y = draw_section_header(c, MARGIN, y, content_width, "Initiative Trackers")
    y -= 5
    
    tracker_width = (content_width - 10) / 2
    tracker_height = 195  # Taller for more rows
    
    # Top row
    draw_initiative_tracker(c, MARGIN, y, tracker_width, tracker_height, 1)
    draw_initiative_tracker(c, MARGIN + tracker_width + 10, y, tracker_width, tracker_height, 2)
    
    y -= tracker_height + 10
    
    # Bottom row
    draw_initiative_tracker(c, MARGIN, y, tracker_width, tracker_height, 3)
    draw_initiative_tracker(c, MARGIN + tracker_width + 10, y, tracker_width, tracker_height, 4)
    
    y -= tracker_height + 15
    
    # === MONSTERS REFERENCE (2 columns) ===
    y = draw_section_header(c, MARGIN, y, content_width, "Monsters Reference")
    y -= 5
    
    col_width = (content_width - 10) / 2
    
    # Column headers
    c.setFont("Helvetica", 8)
    c.setFillColor(LIGHT_GRAY)
    c.drawString(MARGIN + 5, y, "Monster")
    c.drawString(MARGIN + col_width - 40, y, "Page")
    c.drawString(MARGIN + col_width + 15, y, "Monster")
    c.drawString(MARGIN + content_width - 35, y, "Page")
    
    y -= 14
    
    # Draw lines for both columns (4 rows each)
    for i in range(4):
        c.setStrokeColor(LIGHT_GRAY)
        c.setLineWidth(0.5)
        c.setDash([2, 2])
        
        # Left column
        c.line(MARGIN + 5, y, MARGIN + col_width - 50, y)
        c.line(MARGIN + col_width - 45, y, MARGIN + col_width - 5, y)
        
        # Right column
        c.line(MARGIN + col_width + 15, y, MARGIN + content_width - 45, y)
        c.line(MARGIN + content_width - 40, y, MARGIN + content_width - 5, y)
        
        y -= 12
    
    c.setDash([])


# ============ PAGE 7: SESSION NOTES ============

def draw_page7_notes(c):
    """Draw Page 7: Session Notes (full page of ruled lines)."""
    page_width = RM2_WIDTH
    content_width = page_width - 2 * MARGIN
    
    c.bookmarkPage("page7")
    y = draw_nav_bar(c, page_width, 6)
    
    # === SESSION NOTES ===
    y -= 10
    y = draw_section_header(c, MARGIN, y, content_width, "Session Notes")
    y -= 5
    
    # Fill the rest of the page with ruled lines
    remaining_height = y - MARGIN - 10
    num_lines = int(remaining_height / SMALL_LINE_HEIGHT)
    
    draw_ruled_lines(c, MARGIN + 5, y, content_width - 10, num_lines)


# ============ MAIN ============

def create_lazy_dm_template(filename="lazy_dm_session_template.pdf"):
    """Generate the complete Lazy DM session prep template."""
    c = canvas.Canvas(filename, pagesize=(RM2_WIDTH, RM2_HEIGHT))
    
    # Page 1: Overview
    draw_page1_overview(c)
    c.showPage()
    
    # Page 2: Scenes
    draw_page2_scenes(c)
    c.showPage()
    
    # Page 3: Locations
    draw_page3_locations(c)
    c.showPage()
    
    # Page 4: Secrets & Loot
    draw_page4_secrets(c)
    c.showPage()
    
    # Page 5: NPCs
    draw_page5_npcs(c)
    c.showPage()
    
    # Page 6: Combat
    draw_page6_combat(c)
    c.showPage()
    
    # Page 7: Session Notes
    draw_page7_notes(c)
    
    c.save()
    print(f"Created: {filename}")
    print(f"Page size: {RM2_WIDTH:.1f} x {RM2_HEIGHT:.1f} points")
    print(f"Pages: 7")
    print(f"Optimized for reMarkable 2 (1404 x 1872 pixels)")


if __name__ == "__main__":
    create_lazy_dm_template()
