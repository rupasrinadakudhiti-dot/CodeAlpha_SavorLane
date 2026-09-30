from django.contrib.auth.models import User
from django.db import models


class Product(models.Model):
    DIETS = [('VEG', 'Vegetarian'), ('VEGAN', 'Vegan'), ('NONVEG', 'Non-vegetarian')]
    SPICE = [('MILD', 'Mild'), ('MEDIUM', 'Medium'), ('HOT', 'Hot')]

    name = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50)
    cuisine = models.CharField(max_length=50)
    dietary = models.CharField(max_length=12, choices=DIETS, default='VEG')
    spice_level = models.CharField(max_length=10, choices=SPICE, default='MILD')
    description = models.TextField()
    ingredients = models.TextField()
    prep_minutes = models.PositiveSmallIntegerField(default=25)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image_asset = models.CharField(max_length=120, default='img/food/south-indian-menu.png')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def photo_tile(self):
        positions = {
            'ghee-masala-dosa': 0, 'soft-idli-with-sambar': 1,
            'pesarattu-with-upma': 2, 'lemon-rice': 3,
            'curd-rice': 4, 'andhra-chicken-curry': 5,
            'chettinad-pepper-chicken': 6, 'rava-kesari': 7,
            'medu-vada': 8,
        }
        return positions.get(self.slug, 0)


class Order(models.Model):
    STATUS = [('PLACED', 'Placed'), ('PREPARING', 'Preparing'), ('READY', 'Ready'), ('COMPLETED', 'Completed'), ('CANCELLED', 'Cancelled')]
    FULFILLMENT = [('DELIVERY', 'Delivery'), ('PICKUP', 'Pickup')]
    WINDOW = [('ASAP', 'As soon as possible'), ('LUNCH', 'Lunch window'), ('DINNER', 'Dinner window')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_orders')
    full_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    fulfillment = models.CharField(max_length=10, choices=FULFILLMENT, default='DELIVERY')
    preferred_window = models.CharField(max_length=10, choices=WINDOW, default='ASAP')
    address = models.TextField(blank=True)
    city = models.CharField(max_length=80, blank=True)
    pincode = models.CharField(max_length=12, blank=True)
    notes = models.CharField(max_length=250, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=12, choices=STATUS, default='PLACED')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Food order #{self.pk}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=160)
    unit_price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def subtotal(self):
        return self.unit_price * self.quantity
