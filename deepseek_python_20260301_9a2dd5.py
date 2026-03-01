import telebot
from telebot import types
import random
import time
import json
import os
from threading import Timer, RLock, Thread
from datetime import datetime, timedelta
import hashlib
import sys
import signal

# ====================== КОНФИГУРАЦИЯ ======================
TOKEN = os.getenv('BOT_TOKEN', '8019174987:AAFd_qG434htnd94mnCOZfd2ejD0hgTGUJk')
ADMIN_PASSWORD_HASH = hashlib.sha256('Kyniksvs1832'.encode()).hexdigest()

OWNER_USERNAME = '@kyniks'
CHANNEL_USERNAME = '@werdoxz_wiinere'
CHAT_LINK = 'https://t.me/+B7u5OmPsako4MTAy'

# Файлы для хранения данных
DATA_FILE = 'bot_data.json'
USERNAME_CACHE_FILE = 'username_cache.json'
PROMO_FILE = 'promocodes.json'
BUSINESS_FILE = 'business_data.json'
CLAN_FILE = 'clan_data.json'
ACHIEVEMENTS_FILE = 'achievements.json'
QUESTS_FILE = 'quests_data.json'
EVENT_FILE = 'event_data.json'
CASES_FILE = 'cases_data.json'
ORDERS_FILE = 'orders.json'
CHEQUES_FILE = 'cheques.json'
MICE_FILE = 'mice_data.json'
PETS_FILE = 'pets_data.json'
BANK_FILE = 'bank_data.json'
PHONE_FILE = 'phone_data.json'
BONUS_FILE = 'bonus_data.json'
DUEL_FILE = 'duel_data.json'
TOURNAMENT_FILE = 'tournament_data.json'
STATS_FILE = 'stats_data.json'
DAILY_QUESTS_FILE = 'daily_quests.json'

MAX_BET = 100000000
GAME_TIMEOUT = 300

# Константы для игр
TOWER_MULTIPLIERS = {1: 1.3, 2: 1.5, 3: 1.6, 4: 2.0, 5: 3.0}          # изменено
FOOTBALL_MULTIPLIER = 2.0
BASKETBALL_MULTIPLIER = 2.0
PYRAMID_CELLS = 10
PYRAMID_MULTIPLIER = 5.0
DARTS_MULTIPLIERS = {1: 1.5, 2: 2.0, 3: 3.0, 4: 5.0, 5: 10.0}
POKER_MULTIPLIER = 2.0
MINES_MULTIPLIERS = {
    1: {1: 1.1, 2: 1.2, 3: 1.3, 4: 1.4, 5: 1.5, 6: 1.6, 7: 1.7, 8: 1.8, 9: 1.9, 10: 2.0},
    2: {1: 1.2, 2: 1.4, 3: 1.6, 4: 1.8, 5: 2.0, 6: 2.2, 7: 2.4, 8: 2.6, 9: 2.8, 10: 3.0},
    3: {1: 1.3, 2: 1.6, 3: 2.0, 4: 2.4, 5: 2.8, 6: 3.2, 7: 3.6, 8: 4.0, 9: 4.5, 10: 5.0},
    4: {1: 1.5, 2: 2.0, 3: 2.5, 4: 3.0, 5: 3.5, 6: 4.0, 7: 4.5, 8: 5.0, 9: 5.5, 10: 6.0},
    5: {1: 2.0, 2: 3.0, 3: 4.0, 4: 5.0, 5: 6.0, 6: 7.0, 7: 8.0, 8: 9.0, 9: 10.0, 10: 12.0}
}
BLACKJACK_MULTIPLIER = 2.0
SLOTS_SYMBOLS = ['🍒', '🍋', '🍊', '🍇', '💎', '7️⃣']
SLOTS_PAYOUTS = {
    ('7️⃣', '7️⃣', '7️⃣'): 10.0,
    ('💎', '💎', '💎'): 5.0,
    ('🍇', '🍇', '🍇'): 3.0,
    ('🍊', '🍊', '🍊'): 2.0,
    ('🍋', '🍋', '🍋'): 1.5,
    ('🍒', '🍒', '🍒'): 1.2
}
HILO_MULT = 2.0
HILO_WIN_CHANCE = 0.5
ROULETTE_NUMBERS = list(range(37))
RED_NUMBERS = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
BLACK_NUMBERS = [2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35]
ROULETTE_MULTIPLIERS = {
    'straight': 36,
    'red': 2,
    'black': 2,
    'even': 2,
    'odd': 2,
    '1-18': 2,
    '19-36': 2,
    'dozen': 3
}

# Ивент к 1 марта (множитель отключён)
RELEASE_EVENT = {
    'active': True,
    'multiplier': 1.0,
    'end_time': time.time() + 3 * 86400
}

# ====================== VIP СИСТЕМА ======================
VIP_LEVELS = {
    'bronze': {
        'name': '🥉 Бронзовый',
        'price': 50000,
        'duration': 30 * 86400,
        'bonus_mult': 1.0,
        'daily_bonus_mult': 1.0,
        'work_mult': 1.0,
        'max_bet_mult': 1.5,
        'quest_slots': 3,
        'krds_weekly': 5,
        'color': '🟫',
        'perks': [
            '🎰 +50% к макс ставке',
            '💎 +5 KRDS в неделю',
            '📋 3 ежедневных квеста'
        ]
    },
    'silver': {
        'name': '🥈 Серебряный',
        'price': 150000,
        'duration': 30 * 86400,
        'bonus_mult': 1.0,
        'daily_bonus_mult': 1.0,
        'work_mult': 1.0,
        'max_bet_mult': 2.0,
        'quest_slots': 4,
        'krds_weekly': 15,
        'color': '⚪️',
        'perks': [
            '🎰 x2 к макс ставке',
            '💎 +15 KRDS в неделю',
            '📋 4 ежедневных квеста'
        ]
    },
    'gold': {
        'name': '🥇 Золотой',
        'price': 500000,
        'duration': 30 * 86400,
        'bonus_mult': 1.0,
        'daily_bonus_mult': 1.0,
        'work_mult': 1.0,
        'max_bet_mult': 3.0,
        'quest_slots': 5,
        'krds_weekly': 30,
        'color': '🌟',
        'perks': [
            '🎰 x3 к макс ставке',
            '💎 +30 KRDS в неделю',
            '📋 5 ежедневных квеста'
        ]
    },
    'platinum': {
        'name': '💎 Платиновый',
        'price': 1000000,
        'duration': 30 * 86400,
        'bonus_mult': 1.0,
        'daily_bonus_mult': 1.0,
        'work_mult': 1.0,
        'max_bet_mult': 5.0,
        'quest_slots': 6,
        'krds_weekly': 50,
        'color': '💫',
        'perks': [
            '🎰 x5 к макс ставке',
            '💎 +50 KRDS в неделю',
            '📋 6 ежедневных квеста'
        ]
    }
}

# ====================== ЕЖЕДНЕВНЫЕ КВЕСТЫ ======================
DAILY_QUESTS = {
    'play_games': {
        'name': '🎮 Игроман',
        'desc': 'Сыграть {target} игр',
        'rewards': {1: 500, 3: 2000, 5: 5000, 10: 15000},
        'icon': '🎮',
        'type': 'games_played'
    },
    'win_games': {
        'name': '🏆 Победитель',
        'desc': 'Выиграть {target} игр',
        'rewards': {1: 1000, 3: 3000, 5: 7500, 10: 20000},
        'icon': '🏆',
        'type': 'wins'
    },
    'mice_collect': {
        'name': '🐭 Мышиная лихорадка',
        'desc': 'Собрать доход с мышек {target} раз',
        'rewards': {1: 1000, 3: 2500, 5: 6000, 10: 15000},
        'icon': '🐭',
        'type': 'mice_collects'
    },
    'business_collect': {
        'name': '🏢 Бизнесмен',
        'desc': 'Собрать доход с бизнеса {target} раз',
        'rewards': {1: 1500, 3: 4000, 5: 10000, 10: 25000},
        'icon': '🏢',
        'type': 'business_collects'
    },
    'work': {
        'name': '💼 Трудяга',
        'desc': 'Поработать {target} раз',
        'rewards': {1: 500, 3: 1500, 5: 3000, 10: 8000},
        'icon': '💼',
        'type': 'works'
    },
    'referrals': {
        'name': '🤝 Реферал',
        'desc': 'Пригласить {target} друзей',
        'rewards': {1: 5000, 3: 15000, 5: 30000},
        'icon': '🤝',
        'type': 'referrals'
    },
    'bank_deposit': {
        'name': '💰 Банкир',
        'desc': 'Положить в банк {target} кредиксов',
        'rewards': {10000: 1000, 50000: 5000, 100000: 10000, 500000: 50000},
        'icon': '💰',
        'type': 'deposit_amount'
    },
    'games_big_win': {
        'name': '🎰 Крупный выигрыш',
        'desc': 'Выиграть {target} кредиксов за одну игру',
        'rewards': {10000: 2000, 50000: 10000, 100000: 25000, 500000: 100000},
        'icon': '🎰',
        'type': 'biggest_win'
    }
}

# Ивентовые квесты к 1 марта
EVENT_QUESTS = {
    'march_1': {
        'name': '🌸 Весенний',
        'desc': 'Сыграть 5 игр с ивентовым множителем',
        'rewards': 5000,
        'icon': '🌸',
        'type': 'event_games'
    }
}

# ====================== ТУРНИРЫ ======================
TOURNAMENT_TYPES = {
    'daily': {
        'name': '📅 Ежедневный',
        'duration': 86400,
        'prize_pool': 100000,
        'entry_fee': 1000
    },
    'weekly': {
        'name': '📆 Еженедельный',
        'duration': 604800,
        'prize_pool': 500000,
        'entry_fee': 5000
    },
    'monthly': {
        'name': '📅 Месячный',
        'duration': 2592000,
        'prize_pool': 2000000,
        'entry_fee': 20000
    }
}

# ====================== ДАННЫЕ О МЫШКАХ, ПИТОМЦАХ, БИЗНЕСАХ И КЕЙСАХ ======================
MICE_DATA = {
    'standard': {
        'name': '💖 Мышка - стандарт 💖',
        'price': 100000,
        'total': 100,
        'sold': 0,
        'rarity': 'обычная',
        'description': '👻 Для украшения аккаунта',
        'signature': 'kyn k.y 🌟',
        'version': 'стандарт',
        'income': 500,
        'income_interval': 3600,
        'icon': '🐭'
    },
    'china': {
        'name': '🤩 Мышка - чуньхаохаокакао 🤩',
        'price': 500000,
        'total': 100,
        'sold': 0,
        'rarity': 'средняя',
        'description': '💖 Китайская коллекционная мышка',
        'signature': 'chinalals k.y 💖',
        'version': 'china',
        'income': 1000,
        'income_interval': 3600,
        'icon': '🐹'
    },
    'world': {
        'name': '🌍 Мышка - мира 🌍',
        'price': 1000000,
        'total': 100,
        'sold': 0,
        'rarity': 'Lux',
        'description': '🍦 Эксклюзивная мышка мира',
        'signature': 'lux k.y 🖊️',
        'version': 'maximum',
        'income': 5000,
        'income_interval': 3600,
        'icon': '🐼'
    }
}

PETS_DATA = {
    'dog': {
        'name': '🐕 Пёс',
        'price': 5000,
        'food_cost': 10,
        'happiness': 100,
        'income': 50,
        'rarity': 'обычный',
        'description': 'Верный друг, приносит небольшой доход'
    },
    'cat': {
        'name': '🐈 Кот',
        'price': 7500,
        'food_cost': 8,
        'happiness': 100,
        'income': 70,
        'rarity': 'обычный',
        'description': 'Независимый, но прибыльный'
    },
    'parrot': {
        'name': '🦜 Попугай',
        'price': 12000,
        'food_cost': 5,
        'happiness': 100,
        'income': 100,
        'rarity': 'редкий',
        'description': 'Говорящий, приносит хороший доход'
    },
    'hamster': {
        'name': '🐹 Хомяк',
        'price': 3000,
        'food_cost': 3,
        'happiness': 100,
        'income': 30,
        'rarity': 'обычный',
        'description': 'Маленький, но трудолюбивый'
    },
    'dragon': {
        'name': '🐲 Дракон',
        'price': 100000,
        'food_cost': 50,
        'happiness': 100,
        'income': 1000,
        'rarity': 'легендарный',
        'description': 'Мифическое существо, огромный доход'
    }
}

BUSINESS_DATA = {
    'kiosk': {
        'name': '🏪 Ларёк',
        'price': 10000,
        'income': 500,
        'level': 1,
        'max_level': 10,
        'upgrade_cost': 5000,
        'icon': '🏪',
        'description': 'Маленький, но стабильный доход'
    },
    'shop': {
        'name': '🏬 Магазин',
        'price': 50000,
        'income': 2000,
        'level': 1,
        'max_level': 10,
        'upgrade_cost': 25000,
        'icon': '🏬',
        'description': 'Серьёзный бизнес'
    },
    'restaurant': {
        'name': '🍽️ Ресторан',
        'price': 200000,
        'income': 10000,
        'level': 1,
        'max_level': 10,
        'upgrade_cost': 100000,
        'icon': '🍽️',
        'description': 'Премиум сегмент'
    },
    'factory': {
        'name': '🏭 Завод',
        'price': 1000000,
        'income': 50000,
        'level': 1,
        'max_level': 10,
        'upgrade_cost': 500000,
        'icon': '🏭',
        'description': 'Промышленный масштаб'
    },
    'corporation': {
        'name': '🏢 Корпорация',
        'price': 10000000,
        'income': 500000,
        'level': 1,
        'max_level': 10,
        'upgrade_cost': 5000000,
        'icon': '🏢',
        'description': 'Мировой уровень'
    }
}

CLAN_DATA = {
    'create_cost': 100000,
    'max_members': 50,
    'war_cost': 50000,
    'bonus_per_member': 1000
}

CASES = {
    'case1': {'name': '😁 лол 😁', 'price': 3000, 'min_win': 1000, 'max_win': 5000, 'icon': '📦'},
    'case2': {'name': '🎮 лотус 🎮', 'price': 10000, 'min_win': 7500, 'max_win': 15000, 'icon': '🎮'},
    'case3': {'name': '💫 люкс кейс 💫', 'price': 50000, 'min_win': 35000, 'max_win': 65000, 'icon': '💫'},
    'case4': {'name': '💎 Платинум 💍', 'price': 200000, 'min_win': 175000, 'max_win': 250000, 'icon': '💎'},
    'case5': {'name': '💫 специальный кейс 👾', 'price': 1000000, 'min_win': 750000, 'max_win': 1250000, 'icon': '👾'},
    'case6': {'name': '🎉 ивентовый 🎊', 'price': 0, 'min_win': 12500, 'max_win': 75000, 'icon': '🎉'}
}

# ====================== ДОСТИЖЕНИЯ ======================
achievements = {
    'first_game': {'name': '🎮 Первый шаг', 'desc': 'Сыграть первую игру', 'reward': 1000},
    'millionaire': {'name': '💰 Миллионер', 'desc': 'Накопить 1,000,000 кредиксов', 'reward': 50000},
    'referral_master': {'name': '🤝 Реферал', 'desc': 'Пригласить 10 друзей', 'reward': 100000},
    'mice_collector': {'name': '🐭 Мышиный король', 'desc': 'Собрать всех видов мышек', 'reward': 150000},
    'pet_collector': {'name': '🐾 Зоофил', 'desc': 'Собрать всех питомцев', 'reward': 100000},
    'clan_leader': {'name': '👑 Лидер клана', 'desc': 'Создать клан', 'reward': 50000},
    'banker': {'name': '💳 Банкир', 'desc': 'Положить 1,000,000 в банк', 'reward': 75000},
    'businessman': {'name': '💼 Бизнесмен', 'desc': 'Купить 5 бизнесов', 'reward': 100000},
    'phone_addict': {'name': '📱 Телефономан', 'desc': 'Сделать 100 звонков', 'reward': 25000},
    'bonus_hunter': {'name': '🎁 Охотник за бонусами', 'desc': 'Забрать 30 ежедневных бонусов', 'reward': 50000},
    'tournament_winner': {'name': '🏆 Чемпион', 'desc': 'Выиграть турнир', 'reward': 100000},
    'quest_master': {'name': '✨ Мастер квестов', 'desc': 'Выполнить 100 квестов', 'reward': 75000}
}

# ====================== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ ======================
users = {}
username_cache = {}
game_timers = {}
crash_update_timers = {}
crash_locks = {}
admin_users = set()
promocodes = {}
orders = {}
next_order_id = 1
cheques = {}
user_cases = {}
user_achievements = {}
user_quests = {}
duels = {}
clans = {}
businesses = {}
event_data = {'active': True, 'participants': {}, 'leaderboard': [], 'last_update': time.time()}
jackpot = {'total': 0, 'last_winner': None, 'last_win_time': None, 'history': []}
daily_reward = {}
daily_quests_data = {}
tournaments = {}

bank_data = {
    'loans': {},
    'deposits': {},
    'transfers': [],
    'total_deposits': 0,
    'interest_rate': 0.05
}

phone_data = {
    'contacts': {},
    'calls': {},
    'messages': {},
    'phone_numbers': {}
}

bonus_data = {
    'daily': {},
    'weekly': {},
    'monthly': {},
    'referral_bonus': 5000
}

pets_data = {}
clans_data = {}
businesses_data = {}
stats_data = {}

data_lock = RLock()
user_locks = {}

# ====================== ИНИЦИАЛИЗАЦИЯ БОТА ======================
bot = telebot.TeleBot(TOKEN)

# ---------------------- Функции загрузки/сохранения ----------------------
def safe_json_load(file_path, default_value=None):
    if default_value is None:
        default_value = {}
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
                else:
                    return default_value
        except Exception as e:
            print(f"Ошибка загрузки {file_path}: {e}")
            return default_value
    return default_value

def default_user():
    return {
        'balance': 1000,
        'krds_balance': 0,
        'game': None,
        'referrals': 0,
        'referrer': None,
        'banned': False,
        'bank': {'balance': 0, 'last_interest': time.time(), 'history': []},
        'used_promos': [],
        'clan': None,
        'total_wins': 0,
        'total_losses': 0,
        'games_played': 0,
        'win_streak': 0,
        'max_win_streak': 0,
        'total_lost': 0,
        'quests_completed': 0,
        'event_points': 0,
        'game_history': [],
        'daily_last_claim': 0,
        'daily_streak': 0,
        'last_case6_open': 0,
        'mice': {},
        'mice_last_collect': {},
        'pets': {},
        'pets_last_feed': {},
        'businesses': {},
        'businesses_last_collect': {},
        'phone_number': None,
        'phone_contacts': [],
        'phone_call_history': [],
        'phone_messages': [],
        'daily_bonus': {'last_claim': 0, 'streak': 0},
        'weekly_bonus': {'last_claim': 0, 'streak': 0},
        'bank_deposit': {'amount': 0, 'time': 0},
        'bank_loan': {'amount': 0, 'time': 0},
        'work_count': 0,
        'vip_level': None,
        'vip_expires': 0,
        'vip_last_krds_claim': 0,
        'daily_quests': {},
        'quest_stats': {
            'games_played': 0,
            'wins': 0,
            'mice_collects': 0,
            'business_collects': 0,
            'works': 0,
            'deposit_amount': 0,
            'biggest_win': 0,
            'event_games': 0
        },
        'tournament_points': 0,
        'current_tournament': None,
        'event_purchases': []
    }

def ensure_user_structure(user_data):
    default = default_user()
    for key, value in default.items():
        if key not in user_data:
            user_data[key] = value
        elif isinstance(value, dict):
            for subkey, subvalue in value.items():
                if subkey not in user_data[key]:
                    user_data[key][subkey] = subvalue
    return user_data

def load_data():
    global users, username_cache, promocodes, user_achievements, user_quests, event_data
    global user_cases, orders, next_order_id, cheques, jackpot, duels, clans, businesses
    global bank_data, phone_data, bonus_data, pets_data, clans_data, businesses_data
    global stats_data, daily_quests_data, tournaments

    with data_lock:
        users_data = safe_json_load(DATA_FILE, {})
        if users_data:
            users = {str(k): ensure_user_structure(v) for k, v in users_data.items()}
        else:
            users = {}

        username_cache = safe_json_load(USERNAME_CACHE_FILE, {})
        promocodes = safe_json_load(PROMO_FILE, {})
        
        mice_data = safe_json_load(MICE_FILE, {})
        if mice_data and 'mice_sold' in mice_data:
            for mouse_id, data in mice_data['mice_sold'].items():
                if mouse_id in MICE_DATA:
                    MICE_DATA[mouse_id]['sold'] = data

        orders_data = safe_json_load(ORDERS_FILE, {})
        if orders_data:
            orders = orders_data.get('orders', {})
            next_order_id = orders_data.get('next_id', 1)

        cheques = safe_json_load(CHEQUES_FILE, {})
        user_achievements = safe_json_load(ACHIEVEMENTS_FILE, {})
        user_quests = safe_json_load(QUESTS_FILE, {})
        user_cases = safe_json_load(CASES_FILE, {})
        duels = safe_json_load(DUEL_FILE, {})
        clans = safe_json_load(CLAN_FILE, {})
        businesses = safe_json_load(BUSINESS_FILE, {})

        bank_data = safe_json_load(BANK_FILE, {
            'loans': {},
            'deposits': {},
            'transfers': [],
            'total_deposits': 0,
            'interest_rate': 0.05
        })
        
        phone_data = safe_json_load(PHONE_FILE, {
            'contacts': {},
            'calls': {},
            'messages': {},
            'phone_numbers': {}
        })
        
        bonus_data = safe_json_load(BONUS_FILE, {
            'daily': {},
            'weekly': {},
            'monthly': {},
            'referral_bonus': 5000
        })
        
        pets_data = safe_json_load(PETS_FILE, {})
        clans_data = safe_json_load(CLAN_FILE, {})
        businesses_data = safe_json_load(BUSINESS_FILE, {})
        stats_data = safe_json_load(STATS_FILE, {})
        daily_quests_data = safe_json_load(DAILY_QUESTS_FILE, {})
        tournaments = safe_json_load(TOURNAMENT_FILE, {})

        jackpot_data = safe_json_load('jackpot.json', {'total': 0})
        if jackpot_data:
            jackpot.update(jackpot_data)

        event_data = safe_json_load(EVENT_FILE, {
            'active': RELEASE_EVENT['active'],
            'participants': {},
            'leaderboard': [],
            'last_update': time.time()
        })

def save_data():
    with data_lock:
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=2)
            with open(USERNAME_CACHE_FILE, 'w', encoding='utf-8') as f:
                json.dump(username_cache, f, ensure_ascii=False, indent=2)
            with open(PROMO_FILE, 'w', encoding='utf-8') as f:
                json.dump(promocodes, f, ensure_ascii=False, indent=2)
            with open(ACHIEVEMENTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(user_achievements, f, ensure_ascii=False, indent=2)
            with open(QUESTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(user_quests, f, ensure_ascii=False, indent=2)
            with open(CASES_FILE, 'w', encoding='utf-8') as f:
                json.dump(user_cases, f, ensure_ascii=False, indent=2)
            with open(DUEL_FILE, 'w', encoding='utf-8') as f:
                json.dump(duels, f, ensure_ascii=False, indent=2)
            with open(CLAN_FILE, 'w', encoding='utf-8') as f:
                json.dump(clans, f, ensure_ascii=False, indent=2)
            with open(BUSINESS_FILE, 'w', encoding='utf-8') as f:
                json.dump(businesses, f, ensure_ascii=False, indent=2)
            with open('jackpot.json', 'w', encoding='utf-8') as f:
                json.dump(jackpot, f, ensure_ascii=False, indent=2)
            with open(EVENT_FILE, 'w', encoding='utf-8') as f:
                json.dump(event_data, f, ensure_ascii=False, indent=2)
            with open(STATS_FILE, 'w', encoding='utf-8') as f:
                json.dump(stats_data, f, ensure_ascii=False, indent=2)
            with open(DAILY_QUESTS_FILE, 'w', encoding='utf-8') as f:
                json.dump(daily_quests_data, f, ensure_ascii=False, indent=2)
            with open(TOURNAMENT_FILE, 'w', encoding='utf-8') as f:
                json.dump(tournaments, f, ensure_ascii=False, indent=2)
            
            with open(BANK_FILE, 'w', encoding='utf-8') as f:
                json.dump(bank_data, f, ensure_ascii=False, indent=2)
            with open(PHONE_FILE, 'w', encoding='utf-8') as f:
                json.dump(phone_data, f, ensure_ascii=False, indent=2)
            with open(BONUS_FILE, 'w', encoding='utf-8') as f:
                json.dump(bonus_data, f, ensure_ascii=False, indent=2)
            with open(PETS_FILE, 'w', encoding='utf-8') as f:
                json.dump(pets_data, f, ensure_ascii=False, indent=2)
            
            mice_data = {'mice_sold': {mid: MICE_DATA[mid]['sold'] for mid in MICE_DATA}}
            with open(MICE_FILE, 'w', encoding='utf-8') as f:
                json.dump(mice_data, f, ensure_ascii=False, indent=2)
            
            orders_data = {'orders': orders, 'next_id': next_order_id}
            with open(ORDERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(orders_data, f, ensure_ascii=False, indent=2)
            
            with open(CHEQUES_FILE, 'w', encoding='utf-8') as f:
                json.dump(cheques, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения данных: {e}")

def get_user_lock(user_id):
    if user_id not in user_locks:
        user_locks[user_id] = RLock()
    return user_locks[user_id]

def get_user(user_id):
    user_id = str(user_id)
    with get_user_lock(user_id):
        if user_id not in users:
            users[user_id] = default_user()
            save_data()
        return users[user_id]

def is_banned(user_id):
    user = get_user(user_id)
    return user.get('banned', False)

def is_admin(user_id):
    return str(user_id) in admin_users

def update_username_cache(user_id, username):
    if username:
        with data_lock:
            username_cache[username.lower()] = str(user_id)
            save_data()

def parse_bet(bet_str):
    try:
        bet_str = bet_str.lower().strip()
        if 'кк' in bet_str or 'ку' in bet_str:
            bet_str = bet_str.replace('кк', '').replace('ку', '')
            if bet_str == '':
                bet_str = '1'
            return int(float(bet_str) * 1000000)
        elif 'к' in bet_str:
            bet_str = bet_str.replace('к', '')
            if bet_str == '':
                bet_str = '1'
            return int(float(bet_str) * 1000)
        else:
            return int(bet_str)
    except:
        return None

def format_number(num):
    if num >= 1000000:
        return f"{num/1000000:.1f}М"
    elif num >= 1000:
        return f"{num/1000:.1f}К"
    return str(num)

def format_time(seconds):
    if seconds < 60:
        return f"{int(seconds)} сек"
    elif seconds < 3600:
        return f"{int(seconds/60)} мин"
    elif seconds < 86400:
        return f"{int(seconds/3600)} ч"
    else:
        return f"{int(seconds/86400)} д"

def get_event_multiplier():
    # Возвращаем 1.0, ивент не влияет на игры
    return 1.0

def get_vip_multiplier(user_id, multiplier_type='bonus_mult'):
    # Возвращаем 1.0, VIP не даёт множителей выигрыша
    return 1.0

def unlock_achievement(user_id, achievement_id):
    if achievement_id not in achievements:
        return
    with data_lock:
        if user_id not in user_achievements:
            user_achievements[user_id] = {}
        if achievement_id in user_achievements[user_id]:
            return
        achievement = achievements[achievement_id]
        user_achievements[user_id][achievement_id] = time.time()
        
        user = get_user(user_id)
        user['balance'] += achievement['reward']
        save_data()
    
    try:
        bot.send_message(int(user_id), 
            f"🏆 ** ДОСТИЖЕНИЕ РАЗБЛОКИРОВАНО! ** 🏆\n\n"
            f"{achievement['name']}\n"
            f"{achievement['desc']}\n"
            f"💰 Награда: +{format_number(achievement['reward'])} кредиксов",
            parse_mode='Markdown')
    except:
        pass

def update_quest_progress(user_id, quest_type, value=1):
    user = get_user(user_id)
    
    if quest_type in user['quest_stats']:
        if quest_type == 'deposit_amount':
            user['quest_stats'][quest_type] += value
        elif quest_type == 'biggest_win':
            if value > user['quest_stats']['biggest_win']:
                user['quest_stats']['biggest_win'] = value
        else:
            user['quest_stats'][quest_type] += value
    
    today = datetime.now().strftime('%Y-%m-%d')
    if today not in user['daily_quests']:
        generate_daily_quests(user_id)
    
    completed = []
    for qid, qdata in user['daily_quests'].get(today, {}).items():
        if qdata['completed']:
            continue
        
        quest = DAILY_QUESTS.get(qid)
        if not quest:
            continue
        
        current_value = user['quest_stats'].get(quest['type'], 0)
        
        targets = sorted(quest['rewards'].keys())
        target = None
        reward = 0
        for t in targets:
            if current_value >= t:
                target = t
                reward = quest['rewards'][t]
        
        if target:
            qdata['completed'] = True
            qdata['reward'] = reward
            
            vip_mult = get_vip_multiplier(user_id, 'daily_bonus_mult')
            final_reward = int(reward * vip_mult)
            
            user['balance'] += final_reward
            user['quests_completed'] = user.get('quests_completed', 0) + 1
            completed.append(f"{quest['icon']} {quest['name']} +{format_number(final_reward)}")
            
            if user['quests_completed'] >= 100:
                unlock_achievement(user_id, 'quest_master')
    
    # Проверка ивентового квеста
    if RELEASE_EVENT['active'] and time.time() < RELEASE_EVENT['end_time']:
        if 'event_quest' not in user['daily_quests'].get(today, {}):
            user['daily_quests'][today]['event_quest'] = {
                'target': 5,
                'completed': False,
                'reward': EVENT_QUESTS['march_1']['rewards']
            }
        else:
            qdata = user['daily_quests'][today]['event_quest']
            if not qdata['completed'] and user['quest_stats']['event_games'] >= 5:
                qdata['completed'] = True
                user['balance'] += qdata['reward']
                user['quests_completed'] += 1
                completed.append(f"{EVENT_QUESTS['march_1']['icon']} {EVENT_QUESTS['march_1']['name']} +{format_number(qdata['reward'])}")
    
    if completed:
        try:
            bot.send_message(int(user_id),
                f"✅ ** КВЕСТЫ ВЫПОЛНЕНЫ! ** ✅\n\n" +
                "\n".join(completed) +
                f"\n\n💰 Баланс: {format_number(user['balance'])}",
                parse_mode='Markdown')
        except:
            pass
    
    save_data()

def generate_daily_quests(user_id):
    user = get_user(user_id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    base_slots = 3
    vip_slots = 0
    if user.get('vip_level') and user.get('vip_expires', 0) > time.time():
        vip_slots = VIP_LEVELS[user['vip_level']].get('quest_slots', 0) - base_slots
    
    total_slots = base_slots + max(0, vip_slots)
    
    quest_ids = list(DAILY_QUESTS.keys())
    selected = random.sample(quest_ids, min(total_slots, len(quest_ids)))
    
    quests = {}
    for qid in selected:
        quest = DAILY_QUESTS[qid]
        targets = list(quest['rewards'].keys())
        target = random.choice(targets)
        
        quests[qid] = {
            'target': target,
            'completed': False,
            'reward': quest['rewards'][target]
        }
    
    if RELEASE_EVENT['active'] and time.time() < RELEASE_EVENT['end_time']:
        quests['event_quest'] = {
            'target': 5,
            'completed': False,
            'reward': EVENT_QUESTS['march_1']['rewards']
        }
    
    if today not in user['daily_quests']:
        user['daily_quests'][today] = {}
    
    user['daily_quests'][today] = quests
    save_data()

def update_game_stats(user_id, won, bet, win_amount=0):
    user = get_user(user_id)
    with get_user_lock(user_id):
        user['games_played'] = user.get('games_played', 0) + 1
        
        if won:
            user['total_wins'] = user.get('total_wins', 0) + 1
            user['win_streak'] = user.get('win_streak', 0) + 1
            if user['win_streak'] > user.get('max_win_streak', 0):
                user['max_win_streak'] = user['win_streak']
            if 'game_history' not in user:
                user['game_history'] = []
            user['game_history'].append({
                'time': time.time(),
                'game': 'game',
                'bet': bet,
                'result': 'win',
                'profit': win_amount - bet
            })
            
            update_quest_progress(user_id, 'games_played')
            update_quest_progress(user_id, 'wins')
            update_quest_progress(user_id, 'biggest_win', win_amount)
            if RELEASE_EVENT['active']:
                update_quest_progress(user_id, 'event_games', 1)
        else:
            user['total_losses'] = user.get('total_losses', 0) + 1
            user['win_streak'] = 0
            user['total_lost'] = user.get('total_lost', 0) + bet
            if 'game_history' not in user:
                user['game_history'] = []
            user['game_history'].append({
                'time': time.time(),
                'game': 'game',
                'bet': bet,
                'result': 'loss',
                'profit': -bet
            })
            
            update_quest_progress(user_id, 'games_played')
            if RELEASE_EVENT['active']:
                update_quest_progress(user_id, 'event_games', 1)
        
        save_data()
    
    if user['games_played'] == 1:
        unlock_achievement(user_id, 'first_game')
    
    if user['balance'] >= 1000000:
        unlock_achievement(user_id, 'millionaire')
    
    if len(user.get('mice', {})) >= 3:
        unlock_achievement(user_id, 'mice_collector')
    
    if len(user.get('pets', {})) >= 5:
        unlock_achievement(user_id, 'pet_collector')
    
    if len(user.get('businesses', {})) >= 5:
        unlock_achievement(user_id, 'businessman')
    
    if user.get('clan') is not None:
        unlock_achievement(user_id, 'clan_leader')
    
    if user.get('bank_deposit', {}).get('amount', 0) >= 1000000:
        unlock_achievement(user_id, 'banker')
    
    if len(user.get('phone_contacts', [])) >= 100:
        unlock_achievement(user_id, 'phone_addict')
    
    if user.get('daily_bonus', {}).get('streak', 0) >= 30:
        unlock_achievement(user_id, 'bonus_hunter')

def cancel_user_game(user_id):
    with get_user_lock(user_id):
        if user_id in crash_update_timers:
            try:
                crash_update_timers[user_id].cancel()
            except:
                pass
            del crash_update_timers[user_id]
        
        if user_id in game_timers:
            try:
                game_timers[user_id].cancel()
            except:
                pass
            del game_timers[user_id]
        
        user = get_user(user_id)
        if user.get('game') is not None:
            user['game'] = None
            save_data()
            return True
    return False

def cleanup_all_timers():
    with data_lock:
        for user_id in list(crash_update_timers.keys()):
            try:
                crash_update_timers[user_id].cancel()
            except:
                pass
        for user_id in list(game_timers.keys()):
            try:
                game_timers[user_id].cancel()
            except:
                pass
        crash_update_timers.clear()
        game_timers.clear()

# ====================== ТУРНИРЫ ======================
def init_tournaments():
    for t_type, t_data in TOURNAMENT_TYPES.items():
        if t_type not in tournaments:
            tournaments[t_type] = {
                'active': True,
                'start_time': time.time(),
                'end_time': time.time() + t_data['duration'],
                'participants': {},
                'prize_pool': t_data['prize_pool'],
                'entry_fee': t_data['entry_fee']
            }
    save_data()

@bot.message_handler(commands=['турнир', 'турниры'])
def tournament_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    text = "🏆 ** ТУРНИРЫ ** 🏆\n\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for t_type, t_data in tournaments.items():
        if not t_data['active']:
            continue
        
        time_left = t_data['end_time'] - time.time()
        if time_left <= 0:
            continue
        
        tourn_info = TOURNAMENT_TYPES[t_type]
        
        is_participant = user_id in t_data['participants']
        user_points = t_data['participants'].get(user_id, 0) if is_participant else 0
        
        text += (
            f"{tourn_info['name']}\n"
            f"   ⏳ Осталось: {format_time(time_left)}\n"
            f"   💰 Призовой фонд: {format_number(t_data['prize_pool'])}\n"
            f"   💸 Взнос: {format_number(t_data['entry_fee'])}\n"
        )
        
        if is_participant:
            text += f"   📊 Твои очки: {user_points}\n"
            text += f"   🚫 /турнир_покинуть {t_type}\n\n"
        else:
            text += f"   ✅ /турнир_вступить {t_type}\n\n"
    
    for t_type, t_data in tournaments.items():
        if not t_data['active']:
            continue
        
        sorted_parts = sorted(t_data['participants'].items(), key=lambda x: x[1], reverse=True)[:5]
        if sorted_parts:
            text += f"\n📊 **ТОП {TOURNAMENT_TYPES[t_type]['name']}:**\n"
            for i, (uid, points) in enumerate(sorted_parts, 1):
                try:
                    u = bot.get_chat(int(uid))
                    name = f"@{u.username}" if u.username else u.first_name
                except:
                    name = f"ID {uid}"
                text += f"{i}. {name} - {points} очков\n"
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['турнир_вступить'])
def tournament_join(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /турнир_вступить [тип]\nТипы: daily, weekly, monthly", parse_mode='Markdown')
        return
    
    t_type = args[1]
    if t_type not in tournaments:
        bot.send_message(message.chat.id, "❌ Турнир не найден!", parse_mode='Markdown')
        return
    
    t_data = tournaments[t_type]
    if not t_data['active']:
        bot.send_message(message.chat.id, "❌ Турнир не активен!", parse_mode='Markdown')
        return
    
    if t_data['end_time'] <= time.time():
        bot.send_message(message.chat.id, "❌ Турнир уже закончился!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    if user_id in t_data['participants']:
        bot.send_message(message.chat.id, "❌ Ты уже участвуешь в турнире!", parse_mode='Markdown')
        return
    
    entry_fee = t_data['entry_fee']
    if user['balance'] < entry_fee:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Нужно: {format_number(entry_fee)}", parse_mode='Markdown')
        return
    
    with data_lock, get_user_lock(user_id):
        user['balance'] -= entry_fee
        t_data['prize_pool'] += entry_fee // 2
        t_data['participants'][user_id] = 0
        user['current_tournament'] = t_type
        save_data()
    
    bot.send_message(message.chat.id, f"✅ Ты вступил в турнир! Взнос: {format_number(entry_fee)}", parse_mode='Markdown')

@bot.message_handler(commands=['турнир_покинуть'])
def tournament_leave(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /турнир_покинуть [тип]", parse_mode='Markdown')
        return
    
    t_type = args[1]
    if t_type not in tournaments:
        bot.send_message(message.chat.id, "❌ Турнир не найден!", parse_mode='Markdown')
        return
    
    t_data = tournaments[t_type]
    if user_id not in t_data['participants']:
        bot.send_message(message.chat.id, "❌ Ты не участвуешь в этом турнире!", parse_mode='Markdown')
        return
    
    with data_lock:
        del t_data['participants'][user_id]
        user = get_user(user_id)
        user['current_tournament'] = None
        save_data()
    
    bot.send_message(message.chat.id, "✅ Ты покинул турнир!", parse_mode='Markdown')

def add_tournament_points(user_id, game_type, bet, win_amount):
    user = get_user(user_id)
    if not user.get('current_tournament'):
        return
    
    t_type = user['current_tournament']
    if t_type not in tournaments:
        return
    
    t_data = tournaments[t_type]
    if not t_data['active'] or t_data['end_time'] <= time.time():
        return
    
    points = 0
    if win_amount > bet:
        points = int((win_amount - bet) / 1000)
    elif win_amount == 0:
        points = max(1, bet // 10000)
    
    with data_lock:
        if user_id in t_data['participants']:
            t_data['participants'][user_id] = t_data['participants'].get(user_id, 0) + points
            save_data()

def check_tournament_ends():
    with data_lock:
        for t_type, t_data in tournaments.items():
            if not t_data['active']:
                continue
            
            if t_data['end_time'] <= time.time():
                t_data['active'] = False
                
                sorted_parts = sorted(t_data['participants'].items(), key=lambda x: x[1], reverse=True)
                
                if sorted_parts:
                    prize_pool = t_data['prize_pool']
                    
                    if len(sorted_parts) >= 1:
                        winner_id = sorted_parts[0][0]
                        prize = int(prize_pool * 0.5)
                        winner = get_user(winner_id)
                        winner['balance'] += prize
                        unlock_achievement(winner_id, 'tournament_winner')
                        try:
                            bot.send_message(int(winner_id), f"🏆 Ты выиграл турнир! Приз: {format_number(prize)}", parse_mode='Markdown')
                        except:
                            pass
                    
                    if len(sorted_parts) >= 2:
                        winner_id = sorted_parts[1][0]
                        prize = int(prize_pool * 0.3)
                        get_user(winner_id)['balance'] += prize
                        try:
                            bot.send_message(int(winner_id), f"🥈 Ты занял 2 место в турнире! Приз: {format_number(prize)}", parse_mode='Markdown')
                        except:
                            pass
                    
                    if len(sorted_parts) >= 3:
                        winner_id = sorted_parts[2][0]
                        prize = int(prize_pool * 0.2)
                        get_user(winner_id)['balance'] += prize
                        try:
                            bot.send_message(int(winner_id), f"🥉 Ты занял 3 место в турнире! Приз: {format_number(prize)}", parse_mode='Markdown')
                        except:
                            pass
                
                for uid in list(t_data['participants'].keys()):
                    user = get_user(uid)
                    if user.get('current_tournament') == t_type:
                        user['current_tournament'] = None
                
                tourn_info = TOURNAMENT_TYPES[t_type]
                tournaments[t_type] = {
                    'active': True,
                    'start_time': time.time(),
                    'end_time': time.time() + tourn_info['duration'],
                    'participants': {},
                    'prize_pool': tourn_info['prize_pool'],
                    'entry_fee': tourn_info['entry_fee']
                }
        
        save_data()

def start_tournament_checker():
    def check():
        while True:
            time.sleep(60)
            check_tournament_ends()
    
    thread = Thread(target=check, daemon=True)
    thread.start()

# ====================== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ДЛЯ ИГР ======================
def start_game(user_id, game_name, bet, game_data=None):
    user = get_user(user_id)
    with get_user_lock(user_id):
        if user['game'] is not None:
            return False, "❌ У тебя уже есть активная игра! Заверши её."
        if user['balance'] < bet:
            return False, "❌ Недостаточно средств!"
        
        user['balance'] -= bet
        user['game'] = {
            'name': game_name,
            'bet': bet,
            'stage': 'active',
            'data': game_data or {}
        }
        save_data()
        
        timer = Timer(GAME_TIMEOUT, cancel_user_game, args=[user_id])
        timer.start()
        game_timers[user_id] = timer
        
        return True, "Игра началась!"

def end_game(user_id, won, win_amount=0):
    user = get_user(user_id)
    with get_user_lock(user_id):
        if user['game'] is None:
            return False
        
        bet = user['game']['bet']
        
        if won:
            user['balance'] += win_amount
            profit = win_amount - bet
        else:
            profit = -bet
        
        user['games_played'] = user.get('games_played', 0) + 1
        if won:
            user['total_wins'] = user.get('total_wins', 0) + 1
            user['win_streak'] = user.get('win_streak', 0) + 1
            if user['win_streak'] > user.get('max_win_streak', 0):
                user['max_win_streak'] = user['win_streak']
        else:
            user['total_losses'] = user.get('total_losses', 0) + 1
            user['win_streak'] = 0
            user['total_lost'] = user.get('total_lost', 0) + bet
        
        user['game_history'].append({
            'time': time.time(),
            'game': user['game']['name'],
            'bet': bet,
            'result': 'win' if won else 'loss',
            'profit': profit
        })
        
        update_quest_progress(user_id, 'games_played')
        if won:
            update_quest_progress(user_id, 'wins')
            update_quest_progress(user_id, 'biggest_win', win_amount)
        if RELEASE_EVENT['active']:
            update_quest_progress(user_id, 'event_games', 1)
        
        add_tournament_points(user_id, user['game']['name'], bet, win_amount if won else 0)
        
        if user['games_played'] == 1:
            unlock_achievement(user_id, 'first_game')
        if user['balance'] >= 1000000:
            unlock_achievement(user_id, 'millionaire')
        
        if len(user.get('mice', {})) >= 3:
            unlock_achievement(user_id, 'mice_collector')
        if len(user.get('pets', {})) >= 5:
            unlock_achievement(user_id, 'pet_collector')
        if len(user.get('businesses', {})) >= 5:
            unlock_achievement(user_id, 'businessman')
        if user.get('clan') is not None:
            unlock_achievement(user_id, 'clan_leader')
        if user.get('bank_deposit', {}).get('amount', 0) >= 1000000:
            unlock_achievement(user_id, 'banker')
        if len(user.get('phone_contacts', [])) >= 100:
            unlock_achievement(user_id, 'phone_addict')
        if user.get('daily_bonus', {}).get('streak', 0) >= 30:
            unlock_achievement(user_id, 'bonus_hunter')
        
        user['game'] = None
        save_data()
        
        if user_id in game_timers:
            try:
                game_timers[user_id].cancel()
            except:
                pass
            del game_timers[user_id]
        
        return True

# ====================== ИГРЫ ======================
# ---------- Башня ----------
@bot.message_handler(commands=['башня', 'tower'])
def tower_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "❌ Использование: /башня [сумма]", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    if user['balance'] < bet:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Баланс: {format_number(user['balance'])}", parse_mode='Markdown')
        return
    
    # Генерируем поле из 5 уровней по 5 ячеек
    cells = []
    for level in range(5):
        level_cells = ['💎'] * 4 + ['💣']
        random.shuffle(level_cells)
        cells.extend(level_cells)
    
    user['balance'] -= bet
    user['game'] = {
        'type': 'tower',
        'bet': bet,
        'stage': 'playing',
        'level': 1,
        'max_level': 5,
        'cells': cells,
        'opened': [False] * 25
    }
    save_data()
    
    markup = types.InlineKeyboardMarkup(row_width=5)
    buttons = []
    for i in range(5):
        buttons.append(types.InlineKeyboardButton(f"{i+1}", callback_data=f"tower_{i}"))
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("💰 Забрать", callback_data="tower_take"))
    
    potential_win = int(bet * TOWER_MULTIPLIERS[1])
    
    bot.send_message(message.chat.id,
        f"🏰 ** БАШНЯ ** 🏰\n\n"
        f"Ставка: {format_number(bet)}\n"
        f"Уровень: 1/5\n"
        f"Множитель: x{TOWER_MULTIPLIERS[1]}\n"
        f"Забрать сейчас: {format_number(potential_win)}\n\n"
        f"Выбери ячейку (1-5):", reply_markup=markup, parse_mode='Markdown')

# ---------- Футбол ----------
@bot.message_handler(commands=['футбол', 'football'])
def football_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "❌ Использование: /футбол [сумма]", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    success, msg = start_game(user_id, 'football', bet)
    if not success:
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')
        return
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⚽ Забить гол!", callback_data="football_play"))
    bot.send_message(message.chat.id,
        f"⚽ ** ФУТБОЛ **\n\n"
        f"Ставка: {format_number(bet)}\n"
        f"Множитель: x{FOOTBALL_MULTIPLIER}\n\n"
        f"Нажми кнопку, чтобы ударить по воротам!", reply_markup=markup, parse_mode='Markdown')

# ---------- Баскетбол ----------
@bot.message_handler(commands=['баскетбол', 'basketball'])
def basketball_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "❌ Использование: /баскетбол [сумма]", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    success, msg = start_game(user_id, 'basketball', bet)
    if not success:
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')
        return
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🏀 Бросить мяч!", callback_data="basketball_play"))
    bot.send_message(message.chat.id,
        f"🏀 ** БАСКЕТБОЛ **\n\n"
        f"Ставка: {format_number(bet)}\n"
        f"Множитель: x{BASKETBALL_MULTIPLIER}\n\n"
        f"Нажми кнопку, чтобы сделать бросок!", reply_markup=markup, parse_mode='Markdown')

# ---------- Дартс ----------
@bot.message_handler(commands=['дартс', 'darts'])
def darts_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "❌ Использование: /дартс [сумма]", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    success, msg = start_game(user_id, 'darts', bet)
    if not success:
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')
        return
    
    markup = types.InlineKeyboardMarkup(row_width=3)
    buttons = []
    for i in range(1, 6):
        buttons.append(types.InlineKeyboardButton(f"{i} (x{DARTS_MULTIPLIERS[i]})", callback_data=f"darts_{i}"))
    markup.add(*buttons)
    
    bot.send_message(message.chat.id,
        f"🎯 ** ДАРТС **\n\n"
        f"Ставка: {format_number(bet)}\n"
        f"Выбери сектор (1-5):", reply_markup=markup, parse_mode='Markdown')

# ---------- Покер ----------
@bot.message_handler(commands=['покер', 'poker'])
def poker_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "❌ Использование: /покер [сумма]", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    success, msg = start_game(user_id, 'poker', bet)
    if not success:
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')
        return
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🃏 Сыграть", callback_data="poker_play"))
    bot.send_message(message.chat.id,
        f"🃏 ** ПОКЕР **\n\n"
        f"Ставка: {format_number(bet)}\n"
        f"Множитель: x{POKER_MULTIPLIER}\n\n"
        f"Нажми кнопку, чтобы сыграть против дилера!", reply_markup=markup, parse_mode='Markdown')

# ---------- Пирамида ----------
@bot.message_handler(commands=['пирамида', 'pyramid'])
def pyramid_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "❌ Использование: /пирамида [сумма]", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    success, msg = start_game(user_id, 'pyramid', bet, {'level': 1})
    if not success:
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')
        return
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🔺 Открыть ячейку", callback_data="pyramid_open"))
    bot.send_message(message.chat.id,
        f"🔺 ** ПИРАМИДА **\n\n"
        f"Ставка: {format_number(bet)}\n"
        f"Уровень 1/{PYRAMID_CELLS}\n"
        f"Множитель при победе: x{PYRAMID_MULTIPLIER}\n\n"
        f"Нажимай, чтобы открывать ячейки. На каждом уровне спрятан приз или бомба!", reply_markup=markup, parse_mode='Markdown')

# ---------- Мины ----------
@bot.message_handler(commands=['мины', 'mines'])
def mines_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "❌ Использование: /мины [сумма]", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    if user['balance'] < bet:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Баланс: {format_number(user['balance'])}", parse_mode='Markdown')
        return
    
    # Создаем поле
    num_mines = random.randint(1, 5)
    field = ['💎'] * (25 - num_mines) + ['💣'] * num_mines
    random.shuffle(field)
    
    user['balance'] -= bet
    user['game'] = {
        'type': 'mines',
        'bet': bet,
        'stage': 'playing',
        'field': field,
        'opened': [False] * 25,
        'mines': num_mines,
        'steps': 0
    }
    save_data()
    
    markup = types.InlineKeyboardMarkup(row_width=5)
    buttons = []
    for i in range(25):
        buttons.append(types.InlineKeyboardButton("⬜", callback_data=f"mines_{i}"))
    markup.add(*buttons)
    markup.add(types.InlineKeyboardButton("💰 Забрать", callback_data="mines_take"))
    
    bot.send_message(
        message.chat.id,
        f"💣 ** МИНЫ ** 💣\n\n"
        f"Ставка: {format_number(bet)}\n"
        f"Мин на поле: {num_mines}\n\n"
        f"Открывай ячейки, но берегись мин!\n"
        f"Если найдешь мину - ставка сгорает!",
        reply_markup=markup, parse_mode='Markdown'
    )

# ---------- Слоты ----------
@bot.message_handler(commands=['слоты', 'slots'])
def slots_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "❌ Использование: /слоты [сумма]", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    success, msg = start_game(user_id, 'slots', bet)
    if not success:
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')
        return
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🎰 Крутить", callback_data="slots_spin"))
    bot.send_message(message.chat.id,
        f"🎰 ** СЛОТЫ **\n\n"
        f"Ставка: {format_number(bet)}\n"
        f"Нажми кнопку, чтобы крутить барабаны!", reply_markup=markup, parse_mode='Markdown')

# ---------- Рулетка казино ----------
@bot.message_handler(commands=['рулетка_каз', 'roulette'])
def roulette_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 3:
        bot.send_message(message.chat.id, 
            "❌ Использование: /рулетка_каз [сумма] [тип ставки] [число/цвет]\n"
            "Типы: straight (число от 0 до 36), red, black, even, odd, 1-18, 19-36, dozen1, dozen2, dozen3", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    bet_type = args[2].lower()
    number = None
    if bet_type == 'straight':
        if len(args) < 4:
            bot.send_message(message.chat.id, "❌ Укажи число от 0 до 36", parse_mode='Markdown')
            return
        try:
            number = int(args[3])
            if number < 0 or number > 36:
                bot.send_message(message.chat.id, "❌ Число должно быть от 0 до 36", parse_mode='Markdown')
                return
        except:
            bot.send_message(message.chat.id, "❌ Неверное число", parse_mode='Markdown')
            return
    elif bet_type not in ['red', 'black', 'even', 'odd', '1-18', '19-36', 'dozen1', 'dozen2', 'dozen3']:
        bot.send_message(message.chat.id, "❌ Неверный тип ставки", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    success, msg = start_game(user_id, 'roulette', bet, {'type': bet_type, 'number': number})
    if not success:
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')
        return
    
    # Крутим рулетку
    result = random.choice(ROULETTE_NUMBERS)
    color = 'green'
    if result in RED_NUMBERS:
        color = 'red'
    elif result in BLACK_NUMBERS:
        color = 'black'
    
    win = False
    mult = 0
    if bet_type == 'straight':
        if result == number:
            win = True
            mult = ROULETTE_MULTIPLIERS['straight']
    elif bet_type == 'red' and color == 'red':
        win = True
        mult = ROULETTE_MULTIPLIERS['red']
    elif bet_type == 'black' and color == 'black':
        win = True
        mult = ROULETTE_MULTIPLIERS['black']
    elif bet_type == 'even' and result != 0 and result % 2 == 0:
        win = True
        mult = ROULETTE_MULTIPLIERS['even']
    elif bet_type == 'odd' and result % 2 == 1:
        win = True
        mult = ROULETTE_MULTIPLIERS['odd']
    elif bet_type == '1-18' and 1 <= result <= 18:
        win = True
        mult = ROULETTE_MULTIPLIERS['1-18']
    elif bet_type == '19-36' and 19 <= result <= 36:
        win = True
        mult = ROULETTE_MULTIPLIERS['19-36']
    elif bet_type == 'dozen1' and 1 <= result <= 12:
        win = True
        mult = ROULETTE_MULTIPLIERS['dozen']
    elif bet_type == 'dozen2' and 13 <= result <= 24:
        win = True
        mult = ROULETTE_MULTIPLIERS['dozen']
    elif bet_type == 'dozen3' and 25 <= result <= 36:
        win = True
        mult = ROULETTE_MULTIPLIERS['dozen']
    
    if win:
        win_amount = int(bet * mult)
        end_game(user_id, True, win_amount)
        text = f"🎰 ** РУЛЕТКА **\n\nВыпало: {result} {color}\n✅ Ты выиграл {format_number(win_amount)}!"
    else:
        end_game(user_id, False)
        text = f"🎰 ** РУЛЕТКА **\n\nВыпало: {result} {color}\n❌ Ты проиграл {format_number(bet)}."
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# ---------- Хило ----------
@bot.message_handler(commands=['хило', 'hilo'])
def hilo_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "❌ Использование: /хило [сумма]", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    current_card = random.randint(2, 14)
    success, msg = start_game(user_id, 'hilo', bet, {'card': current_card})
    if not success:
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')
        return
    
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton("⬆️ Выше", callback_data="hilo_hi"),
        types.InlineKeyboardButton("⬇️ Ниже", callback_data="hilo_lo"),
        types.InlineKeyboardButton("💰 Забрать", callback_data="hilo_cashout")
    )
    
    card_display = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}.get(current_card, str(current_card))
    bot.send_message(message.chat.id,
        f"🃏 ** ХИЛО **\n\n"
        f"Ставка: {format_number(bet)}\n"
        f"Текущая карта: {card_display}\n\n"
        f"Следующая карта будет выше или ниже? Или забери выигрыш (x{HILO_MULT} если угадаешь).", reply_markup=markup, parse_mode='Markdown')

# ---------- Очко (блэкджек) ----------
@bot.message_handler(commands=['очко', 'blackjack'])
def blackjack_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "❌ Использование: /очко [сумма]", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    def random_card():
        return random.randint(1, 11)
    player = [random_card(), random_card()]
    dealer = [random_card(), random_card()]
    
    success, msg = start_game(user_id, 'blackjack', bet, {'player': player, 'dealer': dealer, 'turn': 'player'})
    if not success:
        bot.send_message(message.chat.id, msg, parse_mode='Markdown')
        return
    
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("➕ Ещё", callback_data="bj_hit"),
        types.InlineKeyboardButton("⏹️ Хватит", callback_data="bj_stand")
    )
    
    player_sum = sum(player)
    bot.send_message(message.chat.id,
        f"🃏 ** ОЧКО **\n\n"
        f"Ставка: {format_number(bet)}\n"
        f"Твои карты: {player} сумма: {player_sum}\n"
        f"Карты дилера: [{dealer[0]}, ?]\n\n"
        f"Твой ход.", reply_markup=markup, parse_mode='Markdown')

# ---------- Краш ----------
@bot.message_handler(commands=['краш', 'crash'])
def crash_game(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    
    parts = message.text.split()
    if len(parts) < 2:
        bot.send_message(message.chat.id, "❌ Использование: краш [ставка]\nПример: краш 1к", parse_mode='Markdown')
        return
    
    bet = parse_bet(parts[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверный формат ставки.", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    if bet > user['balance']:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Баланс: {format_number(user['balance'])}", parse_mode='Markdown')
        return
    
    if user.get('game') is not None:
        bot.send_message(message.chat.id, "❌ У тебя уже есть активная игра! Закончи её или отмени (отмена)", parse_mode='Markdown')
        return
    
    crash_point = random.uniform(1.0, 10.0)
    
    with get_user_lock(user_id):
        user['balance'] -= bet
        user['game'] = {
            'type': 'crash',
            'bet': bet,
            'stage': 'playing',
            'multiplier': 1.0,
            'crash_point': crash_point,
            'start_time': time.time()
        }
        save_data()
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💰 Забрать", callback_data="crash_take"))
    
    msg = bot.send_message(
        message.chat.id,
        f"🚀 ** КРАШ ** 🚀\n\n"
        f"Ставка: {format_number(bet)}\n"
        f"Множитель: 1.00x\n\n"
        f"Жди...",
        reply_markup=markup, parse_mode='Markdown'
    )
    
    def update_crash():
        user = get_user(user_id)
        if user.get('game') is None or user['game'].get('type') != 'crash':
            return
        
        game = user['game']
        if game['stage'] != 'playing':
            return
        
        elapsed = time.time() - game['start_time']
        mult = 1.0 + elapsed * 0.5
        game['multiplier'] = mult
        
        if mult >= game['crash_point']:
            with get_user_lock(user_id):
                game['stage'] = 'crashed'
                update_game_stats(user_id, False, game['bet'])
                add_tournament_points(user_id, 'краш', game['bet'], 0)
                user['game'] = None
                save_data()
            
            try:
                bot.edit_message_text(
                    f"🚀 ** КРАШ ** 🚀\n\n"
                    f"💥 БУМ! Краш на x{game['crash_point']:.2f}\n\n"
                    f"❌ Ты проиграл {format_number(game['bet'])} кредиксов\n"
                    f"💰 Баланс: {format_number(user['balance'])}",
                    msg.chat.id,
                    msg.message_id,
                    parse_mode='Markdown'
                )
            except:
                pass
            return
        
        try:
            bot.edit_message_text(
                f"🚀 ** КРАШ ** 🚀\n\n"
                f"Ставка: {format_number(game['bet'])}\n"
                f"Множитель: {mult:.2f}x\n\n"
                f"Забирай, пока не крашнулось!",
                msg.chat.id,
                msg.message_id,
                reply_markup=markup,
                parse_mode='Markdown'
            )
        except:
            pass
        
        timer = Timer(0.5, update_crash)
        timer.start()
        with data_lock:
            crash_update_timers[user_id] = timer
    
    update_crash()

# ---------- x2/x3/x5 ----------
@bot.message_handler(commands=['x2', 'x3', 'x5'])
def multiplier_game(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    command = message.text.split()[0][1:]
    mult = float(command[1:])
    
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, f"❌ Использование: /{command} [сумма]", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    if user['balance'] < bet:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Баланс: {format_number(user['balance'])}", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['balance'] -= bet
        win = random.random() < 0.5
        if win:
            win_amount = int(bet * mult)
            user['balance'] += win_amount
            update_game_stats(user_id, True, bet, win_amount)
            add_tournament_points(user_id, command, bet, win_amount)
            text = f"✅ Ты выиграл! x{mult}: +{format_number(win_amount)} кредиксов"
        else:
            update_game_stats(user_id, False, bet)
            add_tournament_points(user_id, command, bet, 0)
            text = f"❌ Ты проиграл {format_number(bet)} кредиксов"
        
        save_data()
    
    bot.send_message(message.chat.id,
        f"🎲 ** x{mult} ** 🎲\n\n"
        f"{text}\n"
        f"💰 Баланс: {format_number(user['balance'])}", parse_mode='Markdown')

# ---------- Фишки ----------
@bot.message_handler(commands=['фишки', 'chips'])
def chips_game(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 3:
        bot.send_message(message.chat.id, "❌ Использование: фишки [ставка] [black/white]", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    color = args[2].lower()
    if color not in ['black', 'white']:
        bot.send_message(message.chat.id, "❌ Выбери black или white", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    if user['balance'] < bet:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Баланс: {format_number(user['balance'])}", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['balance'] -= bet
        result = random.choice(['black', 'white'])
        if result == color:
            win_amount = int(bet * 2)
            user['balance'] += win_amount
            update_game_stats(user_id, True, bet, win_amount)
            add_tournament_points(user_id, 'фишки', bet, win_amount)
            text = f"✅ Выпало {result.upper()}! Ты выиграл: +{format_number(win_amount)} кредиксов"
        else:
            update_game_stats(user_id, False, bet)
            add_tournament_points(user_id, 'фишки', bet, 0)
            text = f"❌ Выпало {result.upper()}! Ты проиграл {format_number(bet)} кредиксов"
        
        save_data()
    
    bot.send_message(message.chat.id,
        f"⚫️⚪️ ** ФИШКИ ** ⚫️⚪️\n\n"
        f"{text}\n"
        f"💰 Баланс: {format_number(user['balance'])}", parse_mode='Markdown')

# ---------- Русская рулетка ----------
@bot.message_handler(commands=['рулетка_рус', 'russian_roulette'])
def russian_roulette(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "❌ Использование: рулетка_рус [ставка]", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    if user['balance'] < bet:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Баланс: {format_number(user['balance'])}", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['balance'] -= bet
        if random.randint(1, 6) == 1:
            update_game_stats(user_id, False, bet)
            add_tournament_points(user_id, 'рулетка_рус', bet, 0)
            text = f"🔫 БАХ! Ты проиграл {format_number(bet)} кредиксов"
        else:
            win_amount = int(bet * 1.9)   # изменено на 1.9
            user['balance'] += win_amount
            update_game_stats(user_id, True, bet, win_amount)
            add_tournament_points(user_id, 'рулетка_рус', bet, win_amount)
            text = f"🎉 Ты выжил! Выигрыш: +{format_number(win_amount)} кредиксов"
        
        save_data()
    
    bot.send_message(message.chat.id,
        f"🔫 ** РУССКАЯ РУЛЕТКА ** 🔫\n\n"
        f"{text}\n"
        f"💰 Баланс: {format_number(user['balance'])}", parse_mode='Markdown')

# ---------- Джекпот ----------
@bot.message_handler(commands=['джекпот', 'jackpot'])
def jackpot_game(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 2:
        bot.send_message(message.chat.id, "❌ Использование: джекпот [ставка]", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    if user['balance'] < bet:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Баланс: {format_number(user['balance'])}", parse_mode='Markdown')
        return
    
    with data_lock, get_user_lock(user_id):
        user['balance'] -= bet
        jackpot['total'] += bet
        
        if random.random() < 0.01:
            win_amount = jackpot['total']
            user['balance'] += win_amount
            jackpot['total'] = 0
            jackpot['last_winner'] = user_id
            jackpot['last_win_time'] = time.time()
            jackpot['history'].append({'user': user_id, 'amount': win_amount, 'time': time.time()})
            update_game_stats(user_id, True, bet, win_amount)
            add_tournament_points(user_id, 'джекпот', bet, win_amount)
            text = f"🎉 ** ДЖЕКПОТ! ** 🎉\n\nТы выиграл {format_number(win_amount)} кредиксов!"
        else:
            update_game_stats(user_id, False, bet)
            add_tournament_points(user_id, 'джекпот', bet, 0)
            text = f"❌ Ты не выиграл джекпот. Потеряно: {format_number(bet)}"
        
        save_data()
    
    bot.send_message(message.chat.id,
        f"🎰 ** ДЖЕКПОТ ** 🎰\n\n"
        f"{text}\n"
        f"💰 Текущий джекпот: {format_number(jackpot['total'])}\n"
        f"💰 Баланс: {format_number(user['balance'])}", parse_mode='Markdown')

# ---------- Кости ----------
@bot.message_handler(commands=['кости', 'dice'])
def dice_game(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) < 3:
        bot.send_message(message.chat.id, 
            "❌ Использование: кости [ставка] [тип]\n"
            "Типы: больше6, меньше6, чет, нечет", parse_mode='Markdown')
        return
    
    bet = parse_bet(args[1])
    if bet is None or bet <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма ставки!", parse_mode='Markdown')
        return
    
    bet_type = args[2].lower()
    if bet_type not in ['больше6', 'меньше6', 'чет', 'нечет']:
        bot.send_message(message.chat.id, "❌ Неверный тип! Доступно: больше6, меньше6, чет, нечет", parse_mode='Markdown')
        return
    
    max_bet = MAX_BET * get_vip_multiplier(user_id, 'max_bet_mult')
    if bet > max_bet:
        bot.send_message(message.chat.id, f"❌ Максимальная ставка: {format_number(max_bet)}", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    if user['balance'] < bet:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Баланс: {format_number(user['balance'])}", parse_mode='Markdown')
        return
    
    dice1 = random.randint(1, 6)
    dice2 = random.randint(1, 6)
    total = dice1 + dice2
    
    win = False
    if bet_type == 'больше6' and total > 6:
        win = True
    elif bet_type == 'меньше6' and total < 6:
        win = True
    elif bet_type == 'чет' and total % 2 == 0:
        win = True
    elif bet_type == 'нечет' and total % 2 == 1:
        win = True
    
    with get_user_lock(user_id):
        user['balance'] -= bet
        if win:
            win_amount = int(bet * 2)
            user['balance'] += win_amount
            update_game_stats(user_id, True, bet, win_amount)
            add_tournament_points(user_id, 'кости', bet, win_amount)
            text = f"✅ Выпало {dice1}+{dice2}={total}. Ты выиграл: +{format_number(win_amount)}"
        else:
            update_game_stats(user_id, False, bet)
            add_tournament_points(user_id, 'кости', bet, 0)
            text = f"❌ Выпало {dice1}+{dice2}={total}. Ты проиграл {format_number(bet)}"
        
        save_data()
    
    bot.send_message(message.chat.id,
        f"🎲 ** КОСТИ ** 🎲\n\n"
        f"{text}\n"
        f"💰 Баланс: {format_number(user['balance'])}", parse_mode='Markdown')

# ====================== КНОПКИ ДЛЯ ИГР (CALLBACK) ======================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = str(call.from_user.id)
    user = get_user(user_id)
    
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "⛔ Вы забанены!")
        return
    
    # ---------------------- Башня ----------------------
    if call.data.startswith('tower_'):
        if user.get('game') is None or user['game'].get('type') != 'tower':
            bot.answer_callback_query(call.id, "❌ Игра не найдена!")
            try:
                bot.edit_message_text("Игра завершена.", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            except:
                pass
            return
        
        if call.data == 'tower_take':
            game = user['game']
            if game.get('stage') != 'playing':
                bot.answer_callback_query(call.id, "❌ Игра уже закончена!")
                return
            
            with get_user_lock(user_id):
                current_mult = TOWER_MULTIPLIERS[game['level']]
                win_amount = int(game['bet'] * current_mult)
                
                user['balance'] += win_amount
                update_game_stats(user_id, True, game['bet'], win_amount)
                add_tournament_points(user_id, 'башня', game['bet'], win_amount)
                
                text = (
                    f"🏰 ** БАШНЯ ** 🏰\n\n"
                    f"💰 Ты забрал выигрыш!\n\n"
                    f"✅ Выигрыш: +{format_number(win_amount)} кредиксов\n"
                    f"💰 Баланс: {format_number(user['balance'])}"
                )
                user['game'] = None
                save_data()
            
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            bot.answer_callback_query(call.id, "Ты вовремя остановился!")
            return
        
        level = int(call.data.split('_')[1])
        game = user['game']
        
        if game.get('stage') != 'playing':
            bot.answer_callback_query(call.id, "❌ Игра уже закончена!")
            return
        
        cell_index = (game['level'] - 1) * 5 + level
        if game['opened'][cell_index]:
            bot.answer_callback_query(call.id, "❌ Эта ячейка уже открыта!")
            return
        
        cell = game['cells'][cell_index]
        
        with get_user_lock(user_id):
            game['opened'][cell_index] = True
            
            if cell == '💣':
                game['stage'] = 'lost'
                update_game_stats(user_id, False, game['bet'])
                add_tournament_points(user_id, 'башня', game['bet'], 0)
                
                text = (
                    f"🏰 ** БАШНЯ ** 🏰\n\n"
                    f"💥 Ты нашёл бомбу!\n\n"
                    f"❌ Проигрыш: -{format_number(game['bet'])} кредиксов\n"
                    f"💰 Баланс: {format_number(user['balance'])}"
                )
                user['game'] = None
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            else:
                game['level'] += 1
                
                if game['level'] > game['max_level']:
                    win_amount = int(game['bet'] * TOWER_MULTIPLIERS[game['max_level']])
                    
                    user['balance'] += win_amount
                    update_game_stats(user_id, True, game['bet'], win_amount)
                    add_tournament_points(user_id, 'башня', game['bet'], win_amount)
                    
                    text = (
                        f"🏰 ** БАШНЯ ** 🏰\n\n"
                        f"🎉 Ты прошёл всю башню!\n\n"
                        f"✅ Выигрыш: +{format_number(win_amount)} кредиксов\n"
                        f"💰 Баланс: {format_number(user['balance'])}"
                    )
                    user['game'] = None
                    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
                else:
                    potential_win = int(game['bet'] * TOWER_MULTIPLIERS[game['level']])
                    
                    markup = types.InlineKeyboardMarkup(row_width=5)
                    buttons = []
                    for i in range(5):
                        buttons.append(types.InlineKeyboardButton(f"{i+1}", callback_data=f"tower_{i}"))
                    markup.add(*buttons)
                    markup.add(types.InlineKeyboardButton("💰 Забрать", callback_data="tower_take"))
                    
                    bot.edit_message_text(
                        f"🏰 ** БАШНЯ ** 🏰\n\n"
                        f"Ставка: {format_number(game['bet'])}\n"
                        f"Уровень: {game['level']}/{game['max_level']}\n"
                        f"Множитель: x{TOWER_MULTIPLIERS[game['level']]}\n"
                        f"Забрать сейчас: {format_number(potential_win)}\n\n"
                        f"Выбери ячейку (1-5):",
                        call.message.chat.id,
                        call.message.message_id,
                        reply_markup=markup,
                        parse_mode='Markdown'
                    )
            
            save_data()
        bot.answer_callback_query(call.id)
    
    # ---------------------- Футбол ----------------------
    elif call.data == 'football_play':
        if user.get('game') is None or user['game']['name'] != 'football':
            bot.answer_callback_query(call.id, "Нет активной игры!")
            try:
                bot.edit_message_text("Игра завершена.", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            except:
                pass
            return
        
        bet = user['game']['bet']
        win = random.random() < 0.5
        if win:
            win_amount = int(bet * FOOTBALL_MULTIPLIER)
            end_game(user_id, True, win_amount)
            text = f"⚽ **ГОЛ!**\n\n✅ Ты выиграл {format_number(win_amount)}!"
        else:
            end_game(user_id, False)
            text = f"⚽ **МИМО!**\n\n❌ Ты проиграл {format_number(bet)}."
        
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        except:
            pass
        bot.answer_callback_query(call.id)
    
    # ---------------------- Баскетбол ----------------------
    elif call.data == 'basketball_play':
        if user.get('game') is None or user['game']['name'] != 'basketball':
            bot.answer_callback_query(call.id, "Нет активной игры!")
            try:
                bot.edit_message_text("Игра завершена.", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            except:
                pass
            return
        
        bet = user['game']['bet']
        win = random.random() < 0.5
        if win:
            win_amount = int(bet * BASKETBALL_MULTIPLIER)
            end_game(user_id, True, win_amount)
            text = f"🏀 **ПОПАДАНИЕ!**\n\n✅ Ты выиграл {format_number(win_amount)}!"
        else:
            end_game(user_id, False)
            text = f"🏀 **ПРОМАХ!**\n\n❌ Ты проиграл {format_number(bet)}."
        
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        except:
            pass
        bot.answer_callback_query(call.id)
    
    # ---------------------- Дартс ----------------------
    elif call.data.startswith('darts_'):
        if user.get('game') is None or user['game']['name'] != 'darts':
            bot.answer_callback_query(call.id, "Нет активной игры!")
            try:
                bot.edit_message_text("Игра завершена.", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            except:
                pass
            return
        
        bet = user['game']['bet']
        chosen = int(call.data.split('_')[1])
        result = random.randint(1, 5)
        if result == chosen:
            win_amount = int(bet * DARTS_MULTIPLIERS[chosen])
            end_game(user_id, True, win_amount)
            text = f"🎯 **ПОПАДАНИЕ!**\n\n✅ Ты выиграл {format_number(win_amount)}!"
        else:
            end_game(user_id, False)
            text = f"🎯 **МИМО!**\n\n❌ Ты проиграл {format_number(bet)}. Выпало: {result}"
        
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        except:
            pass
        bot.answer_callback_query(call.id)
    
    # ---------------------- Покер ----------------------
    elif call.data == 'poker_play':
        if user.get('game') is None or user['game']['name'] != 'poker':
            bot.answer_callback_query(call.id, "Нет активной игры!")
            try:
                bot.edit_message_text("Игра завершена.", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            except:
                pass
            return
        
        bet = user['game']['bet']
        player = random.randint(2, 14)
        dealer = random.randint(2, 14)
        if player > dealer:
            win_amount = int(bet * POKER_MULTIPLIER)
            end_game(user_id, True, win_amount)
            text = f"🃏 **ПОБЕДА!**\n\nТвоя карта: {player}, дилер: {dealer}\n✅ Выигрыш: {format_number(win_amount)}"
        elif player < dealer:
            end_game(user_id, False)
            text = f"🃏 **ПРОИГРЫШ**\n\nТвоя карта: {player}, дилер: {dealer}\n❌ Потеряно: {format_number(bet)}"
        else:
            user['balance'] += bet
            user['game'] = None
            save_data()
            text = f"🃏 **НИЧЬЯ**\n\nТвоя карта: {player}, дилер: {dealer}\n💰 Ставка возвращена."
        
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        except:
            pass
        bot.answer_callback_query(call.id)
    
    # ---------------------- Пирамида ----------------------
    elif call.data == 'pyramid_open':
        if user.get('game') is None or user['game']['name'] != 'pyramid':
            bot.answer_callback_query(call.id, "Нет активной игры!")
            try:
                bot.edit_message_text("Игра завершена.", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            except:
                pass
            return
        
        bet = user['game']['bet']
        level = user['game']['data'].get('level', 1)
        bomb_chance = 0.1 + 0.05 * (level - 1)
        bomb = random.random() < bomb_chance
        
        if bomb:
            end_game(user_id, False)
            try:
                bot.edit_message_text(
                    f"🔺 **ПИРАМИДА**\n\n💥 Бомба! Ты проиграл {format_number(bet)}.",
                    call.message.chat.id, call.message.message_id, parse_mode='Markdown'
                )
            except:
                pass
            bot.answer_callback_query(call.id, "БАБАХ!")
        else:
            level += 1
            if level > PYRAMID_CELLS:
                win_amount = int(bet * PYRAMID_MULTIPLIER)
                end_game(user_id, True, win_amount)
                try:
                    bot.edit_message_text(
                        f"🔺 **ПИРАМИДА**\n\n🎉 Ты прошёл всю пирамиду!\nВыигрыш: {format_number(win_amount)}",
                        call.message.chat.id, call.message.message_id, parse_mode='Markdown'
                    )
                except:
                    pass
                bot.answer_callback_query(call.id, "Ты выиграл!")
            else:
                user['game']['data']['level'] = level
                save_data()
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton("🔺 Открыть ячейку", callback_data="pyramid_open"))
                try:
                    bot.edit_message_text(
                        f"🔺 **ПИРАМИДА**\n\n"
                        f"Ставка: {format_number(bet)}\n"
                        f"Уровень {level}/{PYRAMID_CELLS}\n"
                        f"Множитель при победе: x{PYRAMID_MULTIPLIER}\n\n"
                        f"Продолжаем!", reply_markup=markup,
                        chat_id=call.message.chat.id, message_id=call.message.message_id,
                        parse_mode='Markdown'
                    )
                except:
                    pass
                bot.answer_callback_query(call.id, f"Уровень {level}")
    
    # ---------------------- Мины ----------------------
    elif call.data.startswith('mines_'):
        if user.get('game') is None or user['game'].get('type') != 'mines':
            bot.answer_callback_query(call.id, "❌ Игра не найдена!")
            return
        
        if call.data == 'mines_take':
            game = user['game']
            if game.get('stage') != 'playing':
                bot.answer_callback_query(call.id, "❌ Игра уже закончена!")
                return
            
            if game.get('steps', 0) == 0:
                bot.answer_callback_query(call.id, "❌ Открой хотя бы одну ячейку!")
                return
            
            with get_user_lock(user_id):
                multiplier = MINES_MULTIPLIERS[game['mines']][game['steps']]
                win_amount = int(game['bet'] * multiplier)
                
                user['balance'] += win_amount
                update_game_stats(user_id, True, game['bet'], win_amount)
                add_tournament_points(user_id, 'мины', game['bet'], win_amount)
                
                field_display = []
                for i in range(25):
                    if game['field'][i] == '💣':
                        field_display.append('💣')
                    else:
                        field_display.append('💎' if game['opened'][i] else '⬜')
                
                field_rows = []
                for i in range(0, 25, 5):
                    field_rows.append(''.join(field_display[i:i+5]))
                
                text = (
                    f"💣 ** МИНЫ ** 💣\n\n"
                    f"{chr(10).join(field_rows)}\n\n"
                    f"💰 Ты забрал выигрыш!\n\n"
                    f"✅ Выигрыш: +{format_number(win_amount)} кредиксов\n"
                    f"💰 Баланс: {format_number(user['balance'])}"
                )
                user['game'] = None
                save_data()
            
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            bot.answer_callback_query(call.id, "Умно!")
            return
        
        if call.data == 'mines_no':
            bot.answer_callback_query(call.id, "❌ Эта ячейка уже открыта!")
            return
        
        pos = int(call.data.split('_')[1])
        game = user['game']
        
        if game.get('stage') != 'playing':
            bot.answer_callback_query(call.id, "❌ Игра уже закончена!")
            return
        
        if game['opened'][pos]:
            bot.answer_callback_query(call.id, "❌ Эта ячейка уже открыта!")
            return
        
        with get_user_lock(user_id):
            game['opened'][pos] = True
            cell = game['field'][pos]
            
            if cell == '💣':
                game['stage'] = 'lost'
                update_game_stats(user_id, False, game['bet'])
                add_tournament_points(user_id, 'мины', game['bet'], 0)
                
                field_display = []
                for i in range(25):
                    if game['field'][i] == '💣':
                        field_display.append('💣')
                    elif game['opened'][i]:
                        field_display.append('💎')
                    else:
                        field_display.append('⬜')
                
                field_rows = []
                for i in range(0, 25, 5):
                    field_rows.append(''.join(field_display[i:i+5]))
                
                text = (
                    f"💣 ** МИНЫ ** 💣\n\n"
                    f"{chr(10).join(field_rows)}\n\n"
                    f"💥 Ты нашёл мину!\n\n"
                    f"❌ Проигрыш: -{format_number(game['bet'])} кредиксов\n"
                    f"💰 Баланс: {format_number(user['balance'])}"
                )
                user['game'] = None
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            else:
                game['steps'] += 1
                multiplier = MINES_MULTIPLIERS[game['mines']][game['steps']]
                potential_win = int(game['bet'] * multiplier)
                
                markup = types.InlineKeyboardMarkup(row_width=5)
                buttons = []
                for i in range(25):
                    if game['opened'][i]:
                        buttons.append(types.InlineKeyboardButton("💎", callback_data="mines_no"))
                    else:
                        buttons.append(types.InlineKeyboardButton("⬜", callback_data=f"mines_{i}"))
                markup.add(*buttons)
                markup.add(types.InlineKeyboardButton("💰 Забрать", callback_data="mines_take"))
                
                bot.edit_message_text(
                    f"💣 ** МИНЫ ** 💣\n\n"
                    f"Ставка: {format_number(game['bet'])}\n"
                    f"Мин: {game['mines']}\n"
                    f"Шагов: {game['steps']}\n"
                    f"Множитель: x{multiplier}\n"
                    f"Забрать сейчас: {format_number(potential_win)} кредиксов\n\n"
                    f"Открывай ячейки, но берегись мин!",
                    call.message.chat.id,
                    call.message.message_id,
                    reply_markup=markup,
                    parse_mode='Markdown'
                )
            
            save_data()
        bot.answer_callback_query(call.id)
    
    # ---------------------- Слоты ----------------------
    elif call.data == 'slots_spin':
        if user.get('game') is None or user['game']['name'] != 'slots':
            bot.answer_callback_query(call.id, "Нет активной игры!")
            try:
                bot.edit_message_text("Игра завершена.", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            except:
                pass
            return
        
        bet = user['game']['bet']
        symbols = [random.choice(SLOTS_SYMBOLS) for _ in range(3)]
        line = ' | '.join(symbols)
        mult = SLOTS_PAYOUTS.get((symbols[0], symbols[1], symbols[2]), 0)
        if mult > 0:
            win_amount = int(bet * mult)
            end_game(user_id, True, win_amount)
            text = f"🎰 **СЛОТЫ**\n\n{line}\n\n✅ Ты выиграл {format_number(win_amount)}!"
        else:
            end_game(user_id, False)
            text = f"🎰 **СЛОТЫ**\n\n{line}\n\n❌ Ты проиграл {format_number(bet)}."
        
        try:
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        except:
            pass
        bot.answer_callback_query(call.id)
    
    # ---------------------- Хило ----------------------
    elif call.data.startswith('hilo_'):
        if user.get('game') is None or user['game']['name'] != 'hilo':
            bot.answer_callback_query(call.id, "Нет активной игры!")
            try:
                bot.edit_message_text("Игра завершена.", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            except:
                pass
            return
        
        bet = user['game']['bet']
        current_card = user['game']['data']['card']
        
        if call.data == 'hilo_cashout':
            win_amount = int(bet * HILO_MULT)
            end_game(user_id, True, win_amount)
            try:
                bot.edit_message_text(
                    f"🃏 **ХИЛО**\n\n✅ Ты забрал {format_number(win_amount)}!",
                    call.message.chat.id, call.message.message_id, parse_mode='Markdown'
                )
            except:
                pass
            bot.answer_callback_query(call.id, "Отличный выбор!")
            return
        
        next_card = random.randint(2, 14)
        guess = call.data.split('_')[1]
        win = False
        if guess == 'hi' and next_card > current_card:
            win = True
        elif guess == 'lo' and next_card < current_card:
            win = True
        
        if win:
            user['game']['data']['card'] = next_card
            save_data()
            markup = types.InlineKeyboardMarkup(row_width=3)
            markup.add(
                types.InlineKeyboardButton("⬆️ Выше", callback_data="hilo_hi"),
                types.InlineKeyboardButton("⬇️ Ниже", callback_data="hilo_lo"),
                types.InlineKeyboardButton("💰 Забрать", callback_data="hilo_cashout")
            )
            card_display = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}.get(next_card, str(next_card))
            try:
                bot.edit_message_text(
                    f"🃏 **ХИЛО**\n\n"
                    f"Ставка: {format_number(bet)}\n"
                    f"Текущая карта: {card_display}\n\n"
                    f"Следующая карта будет выше или ниже?",
                    call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='Markdown'
                )
            except:
                pass
            bot.answer_callback_query(call.id, "Угадал!")
        else:
            end_game(user_id, False)
            prev_display = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}.get(current_card, str(current_card))
            next_display = {11: 'J', 12: 'Q', 13: 'K', 14: 'A'}.get(next_card, str(next_card))
            try:
                bot.edit_message_text(
                    f"🃏 **ХИЛО**\n\n"
                    f"Твоя карта: {prev_display}, следующая: {next_display}\n"
                    f"❌ Ты проиграл {format_number(bet)}.",
                    call.message.chat.id, call.message.message_id, parse_mode='Markdown'
                )
            except:
                pass
            bot.answer_callback_query(call.id, "Не повезло!")
    
    # ---------------------- Очко ----------------------
    elif call.data.startswith('bj_'):
        if user.get('game') is None or user['game']['name'] != 'blackjack':
            bot.answer_callback_query(call.id, "Нет активной игры!")
            try:
                bot.edit_message_text("Игра завершена.", call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            except:
                pass
            return
        
        bet = user['game']['bet']
        data = user['game']['data']
        player = data['player']
        dealer = data['dealer']
        
        if call.data == 'bj_hit':
            card = random.randint(1, 11)
            player.append(card)
            player_sum = sum(player)
            if player_sum > 21:
                end_game(user_id, False)
                try:
                    bot.edit_message_text(
                        f"🃏 **ОЧКО**\n\n"
                        f"Твои карты: {player} сумма: {player_sum} - ПЕРЕБОР!\n"
                        f"❌ Ты проиграл {format_number(bet)}.",
                        call.message.chat.id, call.message.message_id, parse_mode='Markdown'
                    )
                except:
                    pass
                bot.answer_callback_query(call.id, "Перебор!")
            else:
                data['player'] = player
                save_data()
                markup = types.InlineKeyboardMarkup()
                markup.add(
                    types.InlineKeyboardButton("➕ Ещё", callback_data="bj_hit"),
                    types.InlineKeyboardButton("⏹️ Хватит", callback_data="bj_stand")
                )
                try:
                    bot.edit_message_text(
                        f"🃏 **ОЧКО**\n\n"
                        f"Ставка: {format_number(bet)}\n"
                        f"Твои карты: {player} сумма: {player_sum}\n"
                        f"Карты дилера: [{dealer[0]}, ?]\n\n"
                        f"Твой ход.",
                        call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode='Markdown'
                    )
                except:
                    pass
                bot.answer_callback_query(call.id, f"Ещё карта: {card}")
        elif call.data == 'bj_stand':
            dealer_sum = sum(dealer)
            while dealer_sum < 17:
                card = random.randint(1, 11)
                dealer.append(card)
                dealer_sum = sum(dealer)
            player_sum = sum(player)
            
            if dealer_sum > 21:
                win_amount = int(bet * BLACKJACK_MULTIPLIER)
                end_game(user_id, True, win_amount)
                text = f"🃏 **ОЧКО**\n\nДилер перебрал! Ты выиграл {format_number(win_amount)}."
            elif dealer_sum > player_sum:
                end_game(user_id, False)
                text = f"🃏 **ОЧКО**\n\nУ дилера {dealer_sum}, у тебя {player_sum}. Ты проиграл {format_number(bet)}."
            elif dealer_sum < player_sum:
                win_amount = int(bet * BLACKJACK_MULTIPLIER)
                end_game(user_id, True, win_amount)
                text = f"🃏 **ОЧКО**\n\nУ дилера {dealer_sum}, у тебя {player_sum}. Ты выиграл {format_number(win_amount)}."
            else:
                user['balance'] += bet
                user['game'] = None
                save_data()
                text = f"🃏 **ОЧКО**\n\nНичья! Ставка возвращена."
            
            try:
                bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
            except:
                pass
            bot.answer_callback_query(call.id, "Игра завершена")
    
    # ---------------------- Краш ----------------------
    elif call.data == 'crash_take':
        if user.get('game') is None or user['game'].get('type') != 'crash':
            bot.answer_callback_query(call.id, "❌ Игра не найдена!")
            return
        
        game = user['game']
        if game.get('stage') != 'playing':
            bot.answer_callback_query(call.id, "❌ Игра уже закончена!")
            return
        
        with get_user_lock(user_id):
            win_amount = int(game['bet'] * game['multiplier'])
            
            user['balance'] += win_amount
            game['stage'] = 'taken'
            update_game_stats(user_id, True, game['bet'], win_amount)
            add_tournament_points(user_id, 'краш', game['bet'], win_amount)
            
            if user_id in crash_update_timers:
                try:
                    crash_update_timers[user_id].cancel()
                except:
                    pass
                del crash_update_timers[user_id]
            
            text = (
                f"🚀 ** КРАШ ** 🚀\n\n"
                f"💰 Ты забрал x{game['multiplier']:.2f}!\n\n"
                f"✅ Выигрыш: +{format_number(win_amount)} кредиксов\n"
                f"💰 Баланс: {format_number(user['balance'])}"
            )
            user['game'] = None
            save_data()
        
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        bot.answer_callback_query(call.id, "Ты вовремя остановился!")

    # ---------------------- Телефон (добавим обработчики для телефона позже) ----------------------
    elif call.data.startswith('phone_'):
        phone_callback_handler(call)

# ====================== VIP СИСТЕМА ======================
@bot.message_handler(commands=['вип', 'vip'])
def vip_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    
    current_vip = None
    if user.get('vip_level') and user.get('vip_expires', 0) > time.time():
        current_vip = VIP_LEVELS[user['vip_level']]
        days_left = int((user['vip_expires'] - time.time()) / 86400)
        
        last_claim = user.get('vip_last_krds_claim', 0)
        if time.time() - last_claim > 7 * 86400:
            can_claim_krds = True
        else:
            next_claim = int((7 * 86400) - (time.time() - last_claim))
            next_claim_days = next_claim / 86400
            can_claim_krds = False
    
    text = f"👑 ** VIP СИСТЕМА ** 👑\n\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    if current_vip:
        text += (
            f"✅ Твой статус: {current_vip['color']} {current_vip['name']}\n"
            f"⏳ Осталось: {days_left} дней\n\n"
            f"**Твои бонусы:**\n"
        )
        for perk in current_vip['perks']:
            text += f"• {perk}\n"
        
        if can_claim_krds:
            text += f"\n💎 **Доступно KRDS:** +{current_vip['krds_weekly']} (напиши /вип_крдс)\n"
        else:
            if 'next_claim_days' in locals():
                text += f"\n⏳ **Следующие KRDS:** через {next_claim_days:.1f} дней\n"
        
        text += f"\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    else:
        text += "❌ У тебя нет активного VIP\n\n"
    
    text += "**Доступные VIP уровни:**\n\n"
    
    for level_id, vip in VIP_LEVELS.items():
        text += (
            f"{vip['color']} {vip['name']}\n"
            f"   💰 Цена: {format_number(vip['price'])} кредиксов\n"
            f"   💎 KRDS/неделя: +{vip['krds_weekly']}\n"
            f"   ⏳ 30 дней\n"
            f"   **Бонусы:**\n"
        )
        for perk in vip['perks'][:3]:
            text += f"      • {perk}\n"
        text += f"   /купить_вип {level_id}\n\n"
    
    text += "━━━━━━━━━━━━━━━━━━━━━━\n"
    text += "💡 VIP окупается если ты активно играешь!"
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['купить_вип'])
def buy_vip_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /купить_вип [уровень]\nДоступно: bronze, silver, gold, platinum", parse_mode='Markdown')
        return
    
    level = args[1].lower()
    if level not in VIP_LEVELS:
        bot.send_message(message.chat.id, "❌ Неверный уровень! Доступно: bronze, silver, gold, platinum", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    vip_data = VIP_LEVELS[level]
    
    if user.get('vip_expires', 0) > time.time():
        bot.send_message(message.chat.id, "❌ У тебя уже есть активный VIP! Дождись окончания.", parse_mode='Markdown')
        return
    
    if user['balance'] < vip_data['price']:
        bot.send_message(message.chat.id, 
            f"❌ Недостаточно средств! Нужно: {format_number(vip_data['price'])}", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['balance'] -= vip_data['price']
        user['vip_level'] = level
        user['vip_expires'] = time.time() + vip_data['duration']
        user['vip_last_krds_claim'] = time.time()
        
        generate_daily_quests(user_id)
        
        save_data()
    
    text = (
        f"🎉 ** ПОЗДРАВЛЯЮ! ** 🎉\n\n"
        f"Ты купил {vip_data['color']} {vip_data['name']} VIP!\n\n"
        f"**Твои бонусы активированы:**\n"
    )
    for perk in vip_data['perks']:
        text += f"✅ {perk}\n"
    
    text += f"\n💰 Баланс: {format_number(user['balance'])}"
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['вип_крдс'])
def vip_krds_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    
    if not user.get('vip_level') or user.get('vip_expires', 0) < time.time():
        bot.send_message(message.chat.id, "❌ У тебя нет активного VIP!", parse_mode='Markdown')
        return
    
    vip_data = VIP_LEVELS[user['vip_level']]
    last_claim = user.get('vip_last_krds_claim', 0)
    
    if time.time() - last_claim < 7 * 86400:
        next_claim = int((7 * 86400) - (time.time() - last_claim))
        next_claim_days = next_claim / 86400
        bot.send_message(message.chat.id, 
            f"⏳ Следующие KRDS можно будет получить через {next_claim_days:.1f} дней", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['krds_balance'] += vip_data['krds_weekly']
        user['vip_last_krds_claim'] = time.time()
        save_data()
    
    bot.send_message(message.chat.id, 
        f"💎 ** ПОЛУЧЕНО! ** 💎\n\n"
        f"Ты получил +{vip_data['krds_weekly']} KRDS за неделю VIP!\n"
        f"💎 Новый баланс KRDS: {user['krds_balance']}", parse_mode='Markdown')

# ====================== ЕЖЕДНЕВНЫЕ КВЕСТЫ ======================
@bot.message_handler(commands=['квесты', 'quests'])
def quests_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    today = datetime.now().strftime('%Y-%m-%d')
    
    if today not in user['daily_quests']:
        generate_daily_quests(user_id)
    
    text = "📋 ** ЕЖЕДНЕВНЫЕ КВЕСТЫ ** 📋\n\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    quests = user['daily_quests'].get(today, {})
    if not quests:
        text += "У тебя нет активных квестов сегодня.\n"
    else:
        for qid, qdata in quests.items():
            if qid == 'event_quest':
                quest = EVENT_QUESTS['march_1']
                status = "✅" if qdata['completed'] else "⏳"
                current_value = user['quest_stats'].get('event_games', 0)
                target = qdata['target']
                text += (
                    f"{status} {quest['icon']} {quest['name']}\n"
                    f"   {quest['desc']}\n"
                    f"   Прогресс: {current_value}/{target}\n"
                    f"   Награда: {format_number(qdata['reward'])} кредиксов\n\n"
                )
            else:
                quest = DAILY_QUESTS.get(qid)
                if not quest:
                    continue
                status = "✅" if qdata['completed'] else "⏳"
                current_value = user['quest_stats'].get(quest['type'], 0)
                target = qdata['target']
                text += (
                    f"{status} {quest['icon']} {quest['name']}\n"
                    f"   {quest['desc'].format(target=format_number(target))}\n"
                    f"   Прогресс: {format_number(current_value)}/{format_number(target)}\n"
                    f"   Награда: {format_number(qdata['reward'])} кредиксов\n\n"
                )
    
    text += "━━━━━━━━━━━━━━━━━━━━━━\n"
    text += "💡 Квесты обновляются каждый день!"
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# ====================== СТАТИСТИКА ======================
@bot.message_handler(commands=['статистика', 'stats'])
def stats_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    
    total_users = len(users)
    total_balance = sum(u.get('balance', 0) for u in users.values())
    total_krds = sum(u.get('krds_balance', 0) for u in users.values())
    
    win_rate = 0
    if user.get('games_played', 0) > 0:
        win_rate = (user.get('total_wins', 0) / user['games_played']) * 100
    
    text = (
        f"📊 ** СТАТИСТИКА ** 📊\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"**ГЛОБАЛЬНАЯ:**\n"
        f"👥 Всего игроков: {total_users}\n"
        f"💰 Всего кредиксов: {format_number(total_balance)}\n"
        f"💎 Всего KRDS: {total_krds}\n\n"
        f"**ТВОЯ СТАТИСТИКА:**\n"
        f"🎮 Сыграно игр: {user.get('games_played', 0)}\n"
        f"✅ Побед: {user.get('total_wins', 0)}\n"
        f"❌ Поражений: {user.get('total_losses', 0)}\n"
        f"📊 Винрейт: {win_rate:.1f}%\n"
        f"💰 Проиграно всего: {format_number(user.get('total_lost', 0))}\n"
        f"🔥 Макс стрик: {user.get('max_win_streak', 0)}\n"
        f"📋 Квестов выполнено: {user.get('quests_completed', 0)}\n\n"
        f"**АКТИВНОСТЬ:**\n"
        f"🐭 Мышек: {sum(user.get('mice', {}).values())}\n"
        f"🐾 Питомцев: {len(user.get('pets', {}))}\n"
        f"🏪 Бизнесов: {len(user.get('businesses', {}))}\n"
        f"💼 Работ: {user.get('work_count', 0)}\n"
        f"👥 Рефералов: {user.get('referrals', 0)}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# ====================== ТОП ======================
@bot.message_handler(commands=['топ', 'Топ'])
def top_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    with data_lock:
        users_list = [(uid, data) for uid, data in users.items()]
        sorted_by_balance = sorted(users_list, key=lambda x: x[1].get('balance', 0), reverse=True)[:10]
        sorted_by_games = sorted(users_list, key=lambda x: x[1].get('games_played', 0), reverse=True)[:5]
        sorted_by_wins = sorted(users_list, key=lambda x: x[1].get('total_wins', 0), reverse=True)[:5]
    
    if not sorted_by_balance:
        bot.send_message(message.chat.id, "📊 Пока нет пользователей в топе.", parse_mode='Markdown')
        return
    
    text = "🏆 ** ТОП ИГРОКОВ ** 🏆\n\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    text += "💰 **ПО БАЛАНСУ:**\n"
    for i, (uid, data) in enumerate(sorted_by_balance, 1):
        try:
            user = bot.get_chat(int(uid))
            name = f"@{user.username}" if user.username else user.first_name
        except:
            name = f"ID {uid}"
        
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
        text += f"{medal} {name} - {format_number(data.get('balance', 0))}\n"
    
    text += "\n🎮 **ПО ИГРАМ:**\n"
    for i, (uid, data) in enumerate(sorted_by_games, 1):
        try:
            user = bot.get_chat(int(uid))
            name = f"@{user.username}" if user.username else user.first_name
        except:
            name = f"ID {uid}"
        text += f"{i}. {name} - {data.get('games_played', 0)} игр\n"
    
    text += "\n✅ **ПО ПОБЕДАМ:**\n"
    for i, (uid, data) in enumerate(sorted_by_wins, 1):
        try:
            user = bot.get_chat(int(uid))
            name = f"@{user.username}" if user.username else user.first_name
        except:
            name = f"ID {uid}"
        text += f"{i}. {name} - {data.get('total_wins', 0)} побед\n"
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# ====================== БАЛАНС ======================
@bot.message_handler(commands=['баланс', 'Баланс'])
def balance_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    
    total_profit = user['balance'] - 1000 + user.get('total_lost', 0)
    
    try:
        chat = bot.get_chat(int(user_id))
        name = f"@{chat.username}" if chat.username else chat.first_name
    except:
        name = f"ID {user_id}"
    
    vip_status = "Нет"
    if user.get('vip_level') and user.get('vip_expires', 0) > time.time():
        vip_status = VIP_LEVELS[user['vip_level']]['name']
    
    text = (
        f"⚡ **{name}** твой баланс: {format_number(user['balance'])}💲\n"
        f"________________________________________\n"
        f"👾 Проиграно кредиксов: {format_number(user.get('total_lost', 0))}⚡\n"
        f"🌅 Сыграно игр: {user.get('games_played', 0)}🌟\n"
        f"☃️ Выиграно кредиксов: {format_number(total_profit)}☃️\n"
        f"🏆 Ваш уровень VIP: {vip_status}👑\n"
        f"─────────────────────────────────"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# ====================== СИСТЕМА МЫШЕК ======================
@bot.message_handler(commands=['мышки', 'mice'])
def mice_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    text = "🐭 ** МАГАЗИН МЫШЕК ** 🐭\n\n"
    for mid, data in MICE_DATA.items():
        count = user['mice'].get(mid, 0)
        text += f"{data['icon']} {data['name']}\n   💰 Цена: {format_number(data['price'])} | 💵 Доход: {format_number(data['income'])}/час\n   У тебя: {count}\n   /купить_мышь {mid}\n\n"
    
    now = time.time()
    total_income = 0
    for mid, count in user['mice'].items():
        last = user['mice_last_collect'].get(mid, 0)
        elapsed = now - last
        hours = elapsed / 3600
        income = MICE_DATA[mid]['income'] * count * hours
        if income > 0:
            total_income += income
    
    if total_income > 0:
        text += f"\n💰 Накопленный доход от мышек: {format_number(int(total_income))}\n/собрать_мышей"
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['купить_мышь'])
def buy_mouse_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /купить_мышь [id]\nID: standard, china, world", parse_mode='Markdown')
        return
    
    mouse_id = args[1]
    if mouse_id not in MICE_DATA:
        bot.send_message(message.chat.id, "❌ Неверный ID мышки!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    price = MICE_DATA[mouse_id]['price']
    if user['balance'] < price:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Нужно: {format_number(price)}", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['balance'] -= price
        user['mice'][mouse_id] = user['mice'].get(mouse_id, 0) + 1
        user['mice_last_collect'][mouse_id] = time.time()
        MICE_DATA[mouse_id]['sold'] += 1
        save_data()
    
    bot.send_message(message.chat.id, f"✅ Ты купил {MICE_DATA[mouse_id]['icon']} {MICE_DATA[mouse_id]['name']}!", parse_mode='Markdown')

@bot.message_handler(commands=['собрать_мышей'])
def collect_mice_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    now = time.time()
    total = 0
    collected_text = []
    
    with get_user_lock(user_id):
        for mid, count in user['mice'].items():
            last = user['mice_last_collect'].get(mid, now)
            elapsed = now - last
            hours = elapsed / 3600
            income = MICE_DATA[mid]['income'] * count * hours
            if income > 0:
                total += income
                user['mice_last_collect'][mid] = now
                collected_text.append(f"{MICE_DATA[mid]['icon']} {MICE_DATA[mid]['name']}: +{format_number(int(income))}")
        
        if total > 0:
            total = int(total)
            user['balance'] += total
            update_quest_progress(user_id, 'mice_collects')
            save_data()
    
    if total > 0:
        text = (
            f"✅ ** СБОР С МЫШЕК ** ✅\n\n"
            f"{chr(10).join(collected_text)}\n\n"
            f"💰 Всего собрано: +{format_number(total)} кредиксов\n"
            f"💸 Новый баланс: {format_number(user['balance'])}"
        )
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "❌ Нет дохода для сбора.", parse_mode='Markdown')

# ====================== ПИТОМЦЫ ======================
@bot.message_handler(commands=['питомцы', 'pets'])
def pets_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    text = "🐾 ** МОИ ПИТОМЦЫ ** 🐾\n\n"
    if not user['pets']:
        text += "У тебя нет питомцев. Купи в магазине: /магазин_питомцев\n"
    else:
        for pid, pet_data in user['pets'].items():
            data = PETS_DATA.get(pid)
            if not data:
                continue
            last_feed = user['pets_last_feed'].get(pid, 0)
            happiness = data['happiness']
            if last_feed:
                elapsed = time.time() - last_feed
                happiness = max(0, data['happiness'] - int(elapsed / 3600) * 10)
            text += f"{data['name']}\n   Счастье: {happiness}%\n   Доход в час: {data['income']}\n\n"
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['магазин_питомцев'])
def pet_shop_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    text = "🐾 ** МАГАЗИН ПИТОМЦЕВ ** 🐾\n\n"
    for pid, data in PETS_DATA.items():
        text += f"{data['name']}\n"
        text += f"   💰 Цена: {format_number(data['price'])} кредиксов\n"
        text += f"   💵 Доход: {data['income']}/час\n"
        text += f"   🍖 Корм: {data['food_cost']} кредиксов\n"
        text += f"   📝 {data['description']}\n"
        text += f"   /купить_питомца {pid}\n\n"
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['купить_питомца'])
def buy_pet_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /купить_питомца [id]", parse_mode='Markdown')
        return
    
    pet_id = args[1]
    if pet_id not in PETS_DATA:
        bot.send_message(message.chat.id, "❌ Неверный ID питомца!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    price = PETS_DATA[pet_id]['price']
    if user['balance'] < price:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Нужно: {format_number(price)}", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['balance'] -= price
        user['pets'][pet_id] = {
            'bought': time.time(),
            'happiness': 100
        }
        user['pets_last_feed'][pet_id] = time.time()
        save_data()
    
    bot.send_message(message.chat.id, f"✅ Ты купил {PETS_DATA[pet_id]['name']}!", parse_mode='Markdown')

@bot.message_handler(commands=['покормить'])
def feed_pet_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /покормить [id]", parse_mode='Markdown')
        return
    
    pet_id = args[1]
    if pet_id not in PETS_DATA:
        bot.send_message(message.chat.id, "❌ Неверный ID питомца!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    if pet_id not in user['pets']:
        bot.send_message(message.chat.id, "❌ У тебя нет такого питомца!", parse_mode='Markdown')
        return
    
    food_cost = PETS_DATA[pet_id]['food_cost']
    if user['balance'] < food_cost:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Нужно: {food_cost}", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['balance'] -= food_cost
        user['pets_last_feed'][pet_id] = time.time()
        save_data()
    
    bot.send_message(message.chat.id, f"✅ Ты покормил {PETS_DATA[pet_id]['name']}! Счастье восстановлено.", parse_mode='Markdown')

@bot.message_handler(commands=['собрать_питомцы'])
def collect_pets_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    now = time.time()
    total = 0
    collected_text = []
    
    with get_user_lock(user_id):
        for pid, pet_data in user['pets'].items():
            data = PETS_DATA.get(pid)
            if not data:
                continue
            last_feed = user['pets_last_feed'].get(pid, now)
            elapsed = now - last_feed
            hours = elapsed / 3600
            happiness = data['happiness']
            if last_feed:
                elapsed_feed = now - last_feed
                happiness = max(0, data['happiness'] - int(elapsed_feed / 3600) * 10)
            income_mult = happiness / 100
            earned = int(data['income'] * hours * income_mult)
            if earned > 0:
                total += earned
                collected_text.append(f"{data['name']}: +{format_number(earned)}")
        
        if total > 0:
            user['balance'] += total
            save_data()
    
    if total > 0:
        text = (
            f"✅ ** СБОР С ПИТОМЦЕВ ** ✅\n\n"
            f"{chr(10).join(collected_text)}\n\n"
            f"💰 Всего собрано: +{format_number(total)} кредиксов\n"
            f"💸 Новый баланс: {format_number(user['balance'])}"
        )
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "❌ Нет дохода для сбора.", parse_mode='Markdown')

# ====================== БИЗНЕС ======================
@bot.message_handler(commands=['бизнес', 'business'])
def business_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    text = "🏪 ** МОЙ БИЗНЕС ** 🏪\n\n"
    if not user['businesses']:
        text += "У тебя нет бизнеса. Купи в магазине: /магазин_бизнеса\n"
    else:
        for bid, biz_data in user['businesses'].items():
            data = BUSINESS_DATA.get(bid)
            if not data:
                continue
            level = biz_data.get('level', 1)
            income = data['income'] * level
            text += f"{data['icon']} {data['name']} (ур. {level})\n   Доход в час: {format_number(income)}\n\n"
    
    now = time.time()
    total_income = 0
    for bid, biz_data in user['businesses'].items():
        data = BUSINESS_DATA.get(bid)
        if not data:
            continue
        last = user['businesses_last_collect'].get(bid, now)
        elapsed = now - last
        hours = elapsed / 3600
        level = biz_data.get('level', 1)
        income = data['income'] * level * hours
        if income > 0:
            total_income += income
    
    if total_income > 0:
        text += f"\n💰 Накопленный доход: {format_number(int(total_income))}\n/собрать_бизнес"
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['магазин_бизнеса'])
def business_shop_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    text = "🏪 ** МАГАЗИН БИЗНЕСА ** 🏪\n\n"
    for bid, data in BUSINESS_DATA.items():
        text += f"{data['icon']} {data['name']}\n"
        text += f"   💰 Цена: {format_number(data['price'])} кредиксов\n"
        text += f"   💵 Доход: {format_number(data['income'])}/час (за 1 ур.)\n"
        text += f"   📈 Макс уровень: {data['max_level']}\n"
        text += f"   📝 {data['description']}\n"
        text += f"   /купить_бизнес {bid}\n\n"
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['купить_бизнес'])
def buy_business_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /купить_бизнес [id]", parse_mode='Markdown')
        return
    
    business_id = args[1]
    if business_id not in BUSINESS_DATA:
        bot.send_message(message.chat.id, "❌ Неверный ID бизнеса!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    price = BUSINESS_DATA[business_id]['price']
    if user['balance'] < price:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Нужно: {format_number(price)}", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['balance'] -= price
        user['businesses'][business_id] = {
            'level': 1,
            'bought': time.time()
        }
        user['businesses_last_collect'][business_id] = time.time()
        save_data()
    
    bot.send_message(message.chat.id, f"✅ Ты купил {BUSINESS_DATA[business_id]['icon']} {BUSINESS_DATA[business_id]['name']}!", parse_mode='Markdown')

@bot.message_handler(commands=['улучшить'])
def upgrade_business_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /улучшить [id]", parse_mode='Markdown')
        return
    
    business_id = args[1]
    if business_id not in BUSINESS_DATA:
        bot.send_message(message.chat.id, "❌ Неверный ID бизнеса!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    if business_id not in user['businesses']:
        bot.send_message(message.chat.id, "❌ У тебя нет такого бизнеса!", parse_mode='Markdown')
        return
    
    biz_data = user['businesses'][business_id]
    current_level = biz_data.get('level', 1)
    data = BUSINESS_DATA[business_id]
    
    if current_level >= data['max_level']:
        bot.send_message(message.chat.id, "❌ Достигнут максимальный уровень!", parse_mode='Markdown')
        return
    
    upgrade_cost = data['upgrade_cost']
    if user['balance'] < upgrade_cost:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Нужно: {format_number(upgrade_cost)}", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['balance'] -= upgrade_cost
        biz_data['level'] = current_level + 1
        save_data()
    
    bot.send_message(message.chat.id, f"✅ Бизнес {data['icon']} {data['name']} улучшен до {current_level+1} уровня!", parse_mode='Markdown')

@bot.message_handler(commands=['собрать_бизнес'])
def collect_business_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    now = time.time()
    total = 0
    collected_text = []
    
    with get_user_lock(user_id):
        for bid, biz_data in user['businesses'].items():
            data = BUSINESS_DATA.get(bid)
            if not data:
                continue
            last = user['businesses_last_collect'].get(bid, now)
            elapsed = now - last
            hours = elapsed / 3600
            level = biz_data.get('level', 1)
            income = data['income'] * level * hours
            if income > 0:
                total += income
                user['businesses_last_collect'][bid] = now
                collected_text.append(f"{data['icon']} {data['name']} ур.{level}: +{format_number(int(income))}")
        
        if total > 0:
            total = int(total)
            user['balance'] += total
            update_quest_progress(user_id, 'business_collects')
            save_data()
    
    if total > 0:
        text = (
            f"✅ ** СБОР С БИЗНЕСА ** ✅\n\n"
            f"{chr(10).join(collected_text)}\n\n"
            f"💰 Всего собрано: +{format_number(total)} кредиксов\n"
            f"💸 Новый баланс: {format_number(user['balance'])}"
        )
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "❌ Нет дохода для сбора.", parse_mode='Markdown')

# ====================== БАНК ======================
@bot.message_handler(commands=['банк', 'bank'])
def bank_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    deposit = user.get('bank_deposit', {'amount': 0, 'time': 0})
    loan = user.get('bank_loan', {'amount': 0, 'time': 0})
    
    text = (
        f"🏦 ** БАНК ** 🏦\n\n"
        f"💵 Твой депозит: {format_number(deposit['amount'])}\n"
        f"💰 Проценты: 5% в день\n"
        f"💸 Твой кредит: {format_number(loan['amount'])}\n"
        f"📉 Ставка по кредиту: 10% в день\n\n"
        f"**Команды:**\n"
        f"/депозит [сумма] - положить деньги\n"
        f"/снять [сумма] - снять с депозита\n"
        f"/кредит [сумма] - взять кредит\n"
        f"/выплатить [сумма] - выплатить кредит\n"
        f"/проценты - начислить проценты"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['депозит'])
def deposit_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /депозит [сумма]", parse_mode='Markdown')
        return
    
    amount = parse_bet(args[1])
    if amount is None or amount <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    if user['balance'] < amount:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Баланс: {format_number(user['balance'])}", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['balance'] -= amount
        user['bank_deposit']['amount'] += amount
        user['bank_deposit']['time'] = time.time()
        bank_data['total_deposits'] += amount
        update_quest_progress(user_id, 'deposit_amount', amount)
        save_data()
    
    bot.send_message(message.chat.id, f"✅ Ты положил {format_number(amount)} на депозит.", parse_mode='Markdown')

@bot.message_handler(commands=['снять'])
def withdraw_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /снять [сумма]", parse_mode='Markdown')
        return
    
    amount = parse_bet(args[1])
    if amount is None or amount <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    deposit = user['bank_deposit']['amount']
    if deposit < amount:
        bot.send_message(message.chat.id, f"❌ На депозите недостаточно! Доступно: {format_number(deposit)}", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['balance'] += amount
        user['bank_deposit']['amount'] -= amount
        bank_data['total_deposits'] -= amount
        save_data()
    
    bot.send_message(message.chat.id, f"✅ Ты снял {format_number(amount)} с депозита.", parse_mode='Markdown')

@bot.message_handler(commands=['кредит'])
def loan_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /кредит [сумма]", parse_mode='Markdown')
        return
    
    amount = parse_bet(args[1])
    if amount is None or amount <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    loan = user['bank_loan']['amount']
    max_loan = user['balance'] * 2
    
    if amount > max_loan:
        bot.send_message(message.chat.id, f"❌ Максимальная сумма кредита: {format_number(max_loan)}", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['balance'] += amount
        user['bank_loan']['amount'] += amount
        user['bank_loan']['time'] = time.time()
        save_data()
    
    bot.send_message(message.chat.id, f"✅ Ты взял кредит {format_number(amount)} кредиксов.", parse_mode='Markdown')

@bot.message_handler(commands=['выплатить'])
def repay_loan_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /выплатить [сумма]", parse_mode='Markdown')
        return
    
    amount = parse_bet(args[1])
    if amount is None or amount <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    loan = user['bank_loan']['amount']
    if loan == 0:
        bot.send_message(message.chat.id, "❌ У тебя нет кредита!", parse_mode='Markdown')
        return
    
    if user['balance'] < amount:
        bot.send_message(message.chat.id, f"❌ Недостаточно средств! Баланс: {format_number(user['balance'])}", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['balance'] -= amount
        user['bank_loan']['amount'] -= amount
        if user['bank_loan']['amount'] < 0:
            user['balance'] += abs(user['bank_loan']['amount'])
            user['bank_loan']['amount'] = 0
        save_data()
    
    bot.send_message(message.chat.id, f"✅ Ты выплатил {format_number(amount)} кредита. Остаток: {format_number(user['bank_loan']['amount'])}", parse_mode='Markdown')

@bot.message_handler(commands=['проценты'])
def interest_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    now = time.time()
    
    deposit = user['bank_deposit']
    if deposit['amount'] > 0 and deposit['time'] > 0:
        elapsed = now - deposit['time']
        days = elapsed / 86400
        if days >= 1:
            interest = int(deposit['amount'] * 0.05 * days)
            with get_user_lock(user_id):
                user['balance'] += interest
                deposit['time'] = now
                save_data()
            bot.send_message(message.chat.id, f"💰 Начислены проценты по депозиту: +{format_number(interest)} кредиксов", parse_mode='Markdown')
    
    loan = user['bank_loan']
    if loan['amount'] > 0 and loan['time'] > 0:
        elapsed = now - loan['time']
        days = elapsed / 86400
        if days >= 1:
            interest = int(loan['amount'] * 0.1 * days)
            with get_user_lock(user_id):
                loan['amount'] += interest
                loan['time'] = now
                save_data()
            bot.send_message(message.chat.id, f"⚠️ Начислены проценты по кредиту: +{format_number(interest)} к долгу", parse_mode='Markdown')

# ====================== СИСТЕМА KRDS ======================
@bot.message_handler(commands=['донат'])
def donate_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    text = (
        f"💎 ** KRDS СИСТЕМА ** 💎\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
        f"Твой баланс KRDS: {user['krds_balance']}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"**Команды:**\n"
        f"/сенд @ник сумма - отправить KRDS\n"
        f"/продать количество - продать боту (3250 кредиксов за 1 KRDS)\n"
        f"/обменник - P2P обменник\n\n"
        f"💡 1 KRDS можно обменять на 3250 кредиксов у бота"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['сенд'])
def send_krds_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, "❌ Использование: /сенд @ник сумма", parse_mode='Markdown')
        return
    
    target_username = args[1].replace('@', '').lower()
    try:
        amount = int(args[2])
        if amount <= 0:
            bot.send_message(message.chat.id, "❌ Сумма должна быть положительной!", parse_mode='Markdown')
            return
    except ValueError:
        bot.send_message(message.chat.id, "❌ Введите число!", parse_mode='Markdown')
        return
    
    with data_lock:
        target_id = username_cache.get(target_username)
        if not target_id:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!", parse_mode='Markdown')
            return
        
        user = get_user(user_id)
        if user['krds_balance'] < amount:
            bot.send_message(message.chat.id, f"❌ У тебя недостаточно KRDS! Баланс: {user['krds_balance']}", parse_mode='Markdown')
            return
        
        with get_user_lock(user_id), get_user_lock(target_id):
            user['krds_balance'] -= amount
            users[target_id]['krds_balance'] += amount
            save_data()
    
    bot.send_message(message.chat.id, f"✅ Ты отправил {amount} KRDS пользователю @{target_username}", parse_mode='Markdown')

@bot.message_handler(commands=['продать'])
def sell_to_bot_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /продать количество", parse_mode='Markdown')
        return
    
    try:
        amount = int(args[1])
        if amount <= 0:
            bot.send_message(message.chat.id, "❌ Количество должно быть положительным!", parse_mode='Markdown')
            return
    except ValueError:
        bot.send_message(message.chat.id, "❌ Введите число!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    if user['krds_balance'] < amount:
        bot.send_message(message.chat.id, f"❌ У тебя недостаточно KRDS! Баланс: {user['krds_balance']}", parse_mode='Markdown')
        return
    
    price_per_krds = 3250
    total = amount * price_per_krds
    
    with get_user_lock(user_id):
        user['krds_balance'] -= amount
        user['balance'] += total
        save_data()
    
    bot.send_message(message.chat.id, 
        f"✅ Ты продал {amount} KRDS боту за {format_number(total)} кредиксов.\n"
        f"💰 Новый баланс: {format_number(user['balance'])}\n"
        f"💎 KRDS: {user['krds_balance']}", parse_mode='Markdown')

# ====================== P2P ОБМЕННИК ======================
@bot.message_handler(commands=['обменник'])
def exchange_menu(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📤 Продать KRDS", callback_data="exchange_sell"),
        types.InlineKeyboardButton("📥 Купить KRDS", callback_data="exchange_buy"),
        types.InlineKeyboardButton("📋 Мои ордера", callback_data="exchange_my_orders"),
        types.InlineKeyboardButton("📊 Все ордера", callback_data="exchange_all_orders"),
        types.InlineKeyboardButton("❓ Помощь", callback_data="exchange_help")
    )
    
    bot.send_message(
        message.chat.id,
        "💎 ** P2P ОБМЕННИК KRDS ** 💎\n\n"
        "Здесь ты можешь купить или продать KRDS другим игрокам.\n"
        "Цены устанавливаются самими игроками.",
        reply_markup=markup, parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith('exchange_'))
def exchange_callback(call):
    user_id = str(call.from_user.id)
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "⛔ Вы забанены!")
        return
    
    data = call.data
    
    if data == "exchange_sell":
        msg = bot.edit_message_text(
            "📤 ** ПРОДАЖА KRDS **\n\n"
            "Введи команду:\n"
            "/продатькрдс [количество] [цена за 1 KRDS]",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
    
    elif data == "exchange_buy":
        msg = bot.edit_message_text(
            "📥 ** ПОКУПКА KRDS **\n\n"
            "Введи команду:\n"
            "/купитькрдс [количество] [макс. цена за 1 KRDS]",
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
    
    elif data == "exchange_my_orders":
        my_orders_command(call.message)
        bot.answer_callback_query(call.id)
    
    elif data == "exchange_all_orders":
        all_orders_command(call.message)
        bot.answer_callback_query(call.id)
    
    elif data == "exchange_help":
        help_text = (
            "❓ ** Помощь по обменнику ** ❓\n\n"
            "📤 Продажа: /продатькрдс [кол-во] [цена]\n"
            "   Пример: /продатькрдс 10 3500\n"
            "   Это выставит ордер на продажу 10 KRDS по 3500 кредиксов за штуку.\n\n"
            "📥 Покупка: /купитькрдс [кол-во] [макс. цена]\n"
            "   Пример: /купитькрдс 5 3400\n"
            "   Это создаст ордер на покупку 5 KRDS по цене не выше 3400.\n\n"
            "📋 Мои ордера: /моиордера\n"
            "📊 Все ордера: /ордера\n"
            "❌ Отменить ордер: /отменитьордер [ID]"
        )
        bot.edit_message_text(help_text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        bot.answer_callback_query(call.id)

@bot.message_handler(commands=['продатькрдс'])
def sell_krds_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, "❌ Использование: /продатькрдс [количество] [цена за 1 KRDS]", parse_mode='Markdown')
        return
    
    try:
        amount = int(args[1])
        price = int(args[2])
        if amount <= 0 or price <= 0:
            bot.send_message(message.chat.id, "❌ Количество и цена должны быть положительными!", parse_mode='Markdown')
            return
    except ValueError:
        bot.send_message(message.chat.id, "❌ Введите числа!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    if user['krds_balance'] < amount:
        bot.send_message(message.chat.id, f"❌ У тебя недостаточно KRDS! Баланс: {user['krds_balance']}", parse_mode='Markdown')
        return
    
    for oid, order in orders.items():
        if order['user_id'] == user_id and order['type'] == 'sell' and order['active']:
            bot.send_message(message.chat.id, "❌ У тебя уже есть активный ордер на продажу!", parse_mode='Markdown')
            return
    
    global next_order_id
    order_id = str(next_order_id)
    next_order_id += 1
    
    with data_lock:
        orders[order_id] = {
            'user_id': user_id,
            'type': 'sell',
            'amount': amount,
            'price': price,
            'total': amount * price,
            'time': time.time(),
            'active': True
        }
        save_data()
    
    bot.send_message(message.chat.id, 
        f"✅ Выставлен ордер на продажу!\n"
        f"🆔 ID: {order_id}\n"
        f"📊 {amount} KRDS по {price} кредиксов\n"
        f"💰 Общая сумма: {format_number(amount * price)}", parse_mode='Markdown')

@bot.message_handler(commands=['купитькрдс'])
def buy_krds_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, "❌ Использование: /купитькрдс [количество] [макс. цена за 1 KRDS]", parse_mode='Markdown')
        return
    
    try:
        amount = int(args[1])
        max_price = int(args[2])
        if amount <= 0 or max_price <= 0:
            bot.send_message(message.chat.id, "❌ Количество и цена должны быть положительными!", parse_mode='Markdown')
            return
    except ValueError:
        bot.send_message(message.chat.id, "❌ Введите числа!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    total_cost = amount * max_price
    if user['balance'] < total_cost:
        bot.send_message(message.chat.id, f"❌ Недостаточно кредиксов! Нужно: {format_number(total_cost)}", parse_mode='Markdown')
        return
    
    found = None
    with data_lock:
        for oid, order in orders.items():
            if (order['type'] == 'sell' and order['active'] and 
                order['price'] <= max_price and order['amount'] >= amount):
                found = order
                found_id = oid
                break
    
    if found:
        seller_id = found['user_id']
        seller = get_user(seller_id)
        total_price = amount * found['price']
        
        with get_user_lock(user_id), get_user_lock(seller_id), data_lock:
            user['balance'] -= total_price
            user['krds_balance'] += amount
            
            seller['balance'] += total_price
            seller['krds_balance'] -= amount
            
            if found['amount'] == amount:
                found['active'] = False
            else:
                found['amount'] -= amount
            
            save_data()
        
        bot.send_message(message.chat.id, 
            f"✅ Сделка совершена!\n"
            f"Ты купил {amount} KRDS у @{username_cache.get(seller_id, 'неизвестно')}\n"
            f"💰 Цена: {format_number(total_price)} кредиксов", parse_mode='Markdown')
    else:
        global next_order_id
        order_id = str(next_order_id)
        next_order_id += 1
        
        with data_lock:
            orders[order_id] = {
                'user_id': user_id,
                'type': 'buy',
                'amount': amount,
                'price': max_price,
                'total': amount * max_price,
                'time': time.time(),
                'active': True
            }
            save_data()
        
        bot.send_message(message.chat.id, 
            f"✅ Создан ордер на покупку!\n"
            f"🆔 ID: {order_id}\n"
            f"📊 {amount} KRDS по макс. цене {max_price}\n"
            f"💰 Общая сумма: {format_number(amount * max_price)}", parse_mode='Markdown')

@bot.message_handler(commands=['моиордера'])
def my_orders_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    text = "📋 ** МОИ ОРДЕРА **\n\n"
    found = False
    for oid, order in orders.items():
        if order['user_id'] == user_id and order['active']:
            found = True
            type_emoji = "📤" if order['type'] == 'sell' else "📥"
            text += f"{type_emoji} ID: {oid}\n"
            text += f"   {order['amount']} KRDS по {order['price']}\n"
            text += f"   /отменитьордер {oid}\n\n"
    
    if not found:
        text += "У тебя нет активных ордеров."
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['ордера'])
def all_orders_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    text = "📊 ** ВСЕ ОРДЕРА **\n\n"
    sell_orders = []
    buy_orders = []
    
    for oid, order in orders.items():
        if not order['active']:
            continue
        if order['type'] == 'sell':
            sell_orders.append((oid, order))
        else:
            buy_orders.append((oid, order))
    
    if sell_orders:
        text += "📤 ** Продажа:**\n"
        for oid, order in sell_orders:
            try:
                u = bot.get_chat(int(order['user_id']))
                name = f"@{u.username}" if u.username else u.first_name
            except:
                name = f"ID {order['user_id']}"
            text += f"   ID {oid}: {order['amount']} KRDS по {order['price']} от {name}\n"
    
    if buy_orders:
        text += "\n📥 ** Покупка:**\n"
        for oid, order in buy_orders:
            try:
                u = bot.get_chat(int(order['user_id']))
                name = f"@{u.username}" if u.username else u.first_name
            except:
                name = f"ID {order['user_id']}"
            text += f"   ID {oid}: {order['amount']} KRDS до {order['price']} от {name}\n"
    
    if not sell_orders and not buy_orders:
        text += "Нет активных ордеров."
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['отменитьордер'])
def cancel_order_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /отменитьордер [ID]", parse_mode='Markdown')
        return
    
    order_id = args[1]
    if order_id not in orders:
        bot.send_message(message.chat.id, "❌ Ордер не найден!", parse_mode='Markdown')
        return
    
    order = orders[order_id]
    if order['user_id'] != user_id:
        bot.send_message(message.chat.id, "❌ Это не твой ордер!", parse_mode='Markdown')
        return
    
    if not order['active']:
        bot.send_message(message.chat.id, "❌ Ордер уже неактивен!", parse_mode='Markdown')
        return
    
    with data_lock:
        order['active'] = False
        save_data()
    
    bot.send_message(message.chat.id, f"✅ Ордер {order_id} отменён.", parse_mode='Markdown')

# ====================== РАБОТА ======================
@bot.message_handler(commands=['работа', 'work'])
def work_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    with get_user_lock(user_id):
        reward = 55
        user['balance'] += reward
        user['work_count'] += 1
        update_quest_progress(user_id, 'works')
        save_data()
    
    bot.send_message(message.chat.id,
        f"💼 ** РАБОТА ** 💼\n\n"
        f"✅ Ты получил: +{reward} кредиксов\n"
        f"💰 Баланс: {format_number(user['balance'])}", parse_mode='Markdown')

# ====================== РЕФЕРАЛЫ ======================
@bot.message_handler(commands=['реф', 'ref'])
def ref_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    bot_info = bot.get_me()
    ref_link = f"https://t.me/{bot_info.username}?start={user_id}"
    user = get_user(user_id)
    
    text = (
        "👥 ** РЕФЕРАЛЬНАЯ СИСТЕМА ** 👥\n\n"
        f"🔗 Твоя ссылка:\n{ref_link}\n\n"
        f"📊 Приглашено друзей: {user.get('referrals', 0)}\n\n"
        f"🎁 За каждого друга: +{format_number(bonus_data['referral_bonus'])} кредиксов и +5 KRDS\n\n"
        f"🏆 Достижение: 10 друзей - 100,000 кредиксов"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# ====================== ПРОФИЛЬ ======================
@bot.message_handler(commands=['профиль', 'profile'])
def profile_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    
    clan_name = "Нет клана"
    if user.get('clan') and user['clan'] in clans:
        clan_name = clans[user['clan']]['name']
    
    deposit = user.get('bank_deposit', {}).get('amount', 0)
    loan = user.get('bank_loan', {}).get('amount', 0)
    
    vip_status = "Нет"
    if user.get('vip_level') and user.get('vip_expires', 0) > time.time():
        vip_status = VIP_LEVELS[user['vip_level']]['name']
    
    text = (
        f"📱 ** ПРОФИЛЬ ** 📱\n\n"
        f"🆔 ID: {user_id}\n"
        f"👑 VIP: {vip_status}\n\n"
        f"💰 ** ФИНАНСЫ **\n"
        f"💸 Кредиксы: {format_number(user['balance'])}\n"
        f"💎 KRDS: {user['krds_balance']}\n"
        f"🏦 Депозит: {format_number(deposit)}\n"
        f"📉 Кредит: {format_number(loan)}\n\n"
        f"📊 ** СТАТИСТИКА ИГР **\n"
        f"🎮 Сыграно: {user.get('games_played', 0)}\n"
        f"✅ Побед: {user.get('total_wins', 0)}\n"
        f"❌ Поражений: {user.get('total_losses', 0)}\n"
        f"🔥 Текущий стрик: {user.get('win_streak', 0)}\n"
        f"🎰 Макс стрик: {user.get('max_win_streak', 0)}\n\n"
        f"🐭 Мышек: {sum(user.get('mice', {}).values())}\n"
        f"🐾 Питомцев: {len(user.get('pets', {}))}\n"
        f"🏪 Бизнесов: {len(user.get('businesses', {}))}\n"
        f"👥 Рефералов: {user.get('referrals', 0)}\n"
        f"💼 Работ: {user.get('work_count', 0)}\n"
        f"📋 Квестов: {user.get('quests_completed', 0)}"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# ====================== ПЕРЕВОДЫ ======================
@bot.message_handler(commands=['дать', 'give'])
def give_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, "❌ Использование: /дать @ник сумма", parse_mode='Markdown')
        return
    
    target_username = args[1].replace('@', '').lower()
    amount = parse_bet(args[2])
    if amount is None or amount <= 0:
        bot.send_message(message.chat.id, "❌ Неверная сумма!", parse_mode='Markdown')
        return
    
    with data_lock:
        target_id = username_cache.get(target_username)
        if not target_id:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!", parse_mode='Markdown')
            return
        
        user = get_user(user_id)
        if user['balance'] < amount:
            bot.send_message(message.chat.id, f"❌ Недостаточно средств! Баланс: {format_number(user['balance'])}", parse_mode='Markdown')
            return
        
        with get_user_lock(user_id), get_user_lock(target_id):
            user['balance'] -= amount
            users[target_id]['balance'] += amount
            save_data()
    
    bot.send_message(message.chat.id, f"✅ Ты отправил {format_number(amount)} кредиксов пользователю @{target_username}", parse_mode='Markdown')

# ====================== ОТМЕНА ИГРЫ ======================
@bot.message_handler(commands=['отмена', 'cancel'])
def cancel_game_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    if cancel_user_game(user_id):
        bot.send_message(message.chat.id, "🛑 Игра отменена. Ставка возвращена.", parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "❌ У тебя нет активной игры.", parse_mode='Markdown')

# ====================== СТАРТ И ПОМОЩЬ ================
 @bot.message_handler(commands=['start', 'help', 'старт', 'помощь'])
def start_help(message):
    try:
        user_id = str(message.from_user.id)
        
        if message.from_user.username:
            update_username_cache(user_id, message.from_user.username)
        
        user = get_user(user_id)
        
        args = message.text.split()
        if len(args) > 1 and args[1].isdigit():
            referrer_id = args[1]
            if referrer_id != user_id and referrer_id in users:
                with get_user_lock(referrer_id), get_user_lock(user_id):
                    referrer = get_user(referrer_id)
                    user['referrer'] = referrer_id
                    referrer['referrals'] += 1
                    referrer['balance'] += bonus_data['referral_bonus']
                    referrer['krds_balance'] += 5
                    user['balance'] += 500
                    # ВАЖНО: передаём 1 (приращение), а не общее количество
                    update_quest_progress(referrer_id, 'referrals', 1)
                    save_data()
                    
                    try:
                        bot.send_message(int(referrer_id),
                            f"🎉 По твоей ссылке зарегистрировался новый игрок!\n"
                            f"💰 +{format_number(bonus_data['referral_bonus'])} кредиксов\n"
                            f"💎 +5 KRDS", parse_mode='Markdown')
                    except:
                        pass
        
        today = datetime.now().strftime('%Y-%m-%d')
        if today not in user['daily_quests']:
            generate_daily_quests(user_id)
        
        text = (
            "🎰 ** ДОБРО ПОЖАЛОВАТЬ В kредиkс! ** 🎰\n\n"
            "💰 **Баланс:** /баланс\n"
            "📊 **Статистика:** /статистика\n"
            "🏆 **Топ игроков:** /топ\n"
            "👑 **VIP система:** /вип\n"
            "📋 **Квесты:** /квесты\n"
            "🏆 **Турниры:** /турнир\n"
            "💎 **KRDS:** /донат\n"
            "📱 **Телефон:** /телефон\n"
            "🎉 **Ивент:** /ивент\n\n"
            "🎮 **Доступные игры:**\n"
            "• Башня: /башня [ставка]\n"
            "• Футбол: /футбол [ставка]\n"
            "• Баскетбол: /баскетбол [ставка]\n"
            "• Дартс: /дартс [ставка]\n"
            "• Покер: /покер [ставка]\n"
            "• Пирамида: /пирамида [ставка]\n"
            "• Мины: /мины [ставка]\n"
            "• Слоты: /слоты [ставка]\n"
            "• Рулетка: /рулетка_каз [ставка] [тип] [число]\n"
            "• Хило: /хило [ставка]\n"
            "• Очко: /очко [ставка]\n"
            "• Краш: /краш [ставка]\n"
            "• x2/x3/x5: /x2 [ставка]\n"
            "• Фишки: /фишки [ставка] [black/white]\n"
            "• Русская рулетка: /рулетка_рус [ставка]\n"
            "• Джекпот: /джекпот [ставка]\n"
            "• Кости: /кости [ставка] [больше6/меньше6/чет/нечет]\n\n"
            "🐭 **Мышки:** /мышки\n"
            "🐾 **Питомцы:** /питомцы\n"
            "🏪 **Бизнес:** /бизнес\n"
            "🏦 **Банк:** /банк\n"
            "👥 **Рефералы:** /реф\n"
            "💼 **Работа:** /работа\n\n"
            "💡 Форматы ставок: 1к = 1000, 1кк/1ку = 1,000,000\n\n"
            f"📢 Канал: {CHANNEL_USERNAME}\n"
            f"💬 Чат: {CHAT_LINK}"
        )
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
        
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"❌ Ошибка в start_help: {e}\n{error_trace}")
        bot.send_message(
            message.chat.id,
            f"❌ Внутренняя ошибка:\n`{e}`\n\nПодробности в консоли.",
            parse_mode='Markdown'
        )        
# ====================== СИСТЕМА ТЕЛЕФОНА ======================
@bot.message_handler(commands=['телефон'])
def phone_menu(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📞 Контакты", callback_data="phone_contacts"),
        types.InlineKeyboardButton("📱 Позвонить", callback_data="phone_call"),
        types.InlineKeyboardButton("✉️ Сообщения", callback_data="phone_messages"),
        types.InlineKeyboardButton("💰 Микрозайм", callback_data="phone_microloan")
    )
    
    bot.send_message(message.chat.id,
        "📱 ** ТЕЛЕФОН ** 📱\n\n"
        "Выбери действие:",
        reply_markup=markup, parse_mode='Markdown')

def phone_callback_handler(call):
    user_id = str(call.from_user.id)
    if is_banned(user_id):
        bot.answer_callback_query(call.id, "⛔ Вы забанены!")
        return
    
    data = call.data
    if data == "phone_contacts":
        user = get_user(user_id)
        contacts = user.get('phone_contacts', [])
        if not contacts:
            text = "📋 У тебя нет сохранённых контактов.\n\nДобавить: /добавить_контакт @ник"
        else:
            text = "📋 ** ТВОИ КОНТАКТЫ **\n\n"
            for contact in contacts:
                try:
                    u = bot.get_chat(int(contact))
                    name = f"@{u.username}" if u.username else u.first_name
                except:
                    name = f"ID {contact}"
                text += f"• {name}\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        bot.answer_callback_query(call.id)
    
    elif data == "phone_call":
        bot.edit_message_text(
            "📞 ** ЗВОНОК **\n\n"
            "Чтобы позвонить, используй команду:\n"
            "/позвонить @ник",
            call.message.chat.id, call.message.message_id, parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
    
    elif data == "phone_messages":
        bot.edit_message_text(
            "✉️ ** СООБЩЕНИЯ **\n\n"
            "Чтобы отправить сообщение, используй:\n"
            "/смс @ник текст",
            call.message.chat.id, call.message.message_id, parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
    
    elif data == "phone_microloan":
        bot.edit_message_text(
            "💰 ** МИКРОЗАЙМ ** 💰\n\n"
            "Ты можешь взять быстрый займ до 10 000 кредиксов.\n"
            "Условия: сумма ×2 через час.\n\n"
            "Используй: /микрозайм сумма",
            call.message.chat.id, call.message.message_id, parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)

@bot.message_handler(commands=['добавить_контакт'])
def add_contact_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /добавить_контакт @ник", parse_mode='Markdown')
        return
    
    target_username = args[1].replace('@', '').lower()
    with data_lock:
        target_id = username_cache.get(target_username)
        if not target_id:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!", parse_mode='Markdown')
            return
        
        user = get_user(user_id)
        if target_id in user.get('phone_contacts', []):
            bot.send_message(message.chat.id, "❌ Этот контакт уже есть!", parse_mode='Markdown')
            return
        
        user['phone_contacts'].append(target_id)
        save_data()
    
    bot.send_message(message.chat.id, f"✅ Контакт @{target_username} добавлен!", parse_mode='Markdown')

@bot.message_handler(commands=['позвонить'])
def call_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /позвонить @ник", parse_mode='Markdown')
        return
    
    target_username = args[1].replace('@', '').lower()
    with data_lock:
        target_id = username_cache.get(target_username)
        if not target_id:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!", parse_mode='Markdown')
            return
        
        user = get_user(user_id)
        if user['balance'] < 10:
            bot.send_message(message.chat.id, "❌ Недостаточно средств для звонка (нужно 10 кредиксов)!", parse_mode='Markdown')
            return
        
        with get_user_lock(user_id), get_user_lock(target_id):
            user['balance'] -= 10
            user.setdefault('phone_call_history', []).append({
                'to': target_id,
                'time': time.time()
            })
            if len(user['phone_call_history']) >= 100:
                unlock_achievement(user_id, 'phone_addict')
            save_data()
        
        try:
            bot.send_message(int(target_id),
                f"📞 Вам звонит @{message.from_user.username or message.from_user.first_name}!\n"
                f"Ответить некуда, но вы можете позвонить в ответ.", parse_mode='Markdown')
        except:
            pass
    
    bot.send_message(message.chat.id, f"📞 Звонок @{target_username} совершён. Списано 10 кредиксов.", parse_mode='Markdown')

@bot.message_handler(commands=['смс'])
def sms_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        bot.send_message(message.chat.id, "❌ Использование: /смс @ник текст", parse_mode='Markdown')
        return
    
    target_username = args[1].replace('@', '').lower()
    text = args[2]
    
    with data_lock:
        target_id = username_cache.get(target_username)
        if not target_id:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!", parse_mode='Markdown')
            return
        
        user = get_user(user_id)
        if user['balance'] < 5:
            bot.send_message(message.chat.id, "❌ Недостаточно средств для отправки СМС (нужно 5 кредиксов)!", parse_mode='Markdown')
            return
        
        with get_user_lock(user_id), get_user_lock(target_id):
            user['balance'] -= 5
            users[target_id].setdefault('phone_messages', []).append({
                'from': user_id,
                'text': text,
                'time': time.time(),
                'read': False
            })
            save_data()
        
        try:
            bot.send_message(int(target_id),
                f"✉️ Новое СМС от @{message.from_user.username or message.from_user.first_name}:\n\n{text}", parse_mode='Markdown')
        except:
            pass
    
    bot.send_message(message.chat.id, f"✉️ СМС отправлено @{target_username} (списано 5 кредиксов).", parse_mode='Markdown')

@bot.message_handler(commands=['микрозайм'])
def microloan_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /микрозайм сумма (до 10000)", parse_mode='Markdown')
        return
    
    try:
        amount = int(args[1])
        if amount <= 0 or amount > 10000:
            bot.send_message(message.chat.id, "❌ Сумма должна быть от 1 до 10000", parse_mode='Markdown')
            return
    except ValueError:
        bot.send_message(message.chat.id, "❌ Введите число!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    now = time.time()
    
    if user.get('microloan'):
        loan_time = user['microloan']['time']
        if now - loan_time < 3600:
            bot.send_message(message.chat.id, "❌ У тебя уже есть активный микрозайм! Верни его через час.", parse_mode='Markdown')
            return
        else:
            if user['balance'] < user['microloan']['amount'] * 2:
                bot.send_message(message.chat.id, "❌ Ты не можешь взять новый займ, пока не вернёшь старый! Не хватает средств.", parse_mode='Markdown')
                return
            with get_user_lock(user_id):
                user['balance'] -= user['microloan']['amount'] * 2
                del user['microloan']
                save_data()
    
    with get_user_lock(user_id):
        user['balance'] += amount
        user['microloan'] = {
            'amount': amount,
            'time': now
        }
        save_data()
    
    bot.send_message(message.chat.id,
        f"💰 ** МИКРОЗАЙМ **\n\n"
        f"Ты получил {amount} кредиксов.\n"
        f"Через час нужно вернуть {amount*2} кредиксов.\n"
        f"Если не вернёшь, не сможешь взять новый займ.", parse_mode='Markdown')

def check_microloans():
    while True:
        time.sleep(60)
        now = time.time()
        with data_lock:
            for uid, user in users.items():
                if user.get('microloan'):
                    loan_time = user['microloan']['time']
                    if now - loan_time > 3600:
                        if user['balance'] >= user['microloan']['amount'] * 2:
                            with get_user_lock(uid):
                                user['balance'] -= user['microloan']['amount'] * 2
                                del user['microloan']
                                save_data()

# ====================== ИВЕНТ ======================
EVENT_SHOP = {
    'skin1': {'name': '🎭 Скин к 1 марта', 'price': 100, 'description': 'Уникальный скин для профиля'},
    'multiplier1': {'name': '⚡ Множитель x2 на 1 час', 'price': 50, 'description': 'Увеличивает все выигрыши в 2 раза на час'},
    'krds10': {'name': '💎 10 KRDS', 'price': 30, 'description': 'Мгновенно получи 10 KRDS'}
}

@bot.message_handler(commands=['ивент'])
def event_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    if not RELEASE_EVENT['active'] or time.time() > RELEASE_EVENT['end_time']:
        bot.send_message(message.chat.id, "❌ Ивент не активен.", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    time_left = RELEASE_EVENT['end_time'] - time.time()
    
    text = (
        f"🎉 ** ИВЕНТ К 1 МАРТА ** 🎉\n\n"
        f"⏳ Осталось: {format_time(int(time_left))}\n"
        f"⚡ Множитель выигрышей: x{RELEASE_EVENT['multiplier']}\n"
        f"🎁 Твои ивентовые очки: {user.get('event_points', 0)}\n\n"
        f"📋 **Ивентовые квесты:**\n"
        f"🌸 Сыграть 5 игр с множителем - 5000 кредиксов\n\n"
        f"🛍 **Ивентовый магазин:**\n"
        f"/ивент_магазин"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['ивент_магазин'])
def event_shop_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    if not RELEASE_EVENT['active'] or time.time() > RELEASE_EVENT['end_time']:
        bot.send_message(message.chat.id, "❌ Ивент не активен.", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    text = f"🛍 ** ИВЕНТОВЫЙ МАГАЗИН **\nТвои очки: {user.get('event_points', 0)}\n\n"
    
    for item_id, item in EVENT_SHOP.items():
        text += f"{item['name']}\n"
        text += f"   {item['description']}\n"
        text += f"   💰 Цена: {item['price']} ивентовых очков\n"
        text += f"   /ивент_купить {item_id}\n\n"
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

@bot.message_handler(commands=['ивент_купить'])
def event_buy_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /ивент_купить [id]", parse_mode='Markdown')
        return
    
    item_id = args[1]
    if item_id not in EVENT_SHOP:
        bot.send_message(message.chat.id, "❌ Неверный ID предмета!", parse_mode='Markdown')
        return
    
    user = get_user(user_id)
    price = EVENT_SHOP[item_id]['price']
    
    if user.get('event_points', 0) < price:
        bot.send_message(message.chat.id, f"❌ Недостаточно ивентовых очков! Нужно: {price}", parse_mode='Markdown')
        return
    
    with get_user_lock(user_id):
        user['event_points'] -= price
        user.setdefault('event_purchases', []).append({
            'item': item_id,
            'time': time.time()
        })
        if item_id == 'krds10':
            user['krds_balance'] += 10
            save_data()
            bot.send_message(message.chat.id, f"✅ Ты купил 10 KRDS!", parse_mode='Markdown')
        elif item_id == 'multiplier1':
            user['temp_multiplier'] = {
                'mult': 2.0,
                'expires': time.time() + 3600
            }
            save_data()
            bot.send_message(message.chat.id, f"✅ Ты активировал множитель x2 на 1 час!", parse_mode='Markdown')
        elif item_id == 'skin1':
            save_data()
            bot.send_message(message.chat.id, f"✅ Ты купил скин! Он появится в твоём профиле.", parse_mode='Markdown')

def get_temp_multiplier(user_id):
    user = get_user(user_id)
    if user.get('temp_multiplier'):
        if time.time() < user['temp_multiplier']['expires']:
            return user['temp_multiplier']['mult']
        else:
            del user['temp_multiplier']
            save_data()
    return 1.0

def get_event_multiplier_ext(user_id):
    base = get_event_multiplier()
    temp = get_temp_multiplier(user_id)
    return base * temp

# ====================== ОБРАБОТЧИК ТЕКСТОВЫХ КОМАНД БЕЗ СЛЭША ======================
@bot.message_handler(func=lambda message: not message.text.startswith('/') and not message.text.startswith('!'))
def text_handler(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        return
    
    text = message.text.lower().strip()
    parts = text.split()
    if len(parts) < 1:
        return
    
    command = parts[0]
    args = ' '.join(parts[1:]) if len(parts) > 1 else ''
    
    cmd_map = {
        'башня': 'tower_command',
        'tower': 'tower_command',
        'футбол': 'football_command',
        'football': 'football_command',
        'баскетбол': 'basketball_command',
        'basketball': 'basketball_command',
        'дартс': 'darts_command',
        'darts': 'darts_command',
        'покер': 'poker_command',
        'poker': 'poker_command',
        'пирамида': 'pyramid_command',
        'pyramid': 'pyramid_command',
        'мины': 'mines_command',
        'mines': 'mines_command',
        'слоты': 'slots_command',
        'slots': 'slots_command',
        'рулетка_каз': 'roulette_command',
        'roulette': 'roulette_command',
        'хило': 'hilo_command',
        'hilo': 'hilo_command',
        'очко': 'blackjack_command',
        'blackjack': 'blackjack_command',
        'краш': 'crash_game',
        'crash': 'crash_game',
        'x2': 'multiplier_game',
        'x3': 'multiplier_game',
        'x5': 'multiplier_game',
        'фишки': 'chips_game',
        'chips': 'chips_game',
        'рулетка_рус': 'russian_roulette',
        'russian_roulette': 'russian_roulette',
        'джекпот': 'jackpot_game',
        'jackpot': 'jackpot_game',
        'кости': 'dice_game',
        'dice': 'dice_game',
        'работа': 'work_command',
        'work': 'work_command',
        'банк': 'bank_command',
        'bank': 'bank_command',
        'депозит': 'deposit_command',
        'снять': 'withdraw_command',
        'кредит': 'loan_command',
        'выплатить': 'repay_loan_command',
        'проценты': 'interest_command',
        'мышки': 'mice_command',
        'mice': 'mice_command',
        'купить_мышь': 'buy_mouse_command',
        'собрать_мышей': 'collect_mice_command',
        'питомцы': 'pets_command',
        'pets': 'pets_command',
        'магазин_питомцев': 'pet_shop_command',
        'купить_питомца': 'buy_pet_command',
        'покормить': 'feed_pet_command',
        'собрать_питомцы': 'collect_pets_command',
        'бизнес': 'business_command',
        'business': 'business_command',
        'магазин_бизнеса': 'business_shop_command',
        'купить_бизнес': 'buy_business_command',
        'улучшить': 'upgrade_business_command',
        'собрать_бизнес': 'collect_business_command',
        'квесты': 'quests_command',
        'quests': 'quests_command',
        'статистика': 'stats_command',
        'stats': 'stats_command',
        'топ': 'top_command',
        'баланс': 'balance_command',
        'вип': 'vip_command',
        'vip': 'vip_command',
        'купить_вип': 'buy_vip_command',
        'вип_крдс': 'vip_krds_command',
        'турнир': 'tournament_command',
        'турнир_вступить': 'tournament_join',
        'турнир_покинуть': 'tournament_leave',
        'донат': 'donate_command',
        'сенд': 'send_krds_command',
        'продать': 'sell_to_bot_command',
        'обменник': 'exchange_menu',
        'продатькрдс': 'sell_krds_command',
        'купитькрдс': 'buy_krds_command',
        'моиордера': 'my_orders_command',
        'ордера': 'all_orders_command',
        'отменитьордер': 'cancel_order_command',
        'реф': 'ref_command',
        'ref': 'ref_command',
        'дать': 'give_command',
        'give': 'give_command',
        'профиль': 'profile_command',
        'profile': 'profile_command',
        'отмена': 'cancel_game_command',
        'cancel': 'cancel_game_command',
        'старт': 'start_help',
        'start': 'start_help',
        'помощь': 'start_help',
        'help': 'start_help',
        'игры': 'games_command',
        'games': 'games_command',
        'телефон': 'phone_menu',
        'добавить_контакт': 'add_contact_command',
        'позвонить': 'call_command',
        'смс': 'sms_command',
        'микрозайм': 'microloan_command',
        'ивент': 'event_command',
        'ивент_магазин': 'event_shop_command',
        'ивент_купить': 'event_buy_command'
    }
    
    if command in cmd_map:
        func_name = cmd_map[command]
        func = globals().get(func_name)
        if func:
            fake_message = message
            fake_message.text = '/' + command + ' ' + args
            func(fake_message)

@bot.message_handler(commands=['игры', 'games'])
def games_command(message):
    user_id = str(message.from_user.id)
    if is_banned(user_id):
        bot.send_message(message.chat.id, "⛔ Вы забанены!", parse_mode='Markdown')
        return
    
    text = (
        "🎮 ** СПИСОК ИГР ** 🎮\n\n"
        "• /башня [ставка]\n"
        "• /футбол [ставка]\n"
        "• /баскетбол [ставка]\n"
        "• /дартс [ставка]\n"
        "• /покер [ставка]\n"
        "• /пирамида [ставка]\n"
        "• /мины [ставка]\n"
        "• /слоты [ставка]\n"
        "• /рулетка_каз [ставка] [тип] [число]\n"
        "• /хило [ставка]\n"
        "• /очко [ставка]\n"
        "• /краш [ставка]\n"
        "• /x2 [ставка]\n"
        "• /x3 [ставка]\n"
        "• /x5 [ставка]\n"
        "• /фишки [ставка] [black/white]\n"
        "• /рулетка_рус [ставка]\n"
        "• /джекпот [ставка]\n"
        "• /кости [ставка] [больше6/меньше6/чет/нечет]"
    )
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# ====================== АДМИН КОМАНДЫ ======================
@bot.message_handler(commands=['admin', 'Admin'])
def admin_login(message):
    user_id = str(message.from_user.id)
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /admin [пароль] или /Admin [пароль]", parse_mode='Markdown')
        return
    
    password_hash = hashlib.sha256(args[1].encode()).hexdigest()
    if password_hash == ADMIN_PASSWORD_HASH:
        admin_users.add(user_id)
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
            types.InlineKeyboardButton("💰 Выдать кредиксы", callback_data="admin_add_balance"),
            types.InlineKeyboardButton("💎 Выдать KRDS", callback_data="admin_add_krds"),
            types.InlineKeyboardButton("👑 Выдать VIP", callback_data="admin_add_vip"),
            types.InlineKeyboardButton("🚫 Забанить", callback_data="admin_ban"),
            types.InlineKeyboardButton("✅ Разбанить", callback_data="admin_unban"),
            types.InlineKeyboardButton("📢 Рассылка", callback_data="admin_mail"),
            types.InlineKeyboardButton("💾 Сохранить", callback_data="admin_save"),
            types.InlineKeyboardButton("🎉 Управление ивентом", callback_data="admin_event"),
            types.InlineKeyboardButton("📱 Телефон (выдать)", callback_data="admin_phone"),
            types.InlineKeyboardButton("🚪 Выход", callback_data="admin_exit")
        )
        
        bot.send_message(
            message.chat.id,
            "🔑 ** АДМИН ПАНЕЛЬ ** 🔑\n\n"
            f"👤 Администратор: {message.from_user.first_name}\n"
            f"🆔 ID: {user_id}\n\n"
            f"Выберите действие:",
            reply_markup=markup, parse_mode='Markdown'
        )
    else:
        bot.send_message(message.chat.id, "🔑❌ Неверный пароль!", parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: call.data.startswith('admin_'))
def admin_callback(call):
    user_id = str(call.from_user.id)
    if not is_admin(user_id):
        bot.answer_callback_query(call.id, "❌ У вас нет прав администратора!")
        return
    
    data = call.data
    
    if data == "admin_stats":
        with data_lock:
            total_users = len(users)
            total_balance = sum(u.get('balance', 0) for u in users.values())
            total_krds = sum(u.get('krds_balance', 0) for u in users.values())
            banned_count = sum(1 for u in users.values() if u.get('banned', False))
            vip_count = sum(1 for u in users.values() if u.get('vip_level') and u.get('vip_expires', 0) > time.time())
        
        text = (
            f"📊 ** СТАТИСТИКА БОТА **\n\n"
            f"👥 Пользователей: {total_users}\n"
            f"💰 Всего кредиксов: {format_number(total_balance)}\n"
            f"💎 Всего KRDS: {total_krds}\n"
            f"👑 VIP игроков: {vip_count}\n"
            f"⛔ Забанено: {banned_count}"
        )
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, parse_mode='Markdown')
        bot.answer_callback_query(call.id)
    
    elif data == "admin_exit":
        admin_users.remove(user_id)
        bot.edit_message_text(
            "👋 Вы вышли из режима администратора.",
            call.message.chat.id,
            call.message.message_id, parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_save":
        save_data()
        bot.answer_callback_query(call.id, "✅ Данные сохранены!")
    
    elif data == "admin_add_balance":
        bot.edit_message_text(
            "💰 ** Выдача кредиксов **\n\n"
            "Отправь команду:\n"
            "/addbalance @ник сумма",
            call.message.chat.id,
            call.message.message_id, parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_add_krds":
        bot.edit_message_text(
            "💎 ** Выдача KRDS **\n\n"
            "Отправь команду:\n"
            "/addkrds @ник сумма",
            call.message.chat.id,
            call.message.message_id, parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_add_vip":
        bot.edit_message_text(
            "👑 ** Выдача VIP **\n\n"
            "Отправь команду:\n"
            "/addvip @ник уровень\n"
            "Уровни: bronze, silver, gold, platinum",
            call.message.chat.id,
            call.message.message_id, parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_ban":
        bot.edit_message_text(
            "🚫 ** Бан пользователя **\n\n"
            "Отправь команду:\n"
            "/ban @ник",
            call.message.chat.id,
            call.message.message_id, parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_unban":
        bot.edit_message_text(
            "✅ ** Разбан пользователя **\n\n"
            "Отправь команду:\n"
            "/unban @ник",
            call.message.chat.id,
            call.message.message_id, parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_event":
        bot.edit_message_text(
            "🎉 ** Управление ивентом **\n\n"
            "Команды:\n"
            "/event_start [множитель] [длительность_дней] - запустить ивент\n"
            "/event_stop - остановить ивент\n"
            "/event_add_points @ник количество - добавить ивентовые очки",
            call.message.chat.id,
            call.message.message_id, parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)
    
    elif data == "admin_phone":
        bot.edit_message_text(
            "📱 ** Управление телефоном **\n\n"
            "Команды:\n"
            "/add_contact @ник - добавить контакт админу\n"
            "/send_sms @ник текст - отправить смс от имени админа",
            call.message.chat.id,
            call.message.message_id, parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id)

@bot.message_handler(commands=['addbalance'])
def admin_add_balance(message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ У вас нет прав администратора!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, "❌ Использование: /addbalance @ник сумма", parse_mode='Markdown')
        return
    
    target_username = args[1].replace('@', '').lower()
    try:
        amount = int(args[2])
        if amount <= 0:
            bot.send_message(message.chat.id, "❌ Сумма должна быть положительной!", parse_mode='Markdown')
            return
    except ValueError:
        bot.send_message(message.chat.id, "❌ Введите число!", parse_mode='Markdown')
        return
    
    with data_lock:
        target_id = username_cache.get(target_username)
        if not target_id:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!", parse_mode='Markdown')
            return
        
        with get_user_lock(target_id):
            users[target_id]['balance'] += amount
            save_data()
    
    bot.send_message(message.chat.id, f"➕✅ Пользователю @{target_username} начислено {format_number(amount)} кредиксов.", parse_mode='Markdown')

@bot.message_handler(commands=['addkrds'])
def admin_add_krds(message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ У вас нет прав администратора!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, "❌ Использование: /addkrds @ник сумма", parse_mode='Markdown')
        return
    
    target_username = args[1].replace('@', '').lower()
    try:
        amount = int(args[2])
        if amount <= 0:
            bot.send_message(message.chat.id, "❌ Сумма должна быть положительной!", parse_mode='Markdown')
            return
    except ValueError:
        bot.send_message(message.chat.id, "❌ Введите число!", parse_mode='Markdown')
        return
    
    with data_lock:
        target_id = username_cache.get(target_username)
        if not target_id:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!", parse_mode='Markdown')
            return
        
        with get_user_lock(target_id):
            users[target_id]['krds_balance'] += amount
            save_data()
    
    bot.send_message(message.chat.id, f"💎✅ Пользователю @{target_username} начислено {amount} KRDS.", parse_mode='Markdown')

@bot.message_handler(commands=['addvip'])
def admin_add_vip(message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ У вас нет прав администратора!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, "❌ Использование: /addvip @ник уровень", parse_mode='Markdown')
        return
    
    target_username = args[1].replace('@', '').lower()
    level = args[2].lower()
    
    if level not in VIP_LEVELS:
        bot.send_message(message.chat.id, "❌ Неверный уровень! Доступно: bronze, silver, gold, platinum", parse_mode='Markdown')
        return
    
    with data_lock:
        target_id = username_cache.get(target_username)
        if not target_id:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!", parse_mode='Markdown')
            return
        
        with get_user_lock(target_id):
            users[target_id]['vip_level'] = level
            users[target_id]['vip_expires'] = time.time() + VIP_LEVELS[level]['duration']
            users[target_id]['vip_last_krds_claim'] = time.time()
            generate_daily_quests(target_id)
            save_data()
    
    bot.send_message(message.chat.id, f"👑✅ Пользователю @{target_username} выдан {VIP_LEVELS[level]['name']} VIP на 30 дней!", parse_mode='Markdown')

@bot.message_handler(commands=['ban'])
def admin_ban(message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ У вас нет прав администратора!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /ban @ник", parse_mode='Markdown')
        return
    
    target_username = args[1].replace('@', '').lower()
    
    with data_lock:
        target_id = username_cache.get(target_username)
        if not target_id:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!", parse_mode='Markdown')
            return
        
        if target_id == user_id:
            bot.send_message(message.chat.id, "❌ Нельзя забанить самого себя!", parse_mode='Markdown')
            return
        
        with get_user_lock(target_id):
            users[target_id]['banned'] = True
            save_data()
    
    bot.send_message(message.chat.id, f"🔨✅ Пользователь @{target_username} забанен.", parse_mode='Markdown')

@bot.message_handler(commands=['unban'])
def admin_unban(message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ У вас нет прав администратора!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 2:
        bot.send_message(message.chat.id, "❌ Использование: /unban @ник", parse_mode='Markdown')
        return
    
    target_username = args[1].replace('@', '').lower()
    
    with data_lock:
        target_id = username_cache.get(target_username)
        if not target_id:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!", parse_mode='Markdown')
            return
        
        with get_user_lock(target_id):
            users[target_id]['banned'] = False
            save_data()
    
    bot.send_message(message.chat.id, f"✅ Пользователь @{target_username} разбанен.", parse_mode='Markdown')

@bot.message_handler(commands=['event_start'])
def admin_event_start(message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ У вас нет прав администратора!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, "❌ Использование: /event_start [множитель] [дней]", parse_mode='Markdown')
        return
    
    try:
        mult = float(args[1])
        days = int(args[2])
        if mult <= 0 or days <= 0:
            bot.send_message(message.chat.id, "❌ Множитель и дни должны быть положительными!", parse_mode='Markdown')
            return
    except ValueError:
        bot.send_message(message.chat.id, "❌ Введите числа!", parse_mode='Markdown')
        return
    
    global RELEASE_EVENT
    RELEASE_EVENT['active'] = True
    RELEASE_EVENT['multiplier'] = mult
    RELEASE_EVENT['end_time'] = time.time() + days * 86400
    
    with data_lock:
        with open(EVENT_FILE, 'w', encoding='utf-8') as f:
            json.dump(RELEASE_EVENT, f, ensure_ascii=False, indent=2)
    
    bot.send_message(message.chat.id, f"🎉 Ивент запущен! Множитель x{mult}, длительность {days} дней.", parse_mode='Markdown')

@bot.message_handler(commands=['event_stop'])
def admin_event_stop(message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ У вас нет прав администратора!", parse_mode='Markdown')
        return
    
    global RELEASE_EVENT
    RELEASE_EVENT['active'] = False
    with data_lock:
        with open(EVENT_FILE, 'w', encoding='utf-8') as f:
            json.dump(RELEASE_EVENT, f, ensure_ascii=False, indent=2)
    
    bot.send_message(message.chat.id, "🛑 Ивент остановлен.", parse_mode='Markdown')

@bot.message_handler(commands=['event_add_points'])
def admin_event_add_points(message):
    user_id = str(message.from_user.id)
    if not is_admin(user_id):
        bot.send_message(message.chat.id, "❌ У вас нет прав администратора!", parse_mode='Markdown')
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.send_message(message.chat.id, "❌ Использование: /event_add_points @ник количество", parse_mode='Markdown')
        return
    
    target_username = args[1].replace('@', '').lower()
    try:
        points = int(args[2])
        if points <= 0:
            bot.send_message(message.chat.id, "❌ Количество должно быть положительным!", parse_mode='Markdown')
            return
    except ValueError:
        bot.send_message(message.chat.id, "❌ Введите число!", parse_mode='Markdown')
        return
    
    with data_lock:
        target_id = username_cache.get(target_username)
        if not target_id:
            bot.send_message(message.chat.id, "❌ Пользователь не найден!", parse_mode='Markdown')
            return
        
        with get_user_lock(target_id):
            users[target_id]['event_points'] = users[target_id].get('event_points', 0) + points
            save_data()
    
    bot.send_message(message.chat.id, f"✅ Пользователю @{target_username} добавлено {points} ивентовых очков.", parse_mode='Markdown')

# ====================== ЗАПУСК БОТА ======================
def signal_handler(sig, frame):
    print("\n🛑 Остановка бота...")
    cleanup_all_timers()
    save_data()
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    load_data()
    init_tournaments()
    start_tournament_checker()
    
    loan_checker = Thread(target=check_microloans, daemon=True)
    loan_checker.start()
    
    print("=" * 60)
    print("✅ БОТ  ЗАПУЩЕН!")
    print("=" * 60)
    print("📋 СИСТЕМЫ:")
    print("  • 🎮 Все игры")
    print("  • 👑 VIP система")
    print("  • 📋 Ежедневные квесты + ивент")
    print("  • 🏆 Турниры")
    print("  • 💎 KRDS и P2P обменник")
    print("  • 📊 Статистика и топ")
    print("  • 🐭 Мышки, 🐾 Питомцы, 🏪 Бизнес")
    print("  • 🏦 Банк (депозиты, кредиты)")
    print("  • 👥 Рефералы")
    print("  • 📱 Телефон (контакты, звонки, СМС, микрозаймы)")
    print("  • 🎉 Ивент с магазином")
    print("=" * 60)
    print("🎮 ИГРЫ (можно без /):")
    print("  • башня, футбол, баскетбол, дартс, покер")
    print("  • пирамида, мины, слоты, рулетка_каз, хило")
    print("  • очко, краш, x2/x3/x5, фишки")
    print("  • русская рулетка, джекпот, кости")
    print("=" * 60)
    print("📌 Форматы ставок: 1к = 1000, 1кк/1ку = 1,000,000")
    print("=" * 60)
    print("🔑 АДМИН ПАНЕЛЬ: /admin Kyniksvs1832 или /Admin Kyniksvs1832")
    print("=" * 60)
    print("🛑 Для остановки нажмите Ctrl+C")
    
    try:
        bot.infinity_polling()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        cleanup_all_timers()
        save_data()
