from django.core.management.base import BaseCommand
from products.models import Category, Product

SAMPLES = [
    ("Classic Black Abaya", "Abayas", 6500, 12, "A flowing everyday abaya in soft black crepe."),
    ("Sand Open Abaya", "Open Abayas", 7200, 8, "A lightweight open-front abaya in warm sand."),
    ("Powder Blue Chiffon Hijab", "Chiffon Hijabs", 1200, 40, "A soft, breathable chiffon hijab in powder blue."),
    ("Ivory Jersey Hijab", "Jersey Hijabs", 1000, 35, "A stretchy jersey hijab that stays in place all day."),
    ("Instant Hijab Set", "Instant Hijabs", 1500, 20, "A slip-on hijab with an undercap included."),
    ("Oud Perfume Oil", "Oud Fragrances", 3800, 15, "A rich, long-lasting oud fragrance oil."),
    ("White Musk Oil", "Musk Oils", 1800, 25, "A clean, soft musk oil in a roll-on bottle."),
    ("Bakhoor Incense Set", "Bakhoor", 2200, 18, "A bakhoor set with a burner for the home."),
    ("Velvet Prayer Mat", "Prayer Mats", 2500, 22, "A cushioned velvet prayer mat with a simple border."),
    ("Wooden Tasbih", "Tasbih", 800, 50, "A 99-bead tasbih in smooth polished wood."),
    ("Leather Tote Bag", "Tote Bags", 4500, 10, "A roomy faux-leather tote for everyday use."),
    ("Minimalist Gold Necklace", "Minimalist Jewellery", 2800, 14, "A delicate gold-tone chain with a small pendant."),
    ("Cotton Thobe", "Thobes", 4200, 9, "A breathable cotton thobe with a classic collar."),
    ("Embroidered Kufi Cap", "Kufi Caps", 700, 30, "A lightly embroidered kufi in soft cotton."),
    ("Children's Everyday Abaya", "Children's Abayas", 3200, 11, "A comfortable abaya made for active children."),
    ("Calligraphy Wall Art", "Arabic Calligraphy", 3500, 7, "A framed Arabic calligraphy print for the home."),
    ("Rose Body Oil", "Body Oils", 1600, 20, "A light body oil with a soft rose scent."),
    ("Hydrating Face Cream", "Skincare", 2000, 16, "A gentle daily moisturiser for all skin types."),
    ("Eid Gift Box", "Eid Gift Collections", 5500, 6, "A gift box with a perfume oil, a tasbih and sweets."),
    ("Perfume and Hijab Bundle", "Perfume and Hijab Bundles", 4800, 8, "A matching chiffon hijab and fragrance oil."),
]


class Command(BaseCommand):
    help = 'Adds sample products for demonstration'

    def handle(self, *args, **options):
        created = 0
        for name, sub_name, price, stock, description in SAMPLES:
            category = Category.objects.filter(name=sub_name, parent__isnull=False).first()
            if category is None:
                self.stdout.write(self.style.WARNING(f'Category not found: {sub_name}'))
                continue
            _, was_created = Product.objects.get_or_create(
                name=name,
                defaults={'description': description, 'price': price,
                          'stock': stock, 'category': category},
            )
            created += was_created
        self.stdout.write(self.style.SUCCESS(f'{created} sample products added.'))