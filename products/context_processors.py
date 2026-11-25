from .models import Category

MENU_GROUPS = [
    ("Women", ["Modest Fashion", "Hijabs and Headwear", "Bags and Accessories"]),
    ("Fragrance and Beauty", ["Perfumes and Fragrance", "Beauty and Self-care"]),
    ("Faith and Home", ["Islamic Essentials", "Home and Living"]),
    ("Family", ["Men's Collection", "Children's Collection"]),
    ("Gifts", ["Gifts and Special Collections"]),
]

def nav_categories(request):
    tops = {c.name: c for c in Category.objects.filter(parent__isnull=True)}
    groups = []
    for title, names in MENU_GROUPS:
        cats = [tops[n] for n in names if n in tops]
        if cats:
            groups.append({'title': title, 'categories': cats})
    return {'nav_categories': list(tops.values()), 'menu_groups': groups}