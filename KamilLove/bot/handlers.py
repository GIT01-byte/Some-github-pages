from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Импортируем настройки, если они нужны для кабинета
from config import settings

router = Router()

# СЮДА ВСТАВЬТЕ ID КАМИЛЯ В ТЕЛЕГРАМЕ (число)
ADMIN_ID = 6250684956


# ==========================================
# КЛАВИАТУРЫ ДЛЯ ЛИЧНОГО КАБИНЕТА
# ==========================================
def get_cabinet_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text="👤 Мой профиль", callback_data="cabinet_profile")
    builder.button(text="⚙️ Настройки", callback_data="cabinet_settings")
    builder.button(text="📩 Обратная связь", callback_data="cabinet_feedback")
    builder.adjust(1)
    return builder.as_markup()


# ==========================================
# ОБРАБОТЧИКИ КОМАНД И КНОПОК
# ==========================================
@router.message(CommandStart())
async def cmd_start(message: Message):
    """Приветствие и вход в личный кабинет."""
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        f"Добро пожаловать в личный кабинет.\n\n"
        f"Выберите нужный раздел ниже:",
        reply_markup=get_cabinet_kb(),
    )


@router.callback_query(F.data == "cabinet_profile")
async def show_profile(callback: CallbackQuery):
    profile_text = (
        "👤 <b>Ваш профиль</b>\n\n"
        f"🆔 ID: <code>{callback.from_user.id}</code>\n"
        f"📛 Имя: {callback.from_user.first_name}\n"
        f"🔗 Username: @{callback.from_user.username or 'не указан'}\n\n"
        "Статус: <b>Красавчик</b> 😎"
    )
    await callback.message.edit_text(profile_text, reply_markup=get_cabinet_kb())
    await callback.answer()


@router.callback_query(F.data == "cabinet_settings")
async def show_settings(callback: CallbackQuery):
    settings_text = (
        "⚙️ <b>Настройки</b>\n\n" "Здесь скоро появятся настройки уведомлений."
    )
    await callback.message.edit_text(settings_text, reply_markup=get_cabinet_kb())
    await callback.answer()


@router.callback_query(F.data == "cabinet_feedback")
async def show_feedback(callback: CallbackQuery):
    feedback_text = (
        "📩 <b>Обратная связь</b>\n\n"
        "Просто напиши сообщение прямо в этот чат, и оно улетит админу!"
    )
    await callback.message.edit_text(feedback_text, reply_markup=get_cabinet_kb())
    await callback.answer()


# ==========================================
# ОТПРАВКА СООБЩЕНИЙ АДМИНУ (В ВИДЕ ЦИТАТЫ)
# ==========================================
@router.message(F.text)
async def handle_text(message: Message):
    """Ловим сообщение и отправляем Камилю в виде цитаты."""

    # Формируем текст для админа (имитация как на скрине)
    admin_text = (
        f"Переслано от <b>{message.from_user.first_name}</b>\n"
        f"У тебя новое сообщение!\n\n"
        # Тег blockquote создает ту самую полоску-цитату слева
        f"<blockquote>{message.text}</blockquote>"
    )

    try:
        # Отправляем сообщение Админу
        await message.bot.send_message(
            chat_id=ADMIN_ID,
            text=admin_text,
            parse_mode="HTML",  # Обязательно, чтобы сработали теги <b> и <blockquote>
        )

        # Отвечаем пользователю, что всё отправлено
        await message.answer(
            "✅ Сообщение отправлено Камилю!",
            reply_markup=get_cabinet_kb(),
        )
    except Exception as e:
        # Если Камиль не нажал /start у бота, бот не сможет ему написать
        await message.answer(
            "❌ Ошибка. Админ еще не нажал /start у бота, поэтому я не могу ему написать.",
            reply_markup=get_cabinet_kb(),
        )
