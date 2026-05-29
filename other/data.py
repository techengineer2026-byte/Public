from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit

W, H = A4

# ── COLORS ──
GOLD       = colors.HexColor('#D4A017')
GOLD_LIGHT = colors.HexColor('#F0C040')
GOLD_BG    = colors.HexColor('#1A1400')
DARK       = colors.HexColor('#080808')
CARD       = colors.HexColor('#111111')
CARD2      = colors.HexColor('#161616')
WHITE      = colors.white
GREY       = colors.HexColor('#AAAAAA')
LGREY      = colors.HexColor('#666666')
GREEN      = colors.HexColor('#22C55E')
RED_CROSS  = colors.HexColor('#888888')
WA_GREEN   = colors.HexColor('#25D366')

def bg(c):
    c.setFillColor(DARK)
    c.rect(0, 0, W, H, fill=1, stroke=0)

def gold_bar(c, top=True):
    c.setFillColor(GOLD)
    if top:
        c.rect(0, H - 5*mm, W, 5*mm, fill=1, stroke=0)
    else:
        c.rect(0, 0, W, 5*mm, fill=1, stroke=0)

def gold_line(c, x, y, w, t=0.8):
    c.setStrokeColor(GOLD)
    c.setLineWidth(t)
    c.line(x, y, x+w, y)

def card_rect(c, x, y, w, h, r=4, fill=CARD, stroke=None):
    c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
        c.setLineWidth(0.6)
        c.roundRect(x, y, w, h, r, fill=1, stroke=1)
    else:
        c.setStrokeColor(fill)
        c.roundRect(x, y, w, h, r, fill=1, stroke=0)

def txt(c, text, x, y, font, size, color, align='left'):
    c.setFont(font, size)
    c.setFillColor(color)
    if align == 'center':
        c.drawCentredString(x, y, text)
    elif align == 'right':
        c.drawRightString(x, y, text)
    else:
        c.drawString(x, y, text)

def wrapped(c, text, x, y, font, size, color, max_w, lh=11):
    c.setFont(font, size)
    c.setFillColor(color)
    for line in simpleSplit(text, font, size, max_w):
        c.drawString(x, y, line)
        y -= lh
    return y

# ════════════════════════════════════════
# PAGE 1 — FRONT COVER
# ════════════════════════════════════════
def page1(c):
    bg(c)
    gold_bar(c, top=True)

    # Dark gold top section gradient feel
    c.setFillColor(colors.HexColor('#0D0B00'))
    c.rect(0, H*0.45, W, H*0.55 - 5*mm, fill=1, stroke=0)

    # Decorative large circle bg
    c.setFillColor(colors.HexColor('#14110000'))
    c.setFillAlpha(0.3)
    c.circle(W - 25*mm, H - 70*mm, 90*mm, fill=1, stroke=0)
    c.setFillAlpha(1.0)

    # ── LOGO PLACEHOLDER (text-based since no image file) ──
    card_rect(c, W/2 - 25*mm, H - 45*mm, 50*mm, 28*mm, 6, GOLD_BG, GOLD)
    txt(c, 'PUADH', W/2, H - 27*mm, 'Helvetica-Bold', 13, GOLD, 'center')
    txt(c, 'PODCAST STUDIO', W/2, H - 34*mm, 'Helvetica-Bold', 7, WHITE, 'center')
    txt(c, 'MOHALI', W/2, H - 40*mm, 'Helvetica', 6, GREY, 'center')

    # ── MAIN HEADLINE ──
    # Line 1
    txt(c, 'YOUR VOICE.', W/2, H - 72*mm, 'Helvetica-Bold', 30, WHITE, 'center')
    # Line 2 gold
    txt(c, 'YOUR BRAND.', W/2, H - 88*mm, 'Helvetica-Bold', 30, GOLD, 'center')
    # Line 3
    txt(c, 'YOUR PODCAST.', W/2, H - 104*mm, 'Helvetica-Bold', 30, WHITE, 'center')

    # Decorative line under headline
    gold_line(c, W/2 - 60*mm, H - 110*mm, 120*mm, 1.5)

    # Sub-headline
    txt(c, 'End-to-end professional podcast production in Mohali.', W/2, H - 120*mm, 'Helvetica', 10, GREY, 'center')

    # ── PRICE TEASER BOX ──
    card_rect(c, W/2 - 45*mm, H - 150*mm, 90*mm, 22*mm, 5, GOLD_BG, GOLD)
    txt(c, 'COMPLETE PACKAGE FROM', W/2, H - 135*mm, 'Helvetica', 7, GREY, 'center')
    txt(c, 'Rs 12,500 / Episode', W/2, H - 143*mm, 'Helvetica-Bold', 14, GOLD, 'center')
    txt(c, 'Everything Included. No Hidden Charges.', W/2, H - 149.5*mm, 'Helvetica', 7, GREY, 'center')

    # ── SERVICES QUICK LIST (2 cols) ──
    svcs = [
        ('Studio Rental', 'Rs 2,000/hr'),
        ('Video Shooting', 'Rs 3,500/ep'),
        ('Podcast Editing', 'Rs 5,000/ep'),
        ('Anchor / Host', 'Rs 2,000/ep'),
        ('Script Writing', 'Rs 2,000/script'),
        ('Shoot+Edit Combo', 'Rs 8,500/pkg'),
    ]
    txt(c, 'Individual Services Also Available:', W/2, H - 161*mm, 'Helvetica', 8, GREY, 'center')
    col_w = 80*mm
    sx0 = W/2 - col_w - 2*mm
    sy = H - 170*mm
    for i, (name, price) in enumerate(svcs):
        col = i % 2
        row = i // 2
        x = sx0 + col*(col_w + 4*mm)
        y = sy - row * 9*mm
        txt(c, '+ ' + name, x, y, 'Helvetica-Bold', 7.5, WHITE)
        txt(c, price, x + col_w, y, 'Helvetica-Bold', 7.5, GOLD, 'right')

    # ── BOTTOM STRIP ──
    c.setFillColor(colors.HexColor('#0D0B00'))
    c.rect(0, 0, W, 30*mm, fill=1, stroke=0)
    gold_line(c, 0, 30*mm, W, 1)

    # Bottom left — trust
    txt(c, 'Trusted by 29+ Brands & Creators', 20*mm, 20*mm, 'Helvetica-Bold', 8.5, WHITE)
    txt(c, '1,000,000+ Total Views  |  4.9 Star Rating', 20*mm, 13*mm, 'Helvetica', 8, GREY)
    txt(c, '50+ Happy Clients  |  Open 7 Days', 20*mm, 7*mm, 'Helvetica', 7, LGREY)

    # Bottom right — contact
    txt(c, 'puadhpunjabipodcast.com/studio', W - 20*mm, 20*mm, 'Helvetica-Bold', 8, GOLD, 'right')
    txt(c, 'WhatsApp: +91 83607 69451', W - 20*mm, 13*mm, 'Helvetica', 8, WHITE, 'right')
    txt(c, 'Phase 8B, Sector 74, Mohali', W - 20*mm, 7*mm, 'Helvetica', 7, GREY, 'right')


# ════════════════════════════════════════
# PAGE 2 — STAR OFFER
# ════════════════════════════════════════
def page2(c):
    bg(c)
    gold_bar(c, top=True)
    gold_bar(c, top=False)

    # Gold tinted top section
    c.setFillColor(colors.HexColor('#0D0B00'))
    c.rect(0, H - 55*mm, W, 50*mm, fill=1, stroke=0)

    # STAR badge
    card_rect(c, W/2 - 35*mm, H - 18*mm, 70*mm, 9*mm, 4, GOLD)
    txt(c, '  THE COMPLETE PODCAST PACKAGE', W/2, H - 12*mm, 'Helvetica-Bold', 9, DARK, 'center')

    # Main header
    txt(c, 'Walk in with your idea.', W/2, H - 27*mm, 'Helvetica-Bold', 18, WHITE, 'center')
    txt(c, 'Walk out with a viral-ready podcast.', W/2, H - 37*mm, 'Helvetica-Bold', 16, GOLD, 'center')
    txt(c, 'We handle absolutely everything.', W/2, H - 46*mm, 'Helvetica', 10, GREY, 'center')

    # ── PRICE BOX ──
    card_rect(c, W/2 - 55*mm, H - 78*mm, 110*mm, 28*mm, 6, GOLD_BG, GOLD)

    # Crossed out old price
    txt(c, 'Rs 20,000+', W/2 - 8*mm, H - 60*mm, 'Helvetica', 11, RED_CROSS, 'center')
    # Draw strikethrough line
    c.setStrokeColor(RED_CROSS)
    c.setLineWidth(1)
    c.line(W/2 - 8*mm - 20*mm, H - 58.5*mm, W/2 - 8*mm + 23*mm, H - 58.5*mm)

    # Actual price BIG
    txt(c, 'Rs 12,500', W/2, H - 68*mm, 'Helvetica-Bold', 28, GOLD, 'center')
    txt(c, 'per episode   |   No Hidden Charges.', W/2, H - 75.5*mm, 'Helvetica', 8, GREY, 'center')

    gold_line(c, 20*mm, H - 82*mm, 170*mm, 0.5)

    # ── CHECKLIST ──
    items = [
        'Multi-camera shooting (Sony FX3 / Canon)',
        'Full episode editing (up to 1 hour)',
        '6 Instagram Reels / YouTube Shorts',
        'Professional Anchor (Punjabi, Hindi, English)',
        'Script writing & topic research',
        'Thumbnail design & subtitles',
        'YouTube-ready files in 48 hours',
        'Studio space fully included',
    ]

    txt(c, "What's Included:", 20*mm, H - 89*mm, 'Helvetica-Bold', 10, WHITE)

    # Two columns of checklist
    col_items = [items[:4], items[4:]]
    for col, col_list in enumerate(col_items):
        cx = 20*mm + col * 90*mm
        cy = H - 100*mm
        for item in col_list:
            # Green check circle
            c.setFillColor(GREEN)
            c.circle(cx + 3*mm, cy + 1.5*mm, 3*mm, fill=1, stroke=0)
            c.setFont('Helvetica-Bold', 7)
            c.setFillColor(DARK)
            c.drawCentredString(cx + 3*mm, cy + 0.2*mm, '+')

            c.setFont('Helvetica-Bold', 8.5)
            c.setFillColor(WHITE)
            c.drawString(cx + 8*mm, cy, item)
            cy -= 11*mm

    gold_line(c, 20*mm, H - 152*mm, 170*mm, 0.5)

    # ── IDEAL FOR ──
    txt(c, 'Ideal for:', 20*mm, H - 160*mm, 'Helvetica-Bold', 9, GREY)

    ideals = ['Business Owners', 'Entrepreneurs', 'Coaches & Consultants', 'NRIs', 'Startups & Brands', 'Tricity Professionals']
    ix = 20*mm
    iy = H - 170*mm
    for ideal in ideals:
        iw = len(ideal)*3.2*mm + 6*mm
        if ix + iw > W - 20*mm:
            ix = 20*mm
            iy -= 9*mm
        card_rect(c, ix, iy - 4*mm, iw, 7*mm, 3, GOLD_BG, GOLD)
        txt(c, ideal, ix + 3*mm, iy, 'Helvetica-Bold', 7, GOLD)
        ix += iw + 3*mm

    # ── BOTTOM CTA ──
    card_rect(c, 20*mm, 12*mm, 170*mm, 18*mm, 5, WA_GREEN)
    txt(c, 'Book This Package Now  —  WhatsApp +91 83607 69451', W/2, 23*mm, 'Helvetica-Bold', 10, WHITE, 'center')
    txt(c, 'puadhpunjabipodcast.com/studio', W/2, 15.5*mm, 'Helvetica', 8, colors.HexColor('#CCFFDD'), 'center')


# ════════════════════════════════════════
# PAGE 3 — A LA CARTE SERVICES
# ════════════════════════════════════════
def page3(c):
    bg(c)
    gold_bar(c, top=True)
    gold_bar(c, top=False)

    # Header
    c.setFillColor(colors.HexColor('#0D0B00'))
    c.rect(0, H - 30*mm, W, 25*mm, fill=1, stroke=0)

    txt(c, 'CHOOSE YOUR SERVICE', W/2, H - 17*mm, 'Helvetica-Bold', 20, WHITE, 'center')
    txt(c, 'Mix and match services. Pay only for what you need.', W/2, H - 24*mm, 'Helvetica', 9, GREY, 'center')
    gold_line(c, 20*mm, H - 30*mm, 170*mm, 1)

    # ── 3x2 SERVICE GRID ──
    services = [
        {
            'icon': 'MIC',
            'icon_color': colors.HexColor('#A855F7'),
            'name': 'Studio on Rent',
            'price': 'Rs 2,000',
            'unit': 'per hour',
            'points': ['Fully soundproofed room', 'Podcast desk & branding', 'AC & lounge area', 'Free parking'],
        },
        {
            'icon': 'CAM',
            'icon_color': colors.HexColor('#3B82F6'),
            'name': 'Video Shooting',
            'price': 'Rs 3,500',
            'unit': 'per episode',
            'points': ['Sony FX3 cinema cameras', 'Multi-camera 2-3 angles', 'Professional LED lighting', '4K quality output'],
        },
        {
            'icon': 'EDI',
            'icon_color': colors.HexColor('#EC4899'),
            'name': 'Podcast Editing',
            'price': 'Rs 5,000',
            'unit': 'per episode',
            'points': ['Up to 1-hour full edit', '6 Reels / YouTube Shorts', 'Color grade + sound mix', 'Thumbnail & subtitles'],
        },
        {
            'icon': 'ANC',
            'icon_color': colors.HexColor('#F97316'),
            'name': 'Anchor / Host',
            'price': 'Rs 2,000',
            'unit': 'per episode',
            'points': ['Pre-episode research', 'Viral strategic questions', 'Punjabi / Hindi / English', 'Guest comfort priority'],
        },
        {
            'icon': 'SCR',
            'icon_color': colors.HexColor('#10B981'),
            'name': 'Script Writing',
            'price': 'Rs 2,000',
            'unit': 'per script',
            'points': ['SEO optimized content', 'Trending topic research', 'Interview question flow', 'Punjabi/Hindi/English'],
        },
        {
            'icon': 'PKG',
            'icon_color': GOLD,
            'name': 'Shoot + Edit Combo',
            'price': 'Rs 8,500',
            'unit': 'per package',
            'save': 'SAVE Rs 500!',
            'points': ['Studio + shooting included', 'Sony FX3 multi-camera', 'Full edit + 6 Reels', 'Thumbnail + subtitles'],
        },
    ]

    col_w = 54*mm
    col_gap = 3*mm
    row_h = 58*mm
    start_x = 20*mm
    start_y = H - 38*mm

    for i, svc in enumerate(services):
        col = i % 3
        row = i // 3
        x = start_x + col * (col_w + col_gap)
        y = start_y - row * (row_h + 3*mm)

        # Card
        card_rect(c, x, y - row_h, col_w, row_h, 5, CARD, colors.HexColor('#222222'))

        # Top colored accent bar
        c.setFillColor(svc['icon_color'])
        c.roundRect(x, y - 3*mm, col_w, 3*mm, 2, fill=1, stroke=0)

        # Icon box
        card_rect(c, x + col_w/2 - 7*mm, y - 16*mm, 14*mm, 10*mm, 3, svc['icon_color'])
        txt(c, svc['icon'], x + col_w/2, y - 9*mm, 'Helvetica-Bold', 6.5, DARK, 'center')

        # Service name
        txt(c, svc['name'], x + col_w/2, y - 21*mm, 'Helvetica-Bold', 8.5, WHITE, 'center')

        # Price
        txt(c, svc['price'], x + col_w/2, y - 28*mm, 'Helvetica-Bold', 12, GOLD, 'center')
        txt(c, svc['unit'], x + col_w/2, y - 33*mm, 'Helvetica', 6.5, GREY, 'center')

        # Save badge
        if 'save' in svc:
            card_rect(c, x + col_w/2 - 14*mm, y - 39*mm, 28*mm, 6*mm, 2, GREEN)
            txt(c, svc['save'], x + col_w/2, y - 34.5*mm, 'Helvetica-Bold', 6, DARK, 'center')
            py = y - 43*mm
        else:
            gold_line(c, x + 4*mm, y - 37*mm, col_w - 8*mm, 0.4)
            py = y - 42*mm

        # Bullet points
        for pt in svc['points']:
            txt(c, '+', x + 3*mm, py, 'Helvetica-Bold', 6, GOLD)
            lines = simpleSplit(pt, 'Helvetica', 6.5, col_w - 8*mm)
            txt(c, lines[0] if lines else pt, x + 7*mm, py, 'Helvetica', 6.5, GREY)
            py -= 8

    # Bottom note
    txt(c, 'All services can be combined. Ask about custom packages.', W/2, 14*mm, 'Helvetica', 8, GREY, 'center')
    txt(c, 'WhatsApp +91 83607 69451  |  puadhpunjabipodcast.com/studio', W/2, 8.5*mm, 'Helvetica-Bold', 8, GOLD, 'center')


# ════════════════════════════════════════
# PAGE 4 — WHY CHOOSE US
# ════════════════════════════════════════
def page4(c):
    bg(c)
    gold_bar(c, top=True)
    gold_bar(c, top=False)

    # Header
    c.setFillColor(colors.HexColor('#0D0B00'))
    c.rect(0, H - 32*mm, W, 27*mm, fill=1, stroke=0)

    txt(c, 'STUDIO-GRADE QUALITY.', W/2, H - 17*mm, 'Helvetica-Bold', 18, WHITE, 'center')
    txt(c, 'VIRAL-READY RESULTS.', W/2, H - 26*mm, 'Helvetica-Bold', 18, GOLD, 'center')
    gold_line(c, 20*mm, H - 32*mm, 170*mm, 1)

    # ── LEFT: THE GEAR ──
    gear_x = 20*mm
    txt(c, 'THE GEAR', gear_x, H - 41*mm, 'Helvetica-Bold', 11, GOLD)
    txt(c, 'Professional equipment. No compromises.', gear_x, H - 48*mm, 'Helvetica', 8, GREY)

    gear = [
        ('CAM', colors.HexColor('#3B82F6'), 'Cameras', 'Sony FX3 & FX30 Cinema Cameras', 'Same cameras used by top YouTube creators worldwide'),
        ('MIC', colors.HexColor('#A855F7'), 'Audio', 'Shure SM7B Microphones', 'Broadcast-grade. Used by Joe Rogan & top podcasters'),
        ('LIT', colors.HexColor('#F59E0B'), 'Lighting', 'Professional LED Panel Lights', 'Adjustable color temp. Perfect cinematic framing'),
        ('EDI', colors.HexColor('#EC4899'), 'Software', 'Adobe Premiere Pro & DaVinci Resolve', 'Industry-standard editing. Color grade + sound design'),
        ('SND', colors.HexColor('#10B981'), 'Studio', 'Acoustic Soundproofing', 'Foam panels, bass traps. Zero echo, zero noise'),
    ]

    gy = H - 57*mm
    gear_card_w = 82*mm
    for icon, icon_c, label, name, desc in gear:
        card_rect(c, gear_x, gy - 18*mm, gear_card_w, 19*mm, 4, CARD, colors.HexColor('#1E1E1E'))
        # Icon
        card_rect(c, gear_x + 2*mm, gy - 16*mm, 13*mm, 13*mm, 3, icon_c)
        txt(c, icon, gear_x + 8.5*mm, gy - 8.5*mm, 'Helvetica-Bold', 5.5, DARK, 'center')
        # Text
        txt(c, label.upper(), gear_x + 18*mm, gy - 5*mm, 'Helvetica-Bold', 5.5, icon_c)
        txt(c, name, gear_x + 18*mm, gy - 10*mm, 'Helvetica-Bold', 8, WHITE)
        wrapped(c, desc, gear_x + 18*mm, gy - 16*mm, 'Helvetica', 7, GREY, gear_card_w - 20*mm, 9)
        gy -= 21*mm

    # ── RIGHT: THE RESULTS ──
    res_x = W/2 + 5*mm
    txt(c, 'THE RESULTS', res_x, H - 41*mm, 'Helvetica-Bold', 11, GOLD)
    txt(c, 'Numbers that prove the quality.', res_x, H - 48*mm, 'Helvetica', 8, GREY)

    results = [
        ('29+', 'Episodes Produced', 'Every episode shot & edited in-house'),
        ('1,000,000+', 'Total Views', 'Across YouTube, Spotify & Apple Podcasts'),
        ('48 Hours', 'Delivery Guarantee', 'Your edited episode ready in 2 days'),
        ('4.9 / 5', 'Client Rating', 'Verified reviews from real podcast guests'),
        ('50+', 'Happy Clients', 'Entrepreneurs, coaches, NRIs & brands'),
    ]

    ry = H - 57*mm
    res_w = 82*mm
    for big, title, sub in results:
        card_rect(c, res_x, ry - 18*mm, res_w, 19*mm, 4, CARD, colors.HexColor('#1E1E1E'))
        # Gold left accent
        c.setFillColor(GOLD)
        c.roundRect(res_x, ry - 18*mm, 2*mm, 19*mm, 1, fill=1, stroke=0)

        txt(c, big, res_x + 5*mm, ry - 7*mm, 'Helvetica-Bold', 14, GOLD)
        txt(c, title, res_x + 5*mm, ry - 13*mm, 'Helvetica-Bold', 8, WHITE)
        txt(c, sub, res_x + 5*mm, ry - 18*mm, 'Helvetica', 7, GREY)
        ry -= 21*mm

    # Remote editing note
    card_rect(c, 20*mm, 12*mm, 170*mm, 12*mm, 4, GOLD_BG, GOLD)
    txt(c, 'Remote Ready:', 25*mm, 20*mm, 'Helvetica-Bold', 8.5, GOLD)
    txt(c, 'Send us your footage from anywhere in India. We edit and deliver online.', 55*mm, 20*mm, 'Helvetica', 8, WHITE)
    txt(c, 'Available across Punjab, Delhi NCR, Mumbai, Bangalore and all of India.', 25*mm, 14*mm, 'Helvetica', 7.5, GREY)


# ════════════════════════════════════════
# PAGE 5 — BACK COVER / CONTACT
# ════════════════════════════════════════
def page5(c):
    bg(c)
    gold_bar(c, top=True)

    # Full gold tinted bg top half
    c.setFillColor(colors.HexColor('#0D0B00'))
    c.rect(0, H*0.35, W, H*0.65 - 5*mm, fill=1, stroke=0)

    # Decorative circles
    c.setFillColor(colors.HexColor('#1A1200'))
    c.circle(30*mm, H - 80*mm, 60*mm, fill=1, stroke=0)
    c.setFillColor(colors.HexColor('#130F00'))
    c.circle(W - 20*mm, H - 60*mm, 70*mm, fill=1, stroke=0)

    # URGENCY badge
    card_rect(c, W/2 - 40*mm, H - 22*mm, 80*mm, 9*mm, 4, colors.HexColor('#7C2D12'), colors.HexColor('#FB923C'))
    txt(c, 'Weekend slots fill fast!', W/2, H - 16*mm, 'Helvetica-Bold', 9, colors.HexColor('#FDBA74'), 'center')

    # Main CTA headline
    txt(c, 'BOOK YOUR SLOT TODAY', W/2, H - 38*mm, 'Helvetica-Bold', 26, WHITE, 'center')
    txt(c, 'Book 48 hours in advance for weekend sessions.', W/2, H - 47*mm, 'Helvetica', 10, GREY, 'center')
    gold_line(c, W/2 - 70*mm, H - 52*mm, 140*mm, 1.5)

    # ── CONTACT CARDS ──
    contacts = [
        {
            'icon': 'WA',
            'color': WA_GREEN,
            'title': 'WhatsApp / Call',
            'value': '+91 83607 69451',
            'sub': 'We respond within 1 hour',
        },
        {
            'icon': 'WEB',
            'color': colors.HexColor('#3B82F6'),
            'title': 'Book Online',
            'value': 'puadhpunjabipodcast.com/studio',
            'sub': 'View packages & availability',
        },
        {
            'icon': 'MAP',
            'color': colors.HexColor('#EF4444'),
            'title': 'Studio Location',
            'value': 'Phase 8B, Sector 74, Mohali',
            'sub': 'Plot F-298, R&R Tower, Punjab 160055',
        },
    ]

    card_w = 52*mm
    gap = 4*mm
    total = 3*card_w + 2*gap
    cx_start = (W - total) / 2
    cy = H - 60*mm

    for i, ct in enumerate(contacts):
        cx = cx_start + i*(card_w + gap)
        card_rect(c, cx, cy - 32*mm, card_w, 33*mm, 5, CARD, ct['color'])

        # Icon box
        card_rect(c, cx + card_w/2 - 8*mm, cy - 11*mm, 16*mm, 11*mm, 3, ct['color'])
        txt(c, ct['icon'], cx + card_w/2, cy - 4.5*mm, 'Helvetica-Bold', 7, DARK, 'center')

        txt(c, ct['title'], cx + card_w/2, cy - 16*mm, 'Helvetica-Bold', 7.5, ct['color'], 'center')
        # Value (possibly wrap)
        lines = simpleSplit(ct['value'], 'Helvetica-Bold', 8, card_w - 4*mm)
        vy = cy - 22*mm
        for line in lines:
            txt(c, line, cx + card_w/2, vy, 'Helvetica-Bold', 8, WHITE, 'center')
            vy -= 9
        txt(c, ct['sub'], cx + card_w/2, cy - 30*mm, 'Helvetica', 6.5, GREY, 'center')

    # ── DIRECTIONS BOX ──
    card_rect(c, 20*mm, H - 110*mm, 170*mm, 16*mm, 5, GOLD_BG, GOLD)
    txt(c, 'Getting Here:', 25*mm, H - 100*mm, 'Helvetica-Bold', 8.5, GOLD)
    directions = '10 min from Chandigarh  |  15 min from Kharar  |  20 min from Zirakpur  |  25 min from Panchkula'
    txt(c, directions, 25*mm, H - 107*mm, 'Helvetica', 7.5, WHITE)

    # ── SOCIAL MEDIA ──
    txt(c, 'Follow Us', W/2, H - 122*mm, 'Helvetica-Bold', 9, GREY, 'center')
    gold_line(c, W/2 - 50*mm, H - 125*mm, 100*mm, 0.5)

    socials = [
        ('IG', colors.HexColor('#E1306C'), '@puadhpunjabipodcast'),
        ('YT', colors.HexColor('#FF0000'), '@puadhpunjabipodcast'),
        ('FB', colors.HexColor('#1877F2'), 'Puadh Punjabi Podcast'),
        ('SP', colors.HexColor('#1DB954'), 'Puadh Punjabi Podcast'),
    ]
    sw = 40*mm
    stotal = 4*sw + 3*3*mm
    sx_start = (W - stotal)/2
    for i, (icon, color, handle) in enumerate(socials):
        sx = sx_start + i*(sw + 3*mm)
        card_rect(c, sx, H - 140*mm, sw, 12*mm, 3, CARD, color)
        txt(c, icon, sx + 6*mm, H - 132.5*mm, 'Helvetica-Bold', 7.5, color)
        txt(c, handle, sx + 13*mm, H - 132.5*mm, 'Helvetica', 6.5, WHITE)
        txt(c, '', sx + 13*mm, H - 138*mm, 'Helvetica', 6, GREY)

    # ── OPEN HOURS ──
    card_rect(c, 20*mm, H - 162*mm, 170*mm, 18*mm, 5, CARD, colors.HexColor('#222'))
    txt(c, 'Opening Hours', 25*mm, H - 150*mm, 'Helvetica-Bold', 9, WHITE)
    txt(c, 'Mon - Sat:', 25*mm, H - 158*mm, 'Helvetica-Bold', 8, GOLD)
    txt(c, '10:00 AM - 8:00 PM', 50*mm, H - 158*mm, 'Helvetica', 8, WHITE)
    txt(c, 'Sunday:', W/2 + 5*mm, H - 150*mm, 'Helvetica-Bold', 8, GOLD)
    txt(c, '11:00 AM - 5:00 PM', W/2 + 25*mm, H - 150*mm, 'Helvetica', 8, WHITE)
    txt(c, 'Free Parking  |  AC Studio  |  Lounge Area  |  Water & Tea Provided', W/2 + 5*mm, H - 158*mm, 'Helvetica', 7, GREY)

    # ── BOTTOM GOLD STRIP ──
    c.setFillColor(GOLD)
    c.rect(0, 0, W, 18*mm, fill=1, stroke=0)

    txt(c, 'Puadh Punjabi Podcast Studio', W/2, 12*mm, 'Helvetica-Bold', 11, DARK, 'center')
    txt(c, 'Plot F-298, R&R Tower, Phase 8B, Industrial Area, Sector 74, Mohali, Punjab 160055  |  Just 10 minutes from Chandigarh', W/2, 6*mm, 'Helvetica', 7, colors.HexColor('#3D2D00'), 'center')


# ════════════════════════════════════════
# BUILD
# ════════════════════════════════════════
output = "E:/PPP/Public/other/Puadh-Studio-Brochure-v2.pdf"
c = canvas.Canvas(output, pagesize=A4)
c.setTitle('Puadh Podcast Studio – Professional Brochure')
c.setAuthor('Puadh Punjabi Podcast Studio, Mohali')
c.setSubject('Professional Podcast Production Services – Mohali, Punjab')
c.setKeywords('podcast studio mohali, podcast recording chandigarh, sony fx3 podcast, podcast editing punjab')

page1(c); c.showPage()
page2(c); c.showPage()
page3(c); c.showPage()
page4(c); c.showPage()
page5(c); c.showPage()

c.save()
print("Done:", output)