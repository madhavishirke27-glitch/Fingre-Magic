"""
FaceStyle AI - Hairstyle Recommendation Module
Matches face shape geometry with compatible hairstyles and provides neutral styling guidance.
"""
from .measurements import FACE_SHAPE_DETAILS

HAIR_LENGTH_CHOICES = [
    ('Short', 'Short Hairstyles'),
    ('Medium', 'Medium Hairstyles'),
    ('Long', 'Long Hairstyles'),
]

HAIR_TYPE_CHOICES = [
    ('Straight', 'Straight Hair'),
    ('Wavy', 'Wavy Hair'),
    ('Curly', 'Curly Hair'),
]

CATEGORY_CHOICES = [
    ('Modern', 'Modern Hairstyles'),
    ('Traditional', 'Traditional Hairstyles'),
    ('Casual', 'Casual Everyday'),
    ('Formal', 'Formal & Professional'),
]

GENDER_CHOICES = [
    ('Female', 'Women'),
    ('Male', 'Men'),
    ('Unisex', 'Unisex (All)'),
]

FACE_SHAPE_CHOICES = [
    ('Oval', 'Oval Face'),
    ('Round', 'Round Face'),
    ('Square', 'Square Face'),
    ('Heart', 'Heart Face'),
    ('Diamond', 'Diamond Face'),
    ('Oblong', 'Oblong Face'),
]


def get_face_shape_details(face_shape):
    """Returns comprehensive styling and architectural notes for a face shape."""
    return FACE_SHAPE_DETAILS.get(face_shape, FACE_SHAPE_DETAILS['Oval'])


def get_recommendations(face_shape, hair_length=None, hair_type=None, category=None, gender=None):
    """
    Queries Django Hairstyle model for hairstyles compatible with the given face shape.
    Supports multi-criteria filtering without gender restrictions.
    """
    from main.models import Hairstyle

    # Query hairstyles compatible with this face shape or all
    queryset = Hairstyle.objects.filter(face_shapes__icontains=face_shape)

    if hair_length and hair_length != 'All':
        queryset = queryset.filter(hair_length=hair_length)

    if hair_type and hair_type != 'All':
        queryset = queryset.filter(hair_type=hair_type)

    if category and category != 'All':
        queryset = queryset.filter(category=category)

    if gender and gender != 'All':
        queryset = queryset.filter(gender__in=[gender, 'Unisex'])

    return queryset.order_by('-id')


def get_styling_principles(face_shape):
    """
    Returns objective cosmetology principles for each facial architecture.
    Emphasizes visual balance and geometric harmony without personal appearance judgment.
    """
    principles = {
        'Oval': {
            'goal': 'Preserve natural facial symmetry and experiment freely with texture and silhouette.',
            'recommended_features': ['Side or center parts', 'Blunt cuts or soft layers', 'Textured bobs', 'Classic fades or pompadours'],
            'avoid_features': ['Heavy forward fringes that obscure forehead proportion', 'Styles with excessive height that elongate the face excessively']
        },
        'Round': {
            'goal': 'Introduce vertical lines and subtle angularity to balance circular cheek proportions.',
            'recommended_features': ['High-volume crowns', 'Asymmetrical cuts and side-swept bangs', 'Long textured layers below chin', 'Textured quiffs and pompadours with short sides'],
            'avoid_features': ['Blunt chin-length bobs', 'Tight center parts with flat sides', 'Wide curls sitting directly level with cheekbones']
        },
        'Square': {
            'goal': 'Soften sharp jawline angles with curved, flowing layers and diffuse silhouettes.',
            'recommended_features': ['Soft wispy fringes', 'Wavy lob (long bob)', 'Deep side parts with graduated volume', 'Textured crop or medium fade with soft top'],
            'avoid_features': ['Sharp geometric bobs cut at jawline', 'Pin-straight hair with blunt micro-bangs', 'Hard, flat buzz cuts']
        },
        'Heart': {
            'goal': 'Broaden the visual width of the lower jaw and balance the wider forehead.',
            'recommended_features': ['Chin-length bobs with outward bounce', 'Curtain bangs and face-framing layers', 'Textured curls starting around jaw level', 'Side-parted brush-back with tapered sides'],
            'avoid_features': ['Extreme crown volume with bare temples', 'Slicked-back high ponytails with no face-framing strands', 'Heavy top-heavy blunt cuts']
        },
        'Diamond': {
            'goal': 'Highlight sculpted cheekbones while complementing a narrower forehead and chin.',
            'recommended_features': ['Chin-length layered cuts', 'Curtain bangs and wispy side fringes', 'Soft voluminous waves', 'Classic textured side-part and textured taper'],
            'avoid_features': ['Center parts with slick flat sides', 'Excessive lateral volume directly on the cheekbones', 'Severe slicked buns']
        },
        'Oblong': {
            'goal': 'Add lateral width and soft horizontal fullness to soften vertical elongation.',
            'recommended_features': ['Full blunt or arched fringes', 'Medium-length layered bobs with side volume', 'Wide beach waves and voluminous curls', 'Side-swept parted crew or classic textured crop with fuller sides'],
            'avoid_features': ['Sky-high pompadours', 'Long, flat, straight hair with zero layers', 'Shaved sides combined with tall vertical volume']
        }
    }
    return principles.get(face_shape, principles['Oval'])
