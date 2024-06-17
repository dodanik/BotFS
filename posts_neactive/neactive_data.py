from database.list_users import get_link_mirror


async def get_posts_with_freebet_code(promo_code):
    link_mirror = await get_link_mirror()
    posts = {
        'ru': {
            'description': f"""
🎉 Готов к новым победам? 
FANSPORT дарит тебе промокод на фрибет! 
🏆 Вводи промокод и начинай выигрывать уже сейчас. 
📈 Не упусти шанс пополнить свой баланс!

👉 Введи промокод: {promo_code}

FANSPORT – твой путь к успеху и азарту! 🎰✨
""",
            'button': "Играть сейчас",
            'link': link_mirror,
            'image': 'img/freebet.png'  # Относительный путь к изображению для фрибета
        },
        'kk': {
            'description': f"""
🎉 Жаңа жеңістерге дайынсың ба?
FANSPORT саған фрибетке арналған промокод сыйлайды!
🏆 Промокодты енгіз де, қазірден бастап жеңіске жетуді баста.
📈 Өз балансыңды толықтыру мүмкіндігін жіберіп алма!

👉 Промокодты енгіз: {promo_code}

FANSPORT – сенің табыс пен құмарлыққа апарар жолың! 🎰✨
""",
            'button': "Ойнау",
            'link': link_mirror,
            'image': 'img/freebet.png'  # Относительный путь к изображению для фрибета
        },
        'en': {
            'description': f"""
🎉 Ready for new victories?
FANSPORT gives you a promo code for a free bet!
🏆 Enter the promo code and start winning now.
📈 Don’t miss the chance to boost your balance!

👉 Enter the promo code: {promo_code}

FANSPORT – your path to success and excitement! 🎰✨
""",
            'button': "Play now",
            'link': link_mirror,
            'image': 'img/freebet.png'  # Относительный путь к изображению для фрибета
        }
    }
    return posts

async def get_posts_with_promo_code(promo_code):
    link_mirror = await get_link_mirror()
    posts = {
        'ru': {
            'description': f"""
🔥 А ты готов к невероятным приключениям? 
🎰 FANSPORT дарит тебе промокод на фриспины! 
💥 Лови момент, вводи промокод и почувствуй настоящую игру! 
💰 Не упусти свой шанс!

👉 Введи промокод: {promo_code}

FANSPORT – играй, выигрывай, наслаждайся! 🎉
""",
            'button': "Играть сейчас",
            'link': link_mirror,
            'image': 'img/freespins.png'  # Относительный путь к изображению для фриспинов
        },
        'kk': {
            'description': f"""
🔥 Сен керемет оқиғаларға дайынсың ба?
🎰 FANSPORT саған фриспиндерге арналған промокод сыйлайды!
💥 Сәттілік сәтін ұстап, промокодты енгізіп, нағыз ойынның дәмін татқандай бол!
💰 Өз мүмкіндігіңді жіберіп алма!

👉 Промокодты енгіз: {promo_code}

FANSPORT – ойна, жең, ләззат ал! 🎉
""",
            'button': "Ойнау",
            'link': link_mirror,
            'image': 'img/freespins.png'  # Относительный путь к изображению для фриспинов
        },
        'en': {
            'description': f"""
🔥 Are you ready for incredible adventures?
🎰 FANSPORT gives you a promo code for free spins!
💥 Catch the moment, enter the promo code, and feel the real game!
💰 Don’t miss your chance!

👉 Enter the promo code: {promo_code}

FANSPORT – play, win, enjoy! 🎉
""",
            'button': "Play now",
            'link': link_mirror,
            'image': 'img/freespins.png'  # Относительный путь к изображению для фриспинов
        }
    }
    return posts

async def get_posts_without_promo():
    link_mirror = await get_link_mirror()
    posts = {
        'ru': {
            'description': f"""
🔥 Братан, мы уже заскучали! 
FANSPORT готов вернуть тебя в игру с новыми победами и яркими эмоциями!
💥 Пора вспомнить, что значит быть в игре! 
Закидывай бабки на баланс и врывайся в наш мир казино и ставок на спорт. 
Не упусти шанс – возвращайся в игру и лови кайф от побед!

👉 Делай депозит прямо сейчас и начни выигрывать с FANSPORT.
""",
            'button': "Депозит сейчас",
            'link': link_mirror,
            'image': 'img/deposit.png'  # Относительный путь к изображению
        },
        'kk': {
            'description': f"""
🔥 Братан, біз сені қатты сағындық!
FANSPORT сені жаңа жеңістер мен жарқын эмоциялармен қайтадан ойынға қосуға дайын!
💥 Ойынның не екенін еске түсіретін уақыт келді!
Балансқа ақша сал да, біздің казино мен спорттық ставкалар әлеміне кіріп кет.
Мүмкіндігіңді жіберіп алма – ойынға қайтып келіп, жеңістің рақатын сезін!

👉 Қазір депозит жаса да, FANSPORT-пен жеңіске жете баста.
""",
            'button': "Депозит қазір",
            'link': link_mirror,
            'image': 'img/deposit.png'  # Относительный путь к изображению
        },
        'en': {
            'description': f"""
🔥 Bro, we’ve missed you!
FANSPORT is ready to bring you back into the game with new victories and bright emotions!
💥 It’s time to remember what it means to be in the game!
Deposit some cash into your balance and dive into our world of casino and sports betting.
Don’t miss your chance – get back in the game and enjoy the thrill of winning!

👉 Make a deposit right now and start winning with FANSPORT.
""",
            'button': "Deposit now",
            'link': link_mirror,
            'image': 'img/deposit.png'  # Относительный путь к изображению
        }
    }
    return posts
