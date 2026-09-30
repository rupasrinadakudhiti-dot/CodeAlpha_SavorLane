# South Indian menu imagery

`static/img/food/south-indian-menu.png` is an AI-generated, photorealistic food contact sheet made for this demo. It is not a photograph of food available for purchase. CSS in `static/css/savorlane.css` displays each square cell independently using `.food-photo.tile-0` through `.tile-8`; the tile chosen for each menu item is in `store/models.py` (`Product.photo_tile`). The demo menu is defined in `store/management/commands/seed_data.py`.

| Tile | Dish |
| --- | --- |
| 0 | Ghee Masala Dosa |
| 1 | Soft Idli with Sambar |
| 2 | Pesarattu with Upma |
| 3 | Lemon Rice |
| 4 | Curd Rice |
| 5 | Andhra Chicken Curry |
| 6 | Chettinad Pepper Chicken |
| 7 | Rava Kesari |
| 8 | Medu Vada |

Generation prompt: A seamless 3 × 3 grid of nine independent, overhead South Indian restaurant food photographs in the order above, each dish recognizable within its own square cell, warm natural daylight, banana-leaf details and neutral tabletop, no labels, text, logos, people, illustration, or watermark.

To use your own food photographs later, replace the atlas and keep the same grid and dish order, or switch the templates to individual image files.
