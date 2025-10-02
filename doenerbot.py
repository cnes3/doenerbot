import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from export_gsheet import export_review
import gettext

gettext.bindtextdomain("messages", "locales")
gettext.textdomain("messages")
_ = gettext.gettext


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# GENDER, PHOTO, LOCATION, BIO = range(4)
LOCATION, PRICE, SIZE, TASTE, FRESHNESS, MEAT, SAUCE, SERVICE, WAITTIME, SPECIAL, TOTAL = range(11)   

star_rating_reply_keyboard = [["1", "2", "3", "4", "5"]]
numpad_reply_keyboard = [
    ["7", "8", "9"],
    ["4", "5", "6"],
    ["1", "2", "3"]
]
numpad_float_reply_keyboard = numpad_reply_keyboard.append(["", "0", "."])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    

    await update.message.reply_text(_(
        "Hi! Let's start rating your Döner. Where did you eat it??"),
        reply_markup=ReplyKeyboardRemove(),
    )

    return LOCATION


# async def gender(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Stores the selected gender and asks for a photo."""
#     user = update.message.from_user
#     logger.info("Gender of %s: %s", user.first_name, update.message.text)
#     await update.message.reply_text(
#         "I see! Please send me a photo of yourself, "
#         "so I know what you look like, or send /skip if you don't want to.",
#         reply_markup=ReplyKeyboardRemove(),
#     )

#     return PHOTO


# async def photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Stores the photo and asks for a location."""
#     user = update.message.from_user
#     photo_file = await update.message.photo[-1].get_file()
#     await photo_file.download_to_drive("user_photo.jpg")
#     logger.info("Photo of %s: %s", user.first_name, "user_photo.jpg")
#     await update.message.reply_text(
#         "Gorgeous! Now, send me your location please, or send /skip if you don't want to."
#     )

#     return LOCATION


# async def skip_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Skips the photo and asks for a location."""
#     user = update.message.from_user
#     logger.info("User %s did not send a photo.", user.first_name)
#     await update.message.reply_text(
#         "I bet you look great! Now, send me your location please, or send /skip."
#     )

#     return LOCATION


async def location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    logger.info(numpad_float_reply_keyboard)
    await update.message.reply_text(_("How expensive was it?"), reply_markup=ReplyKeyboardMarkup(numpad_float_reply_keyboard, one_time_keyboard=True))

    return PRICE

async def abstract_1_10_question(update: Update, context: ContextTypes.DEFAULT_TYPE, current_answer, next_question, return_value) -> int:
    user = update.message.from_user
    answer_value = update.message.text
    logger.info(f"{current_answer} of {user}'s the doener was {answer_value}")
    await update.message.reply_text(_("How was the {next_question} (1-10)?"), reply_markup=ReplyKeyboardMarkup(numpad_reply_keyboard, one_time_keyboard=True))
    return return_value

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return abstract_1_10_question(Update, context, "Price", "Size", SIZE)

async def size(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return abstract_1_10_question(Update, context, "Size", "Taste", TASTE)

async def taste(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return abstract_1_10_question(Update, context, "Taste", "Freshness", FRESHNESS)

async def freshness(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return abstract_1_10_question(Update, context, "Freshness", "Meat", MEAT)

async def meat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return abstract_1_10_question(Update, context, "Meat", "Sauce", SAUCE)

async def sauce(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return abstract_1_10_question(Update, context, "Sauce", "Service", SERVICE)

async def service(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return abstract_1_10_question(Update, context, "Service", "Waittime", WAITTIME)

async def waittime(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    answer_value = update.message.text
    logger.info(f"Waittime of {user}'s the doener was {answer_value}")
    await update.message.reply_text(_("Was there anything special about this Doener?"))
    return SPECIAL

async def special(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    answer_value = update.message.text
    logger.info(f"The special thing about {user}'s the doener was: {answer_value}")
    await update.message.reply_text(_("How would you rank this Doener in general?"), ReplyKeyboardMarkup(star_rating_reply_keyboard, one_time_keyboard=True))
    return TOTAL

async def total(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int: 
    user = update.message.from_user
    answer_value = update.message.text
    logger.info(f"The total review of {user}'s the doener was: {answer_value}")
    await update.message.reply_text(_("Thank you for reviewing this Doener"), reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

# async def skip_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Skips the location and asks for info about the user."""
#     user = update.message.from_user
#     logger.info("User %s did not send a location.", user.first_name)
#     await update.message.reply_text(
#         "You seem a bit paranoid! At last, tell me something about yourself."
#     )

#     return BIO


# async def bio(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Stores the info about the user and ends the conversation."""
#     user = update.message.from_user
#     logger.info("Bio of %s: %s", user.first_name, update.message.text)
#     await update.message.reply_text("Thank you! I hope we can talk again some day.")

#     return ConversationHandler.END


# async def date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
#     """Stores the info about the user and ends the conversation."""
#     user = update.message.from_user
#     logger.info("Date of the Purchase %s: %s", user.first_name, update.message.text)
#     await update.message.reply_text("Thank you! I hope we can talk again some day.")

#     return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(_(
        "Bye! I hope we can talk again some day."), reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    with open("bottoken.txt", "r") as f:
        token = f.read();
    application = Application.builder().token(token).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            # Use case-insensitive regex to accept gender input regardless of letter casing,
            # e.g., "boy", "BOY", "Girl", etc., will all be matched
            # DATE: [MessageHandler(filters.TEXT, date)]
            # GENDER: [MessageHandler(filters.Regex("(?i)^(Boy|Girl|Other)$"), gender)],
            # PHOTO: [MessageHandler(filters.PHOTO, photo), CommandHandler("skip", skip_photo)],
            LOCATION: [
                MessageHandler(filters.LOCATION, location),
                # CommandHandler("skip", skip_location),
            ],
            PRICE: [MessageHandler(filters.Regex("^\\d{1,2}([.]\\d{1,2})?$"), price)],
            SIZE: [MessageHandler(filters.Regex("^10|\\d$"), size)],
            TASTE: [MessageHandler(filters.Regex("^10|\\d$"), taste)],
            FRESHNESS: [MessageHandler(filters.Regex("^10|\\d$"), freshness)],
            MEAT: [MessageHandler(filters.Regex("^10|\\d$"), meat)],
            SAUCE: [MessageHandler(filters.Regex("^10|\\d$"), sauce)],
            SERVICE: [MessageHandler(filters.Regex("^10|\\d$"), service)],
            WAITTIME: [MessageHandler(filters.Regex("^10|\\d$"), waittime)],
            SPECIAL: [MessageHandler(filters.TEXT, special)],
            TOTAL: [MessageHandler(filters.TEXT, total)],
            # BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()