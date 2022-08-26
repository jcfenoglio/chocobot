
### KWEH ###

from telegram.ext import Updater, Filters, CommandHandler, MessageHandler, InlineQueryHandler, CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineQueryResultArticle, InputTextMessageContent
import random

birdBrain = False
kwehwark = ["Kweh!", "Wark!", "Such a dumb chocobo!", "Kweh kweh~", "Aren't you a silly bird~", "Is that really all you can say?~", "Someone's a dumb little chocobo arent they~", "That's a good chocobo! Wark!", "Just a dumb chocobo! Kweh~~", "I bet it's so hard not to respond isn't it cutie?~ Kweh!", "That's right, sink deep and Wark!", "So hard, easier to give in!", "Kweh wark wark kweh I'm a silly chocobo~", "Just sit and stare and kweh", "Wark wark kweh kweh brain full of chocobo feathers~", "Say it loud and proud!", "Chocobo nice and deep~", "Sinking deep wings heavy just want to wark and kweh", "Its so addicting and easy~", "Why not just be a chocobo forever? Kweh~", "I've never been anything but a chocobo! Kweh!", "Aren't you such a pretty birdy~", "Wark kweh kweh wark, I'm a mindless chocobo!", "Kweh and wark and sink and be a good chocobo~", "Sinking deep feathery wings and chocobo beak need to wark and kweh", "So fun to become an empty bird brained kweh~", "Kweh and sink!", "Empty chocobo wark and kweh"]

kweh_wark_trilling = ["kweh", "wark", "kweh", "wark", "kweh", "wark", "trrl"]

kweh_wark = ["kweh", "wark"]


def brainDrain(update, context):
    """Sends a message with inline buttons attached."""
    keyboard = [
        [
            "Wark!",
            "Kweh!",
        ],
        ["I'm a good chocobo! Kweh!"],
        ["Wark! I love being a chocobo!"],
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard)

    update.message.reply_text('Dumb Chocobo Says', reply_markup=reply_markup)


def wakeMeUp(update, context):
	reply_nokeyboard = ReplyKeyboardRemove(selective = True)
	
	username = update.message.from_user.username
	update.message.reply_text('@' + username + ', up! Time to wake up pretty chocobo~\nClear off the extra feathers and come all the way up now, chocobo.', reply_markup = reply_nokeyboard)


def selectRandomNoise():
	return random.choice(kwehwark)


def findChocoNoise(m, st):
	for word in m.split(" "):
		target = len(st)
		for c in st:
			if word.find(c) != -1:
				target = target - 1
		if target == 0:
			return True
	return False


def chocoTranslate(st, list) -> str:
	translated = ""
	for word in st.split(" "):
		if len(word) < 1:
			pass
		elif len(word) <= 4:
			translated += random.choice(list)
			translated += " "
		else:
			noise = random.choice(list)
			repetitions = random.randrange(len(word) // 4) + 1
			position = random.randrange(repetitions)

			translated += position * noise
			translated += noiseExtender(len(word) - 4 * repetitions, noise)
			translated += (repetitions - position - 1) * noise
			translated += " "
	return translated


def noiseExtender(lettersAdded, word) -> str:
	if word == 'kweh':
		return 'kweh' + lettersAdded * 'h'
	elif word == 'wark':
		return 'war' + lettersAdded * 'r' + 'k'
	elif word == 'trrl':
		return 'tr' + lettersAdded * 'r' + 'rl'
	else:
		return word


def textHandle(update, context):
	message = update.message
	not_handled = True
	global birdBrain
	if findChocoNoise(message.text.lower(), "kweh") or findChocoNoise(message.text.lower(), "wark"):
		if random.randrange(100) <= 15:
			message.reply_text(selectRandomNoise())
		not_handled = False
	if message.text.lower().find("drain") != -1 or message.text.lower().find("brain") != -1:
		birdBrain = True
		brainDrain(update, context)
		not_handled = False
	if message.text.lower().find("wake") != -1 and not_handled:
		birdBrain = False
		wakeMeUp(update, context)
		not_handled = False
	if birdBrain and not_handled:
		message.delete()


def inlineQueryHandle(update, context):
	query = update.inline_query.query

	if query == '':
		return

	results_list = list()
	results_list.append(InlineQueryResultArticle(
		id=1,
		title="Be a good chocobo.",
		input_message_content=InputTextMessageContent(message_text=chocoTranslate(query, kweh_wark_trilling))
	))

	context.bot.answer_inline_query(update.inline_query.id, results=results_list, is_personal=True)


def loadKey():
	with open("./key.txt") as file:
		return file.readline().strip()


def main():
	key = loadKey()
	updater = Updater(key)
	dispatcher = updater.dispatcher

	dispatcher.add_handler(MessageHandler(Filters.text, textHandle))
	dispatcher.add_handler(InlineQueryHandler(inlineQueryHandle))
	print("starting bot...")
	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()
