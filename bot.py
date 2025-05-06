import pandas as pd
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from aiogram.types import ReplyKeyboardRemove

# Конфиг
TOKEN = "7904008623:AAGQPJ5Mj9lgw8sW4kMYq24uwhJlBui2cA4"
EXCEL_FILE = "data.xlsx"  # Путь к Excel-файлу

# Загружаем данные из Excel
def load_data():
    return pd.read_excel(EXCEL_FILE)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Отправь номер, и я найду данные из таблицы.",
    )

# Поиск данных по номеру
async def find_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text.strip()
    df = load_data()

    # Предполагаем, что в таблице есть столбец 'ID'
    if "ID" not in df.columns:
        await update.message.reply_text("❌ В таблице нет столбца 'ID'!")
        return

    # Ищем введённый номер
    result = df[df["ID"].astype(str) == user_input]

    if not result.empty:
        response = "\n".join([f"{col}: {val}" for col, val in result.iloc[0].items()])
        await update.message.reply_text(f"🔍 Найдено:\n{response}")
    else:
        await update.message.reply_text("❌ Данные не найдены!")

# Запуск бота
if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, find_data))

    print("Бот запущен!")
    app.run_polling()
