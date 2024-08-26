from flask import Flask, render_template, request, send_file
from reportlab.lib.pagesizes import inch
from reportlab.pdfgen import canvas
from PIL import Image
import os

app = Flask(__name__)

# Manually define the tabloid size (11 inches x 17 inches)
TABLOID = (11 * inch, 17 * inch)

# Add all the tl image mappings
TILE_IMAGES = {
    "tl1": "assets/tiles/tl2 weight+mass.png",
    "tl2": "assets/tiles/tl3 volume & capacity.png",
    "tl3": "assets/tiles/tl4 Time.png",
    "tl4": "assets/tiles/tl5 speed.png",
    "tl5": "assets/tiles/tl6 energy.png",
    "tl6": "assets/tiles/tl9 power.png",
    "tl7": "assets/tiles/tl10 pressure.png",
    "tl8": "assets/tiles/tl11 didgital storage.png",
    "tl9": "assets/tiles/tl13 angles.png",
    "tl10": "assets/tiles/tl14 currency.png",
    "tl11": "assets/tiles/tl15 cooking.png",
    "tl12": "assets/tiles/tl16 constitutional law.png",
    "tl13": "assets/tiles/tl17 contract law.png",
    "tl14": "assets/tiles/tl18 criminal law.png",
    "tl15": "assets/tiles/tl19 business law.png",
    "tl16": "assets/tiles/tl20 property law.png",
    "tl17": "assets/tiles/tl21 tort law.png",
    "tl18": "assets/tiles/tl22 software development.png",
    "tl19": "assets/tiles/tl23 cybersecurity.png",
    "tl20": "assets/tiles/tl24 networking basics.png",
    "tl21": "assets/tiles/tl25 computer architecture.png",
    "tl22": "assets/tiles/tl26 common algorithms.png",
    "tl23": "assets/tiles/tl27 data structures.png",
    "tl24": "assets/tiles/tl28_basic_programming_concepts.png",
    "tl25": "assets/tiles/tl29 cognitive biases.png",
    "tl26": "assets/tiles/tl30 learning theories.png",
    "tl27": "assets/tiles/tl32 mental health disorders.png",
    "tl28": "assets/tiles/tl33 therapeutic approaches.png",
    "tl29": "assets/tiles/tl34 syntax.png",
    "tl30": "assets/tiles/tl35 phonetics.png",
    "tl31": "assets/tiles/tl36 morphology.png",
    "tl32": "assets/tiles/tl37 semantics.png",
    "tl33": "assets/tiles/tl38 pragmatics.png",
    "tl34": "assets/tiles/tl39 advanced vocabulary.png",
    "tl35": "assets/tiles/tl40 business vocabulary.png",
    "tl36": "assets/tiles/tl41 academic vocabulary.png",
    "tl37": "assets/tiles/tl42 common suffixes.png",
    "tl38": "assets/tiles/tl43 cooking techniques.png",
    "tl39": "assets/tiles/tl44 nutrition; macronutrients.png",
    "tl40": "assets/tiles/tl45 herbs & spices.png",
    "tl41": "assets/tiles/tl46 dietary requirements.png",
    "tl42": "assets/tiles/tl47 food safety.png",
    "tl43": "assets/tiles/tl48 10 commandments.png",
    "tl44": "assets/tiles/tl49 the beatitudes.png",
    "tl45": "assets/tiles/tl50 the fruit of the spirit.png",
    "tl46": "assets/tiles/tl51 the lords prayer.png"
}

@app.route('/')
def index():
    return render_template('collage.html')

@app.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    rsid_code = request.form['rsid_code']
    output_pdf_path = "generated/collage.pdf"
    
    # Create a new PDF on manually defined tabloid size paper
    c = canvas.Canvas(output_pdf_path, pagesize=TABLOID)

    # Parse the RSID code to get the tile IDs
    tile_ids = [pair.split(':')[1] for pair in rsid_code.split('|')]
    
    # Calculate split index for front and back
    half_index = len(tile_ids) // 2
    front_tile_ids = tile_ids[:half_index]
    back_tile_ids = tile_ids[half_index:]

    # Set up the grid dimensions for credit card size tiles
    x_start = 0.75 * inch  # Increased margin to avoid going off the page
    y_start = 15.5 * inch  # Starting position on the tabloid paper
    max_image_width = 3.25 * inch  # Adjusted size to maintain aspect ratio
    max_image_height = 2.0 * inch  # Adjusted size to maintain aspect ratio
    images_per_row = 3

    def draw_tiles(tile_ids, c, x_start, y_start, images_per_row, front=True):
        x = x_start
        y = y_start
        for index, tile_id in enumerate(tile_ids):
            if tile_id in TILE_IMAGES:
                img_path = TILE_IMAGES[tile_id]
                if os.path.exists(img_path):
                    # Open the image
                    img = Image.open(img_path)
                    img_width, img_height = img.size
                    aspect_ratio = img_width / img_height

                    # Determine the appropriate width and height to maintain aspect ratio
                    if img_width > max_image_width or img_height > max_image_height:
                        if aspect_ratio > 1:  # Landscape orientation
                            img_width = max_image_width
                            img_height = max_image_width / aspect_ratio
                        else:  # Portrait orientation or square
                            img_height = max_image_height
                            img_width = max_image_height * aspect_ratio

                    # Draw the image on the canvas
                    c.drawImage(img_path, x, y, width=img_width, height=img_height)

                    x += max_image_width + 0.25 * inch  # Spacing between tiles
                    if (index + 1) % images_per_row == 0:
                        x = x_start
                        y -= max_image_height + 0.5 * inch  # Move to next row

    # Draw front side
    draw_tiles(front_tile_ids, c, x_start, y_start, images_per_row, front=True)
    c.showPage()

    # Draw back side
    draw_tiles(back_tile_ids, c, x_start, y_start, images_per_row, front=False)
    c.showPage()
    
    # Save the PDF
    c.save()
    
    return send_file(output_pdf_path, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists('generated'):
        os.makedirs('generated')
    app.run(debug=True)
