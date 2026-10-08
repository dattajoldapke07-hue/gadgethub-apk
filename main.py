"""Gadget Hub - an electronics store app written only in Python (Flet 0.28.3)."""
import hashlib, json, os, re, secrets
from datetime import datetime
import flet as ft

PRIMARY, DARK, MUTED, BORDER, BG = "#2563eb", "#0f172a", "#64748b", "#e2e8f0", "#f8fafc"
U = lambda i: f"https://images.unsplash.com/{i}?auto=format&fit=crop&w=800&q=80"
S, L, A, G, W_, X = "Smartphones", "Laptops", "Audio", "Gaming", "Wearables", "Accessories"

# (id, name, category, price, old price, rating, reviews, badge, image URL, description)
# To change a picture, replace the image URL. An empty "" shows a placeholder.
RAW = [
    (1, "Samsung Galaxy S25", S, 74999, 79999, 4.8, 245, "BEST SELLER", "https://images.samsung.com/is/image/samsung/p6pim/in/feature/165835044/in-feature-galaxy-s25-s931-544962134?$FB_TYPE_A_MO_JPG$", "Premium flagship smartphone with powerful performance and an advanced camera."),
    (2, "iPhone 16 Pro", S, 119999, 124999, 4.9, 512, "PREMIUM", "https://rukminim3.flixcart.com/image/480/640/xif0q/mobile/o/o/9/-resized-original-imahggev6y5zhbjz.jpeg?q=90", "Premium smartphone with a powerful processor, pro camera system and stunning display."),
    (100, "Nothing Phone 3a Pro", S, 34000, 38000, 4.9, 512, "PREMIUM", "https://m.media-amazon.com/images/I/71vGgiknBQL._AC_UF1000,1000_QL80_.jpg", "Premium smartphone with a powerful processor, pro camera system and stunning display."),
    (3, "OnePlus 13", S, 69999, 74999, 4.7, 186, "TRENDING", "https://m.media-amazon.com/images/I/71vRZZ+FCiL._AC_UF1000,1000_QL80_.jpg", "High-performance 5G smartphone with fast charging and a premium design."),
    (4, "Google Pixel 11 Pro", S, 79999, 84999, 4.6, 143, "NEW", "https://media-ik.croma.com/Croma%20Assets/Communication/Mobiles/Images/325392_0_fI1oSY8Vf.png?updatedAt=1786601024435", "Smart Android phone with excellent computational photography and clean software."),
    (5, "Nothing Phone 4a Pro", S, 44999, 49999, 4.5, 97, "HOT", "https://m.media-amazon.com/images/I/31IpyH9EWuL._AC_UF1000,1000_QL80_.jpg", "Stylish smartphone with a unique design and smooth everyday performance."),
    (101, "vivo X300 FE", S, 84999, 96999, 4.5, 97, "HOT", "https://cdn.mobilekidukaan.in/mobile-images/new-sku/2026/05/vivo/vivo-x300-fe/aba399bd3653c39326a80364c2fabc72-fb6c97686c/main-800.webp", "Stylish smartphone with a unique design and smooth everyday performance."),
    (102, "Vivo X300 Ultra", S, 109999, 119999, 4.6, 143, "SUPER", "https://encrypted-tbn1.gstatic.com/shopping?q=tbn:ANd9GcRQbY1AEa7aBg9-jnEsxX50qa6l66KVSYrjE-T9zyyY8pXSqzrhvrFOzoJ6R83nofiS9PLSgW_7ASKgooOpbtM3haRfzT3iq29KpGp9jLCJ2gsL5UcoChxMbrc", "Smart Android phone with excellent computational photography."),
    (103, "Xiaomi 15 Ultra", S, 109999, 119999, 4.6, 143, "SUPER", "", "16GB/512GB, 200 MP Leica quad camera, Snapdragon 8 Elite, WQHD+ AMOLED, Hyper AI."),
    (6, "ASUS Vivobook 16", L, 64999, 69999, 4.7, 184, "POPULAR", "https://m.media-amazon.com/images/I/71oGM-26fZL._SY450_.jpg", "Large-screen laptop for study, office work, coding and entertainment."),
    (7, "MacBook Air M5", L, 139490, 149900, 4.9, 325, "PREMIUM", "https://vsprod.vijaysales.com/media/catalog/product/m/i/midnight_2.jpg?optimize=medium&fit=bounds&height=500&width=500", "Thin and powerful laptop for productivity, creative work and everyday computing."),
    (8, "HP Pavilion 15", L, 75794, 84999, 4.5, 156, "SALE", "https://rukminim2.flixcart.com/image/767/767/xif0q/computer/8/p/b/-original-imahg4utjwvr6bxs.jpeg?q=90", "Reliable everyday laptop for office work, education and multimedia."),
    (9, "Lenovo IdeaPad Plus", L, 184000, 189999, 4.6, 121, "NEW", "https://m.media-amazon.com/images/I/81Ev2S5nrVL.jpg", "Modern performance laptop with a premium design and strong multitasking."),
    (10, "Acer Nitro Gaming", L, 82999, 89999, 4.8, 209, "GAMING", "", "Gaming laptop built for demanding games and high-performance multitasking."),
    (104, "Acer Aspire 5", L, 73990, 99999, 4.6, 121, "NEW", "https://media-ik.croma.com/Croma%20Assets/Computers%20Peripherals/Laptop/Images/323615_0_uEVNRr5R8Y.png?updatedAt=1783326915036&tr=w-360", "Modern performance laptop with a premium design and strong multitasking."),
    (11, "Sony WH-1000XM5", A, 29999, 34999, 4.9, 421, "BEST SELLER", U("photo-1505740420928-5e560c06d30e"), "Premium wireless headphones with powerful sound and noise cancellation."),
    (12, "Apple AirPods Pro", A, 24999, 26999, 4.8, 389, "POPULAR", U("photo-1600294037681-c80b4cb5b434"), "Premium wireless earbuds with active noise cancellation and immersive sound."),
    (13, "JBL Tune 770NC", A, 5999, 7999, 4.6, 287, "VALUE", U("photo-1484704849700-f032a568e944"), "Comfortable wireless headphones with noise cancellation and long battery life."),
    (14, "Boat Airdopes Elite", A, 2499, 3499, 4.4, 632, "HOT", U("photo-1590658268037-6bf12165a8df"), "Affordable true wireless earbuds for music, calls and entertainment."),
    (15, "Bose SoundLink Speaker", A, 14999, 16999, 4.7, 178, "PREMIUM", U("photo-1608043152269-423dbba4e7e1"), "Portable Bluetooth speaker with rich, powerful audio."),
    (16, "PlayStation 5", G, 54999, 59999, 4.9, 516, "BEST SELLER", U("photo-1606813907291-d86efa9b94db"), "Next-generation console for immersive gaming and high-quality graphics."),
    (17, "Xbox Series X", G, 52999, 57999, 4.8, 321, "POPULAR", U("photo-1621259182978-fbf93132d53d"), "Powerful console with fast performance and high-quality gaming."),
    (18, "Gaming RGB Keyboard", G, 3499, 4999, 4.6, 215, "SALE", U("photo-1587829741301-dc798b83add3"), "Mechanical gaming keyboard with RGB lighting and responsive keys."),
    (19, "Pro Gaming Mouse", G, 2499, 3299, 4.7, 194, "HOT", U("photo-1527814050087-3793815479db"), "High-precision gaming mouse with an ergonomic design."),
    (20, "Gaming Headset RGB", G, 3999, 4999, 4.5, 143, "GAMING", U("photo-1599669454699-248893623440"), "Gaming headset with immersive audio, microphone and RGB lighting."),
    (21, "Apple Watch Series 11", W_, 46999, 49999, 4.8, 278, "PREMIUM", U("photo-1546868871-7041f2a55e12"), "Premium smartwatch with notifications, fitness features and modern design."),
    (22, "Samsung Galaxy Watch", W_, 29999, 34999, 4.7, 196, "POPULAR", U("photo-1523275335684-37898b6baf30"), "Smartwatch with health tracking, fitness features and stylish design."),
    (23, "Fitbit Charge", W_, 11999, 14999, 4.5, 157, "FITNESS", U("photo-1575311373937-040b8e1fd5b6"), "Fitness tracker for activity monitoring, workouts and health goals."),
    (24, "Amazfit Active", W_, 8999, 10999, 4.4, 143, "VALUE", U("photo-1508685096489-7aacd43bd3b1"), "Affordable smartwatch with fitness tracking and smart features."),
    (25, "Smart Fitness Band", W_, 1999, 2999, 4.3, 412, "SALE", U("photo-1557935728-e6d1eaabe558"), "Lightweight fitness band for steps, activity and daily notifications."),
    (26, "65W Fast Charger", X, 1499, 1999, 4.6, 523, "VALUE", U("photo-1625842268584-8f3296236761"), "Compact fast charger for smartphones, tablets and compatible devices."),
    (27, "USB-C Hub 7-in-1", X, 2299, 2999, 4.5, 187, "POPULAR", U("photo-1625842268584-8f3296236761"), "Multi-port USB-C hub for laptops and modern devices."),
    (28, "Wireless Power Bank", X, 2999, 3999, 4.4, 231, "HOT", U("photo-1609592424854-5a8b2c7a8d4e"), "Portable power bank for convenient wireless and wired charging."),
    (29, "Premium Phone Case", X, 799, 1299, 4.3, 648, "SALE", U("photo-1601593346740-925612772716"), "Premium protective phone case with a stylish design."),
    (30, "4K Action Camera", X, 15999, 18999, 4.6, 119, "NEW", U("https://static1.industrybuying.com/products/security/cctv-cameras/wifi-camera/SEC.WIF.724089633_1703760821062.webp"), "Compact 4K action camera for travel, adventure and video recording."),
]
KEYS = ("id", "name", "category", "price", "old", "rating", "reviews", "badge", "img", "desc")
PRODUCTS = [dict(zip(KEYS, r)) for r in RAW]
BY = {p["id"]: p for p in PRODUCTS}
CATS = [(S, "📱", "Latest phones"), (L, "💻", "Powerful computing"), (A, "🎧", "Headphones & buds"),
        (G, "🎮", "Level up"), (W_, "⌚", "Smart lifestyle"), (X, "🔌", "Everyday essentials")]

DATA_FILE = os.path.join(os.getenv("FLET_APP_STORAGE_DATA") or ".", "gadgethub.json")


def inr(n):
    s = str(int(round(n)))
    if len(s) > 3:
        s = re.sub(r"(\d)(?=(\d\d)+$)", r"\1,", s[:-3]) + "," + s[-3:]
    return "₹" + s


def hash_pw(pw, salt=None):
    salt = salt or secrets.token_hex(8)
    return salt + ":" + hashlib.pbkdf2_hmac("sha256", pw.encode(), salt.encode(), 100000).hex()


def check_pw(pw, stored):
    return hash_pw(pw, stored.split(":")[0]) == stored


def load():
    try:
        with open(DATA_FILE, encoding="utf-8") as f:
            d = json.load(f)
    except Exception:
        d = {}
    return {"users": d.get("users", {}), "user": d.get("user"), "wish": d.get("wish", []),
            "cart": d.get("cart", {}), "orders": d.get("orders", {})}


def save(db):
    try:
        os.makedirs(os.path.dirname(os.path.abspath(DATA_FILE)), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(db, f)
    except Exception:
        pass


def main(page: ft.Page):
    page.title = "Gadget Hub"
    page.padding = 0
    page.bgcolor = BG
    page.theme_mode = ft.ThemeMode.LIGHT
    db = load()
    view = {"cat": None, "q": "", "sort": "default", "wish": False, "title": "Featured Products"}
    cur = {"dlg": None}
    width = lambda: page.width or 400

    # ---------- small helpers ----------
    def T(v, size=14, bold=False, color=DARK, **k):
        return ft.Text(v, size=size, color=color, weight=ft.FontWeight.BOLD if bold else None, **k)

    def toast(m):
        page.open(ft.SnackBar(T(m, color="white"), bgcolor=DARK))

    def btn(label, fn, primary=True):
        st = ft.ButtonStyle(bgcolor=PRIMARY if primary else "white", color="white" if primary else DARK,
                            shape=ft.RoundedRectangleBorder(radius=9),
                            side=None if primary else ft.BorderSide(1, BORDER))
        return ft.ElevatedButton(label, on_click=fn, style=st)

    def wide(label, fn):
        b = btn(label, fn)
        b.expand = True
        return ft.Row([b])

    def field(label, **k):
        return ft.TextField(label=label, border_radius=9, dense=True, **k)

    def ph():
        return ft.Container(T("📷", 34), alignment=ft.alignment.center, bgcolor="#f1f5f9")

    def img(p, w=None, h=None):
        if not p["img"]:
            return ph()
        return ft.Image(src=p["img"], width=w, height=h, fit=ft.ImageFit.COVER, error_content=ph())

    def close():
        if cur["dlg"]:
            page.close(cur["dlg"])
            cur["dlg"] = None

    def popup(controls, title=None):
        close()
        d = ft.AlertDialog(
            scrollable=True, shape=ft.RoundedRectangleBorder(radius=16),
            title=T(title, 20, True) if title else None,
            content=ft.Container(ft.Column(controls, tight=True, spacing=10), width=min(width() - 60, 460)),
            inset_padding=ft.padding.symmetric(horizontal=12, vertical=20),
            on_dismiss=lambda e: cur.update(dlg=None))
        cur["dlg"] = d
        page.open(d)

    def cart_total():
        return sum(BY[int(k)]["price"] * q for k, q in db["cart"].items())

    # ---------- header icons ----------
    wl_btn = ft.IconButton(ft.Icons.FAVORITE_BORDER, on_click=lambda e: show_wishlist())
    cart_btn = ft.IconButton(ft.Icons.SHOPPING_CART_OUTLINED, on_click=lambda e: open_cart())
    user_btn = ft.IconButton(ft.Icons.PERSON_OUTLINE, on_click=lambda e: open_account())

    def refresh_badges():
        n, w = sum(db["cart"].values()), len(db["wish"])
        cart_btn.badge = ft.Badge(text=str(n)) if n else None
        wl_btn.badge = ft.Badge(text=str(w)) if w else None
        user_btn.icon = ft.Icons.PERSON if db["user"] else ft.Icons.PERSON_OUTLINE
        user_btn.icon_color = PRIMARY if db["user"] else DARK

    # ---------- products ----------
    title_txt = T("Featured Products", 26, True)
    grid = ft.ResponsiveRow(spacing=10, run_spacing=10)

    def current():
        items = PRODUCTS
        if view["wish"]:
            items = [p for p in items if p["id"] in db["wish"]]
        if view["cat"]:
            items = [p for p in items if p["category"] == view["cat"]]
        q = view["q"].strip().lower()
        if q:
            items = [p for p in items if q in (p["name"] + " " + p["category"] + " " + p["desc"]).lower()]
        s = view["sort"]
        if s == "low":
            items = sorted(items, key=lambda p: p["price"])
        elif s == "high":
            items = sorted(items, key=lambda p: -p["price"])
        elif s == "rating":
            items = sorted(items, key=lambda p: -p["rating"])
        return items

    def card(p):
        liked = p["id"] in db["wish"]
        top = ft.Stack([
            ft.Container(img(p), left=0, right=0, top=0, bottom=0, on_click=lambda e, p=p: quick(p)),
            ft.Container(T(p["badge"], 9, True, "white"), bgcolor=DARK, border_radius=5, left=8, top=8,
                         padding=ft.padding.symmetric(horizontal=7, vertical=4)),
            ft.IconButton(ft.Icons.FAVORITE if liked else ft.Icons.FAVORITE_BORDER, icon_size=18, right=2, top=2,
                          icon_color="#ef4444" if liked else MUTED, bgcolor="white",
                          on_click=lambda e, i=p["id"]: toggle_wish(i)),
        ], height=130)
        add = ft.ElevatedButton("Add to Cart", expand=True, on_click=lambda e, i=p["id"]: add_cart(i),
                                style=ft.ButtonStyle(bgcolor=DARK, color="white", shape=ft.RoundedRectangleBorder(radius=8)))
        body = ft.Container(ft.Column([
            T(p["category"].upper(), 9, True, MUTED),
            T(p["name"], 14, True, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
            T(f"★ {p['rating']}  ({p['reviews']})", 11, color="#f59e0b"),
            ft.Row([T(inr(p["price"]), 16, True),
                    T(inr(p["old"]), 11, color="#94a3b8", style=ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH))],
                   wrap=True, spacing=6),
            ft.Row([add, ft.IconButton(ft.Icons.VISIBILITY_OUTLINED, icon_color=PRIMARY, bgcolor="#eff6ff",
                                       on_click=lambda e, p=p: quick(p))], spacing=4),
        ], spacing=4), padding=12)
        return ft.Container(ft.Column([top, body], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                            bgcolor="white", border=ft.border.all(1, BORDER), border_radius=14,
                            clip_behavior=ft.ClipBehavior.ANTI_ALIAS, col={"xs": 6, "sm": 4, "md": 3})

    def render():
        items = current()
        title_txt.value = view["title"]
        grid.controls = [card(p) for p in items] or [ft.Container(
            ft.Column([T("🔍", 50), T("No products found", 18, True), T("Try another search or category.", color=MUTED)],
                      horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=40, alignment=ft.alignment.center, col=12)]
        refresh_badges()
        page.update()

    def go_products():
        main_col.scroll_to(key="products", duration=400)

    def set_view(cat=None, q="", wish=False, title="Featured Products", sort=None):
        view.update(cat=cat, q=q, wish=wish, title=title)
        if sort:
            view["sort"], sort_dd.value = sort, sort
        search.value = q
        render()

    def show_home():
        set_view(sort="default")
        main_col.scroll_to(offset=0, duration=400)

    def show_cat(c):
        set_view(cat=c, title=c)
        go_products()

    def show_all():
        set_view(title="All Products")

    def show_wishlist():
        set_view(wish=True, title="My Wishlist")
        go_products()

    def on_search(e):
        q = search.value or ""
        set_view(q=q, title="Search Results" if q.strip() else "Featured Products")
        if q.strip():
            go_products()

    def toggle_wish(i):
        if i in db["wish"]:
            db["wish"].remove(i)
            toast("Removed from wishlist")
        else:
            db["wish"].append(i)
            toast("Added to wishlist")
        save(db)
        render()

    def add_cart(i, n=1):
        k = str(i)
        db["cart"][k] = min(10, db["cart"].get(k, 0) + n)
        save(db)
        refresh_badges()
        page.update()
        toast("Added to cart")

    def quick(p):
        off = round((1 - p["price"] / p["old"]) * 100)
        popup([
            ft.Container(img(p, min(width() - 92, 428), 220), border_radius=12, clip_behavior=ft.ClipBehavior.ANTI_ALIAS),
            T(p["category"].upper(), 10, True, MUTED),
            T(f"★ {p['rating']}  ({p['reviews']} reviews)", 12, color="#f59e0b"),
            T(p["desc"], color=MUTED),
            ft.Row([T(inr(p["price"]), 26, True), T(inr(p["old"]), 13, color="#94a3b8",
                    style=ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH)), T(f"{off}% off", 13, True, "#16a34a")],
                   wrap=True, spacing=8),
            ft.Row([btn("Add to Cart", lambda e, i=p["id"]: add_cart(i)),
                    btn("Wishlist", lambda e, i=p["id"]: (close(), toggle_wish(i)), False)], wrap=True),
        ], p["name"])

    # ---------- cart ----------
    cart_col = ft.Column(tight=True, spacing=8)

    def change(k, d):
        q = db["cart"].get(k, 0) + d
        if q <= 0:
            db["cart"].pop(k, None)
        else:
            db["cart"][k] = min(10, q)
        save(db)
        refresh_cart()

    def refresh_cart():
        if not db["cart"]:
            cart_col.controls = [T("Your cart is empty.", color=MUTED)]
        else:
            rows = []
            for k, q in db["cart"].items():
                p = BY[int(k)]
                rows.append(ft.Row([
                    ft.Container(img(p, 64, 64), width=64, height=64, border_radius=10, clip_behavior=ft.ClipBehavior.ANTI_ALIAS),
                    ft.Column([T(p["name"], 13, True, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                               T(inr(p["price"]), 12, color=MUTED),
                               ft.Row([ft.IconButton(ft.Icons.REMOVE, icon_size=16, on_click=lambda e, k=k: change(k, -1)),
                                       T(str(q), 14, True),
                                       ft.IconButton(ft.Icons.ADD, icon_size=16, on_click=lambda e, k=k: change(k, 1)),
                                       ft.IconButton(ft.Icons.DELETE_OUTLINE, icon_size=18, icon_color="#dc2626",
                                                     on_click=lambda e, k=k: change(k, -99))], spacing=0)],
                              spacing=0, expand=True)], vertical_alignment=ft.CrossAxisAlignment.START))
            cart_col.controls = rows + [ft.Divider(height=1, color=BORDER),
                                        ft.Row([T("Total", 18, True), T(inr(cart_total()), 18, True)],
                                               alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                                        wide("Proceed to Checkout", lambda e: checkout())]
        refresh_badges()
        page.update()

    def open_cart():
        popup([cart_col], "Your Cart")
        refresh_cart()

    # ---------- account ----------
    def auth_dialog(mode="login"):
        reg = mode == "reg"
        name = field("Full Name")
        email = field("Email Address", keyboard_type=ft.KeyboardType.EMAIL)
        pw = field("Password", password=True, can_reveal_password=True)

        def submit(e):
            em, p = (email.value or "").strip().lower(), pw.value or ""
            if reg:
                if (len((name.value or "").strip()) < 2 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", em)
                        or len(p) < 6):
                    return toast("Enter your name, a valid email and a password of 6+ characters.")
                if em in db["users"]:
                    return toast("This email is already registered.")
                db["users"][em] = {"name": name.value.strip(), "pw": hash_pw(p)}
            else:
                u = db["users"].get(em)
                if not u or not check_pw(p, u["pw"]):
                    return toast("Incorrect email or password.")
            db["user"] = em
            save(db)
            close()
            refresh_badges()
            page.update()
            toast("Welcome, " + db["users"][em]["name"].split()[0] + "!")

        popup([T("Create your account." if reg else "Login to continue shopping.", color=MUTED)]
              + ([name] if reg else []) + [email, pw, wide("Register" if reg else "Login", submit),
              ft.TextButton("Already have an account? Login" if reg else "Don't have an account? Register",
                            on_click=lambda e: auth_dialog("login" if reg else "reg"))],
              "Create Account" if reg else "Welcome Back")

    def open_account():
        if not db["user"]:
            return auth_dialog("login")
        u = db["users"][db["user"]]

        def logout(e):
            db["user"] = None
            save(db)
            close()
            refresh_badges()
            page.update()
            toast("You have been logged out.")

        popup([T(u["name"], 18, True), T(db["user"], color=MUTED),
               ft.Row([btn("My Orders", lambda e: show_orders()), btn("Logout", logout, False)], wrap=True)],
              "My Account")

    def show_orders():
        if not db["user"]:
            return auth_dialog("login")
        orders = db["orders"].get(db["user"], [])
        rows = [ft.Container(ft.Row([
            ft.Column([T(o["no"], 13, True), T(o["date"], 11, color=MUTED), T(inr(o["total"]), 13)], spacing=2, expand=True),
            btn("View", lambda e, o=o: receipt(o), False)]), padding=10, border=ft.border.all(1, BORDER), border_radius=10)
            for o in orders]
        popup(rows or [T("You have no orders yet.", color=MUTED)], "My Orders")

    # ---------- checkout and receipt ----------
    def checkout():
        if not db["cart"]:
            return toast("Your cart is empty.")
        if not db["user"]:
            toast("Please login to continue.")
            return auth_dialog("login")
        name = field("Full Name", value=db["users"][db["user"]]["name"])
        phone = field("Mobile Number", keyboard_type=ft.KeyboardType.PHONE, max_length=10)
        addr = field("Complete Address", multiline=True, min_lines=3)
        city = field("City", expand=True)
        pin = field("Pincode", keyboard_type=ft.KeyboardType.NUMBER, max_length=6, expand=True)
        pay = ft.RadioGroup(value="UPI", content=ft.Column([
            ft.Radio(value="UPI", label="📲 UPI"), ft.Radio(value="Card", label="💳 Card"),
            ft.Radio(value="COD", label="💵 Cash on Delivery")]))
        total = cart_total()

        def place(e):
            if not db["user"]:
                return auth_dialog("login")
            if (len((name.value or "").strip()) < 2 or not re.fullmatch(r"\d{10}", phone.value or "")
                    or len((addr.value or "").strip()) < 5 or not (city.value or "").strip()
                    or not re.fullmatch(r"\d{6}", pin.value or "")):
                return toast("Please fill all details correctly (10-digit mobile, 6-digit pincode).")
            now = datetime.now()
            o = {"no": "GH" + now.strftime("%y%m%d%H%M%S"), "date": now.strftime("%d %b %Y, %I:%M %p"),
                 "items": [{"name": BY[int(k)]["name"], "price": BY[int(k)]["price"], "qty": q}
                           for k, q in db["cart"].items()],
                 "total": total, "name": name.value.strip(), "phone": phone.value,
                 "address": f"{addr.value.strip()}, {city.value.strip()} - {pin.value}", "payment": pay.value}
            db["orders"].setdefault(db["user"], []).insert(0, o)
            db["cart"] = {}
            save(db)
            refresh_badges()
            receipt(o)

        lines = [ft.Row([T(f"{BY[int(k)]['name']} × {q}", 12, color=MUTED, expand=True),
                         T(inr(BY[int(k)]["price"] * q), 12)]) for k, q in db["cart"].items()]
        popup([T("Delivery Address", 16, True), name, phone, addr, ft.Row([city, pin]),
               T("Payment Method", 16, True), pay, ft.Divider(height=1, color=BORDER)] + lines +
              [ft.Row([T("Delivery", 12, color=MUTED), T("Free", 12, color="#16a34a")],
                      alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
               ft.Row([T("Total", 18, True), T(inr(total), 18, True)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
               wide("Place Order →", place)], "Secure Checkout")

    def receipt(o):
        tax = round(o["total"] / 1.18)
        space = ft.MainAxisAlignment.SPACE_BETWEEN
        rows = [ft.Row([T(i["name"], 12, expand=True), T(f"{i['qty']} × {inr(i['price'])}", 11, color=MUTED),
                        T(inr(i["price"] * i["qty"]), 12, True)]) for i in o["items"]]
        text = "\n".join([f"GADGET HUB - Receipt {o['no']}", o["date"], f"Customer: {o['name']} ({o['phone']})",
                          f"Address: {o['address']}", f"Payment: {o['payment']}", ""] +
                         [f"{i['name']} x{i['qty']}  {inr(i['price'] * i['qty'])}" for i in o["items"]] +
                         ["", f"Taxable value: {inr(tax)}", f"GST 18% (included): {inr(o['total'] - tax)}",
                          f"TOTAL: {inr(o['total'])}"])

        def copy(e):
            page.set_clipboard(text)
            toast("Receipt copied to clipboard.")

        popup([ft.Row([T("Gadget Hub", 20, True), T(o["no"], 11, color=MUTED)], alignment=space),
               T(o["date"], 11, color=MUTED), ft.Divider(height=1, color=BORDER),
               T(f"{o['name']} · {o['phone']}", 12, True), T(o["address"], 12, color=MUTED),
               T("Payment: " + o["payment"], 12, color=MUTED), ft.Divider(height=1, color=BORDER)] + rows +
              [ft.Divider(height=1, color=BORDER),
               ft.Row([T("Taxable value", 12, color=MUTED), T(inr(tax), 12)], alignment=space),
               ft.Row([T("GST 18% (included)", 12, color=MUTED), T(inr(o["total"] - tax), 12)], alignment=space),
               ft.Row([T("Grand Total", 18, True), T(inr(o["total"]), 18, True)], alignment=space),
               T("Thank you for shopping with Gadget Hub!", 12, color=MUTED, text_align=ft.TextAlign.CENTER),
               ft.Row([btn("Copy Receipt", copy), btn("Continue Shopping", lambda e: close(), False)], wrap=True)],
              "Order Confirmed")

    # ---------- page layout ----------
    search = ft.TextField(hint_text="Search gadgets...", prefix_icon=ft.Icons.SEARCH, border_radius=10, dense=True,
                          text_size=14, on_change=on_search)
    sort_dd = ft.Dropdown(value="default", width=170, dense=True, border_radius=8, text_size=13,
                          options=[ft.dropdown.Option(key="default", text="Sort by"),
                                   ft.dropdown.Option(key="low", text="Price: Low to High"),
                                   ft.dropdown.Option(key="high", text="Price: High to Low"),
                                   ft.dropdown.Option(key="rating", text="Highest Rated")],
                          on_change=lambda e: (view.update(sort=sort_dd.value), render()))

    def logo(color=DARK):
        return ft.Row([ft.Container(T("G", 18, True, "white"), bgcolor=PRIMARY, width=32, height=32, border_radius=9,
                                    alignment=ft.alignment.center), T("Gadget Hub", 20, True, color)],
                      spacing=6, tight=True)

    header = ft.Container(ft.Column([
        ft.Row([ft.GestureDetector(content=logo(), on_tap=lambda e: show_home()),
                ft.Row([wl_btn, cart_btn, user_btn], spacing=0)], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        search], spacing=4), bgcolor="white", padding=ft.padding.symmetric(horizontal=12, vertical=8),
        border=ft.border.only(bottom=ft.BorderSide(1, BORDER)))

    nav_items = [("Home", show_home), ("Products", go_products)] + [(c, lambda c=c: show_cat(c)) for c, _, _ in CATS]
    nav = ft.Container(ft.Row([ft.TextButton(n, on_click=lambda e, f=f: f(), style=ft.ButtonStyle(color="#475569"))
                               for n, f in nav_items], scroll=ft.ScrollMode.AUTO, spacing=0),
                       bgcolor="white", padding=ft.padding.symmetric(horizontal=6))

    hero = ft.Container(ft.Column([
        ft.Container(T("⚡ Next Generation Gadgets", 12, True, PRIMARY), bgcolor="#dbeafe", border_radius=30,
                     padding=ft.padding.symmetric(horizontal=14, vertical=8)),
        ft.Text(size=42, weight=ft.FontWeight.W_800, color=DARK, spans=[
            ft.TextSpan("Upgrade Your\n"), ft.TextSpan("Digital Life.", ft.TextStyle(color=PRIMARY))]),
        T("Discover smartphones, laptops, gaming gear, audio devices and premium accessories at Gadget Hub.", color=MUTED),
        ft.Row([btn("Shop Now →", lambda e: go_products()), btn("Explore Gaming", lambda e: show_cat(G), False)], wrap=True),
        ft.Row([ft.Column([T(a, 20, True), T(b, 12, color=MUTED)], spacing=2)
                for a, b in (("500+", "Products"), ("10K+", "Customers"), ("4.8★", "Rating"))], spacing=30),
        ft.Row([ft.Container(T("🎧", 80), width=170, height=200, alignment=ft.alignment.center, border_radius=40,
                             gradient=ft.LinearGradient(colors=["#111827", "#334155"]))],
               alignment=ft.MainAxisAlignment.CENTER),
    ], spacing=16), padding=ft.padding.symmetric(horizontal=20, vertical=30),
        gradient=ft.LinearGradient(begin=ft.alignment.top_left, end=ft.alignment.bottom_right, colors=["#eef5ff", "#ffffff"]))

    cats = ft.Container(ft.Column([
        T("EXPLORE", 11, True, PRIMARY), T("Shop by Category", 26, True),
        ft.ResponsiveRow([ft.Container(ft.Column([T(ic, 34), T(c, 14, True), T(sub, 11, color=MUTED)], spacing=4,
                          horizontal_alignment=ft.CrossAxisAlignment.CENTER), bgcolor="white", border_radius=16,
                          border=ft.border.all(1, BORDER), padding=16, ink=True, on_click=lambda e, c=c: show_cat(c),
                          col={"xs": 6, "sm": 4, "md": 2}) for c, ic, sub in CATS], spacing=10, run_spacing=10),
    ], spacing=8), padding=ft.padding.symmetric(horizontal=16, vertical=28))

    shop = ft.Container(ft.Column([
        T("OUR STORE", 11, True, PRIMARY), title_txt,
        ft.Row([sort_dd, btn("View All", lambda e: show_all(), False)], wrap=True), grid], spacing=10),
        key="products", padding=ft.padding.symmetric(horizontal=16, vertical=20))

    feats = ft.Container(ft.ResponsiveRow([
        ft.Row([T(ic, 26), ft.Column([T(a, 14, True), T(b, 11, color=MUTED)], spacing=0)], col={"xs": 12, "sm": 6, "md": 3})
        for ic, a, b in (("🚚", "Fast Delivery", "Quick & secure shipping"), ("🔒", "Secure Payment", "Safe checkout process"),
                         ("↩️", "Easy Returns", "Simple return policy"), ("💬", "Customer Support", "We're here to help"))],
        run_spacing=14), bgcolor="white", padding=ft.padding.symmetric(horizontal=20, vertical=24),
        border=ft.border.symmetric(horizontal=ft.BorderSide(1, BORDER)))

    link = lambda t, f: ft.TextButton(t, on_click=lambda e: f(), style=ft.ButtonStyle(color="#94a3b8"))
    footer = ft.Container(ft.Column([
        logo("white"),
        T("Your destination for smart technology, electronics and digital lifestyle products.", 12, color="#94a3b8"),
        ft.Row([link("My Orders", show_orders), link("Cart", open_cart), link("Wishlist", show_wishlist),
                link("Account", open_account)], wrap=True, spacing=0),
        T("📧 support@gadgethub.com   📞 +91 9561560448  📍 Pune, Maharashtra", 12, color="#94a3b8"),
        ft.Divider(height=1, color="#1e293b"), T("© 2026 Gadget Hub. All rights reserved.", 11, color="#64748b"),
    ], spacing=10), bgcolor="#0b1120", padding=ft.padding.symmetric(horizontal=20, vertical=30))

    main_col = ft.Column([hero, cats, shop, feats, footer], scroll=ft.ScrollMode.AUTO, expand=True, spacing=0,
                         horizontal_alignment=ft.CrossAxisAlignment.STRETCH)
    page.add(ft.SafeArea(ft.Column([header, nav, main_col], expand=True, spacing=0), expand=True))
    render()


if __name__ == "__main__":
    ft.app(target=main)
