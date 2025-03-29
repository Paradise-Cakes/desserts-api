from dotenv import load_dotenv
from pathlib import Path
import os
import requests
import boto3

load_dotenv(dotenv_path=".env.local")

client = boto3.client("cognito-idp", region_name=os.getenv("AWS_REGION"))

response = client.initiate_auth(
    ClientId=os.getenv("COGNITO_APP_CLIENT_ID"),
    AuthFlow="USER_PASSWORD_AUTH",
    AuthParameters={
        "USERNAME": os.getenv("SUPER_ADMIN_TESTER_EMAIL"),
        "PASSWORD": os.getenv("SUPER_ADMIN_TESTER_PASSWORD"),
    },
)

access_token = response["AuthenticationResult"]["AccessToken"]

desserts = [
    {
        "name": "Chocolate Cake",
        "description": "A rich chocolate cake with layers of chocolate frosting.",
        "dessert_type": "cake",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "cocoa powder", "eggs", "butter"],
        "images": [
            {
                "url": "https://sugargeekshow.com/wp-content/uploads/2023/10/easy_chocolate_cake_slice.jpg",
                "file_name": "chocolate_cake.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://theloopywhisk.com/wp-content/uploads/2021/05/Small-Batch-Gluten-Free-Chocolate-Cake_730px-featured.jpg",
                "file_name": "chocolate_cake_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Vanilla Cake",
        "description": "A classic vanilla cake with creamy vanilla frosting.",
        "dessert_type": "cake",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "eggs", "butter", "vanilla"],
        "images": [
            {
                "url": "https://reddessertdive.com/wp-content/uploads/2023/10/Vanilla.jpg",
                "file_name": "vanilla_cake.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://www.modernhoney.com/wp-content/uploads/2024/12/Vanilla-Cake-10-scaled.jpg",
                "file_name": "vanilla_cake_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Red Velvet Cake",
        "description": "A moist red velvet cake with cream cheese frosting.",
        "dessert_type": "cake",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "cocoa powder", "eggs", "butter", "red dye"],
        "images": [
            {
                "url": "https://thescranline.com/wp-content/uploads/2023/06/RED-VELVET-CAKE-23-S-01.jpg",
                "file_name": "red_velvet_cake.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSXqafW63fP1wqJShG8GxeN9FKD623k0iES1Q&s",
                "file_name": "red_velvet_cake_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Lemon Tart",
        "description": "A tangy lemon tart with a buttery crust.",
        "dessert_type": "tart",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 4.99},
            {"size": '8"', "base_price": 6.99},
            {"size": '10"', "base_price": 8.99},
        ],
        "ingredients": ["flour", "sugar", "butter", "eggs", "lemon"],
        "images": [
            {
                "url": "https://thecafesucrefarine.com/wp-content/uploads/2022/04/French-Lemon-Tart-11.jpg",
                "file_name": "lemon_tart.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYP_HRcGZ3qKdNjN2f1HTOswrFaDQdj8fdJw&s",
                "file_name": "lemon_tart_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Cheesecake",
        "description": "A creamy cheesecake with a graham cracker crust.",
        "dessert_type": "cake",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 6.99},
            {"size": '8"', "base_price": 8.99},
            {"size": '10"', "base_price": 10.99},
        ],
        "ingredients": ["cream cheese", "sugar", "eggs", "graham crackers"],
        "images": [
            {
                "url": "https://static01.nyt.com/images/2024/07/29/multimedia/strawberry-cheesecake-cjbt/strawberry-cheesecake-cjbt-jumbo.jpg",
                "file_name": "cheesecake.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://www.jocooks.com/wp-content/uploads/2018/11/cheesecake-1-22.jpg",
                "file_name": "cheesecake_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Carrot Cake",
        "description": "A moist carrot cake with cream cheese frosting.",
        "dessert_type": "cake",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "carrots", "eggs", "butter"],
        "images": [
            {
                "url": "https://www.simplyrecipes.com/thmb/KGjnllq33Hij5UgyLZJL2XRv3U4=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Carrot-Cake-LEAD-3-81e1d3700f0241279f9ba4c2b8b6153c.jpg",
                "file_name": "carrot_cake.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://www.onceuponachef.com/images/2024/03/carrot-cake-1200x1612.jpg",
                "file_name": "carrot_cake_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Pineapple Upside Down Cake",
        "description": "A classic pineapple upside down cake with a caramelized topping.",
        "dessert_type": "cake",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "eggs", "butter", "pineapple"],
        "images": [
            {
                "url": "https://www.tastesoflizzyt.com/wp-content/uploads/2023/07/pineapple-upside-down-bundt-cake-11.jpg",
                "file_name": "pineapple_cake.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://cheneetoday.com/wp-content/uploads/2021/06/IMG_7076-3.jpg",
                "file_name": "pineapple_cake_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Strawberry Shortcake",
        "description": "A light and fluffy strawberry shortcake with whipped cream.",
        "dessert_type": "cake",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "eggs", "butter", "strawberries"],
        "images": [
            {
                "url": "https://sugarspunrun.com/wp-content/uploads/2024/02/Strawberry-shortcake-cake-1-of-1.jpg",
                "file_name": "strawberry_shortcake.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://omgchocolatedesserts.com/wp-content/uploads/2016/03/Strawberry-Shortcake-2.jpg",
                "file_name": "strawberry_shortcake_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Galaxy Cake",
        "description": "A stunning galaxy cake with cosmic colors.",
        "dessert_type": "cake",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "eggs", "butter", "food coloring"],
        "images": [
            {
                "url": "https://celebritycakestudio.com/cdn/shop/files/ACS_3518.jpg?v=1712347208",
                "file_name": "galaxy_cake.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://chelsweets.com/wp-content/uploads/2021/03/staged-cake-slice-horiz-1024x683.jpg.webp",
                "file_name": "galaxy_cake_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Oreo Cake",
        "description": "A delicious Oreo cake with crushed Oreos.",
        "dessert_type": "cake",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "eggs", "butter", "Oreos"],
        "images": [
            {
                "url": "https://abajillianrecipes.com/wp-content/uploads/2023/08/Oreo-Ice-Cream-Cake-A-baJillian-Recipes-7.jpg",
                "file_name": "oreo_cake.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://beyondfrosting.com/wp-content/uploads/2019/04/Oreo-Chocolate-Cake-041-2.jpg",
                "file_name": "oreo_cake_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Chocolate Chip Cookies",
        "description": "Classic chocolate chip cookies with gooey chocolate chips.",
        "dessert_type": "cookie",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "butter", "chocolate chips", "eggs"],
        "images": [
            {
                "url": "https://images.aws.nestle.recipes/resized/5b069c3ed2feea79377014f6766fcd49_Original_NTH_Chocolate_Chip_Cookie_1080_850.jpg",
                "file_name": "chocolate_chip_cookies.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://bakerbynature.com/wp-content/uploads/2017/06/everydaychocolatechipcookies12-1-of-1.jpg",
                "file_name": "chocolate_chip_cookies_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Peanut Butter Cookies",
        "description": "Soft and chewy peanut butter cookies.",
        "dessert_type": "cookie",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "butter", "peanut butter", "eggs"],
        "images": [
            {
                "url": "https://sugarspunrun.com/wp-content/uploads/2023/02/the-best-peanut-butter-cookie-recipe-1-of-1.jpg",
                "file_name": "peanut_butter_cookies.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://www.spicebangla.com/wp-content/uploads/2024/10/2-Ingredient-Peanut-Butter-Cookies.webp",
                "file_name": "peanut_butter_cookies_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Sugar Cookies",
        "description": "Classic sugar cookies with a sweet glaze.",
        "dessert_type": "cookie",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "butter", "eggs"],
        "images": [
            {
                "url": "https://sugargeekshow.com/wp-content/uploads/2020/02/original-lofthouse-cookie-featured-500x500.jpg",
                "file_name": "sugar_cookies.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://lifemadesweeter.com/wp-content/uploads/Soft-Lofthouse-Style-Frosted-Sugar-Cookies-are-the-perfect-sweet-treat-with-a-tall-glass-of-milk-e1449928951316-1.jpg",
                "file_name": "sugar_cookies_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Snickerdoodle Cookies",
        "description": "Soft and chewy snickerdoodle cookies with cinnamon sugar.",
        "dessert_type": "cookie",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "butter", "cinnamon", "eggs"],
        "images": [
            {
                "url": "https://www.modernhoney.com/wp-content/uploads/2018/12/The-Best-Snickerdoodle-Cookie-Recipe-9jpg.jpg",
                "file_name": "snickerdoodle_cookies.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://whatsgabycooking.com/wp-content/uploads/WGC-__-Snickerdoodles-copy.jpg",
                "file_name": "snickerdoodle_cookies_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Macarons",
        "description": "Delicate French macarons with various fillings.",
        "dessert_type": "cookie",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": [
            "almond flour",
            "powdered sugar",
            "egg whites",
            "food coloring",
        ],
        "images": [
            {
                "url": "https://stylesweet.com/wp-content/uploads/2023/01/Pastelmacarons_featured-500x375.jpg",
                "file_name": "macarons.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://mealsbymolly.com/wp-content/uploads/2021/08/Raspberry-Macarons.jpg",
                "file_name": "macarons_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Lucky Charm Cupcakes",
        "description": "Fun cupcakes with Lucky Charm marshmallows.",
        "dessert_type": "cupcake",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "butter", "eggs", "Lucky Charms"],
        "images": [
            {
                "url": "https://inspiredbycharm.com/wp-content/uploads/2016/02/lucky-charms-cupcake.jpg",
                "file_name": "lucky_charms_cupcakes.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://bakerstable.net/wp-content/uploads/2023/03/lucky-charms-cupcakes-23-e1678122210179.jpg",
                "file_name": "lucky_charms_cupcakes_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Chocolate Cupcakes",
        "description": "Rich chocolate cupcakes with chocolate frosting.",
        "dessert_type": "cupcake",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "cocoa powder", "eggs", "butter"],
        "images": [
            {
                "url": "https://sugargeekshow.com/wp-content/uploads/2022/09/1200chocolate_cupcakes_featured-2-.jpg",
                "file_name": "chocolate_cupcakes.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://www.allrecipes.com/thmb/riDYvmalWk8QgJDBT_pZRkpfpR0=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/17377-chocolate-cupcakes-DDMFS-4x3-622a7a66fcd84692947794ed385dc991.jpg",
                "file_name": "chocolate_cupcakes_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Vanilla Cupcakes",
        "description": "Classic vanilla cupcakes with vanilla frosting.",
        "dessert_type": "cupcake",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "eggs", "butter", "vanilla"],
        "images": [
            {
                "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSDFWx3fO-flxR8DUUkphigNgWckzaudjwbag&s",
                "file_name": "vanilla_cupcakes.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://www.mybakingaddiction.com/wp-content/uploads/2011/07/unwrapped-vanilla-cupcake-700x1050.jpg",
                "file_name": "vanilla_cupcakes_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Strawberry Cupcakes",
        "description": "Light and fluffy strawberry cupcakes with strawberry frosting.",
        "dessert_type": "cupcake",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["flour", "sugar", "eggs", "butter", "strawberries"],
        "images": [
            {
                "url": "https://www.glorioustreats.com/wp-content/uploads/2020/06/strawberry-cupcake-recipe-on-cooling-rack-with-strawberry-frosting-square.jpg",
                "file_name": "strawberry_cupcakes.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://www.veggieinspired.com/wp-content/uploads/2015/05/vegan-strawberry-cupcakes-featured.jpg",
                "file_name": "strawberry_cupcakes_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Coconut Cream Pie",
        "description": "A creamy coconut cream pie with a graham cracker crust.",
        "dessert_type": "pie",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["coconut", "sugar", "eggs", "graham crackers"],
        "images": [
            {
                "url": "https://assets.surlatable.com/m/3e20426027e9ec52/72_dpi_webp-REC-325286_CoconutCremePie.jpg",
                "file_name": "coconut_cream_pie.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://tornadoughalli.com/wp-content/uploads/2020/03/COCONUT-CREAM-PIE-RECIPE-2.jpg",
                "file_name": "coconut_cream_pie_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Key Lime Pie",
        "description": "A tangy key lime pie with a graham cracker crust.",
        "dessert_type": "pie",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["key limes", "sugar", "eggs", "graham crackers"],
        "images": [
            {
                "url": "https://www.billyparisi.com/wp-content/uploads/2019/06/key-lime-pie-6.jpg",
                "file_name": "key_lime_pie.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://www.livewellbakeoften.com/wp-content/uploads/2021/05/Key-Lime-Pie-NEW-7s.jpg",
                "file_name": "key_lime_pie_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
    {
        "name": "Apple Pie",
        "description": "A classic apple pie with a flaky crust.",
        "dessert_type": "pie",
        "created_at": 1690000000,
        "last_updated_at": 1690000000,
        "visible": True,
        "prices": [
            {"size": '6"', "base_price": 5.99},
            {"size": '8"', "base_price": 7.99},
            {"size": '10"', "base_price": 9.99},
        ],
        "ingredients": ["apples", "sugar", "cinnamon", "butter"],
        "images": [
            {
                "url": "https://www.southernliving.com/thmb/bbDY1d_ySIrCFcq8WNBkR-3x6pU=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/2589601_Mailb_Mailbox_Apple_Pie_003-da802ff7a8984b2fa9aa0535997ab246.jpg",
                "file_name": "apple_pie.jpg",
                "file_type": "image/jpeg",
                "position": 1,
            },
            {
                "url": "https://shewearsmanyhats.com/wp-content/uploads/2014/11/apple-pie-2.jpg",
                "file_name": "apple_pie_2.jpg",
                "file_type": "image/jpeg",
                "position": 2,
            },
        ],
    },
]

get_desserts_response = requests.get(
    "https://desserts-dev-api.megsparadisecakes.com/v1/desserts",
    headers={
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    },
).json()

for dessert in get_desserts_response:
    requests.delete(
        f"https://desserts-dev-api.megsparadisecakes.com/v1/desserts/{dessert['dessert_id']}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
    )

for dessert in desserts:
    response = requests.post(
        "https://desserts-dev-api.megsparadisecakes.com/v1/desserts",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        json=dessert,
    )
    print(f"Posted dessert: {dessert['name']}, Response: {response.status_code}")
