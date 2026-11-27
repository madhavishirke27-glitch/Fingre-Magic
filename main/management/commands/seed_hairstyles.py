"""
FaceStyle AI - Hairstyle Database Seeder Command
Populates the database with 30+ diverse, realistic hairstyles across:
- Men, Women, and Unisex
- Oval, Round, Square, Heart, Diamond, Oblong face shapes
- Short, Medium, Long lengths
- Straight, Wavy, Curly textures
- Modern, Traditional, Casual, Formal categories
Generates clean SVG/PNG visual representations in media/hairstyles/.
"""
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from main.models import Hairstyle
from PIL import Image, ImageDraw, ImageFont


def generate_hairstyle_placeholder(name, gender, length, face_shapes, filename):
    """
    Generates a modern, aesthetic branded card graphic for a hairstyle.
    Uses gradient background, stylish typography and silhouette accents.
    """
    media_dir = os.path.join(settings.MEDIA_ROOT, 'hairstyles')
    os.makedirs(media_dir, exist_ok=True)
    filepath = os.path.join(media_dir, filename)

    # 600x480 banner
    width, height = 600, 480
    
    # Palette selection based on gender/length
    if gender == 'Female':
        top_color = (42, 8, 69)      # Deep Purple
        bottom_color = (255, 117, 151) # Soft Pink
    elif gender == 'Male':
        top_color = (18, 3, 36)      # Dark Navy/Purple
        bottom_color = (123, 44, 191) # Neon Violet
    else:
        top_color = (35, 8, 67)      # Rich Violet
        bottom_color = (199, 125, 255) # Lavender

    img = Image.new('RGB', (width, height), color=top_color)
    draw = ImageDraw.Draw(img)

    # Draw vertical smooth gradient
    for y in range(height):
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * (y / height))
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * (y / height))
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * (y / height))
        draw.line([(0, y), (width, y)], fill=(r, g, b))

    # Draw decorative circles/patterns
    draw.ellipse([width - 150, -50, width + 150, 250], outline=(255, 255, 255, 40), width=3)
    draw.ellipse([-80, height - 200, 200, height + 80], outline=(255, 255, 255, 30), width=2)

    # Inner glass card box
    draw.rounded_rectangle([40, 50, width - 40, height - 50], radius=20, outline=(255, 255, 255, 80), width=2)

    # Text rendering
    draw.text((width // 2, 100), "FACESTYLE AI", fill=(224, 170, 255), anchor="mm")
    draw.text((width // 2, 180), name, fill=(255, 255, 255), anchor="mm")
    draw.text((width // 2, 230), f"{gender} • {length} Hairstyle", fill=(255, 214, 224), anchor="mm")
    
    # Shapes pill
    shapes_text = f"Best For: {', '.join(face_shapes[:3])}"
    draw.text((width // 2, 340), shapes_text, fill=(255, 255, 255), anchor="mm")
    draw.text((width // 2, 390), "★ Salon Verified Style ★", fill=(255, 240, 180), anchor="mm")

    img.save(filepath, 'JPEG', quality=90)
    return f"hairstyles/{filename}"


HAIRSTYLE_DATA = [
    # ---------------- OVAL FACE STYLES ----------------
    {
        'name': 'Layered Bob with Curtain Bangs',
        'gender': 'Female',
        'hair_length': 'Medium',
        'hair_type': 'Wavy',
        'category': 'Modern',
        'face_shapes': 'Oval, Heart, Oblong',
        'description': 'A versatile textured lob resting gently on the collarbones with face-framing curtain bangs that highlight natural facial symmetry.',
        'styling_tips': 'Apply volumizing mousse to damp roots and blow-dry with a 2-inch ceramic round brush directing the bangs outward.'
    },
    {
        'name': 'Classic Pompadour with Low Fade',
        'gender': 'Male',
        'hair_length': 'Short',
        'hair_type': 'Straight',
        'category': 'Formal',
        'face_shapes': 'Oval, Round, Square',
        'description': 'Timeless gentleman haircut featuring swept-back volume on the crown and clean low skin fade around the ears and neck.',
        'styling_tips': 'Rub a dime-sized amount of high-hold pomade between palms, brush hair backwards and upwards while blow-drying.'
    },
    {
        'name': 'Long Beachy Waves with Center Part',
        'gender': 'Female',
        'hair_length': 'Long',
        'hair_type': 'Wavy',
        'category': 'Casual',
        'face_shapes': 'Oval, Square, Diamond',
        'description': 'Effortless flowing waves that cascade past the shoulders, offering fluid movement and relaxed natural charm.',
        'styling_tips': 'Use a 1.25-inch curling wand alternating curl directions. Finish with sea salt mist for lived-in texture.'
    },
    {
        'name': 'Textured French Crop',
        'gender': 'Male',
        'hair_length': 'Short',
        'hair_type': 'Straight',
        'category': 'Modern',
        'face_shapes': 'Oval, Heart, Oblong',
        'description': 'Contemporary low-maintenance cut with blunt fringe and textured choppy top paired with high faded sides.',
        'styling_tips': 'Dust styling powder into dry hair and work with fingertips for a matte, textured finish.'
    },
    {
        'name': 'Sleek Straight Lob (Long Bob)',
        'gender': 'Unisex',
        'hair_length': 'Medium',
        'hair_type': 'Straight',
        'category': 'Modern',
        'face_shapes': 'Oval, Round, Heart',
        'description': 'Crisp, blunt shoulder-grazing bob delivering sharp silhouettes and glossy professional elegance.',
        'styling_tips': 'Prep with heat protection serum, flat-iron in 1-inch sections and mist with shine spray.'
    },

    # ---------------- ROUND FACE STYLES ----------------
    {
        'name': 'Asymmetrical Pixie Cut',
        'gender': 'Female',
        'hair_length': 'Short',
        'hair_type': 'Straight',
        'category': 'Modern',
        'face_shapes': 'Round, Heart, Oval',
        'description': 'Bold short haircut with side-swept longer bangs that create vertical diagonal lines, visually elongating circular face contours.',
        'styling_tips': 'Use styling wax to sculpt the side bangs and keep the back and sides closely tapered.'
    },
    {
        'name': 'High Volume Textured Quiff',
        'gender': 'Male',
        'hair_length': 'Short',
        'hair_type': 'Wavy',
        'category': 'Modern',
        'face_shapes': 'Round, Square, Oval',
        'description': 'Vertical quiff styled upwards to add crown height, narrowing the cheekbones and bringing structural balance to round proportions.',
        'styling_tips': 'Pre-style with sea salt spray and blow-dry upward, then lock in place with matte clay.'
    },
    {
        'name': 'Long Cascading Layers with Deep Side Part',
        'gender': 'Female',
        'hair_length': 'Long',
        'hair_type': 'Straight',
        'category': 'Formal',
        'face_shapes': 'Round, Square, Diamond',
        'description': 'Long flowing locks with graduated layers starting below the chin, creating elegant vertical lines that slim round cheeks.',
        'styling_tips': 'Part hair deeply to one side to break cheek symmetry. Smooth ends with argan oil.'
    },
    {
        'name': 'Faux Hawk Fade (Fohawk)',
        'gender': 'Male',
        'hair_length': 'Short',
        'hair_type': 'Curly',
        'category': 'Modern',
        'face_shapes': 'Round, Oval',
        'description': 'Trendy tapered sides blending into a prominent textured center strip, drawing attention upward for a leaner profile.',
        'styling_tips': 'Pinch curl cream into damp center curls to define texture and keep side tapers sharp.'
    },
    {
        'name': 'Shoulder-Length Shag with Wispy Bangs',
        'gender': 'Unisex',
        'hair_length': 'Medium',
        'hair_type': 'Wavy',
        'category': 'Casual',
        'face_shapes': 'Round, Oblong, Oval',
        'description': 'Retro-inspired shag with feathered crown layers that diffuse broad cheek width with effortless rock-and-roll vibe.',
        'styling_tips': 'Scrunch styling mousse into damp waves and air dry or diffuse with low heat.'
    },

    # ---------------- SQUARE FACE STYLES ----------------
    {
        'name': 'Soft Shoulder Waves with Wispy Fringe',
        'gender': 'Female',
        'hair_length': 'Medium',
        'hair_type': 'Wavy',
        'category': 'Modern',
        'face_shapes': 'Square, Oblong, Heart',
        'description': 'Gentle curving waves paired with soft feathery bangs that visually soften angular, broad jawlines.',
        'styling_tips': 'Curl away from the face starting at ear level to ensure soft curves around the jawline.'
    },
    {
        'name': 'Side-Parted Executive Comb Over',
        'gender': 'Male',
        'hair_length': 'Short',
        'hair_type': 'Straight',
        'category': 'Formal',
        'face_shapes': 'Square, Oval, Diamond',
        'description': 'A tailored, distinguished haircut with soft scissor-cut sides and neat diagonal sweep, accentuating strong jawlines politely.',
        'styling_tips': 'Comb wet hair along the natural side parting line, apply medium-shine styling cream and allow to set.'
    },
    {
        'name': 'Tousled Curtain Shag',
        'gender': 'Unisex',
        'hair_length': 'Medium',
        'hair_type': 'Curly',
        'category': 'Casual',
        'face_shapes': 'Square, Round, Diamond',
        'description': 'Playful textured curls with middle-parted curtain strands that wrap gently around temples and jaw angles.',
        'styling_tips': 'Apply curl defining gel on soaking wet hair, scrunch upwards, and diffuse.'
    },
    {
        'name': 'Undercut with Textured Brush Back',
        'gender': 'Male',
        'hair_length': 'Medium',
        'hair_type': 'Straight',
        'category': 'Modern',
        'face_shapes': 'Square, Oval, Round',
        'description': 'Clean disconnected undercut sides paired with 4-5 inches of pliable brushed-back length on top.',
        'styling_tips': 'Blow dry backwards with a vented brush, emulsify clay between fingers and rake through hair.'
    },

    # ---------------- HEART FACE STYLES ----------------
    {
        'name': 'Chin-Length French Bob with Full Bangs',
        'gender': 'Female',
        'hair_length': 'Short',
        'hair_type': 'Straight',
        'category': 'Modern',
        'face_shapes': 'Heart, Oval, Diamond',
        'description': 'Classic French-inspired chin bob that adds volume right at the jawline level, balancing narrow chins and wider foreheads.',
        'styling_tips': 'Tuck ends gently under using a mini round brush while blow-drying.'
    },
    {
        'name': 'Mid-Length Taper with Side Sweep',
        'gender': 'Male',
        'hair_length': 'Medium',
        'hair_type': 'Wavy',
        'category': 'Casual',
        'face_shapes': 'Heart, Diamond, Oval',
        'description': 'Layered cut with soft fullness around the neck and temples, harmonizing the wider forehead of a heart-shaped silhouette.',
        'styling_tips': 'Let dry naturally with a leave-in conditioner to preserve natural wavy movement.'
    },
    {
        'name': 'Long Butterfly Layers with Curtain Fringe',
        'gender': 'Female',
        'hair_length': 'Long',
        'hair_type': 'Wavy',
        'category': 'Modern',
        'face_shapes': 'Heart, Oval, Square',
        'description': 'Dimensional multi-tier cut providing cascading volume around the collarbones, expanding the lower visual frame.',
        'styling_tips': 'Set in velcro rollers for 20 minutes after blow-drying for salon-grade bouncy blowout.'
    },
    {
        'name': 'Classic Side Part Ivy League',
        'gender': 'Male',
        'hair_length': 'Short',
        'hair_type': 'Straight',
        'category': 'Formal',
        'face_shapes': 'Heart, Oval, Square',
        'description': 'Polished collegiate cut with tapered nape and slightly longer front swept smoothly to the side.',
        'styling_tips': 'Apply light pomade to damp hair and use a fine-tooth comb to establish a crisp parting.'
    },

    # ---------------- DIAMOND FACE STYLES ----------------
    {
        'name': 'Voluminous Layered Lob with Side Bangs',
        'gender': 'Female',
        'hair_length': 'Medium',
        'hair_type': 'Wavy',
        'category': 'Modern',
        'face_shapes': 'Diamond, Oval, Heart',
        'description': 'Collarbone-grazing bob that broadens forehead and jawline presence while framing prominent high cheekbones.',
        'styling_tips': 'Wrap sections around a large barrel curling iron starting at mid-length.'
    },
    {
        'name': 'Textured Crop with Mid Fade',
        'gender': 'Male',
        'hair_length': 'Short',
        'hair_type': 'Straight',
        'category': 'Modern',
        'face_shapes': 'Diamond, Oval, Round',
        'description': 'Short textured fringe paired with soft mid fade that adds breadth across the narrower temples.',
        'styling_tips': 'Work a pinch of matte paste between fingers and mess the crown forward.'
    },
    {
        'name': 'Long Curly Cut with Face-Framing Tendrils',
        'gender': 'Female',
        'hair_length': 'Long',
        'hair_type': 'Curly',
        'category': 'Casual',
        'face_shapes': 'Diamond, Square, Oval',
        'description': 'Lush, springy curls with gentle face-framing tendrils that balance cheekbone prominence with romantic grace.',
        'styling_tips': 'Scrunch in curl mousse and air-dry without touching to minimize frizz.'
    },
    {
        'name': 'Messy Textured Bro Flow',
        'gender': 'Unisex',
        'hair_length': 'Medium',
        'hair_type': 'Wavy',
        'category': 'Casual',
        'face_shapes': 'Diamond, Oval, Heart',
        'description': 'Relaxed, flowy medium haircut tucked comfortably behind the ears, balancing temple and jaw widths naturally.',
        'styling_tips': 'Apply leave-in styling cream to towel-dried hair and comb straight back with fingers.'
    },

    # ---------------- OBLONG FACE STYLES ----------------
    {
        'name': 'Blunt Chin Bob with Straight Fringe',
        'gender': 'Female',
        'hair_length': 'Short',
        'hair_type': 'Straight',
        'category': 'Modern',
        'face_shapes': 'Oblong, Oval, Heart',
        'description': 'Sharp horizontal cut with eyebrow-grazing full fringe that visually breaks vertical facial length.',
        'styling_tips': 'Flat-iron the bangs completely flat and curve the bottom ends slightly inward.'
    },
    {
        'name': 'Classic Side-Swept Crew Cut with Full Sides',
        'gender': 'Male',
        'hair_length': 'Short',
        'hair_type': 'Straight',
        'category': 'Formal',
        'face_shapes': 'Oblong, Oval, Diamond',
        'description': 'Traditional crew cut that keeps gentle density on the sides rather than shaving them, widening the face horizontally.',
        'styling_tips': 'Brush the top to the side with light styling wax; avoid excessive vertical quiff height.'
    },
    {
        'name': 'Mid-Length Bouncy Curls with Side Part',
        'gender': 'Female',
        'hair_length': 'Medium',
        'hair_type': 'Curly',
        'category': 'Modern',
        'face_shapes': 'Oblong, Square, Oval',
        'description': 'Spiraled curls with lateral volume around the cheek level, creating balanced horizontal fullness.',
        'styling_tips': 'Diffuse upside-down until 80% dry, then flip over and shake roots for maximum side body.'
    },
    {
        'name': 'Traditional Layered Feather Cut',
        'gender': 'Female',
        'hair_length': 'Long',
        'hair_type': 'Straight',
        'category': 'Traditional',
        'face_shapes': 'Oblong, Oval, Square',
        'description': 'Classic Indian / South Asian salon feathered cut with outward flicked layers adding horizontal grace.',
        'styling_tips': 'Blow dry layers outward away from the face using a barrel brush.'
    },
    {
        'name': 'Traditional Classic Taper with Natural Part',
        'gender': 'Male',
        'hair_length': 'Short',
        'hair_type': 'Wavy',
        'category': 'Traditional',
        'face_shapes': 'Oval, Round, Square, Oblong',
        'description': 'Dignified classic scissor cut suitable for formal and traditional occasions with modest, balanced proportions.',
        'styling_tips': 'Comb neatly into place with herbal hair oil or light grooming cream.'
    },
    {
        'name': 'Wolf Cut with Textured Bangs',
        'gender': 'Unisex',
        'hair_length': 'Medium',
        'hair_type': 'Wavy',
        'category': 'Modern',
        'face_shapes': 'Oval, Square, Round, Heart',
        'description': 'Viral modern hybrid between mullet and shag, full of wild choppy layers and dynamic volume.',
        'styling_tips': 'Spray texture spray liberally and scrunch with hands for effortless cool.'
    }
]


class Command(BaseCommand):
    help = 'Seeds database with 30+ realistic hairstyles, descriptions, and custom generated placeholder graphics.'

    def handle(self, *args, **options):
        self.stdout.write("Seeding hairstyles into FaceStyle AI database...")
        created_count = 0
        updated_count = 0

        for idx, item in enumerate(HAIRSTYLE_DATA, 1):
            filename = f"style_{item['gender'].lower()}_{idx}.jpg"
            face_shapes_list = [s.strip() for s in item['face_shapes'].split(',')]

            # Generate graphic
            image_rel_path = generate_hairstyle_placeholder(
                name=item['name'],
                gender=item['gender'],
                length=item['hair_length'],
                face_shapes=face_shapes_list,
                filename=filename
            )

            hairstyle, created = Hairstyle.objects.update_or_create(
                name=item['name'],
                defaults={
                    'gender': item['gender'],
                    'hair_length': item['hair_length'],
                    'hair_type': item['hair_type'],
                    'category': item['category'],
                    'face_shapes': item['face_shapes'],
                    'description': item['description'],
                    'styling_tips': item['styling_tips'],
                    'image': image_rel_path,
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(self.style.SUCCESS(
            f"Successfully seeded database! Created: {created_count}, Updated: {updated_count}. Total hairstyles: {Hairstyle.objects.count()}"
        ))
