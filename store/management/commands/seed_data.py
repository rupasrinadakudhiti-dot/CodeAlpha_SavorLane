from django.core.management.base import BaseCommand
from django.utils.text import slugify
from store.models import Product

DISHES = [
    ('Ghee Masala Dosa', 'Breakfast', 'South Indian', 'VEG', 'MEDIUM', 20, 189, 30, 'Crisp golden dosa filled with spiced potato, served with sambar and coconut chutney.', 'Rice and urad dal batter, potato, onion, ghee, curry leaves, mustard seeds, coconut'),
    ('Soft Idli with Sambar', 'Breakfast', 'South Indian', 'VEGAN', 'MILD', 15, 149, 36, 'Fluffy steamed idlis with warm vegetable sambar and coconut chutney.', 'Rice and urad dal batter, toor dal, vegetables, tamarind, coconut, curry leaves'),
    ('Pesarattu with Upma', 'Breakfast', 'Andhra', 'VEGAN', 'MEDIUM', 22, 209, 25, 'Green moong dosa wrapped around soft upma with ginger chutney.', 'Green moong dal, ginger, green chilli, semolina, onion, curry leaves'),
    ('Lemon Rice', 'Lunch', 'South Indian', 'VEGAN', 'MILD', 18, 199, 28, 'Bright turmeric lemon rice with toasted peanuts and fragrant curry leaves.', 'Rice, lemon, peanuts, turmeric, mustard seeds, curry leaves, dried chilli'),
    ('Curd Rice', 'Lunch', 'South Indian', 'VEG', 'MILD', 15, 179, 26, 'Cool, creamy curd rice finished with a mustard and curry leaf tempering.', 'Rice, yogurt, mustard seeds, curry leaves, ginger, pomegranate'),
    ('Andhra Chicken Curry', 'Dinner', 'Andhra', 'NONVEG', 'HOT', 40, 389, 18, 'A richly spiced Andhra-style chicken curry with steamed rice.', 'Chicken, onion, tomato, garlic, ginger, chilli, coriander, curry leaves, rice'),
    ('Chettinad Pepper Chicken', 'Dinner', 'Chettinad', 'NONVEG', 'HOT', 38, 429, 16, 'Peppery chicken roasted with aromatic spices and curry leaves.', 'Chicken, black pepper, fennel, cinnamon, shallots, curry leaves, coconut'),
    ('Rava Kesari', 'Dessert', 'South Indian', 'VEG', 'MILD', 12, 159, 32, 'Warm saffron semolina sweet with ghee-roasted cashews.', 'Semolina, ghee, sugar, cardamom, saffron, cashews'),
    ('Medu Vada', 'Snack', 'South Indian', 'VEGAN', 'MEDIUM', 18, 169, 27, 'Two crisp lentil vadas with sambar and fresh coconut chutney.', 'Urad dal, ginger, green chilli, pepper, curry leaves, toor dal, coconut'),
]
OLD_SAMPLE_SLUGS = (
    'morning-masala-dosa', 'garden-paneer-bowl', 'coastal-prawn-curry',
    'tamarind-millet-box', 'tandoori-chicken-wrap', 'mango-yogurt-parfait',
    'pepper-mushroom-noodles', 'chai-spiced-french-toast',
)

class Command(BaseCommand):
    help = 'Load fictional South Indian dishes for local demonstration (idempotent)'

    def handle(self, *args, **kwargs):
        Product.objects.filter(slug__in=OLD_SAMPLE_SLUGS).update(is_active=False)
        for name, category, cuisine, dietary, spice, minutes, price, stock, description, ingredients in DISHES:
            slug = slugify(name)
            Product.objects.get_or_create(slug=slug, defaults={
                'name': name, 'category': category, 'cuisine': cuisine,
                'dietary': dietary, 'spice_level': spice, 'prep_minutes': minutes,
                'price': price, 'stock': stock, 'description': description,
                'ingredients': ingredients, 'image_asset': 'img/food/south-indian-menu.png', 'is_active': True,
            })
        self.stdout.write(self.style.SUCCESS(f'{len(DISHES)} South Indian dishes are ready.'))
