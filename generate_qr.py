#!/usr/bin/env python3
"""
Generate QR codes and print materials for Spice Affair menu
"""

import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont
import os
from reportlab.lib.pagesizes import A4, letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, mm
from reportlab.lib.colors import Color
import io

# Configuration
MENU_URL = "https://menu.spiceaffair.com"
QR_ERROR_CORRECTION = ERROR_CORRECT_H
BRAND_GREEN = Color(0.176, 0.353, 0.239)  # #2d5a3d
OUTPUT_DIR = "print"

def create_qr_code(url, filename, size=(1000, 1000), format='PNG'):
    """Create QR code with high error correction"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=QR_ERROR_CORRECTION,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Resize to specified size
    qr_img = qr_img.resize(size, Image.Resampling.LANCZOS)
    
    # Save the image
    qr_img.save(filename, format=format)
    print(f"QR code saved: {filename}")
    return qr_img

def create_svg_qr(url, filename):
    """Create SVG QR code"""
    import qrcode.image.svg
    
    factory = qrcode.image.svg.SvgPathImage
    qr = qrcode.QRCode(
        version=1,
        error_correction=QR_ERROR_CORRECTION,
        box_size=10,
        border=4,
        image_factory=factory
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    img = qr.make_image()
    img.save(filename)
    print(f"SVG QR code saved: {filename}")

def create_a4_poster(qr_image_path, output_path):
    """Create A4 poster with QR code"""
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Set up colors
    c.setFillColor(BRAND_GREEN)
    
    # Background
    c.rect(0, 0, width, height, fill=1)
    
    # White content area
    margin = 40
    content_width = width - 2 * margin
    content_height = height - 2 * margin
    
    c.setFillColorRGB(1, 1, 1)  # White
    c.rect(margin, margin, content_width, content_height, fill=1)
    
    # Title
    c.setFillColor(BRAND_GREEN)
    c.setFont("Helvetica-Bold", 36)
    title_text = "Spice Affair"
    title_width = c.stringWidth(title_text, "Helvetica-Bold", 36)
    c.drawString((width - title_width) / 2, height - 100, title_text)
    
    # Subtitle
    c.setFont("Helvetica", 18)
    subtitle_text = "Digital Menu"
    subtitle_width = c.stringWidth(subtitle_text, "Helvetica", 18)
    c.drawString((width - subtitle_width) / 2, height - 130, subtitle_text)
    
    # QR Code
    qr_size = 300
    qr_x = (width - qr_size) / 2
    qr_y = height / 2 - qr_size / 2
    
    c.drawImage(qr_image_path, qr_x, qr_y, qr_size, qr_size)
    
    # Instructions
    c.setFont("Helvetica-Bold", 24)
    instruction_text = "Scan to browse. Order with the chef."
    instruction_width = c.stringWidth(instruction_text, "Helvetica-Bold", 24)
    c.drawString((width - instruction_width) / 2, qr_y - 60, instruction_text)
    
    # URL
    c.setFont("Helvetica", 14)
    url_text = MENU_URL
    url_width = c.stringWidth(url_text, "Helvetica", 14)
    c.drawString((width - url_width) / 2, qr_y - 90, url_text)
    
    # Motto
    c.setFont("Helvetica-Oblique", 16)
    motto_text = "Where flavor becomes desire"
    motto_width = c.stringWidth(motto_text, "Helvetica-Oblique", 16)
    c.drawString((width - motto_width) / 2, 80, motto_text)
    
    c.save()
    print(f"A4 poster saved: {output_path}")

def create_sticker_4x4(qr_image_path, output_path):
    """Create 4x4 inch sticker"""
    size = (4 * inch, 4 * inch)
    c = canvas.Canvas(output_path, pagesize=size)
    width, height = size
    
    # Background
    c.setFillColor(BRAND_GREEN)
    c.rect(0, 0, width, height, fill=1)
    
    # White border
    border = 0.1 * inch
    c.setFillColorRGB(1, 1, 1)  # White
    c.rect(border, border, width - 2 * border, height - 2 * border, fill=1)
    
    # Title
    c.setFillColor(BRAND_GREEN)
    c.setFont("Helvetica-Bold", 18)
    title_text = "Spice Affair"
    title_width = c.stringWidth(title_text, "Helvetica-Bold", 18)
    c.drawString((width - title_width) / 2, height - 0.6 * inch, title_text)
    
    # QR Code
    qr_size = 2 * inch
    qr_x = (width - qr_size) / 2
    qr_y = (height - qr_size) / 2 - 0.2 * inch
    
    c.drawImage(qr_image_path, qr_x, qr_y, qr_size, qr_size)
    
    # Instructions
    c.setFont("Helvetica-Bold", 10)
    instruction_text = "Scan to browse. Order with the chef."
    instruction_width = c.stringWidth(instruction_text, "Helvetica-Bold", 10)
    c.drawString((width - instruction_width) / 2, qr_y - 0.4 * inch, instruction_text)
    
    c.save()
    print(f"4x4 sticker saved: {output_path}")

def main():
    """Generate all QR codes and print materials"""
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate QR codes
    qr_svg_path = os.path.join(OUTPUT_DIR, "qr-menu.svg")
    qr_png_path = os.path.join(OUTPUT_DIR, "qr-menu-1000.png")
    
    create_svg_qr(MENU_URL, qr_svg_path)
    create_qr_code(MENU_URL, qr_png_path, size=(1000, 1000))
    
    # Generate print materials
    poster_path = os.path.join(OUTPUT_DIR, "qr-poster-A4.pdf")
    sticker_path = os.path.join(OUTPUT_DIR, "qr-sticker-4x4in.pdf")
    
    create_a4_poster(qr_png_path, poster_path)
    create_sticker_4x4(qr_png_path, sticker_path)
    
    print("\nAll QR codes and print materials generated successfully!")
    print(f"Files created in '{OUTPUT_DIR}' directory:")
    print("- qr-menu.svg")
    print("- qr-menu-1000.png")
    print("- qr-poster-A4.pdf")
    print("- qr-sticker-4x4in.pdf")

if __name__ == "__main__":
    main()

