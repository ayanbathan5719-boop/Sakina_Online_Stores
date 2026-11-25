from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category

CATALOG = {
    "Modest Fashion": ["Abayas", "Open Abayas", "Kimono Abayas", "Modest Dresses",
                       "Modest Skirts and Tops", "Matching Sets", "Prayer Dresses"],
    "Hijabs and Headwear": ["Chiffon Hijabs", "Jersey Hijabs", "Cotton Hijabs", "Khimars",
                            "Instant Hijabs", "Undercaps", "Hijab Pins and Magnets",
                            "Hijab Accessories"],
    "Perfumes and Fragrance": ["Arabic Perfumes", "Oud Fragrances", "Musk Oils", "Attar",
                               "Bakhoor", "Perfume Gift Sets", "Home Fragrances"],
    "Islamic Essentials": ["Prayer Mats", "Tasbih", "Quran Covers", "Quran Stands",
                           "Islamic Journals", "Prayer Garment Bags"],
    "Bags and Accessories": ["Handbags", "Tote Bags", "Crossbody Bags", "Wallets",
                             "Sunglasses", "Minimalist Jewellery"],
    "Men's Collection": ["Thobes", "Kufi Caps", "Men's Islamic Clothing",
                         "Prayer Essentials", "Men's Accessories"],
    "Children's Collection": ["Children's Abayas", "Children's Hijabs", "Modest Outfits",
                              "Islamic Learning Materials", "Children's Accessories"],
    "Home and Living": ["Islamic Home Decor", "Arabic Calligraphy", "Islamic Wall Art",
                        "Prayer Corner Accessories"],
    "Beauty and Self-care": ["Skincare", "Body Oils", "Haircare", "Halal-certified Beauty"],
    "Gifts and Special Collections": ["Ramadan Gift Boxes", "Eid Gift Collections",
                                      "Bridal Gift Sets", "Muslimah Gift Boxes",
                                      "Perfume and Hijab Bundles", "Special Occasion Collections"],
}


class Command(BaseCommand):
    help = 'Creates the Sakina product categories and subcategories'

    def handle(self, *args, **options):
        for position, (top_name, subs) in enumerate(CATALOG.items(), start=1):
            top, _ = Category.objects.get_or_create(
                slug=slugify(top_name),
                defaults={'name': top_name, 'position': position},
            )
            for sub_position, sub_name in enumerate(subs, start=1):
                Category.objects.get_or_create(
                    slug=slugify(f'{top_name} {sub_name}'),
                    defaults={'name': sub_name, 'parent': top, 'position': sub_position},
                )
        self.stdout.write(self.style.SUCCESS('Categories ready.'))