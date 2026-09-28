import logging
import os
from html import escape

import telebot
from telebot import types
from telebot.apihelper import ApiTelegramException


# ============================================
# SETTINGS
# ============================================
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN is not set.")

# Your own site — hardcoded so the link can't be silently changed.
SITE_URL = "https://pensjonatgranada.pl/"

PHONE_DISPLAY = "+48 74 866 01 21"
EMAIL = "recepcja@pensjonatgranada.pl"
ADDRESS = "Łężyce 48A, 57-340 Duszniki-Zdrój"

# Optional extras — fill in to show the buttons (empty = hidden).
INSTAGRAM_URL = ""
FACEBOOK_URL = ""

BRAND = "Polska Na Co Dzień"

bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")
USER_LANGUAGES: dict[int, str] = {}


# ============================================
# SECTIONS (bilingual)
# key -> { pl: (title, desc, [items]), en: (title, desc, [items]) }
# ============================================
SECTIONS = {
    "nocleg": {
        "pl": (
            "🛏 Nocleg",
            "Pokoje i domki u stóp Gór Stołowych — kameralnie i blisko natury.",
            ["Pokoje w budynku głównym", "Domki z kominkiem i grillem", "Apartamenty z tarasem"],
        ),
        "en": (
            "🛏 Accommodation",
            "Rooms and cottages at the foot of the Table Mountains — cosy and close to nature.",
            ["Rooms in the main building", "Cottages with fireplace & grill", "Apartments with patio"],
        ),
    },
    "spa": {
        "pl": (
            "💆 Strefa SPA",
            "Odpoczynek i regeneracja po dniu w górach.",
            ["Strefa SPA & wellness", "Relaks i zabiegi", "Idealne po szlaku"],
        ),
        "en": (
            "💆 SPA zone",
            "Rest and recovery after a day in the mountains.",
            ["SPA & wellness zone", "Relaxation & treatments", "Perfect after a hike"],
        ),
    },
    "restauracja": {
        "pl": (
            "🍽 Restauracja & bar",
            "Kuchnia na miejscu i miła atmosfera wieczorem.",
            ["Restauracja", "Bar", "Miejsce do grillowania"],
        ),
        "en": (
            "🍽 Restaurant & bar",
            "On-site kitchen and a relaxed evening atmosphere.",
            ["Restaurant", "Bar", "Grill area"],
        ),
    },
    "udogodnienia": {
        "pl": (
            "✨ Udogodnienia",
            "Wszystko, by pobyt był wygodny — przez cały rok.",
            ["Bezpłatny parking", "Gry planszowe", "Piłkarzyki", "Czynne cały rok"],
        ),
        "en": (
            "✨ Facilities",
            "Everything for a comfortable stay — all year round.",
            ["Free parking", "Board games", "Table football", "Open year-round"],
        ),
    },
    "okolica": {
        "pl": (
            "🧭 Okolica",
            "Co zobaczyć i gdzie wyruszyć w pobliżu pensjonatu.",
            ["Muzeum Papiernictwa w Dusznikach (5 km)", "Duszniki-Zdrój (5 km)",
             "Polanica-Zdrój (15 km)", "Szlaki piesze i rowerowe"],
        ),
        "en": (
            "🧭 Around",
            "What to see and where to head near the guesthouse.",
            ["Paper Museum in Duszniki (5 km)", "Duszniki-Zdrój spa town (5 km)",
             "Polanica-Zdrój (15 km)", "Hiking & cycling trails"],
        ),
    },
}

SECTION_ORDER = ["nocleg", "spa", "restauracja", "udogodnienia", "okolica"]


# ============================================
# UI STRINGS (bilingual)
# ============================================
T = {
    "pl": {
        "sections_btn": "🏡 Oferta",
        "menu_btn": "🗂 Menu",
        "home_btn": "🏔 Start",
        "site_btn": "🌐 Otwórz stronę",
        "book_btn": "✅ Zarezerwuj online",
        "faq_btn": "❓ FAQ",
        "contact_btn": "✏️ Kontakt",
        "ig_btn": "📸 Instagram",
        "fb_btn": "📘 Facebook",
        "lang_btn": "🇬🇧 English",
        "back": "‹ Powrót do oferty",
        "highlights": "W skrócie:",
        "book_note": "Ceny i rezerwacja na stronie.",
        "help": "Wybierz przycisk poniżej, aby przejrzeć ofertę, FAQ lub dane kontaktowe.",
        "unknown": "Nie rozpoznałem tej wiadomości. Skorzystaj z menu poniżej.",
        "start": (
            f"🏔 <b>{escape(BRAND)}</b>\n\n"
            "<i>Pensjonat i SPA w Łężycach, u stóp Parku Narodowego Gór Stołowych.</i>\n\n"
            "Odkryj ofertę i zaplanuj pobyt. Dostępność oraz rezerwacja online "
            "są na naszej stronie."
        ),
        "sections": (
            "🏡 <b>Nasza oferta</b>\n\n"
            "Wybierz kategorię, aby zobaczyć szczegóły. Rezerwacja i ceny na stronie."
        ),
        "menu": (
            "🗂 <b>Menu</b>\n\n"
            "• Przeglądaj <b>ofertę</b> pensjonatu.\n"
            "• Rezerwuj bezpośrednio na stronie.\n"
            "• Zobacz najczęstsze pytania.\n"
            "• Skontaktuj się z recepcją."
        ),
        "faq": (
            "❓ <b>Najczęstsze pytania</b>\n\n"
            "<b>Jak zarezerwować?</b>\n"
            "Użyj przycisku rezerwacji — dostępność i ceny są na stronie. Można też "
            "zadzwonić lub napisać do recepcji.\n\n"
            "<b>Czy jest parking?</b>\n"
            "Tak, bezpłatny parking dla gości.\n\n"
            "<b>Czy przyjmujecie zwierzęta?</b>\n"
            "Prosimy o kontakt z recepcją — potwierdzimy warunki pobytu ze zwierzęciem.\n\n"
            "<b>Czy jest czynne zimą?</b>\n"
            "Tak, pensjonat jest czynny przez cały rok."
        ),
        "contact": (
            "✏️ <b>Kontakt</b>\n\n"
            f"• Telefon: {PHONE_DISPLAY}\n"
            f"• E-mail: {EMAIL}\n"
            f"• Adres: {ADDRESS}\n\n"
            "Rezerwacje i dostępność najszybciej przez stronę."
        ),
    },
    "en": {
        "sections_btn": "🏡 Our offer",
        "menu_btn": "🗂 Menu",
        "home_btn": "🏔 Home",
        "site_btn": "🌐 Open website",
        "book_btn": "✅ Book online",
        "faq_btn": "❓ FAQ",
        "contact_btn": "✏️ Contact",
        "ig_btn": "📸 Instagram",
        "fb_btn": "📘 Facebook",
        "lang_btn": "🇵🇱 Polski",
        "back": "‹ Back to offer",
        "highlights": "In short:",
        "book_note": "Prices and booking on the website.",
        "help": "Choose a button below to explore the stay, FAQs, or contact details.",
        "unknown": "I didn't recognize that message. Use the menu below to continue.",
        "start": (
            f"🏔 <b>{escape(BRAND)}</b>\n\n"
            "<i>Guesthouse &amp; SPA in Łężyce, at the foot of the Table Mountains National Park.</i>\n\n"
            "Explore the offer and plan your stay. Check availability and book online "
            "on our website."
        ),
        "sections": (
            "🏡 <b>Our offer</b>\n\n"
            "Pick a category to see details. Booking and prices are on the website."
        ),
        "menu": (
            "🗂 <b>Menu</b>\n\n"
            "• Browse the guesthouse <b>offer</b>.\n"
            "• Book directly on the website.\n"
            "• Read frequently asked questions.\n"
            "• Contact the reception."
        ),
        "faq": (
            "❓ <b>Frequently asked questions</b>\n\n"
            "<b>How do I book?</b>\n"
            "Use the booking button — availability and prices are on the website. You can "
            "also call or e-mail the reception.\n\n"
            "<b>Is there parking?</b>\n"
            "Yes, free parking for guests.\n\n"
            "<b>Are pets allowed?</b>\n"
            "Please contact reception — we'll confirm the conditions for a stay with a pet.\n\n"
            "<b>Are you open in winter?</b>\n"
            "Yes, the guesthouse is open all year round."
        ),
        "contact": (
            "✏️ <b>Contact</b>\n\n"
            f"• Phone: {PHONE_DISPLAY}\n"
            f"• E-mail: {EMAIL}\n"
            f"• Address: {ADDRESS}\n\n"
            "Bookings and availability are fastest via the website."
        ),
    },
}


# ============================================
# HELPERS  (callback_data: "<lang>|<action>", action may be "sec:nocleg")
# ============================================
def cb(lang, action):
    return f"{lang}|{action}"


def btn(text, lang, action):
    return types.InlineKeyboardButton(text=text, callback_data=cb(lang, action))


def language_for_user(user_id, language_code=None):
    if user_id in USER_LANGUAGES:
        return USER_LANGUAGES[user_id]
    return "pl" if (language_code or "").lower().startswith("pl") else "en"


def url_btn(text, url):
    return types.InlineKeyboardButton(text=text, url=url)


def site_btn(lang):
    return types.InlineKeyboardButton(
        text=T[lang]["site_btn"], web_app=types.WebAppInfo(url=SITE_URL)
    )


def book_btn(lang):
    return types.InlineKeyboardButton(
        text=T[lang]["book_btn"], web_app=types.WebAppInfo(url=SITE_URL)
    )


def ig_btn(lang):
    return url_btn(T[lang]["ig_btn"], INSTAGRAM_URL) if INSTAGRAM_URL else None


def fb_btn(lang):
    return url_btn(T[lang]["fb_btn"], FACEBOOK_URL) if FACEBOOK_URL else None


def lang_btn(lang):
    other = "en" if lang == "pl" else "pl"
    return types.InlineKeyboardButton(text=T[lang]["lang_btn"], callback_data=cb(other, "home"))


def make_markup(rows):
    markup = types.InlineKeyboardMarkup()
    for row in rows:
        row = [b for b in row if b is not None]
        if row:
            markup.row(*row)
    return markup


def nav_row(lang):
    return [
        btn(T[lang]["home_btn"], lang, "home"),
        btn(T[lang]["menu_btn"], lang, "menu"),
    ]


# ============================================
# SCREEN / CARD BUILDERS
# ============================================
def section_text(lang, key):
    title, desc, items = SECTIONS[key][lang]
    lines = "\n".join(f"• {escape(item)}" for item in items)
    return (
        f"<b>{escape(title)}</b>\n"
        "━━━━━━━━━━━━━━\n\n"
        f"{escape(desc)}\n\n"
        f"<b>{T[lang]['highlights']}</b>\n{lines}\n\n"
        "━━━━━━━━━━━━━━\n"
        f"<i>{T[lang]['book_note']}</i>"
    )


def section_rows(lang, key):
    return [
        [book_btn(lang)],
        [btn(T[lang]["back"], lang, "sections"), btn(T[lang]["menu_btn"], lang, "menu")],
        [lang_btn(lang)],
    ]


def screen(lang, action):
    s = T[lang]
    if action in ("home", "start"):
        return s["start"], [
            [btn(s["sections_btn"], lang, "sections")],
            [book_btn(lang)],
            [btn(s["faq_btn"], lang, "faq"), btn(s["contact_btn"], lang, "contact")],
            [site_btn(lang)],
            [ig_btn(lang), fb_btn(lang)],
            [lang_btn(lang)],
        ]
    if action == "sections":
        rows = [[btn(SECTIONS[k][lang][0], lang, f"sec:{k}")] for k in SECTION_ORDER]
        rows.extend([
            nav_row(lang),
            [lang_btn(lang)],
        ])
        return s["sections"], rows
    if action in ("menu", "help"):
        text = s["help"] if action == "help" else s["menu"]
        return text, [
            [btn(s["sections_btn"], lang, "sections")],
            [btn(s["faq_btn"], lang, "faq"), btn(s["contact_btn"], lang, "contact")],
            [site_btn(lang)],
            [ig_btn(lang), fb_btn(lang)],
            nav_row(lang),
            [lang_btn(lang)],
        ]
    if action == "faq":
        return s["faq"], [
            [btn(s["sections_btn"], lang, "sections")],
            [btn(s["contact_btn"], lang, "contact")],
            nav_row(lang),
            [lang_btn(lang)],
        ]
    if action == "contact":
        return s["contact"], [
            [book_btn(lang)],
            [ig_btn(lang), fb_btn(lang)],
            [btn(s["sections_btn"], lang, "sections"), btn(s["menu_btn"], lang, "menu")],
            [btn(s["home_btn"], lang, "home"), lang_btn(lang)],
        ]
    return None


# ============================================
# HANDLERS
# ============================================
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.row(
        types.InlineKeyboardButton("🇵🇱 Polski", callback_data=cb("pl", "home")),
        types.InlineKeyboardButton("🇬🇧 English", callback_data=cb("en", "home")),
    )
    bot.send_message(
        message.chat.id,
        f"🏔 <b>{escape(BRAND)}</b>\n"
        "Pensjonat &amp; SPA · Łężyce\n\n"
        "<i>Wybierz język / Choose your language</i>",
        reply_markup=markup,
    )


@bot.message_handler(commands=["menu"])
def open_menu(message):
    lang = language_for_user(
        message.from_user.id,
        getattr(message.from_user, "language_code", None),
    )
    text, rows = screen(lang, "menu")
    bot.send_message(message.chat.id, text, reply_markup=make_markup(rows))


@bot.message_handler(commands=["help"])
def help_message(message):
    lang = language_for_user(
        message.from_user.id,
        getattr(message.from_user, "language_code", None),
    )
    text, rows = screen(lang, "help")
    bot.send_message(message.chat.id, text, reply_markup=make_markup(rows))


@bot.message_handler(
    func=lambda message: bool(message.text and not message.text.startswith("/")),
    content_types=["text"],
)
def handle_text(message):
    lang = language_for_user(
        message.from_user.id,
        getattr(message.from_user, "language_code", None),
    )
    normalized = message.text.strip().casefold()
    action_aliases = {
        "menu": "menu",
        "offer": "sections",
        "oferta": "sections",
        "faq": "faq",
        "contact": "contact",
        "kontakt": "contact",
    }
    action = action_aliases.get(normalized)
    if action:
        text, rows = screen(lang, action)
    else:
        text = T[lang]["unknown"]
        _, rows = screen(lang, "menu")
    bot.send_message(message.chat.id, text, reply_markup=make_markup(rows))


def render(call, text, rows):
    markup = make_markup(rows)
    try:
        bot.edit_message_text(
            text, chat_id=call.message.chat.id,
            message_id=call.message.message_id, reply_markup=markup,
        )
    except ApiTelegramException as exc:
        if "message is not modified" in str(exc).lower():
            return
        logging.warning("Could not edit the current menu; sending a new message: %s", exc)
        bot.send_message(call.message.chat.id, text, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: "|" in call.data)
def on_callback(call):
    lang, action = call.data.split("|", 1)
    if lang not in T:
        bot.answer_callback_query(call.id, "This menu has expired. Send /start.")
        return
    USER_LANGUAGES[call.from_user.id] = lang
    bot.answer_callback_query(call.id)
    if action.startswith("sec:"):
        key = action.split(":", 1)[1]
        if key in SECTIONS:
            render(call, section_text(lang, key), section_rows(lang, key))
        else:
            result = screen(lang, "sections")
            render(call, result[0], result[1])
        return
    result = screen(lang, action)
    if result:
        render(call, result[0], result[1])
    else:
        result = screen(lang, "menu")
        render(call, result[0], result[1])


def main() -> None:
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        level=logging.INFO,
    )
    logging.getLogger("urllib3").setLevel(logging.WARNING)

    try:
        bot.set_my_commands([
            types.BotCommand("start", "Choose language and open welcome"),
            types.BotCommand("menu", "Open the main menu"),
            types.BotCommand("help", "How to use the bot"),
        ])
    except ApiTelegramException as exc:
        logging.warning("Could not register bot commands: %s", exc)

    try:
        bot.set_chat_menu_button(
            menu_button=types.MenuButtonWebApp(
                type="web_app",
                text="Polska Na Co Dzień",
                web_app=types.WebAppInfo(url=SITE_URL),
            )
        )
    except ApiTelegramException:
        pass

    logging.info("%s bot is starting", BRAND)
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
