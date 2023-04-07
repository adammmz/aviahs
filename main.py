from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import folium

import pickle
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from scikeras.wrappers import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import ezgiphy
import json

import util

filename = 'model-7.sav'

model = pickle.load(open(filename, 'rb'))
giphy = ezgiphy.GiphyPublicAPI('CeWSgXDroTo326aSJZoNOtSi3IMvDJRc')


def create_map(name, start="ATL", end="CVG"):
    # Create a map centered on the United States
    flight_map = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

    start_latlng = util.locs_cord[start]['coords']
    end_latlng = util.locs_cord[end]['coords']
    # Draw the starting and ending airports as red circles
    folium.CircleMarker(location=start_latlng, radius=5, color='red', fill=True, fill_color='red',
                        fill_opacity=0.6, popup=start).add_to(flight_map)
    folium.CircleMarker(location=end_latlng, radius=5, color='red', fill=True, fill_color='red',
                        fill_opacity=0.6, popup=end).add_to(flight_map)

    # Draw the flight path as a blue line
    folium.PolyLine(locations=[list(start_latlng), list(end_latlng)], color='blue', weight=2, opacity=1).add_to(
        flight_map)

    # Display the map
    flight_map.save('output.html')


# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!"
        f"\n\nType:\n" +
        f"DAY_OF_WEEK: MON, TUE, WED...\n" +
        f"DEP_TIME: HH:MM\n" +
        f"ARR_TIME: HH:MM\n" +
        f"ORIGIN: Airport name like LAX, JFK, SHR, etc.\n" +
        f"DESTINATION: Airport name\n\n\nExample: MON 15:00 LWS COD",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    inp = update.message.text.split()

    inp[1] = inp[1].replace(':', '')
    inp[2] = inp[2].replace(':', '')
    df_ = pd.DataFrame(
        [[
            util.days[str.upper(inp[0])],
            int(inp[1]),
            util.locs[inp[2]],
            util.locs[inp[3]]
        ]],
        columns=['DAY_OF_WEEK', 'DEP_TIME',
                 'ORIGIN', 'DEST'])

    if util.locs[inp[2]] is None or util.locs[inp[3]] is None:
        await update.message.reply_text("This airport does not exist")
    else:
        pr = model.predict(df_)
        val = (int(pr[0]))

        if val == 1:
            url = json.loads(giphy.random(tag='laugh', rating='g'))['data']['url']
            await update.message.reply_text(

                "Your flight will probably be delayed\n" + url)
        else:
            url = json.loads(giphy.random(tag='great', rating='g'))['data']['url']
            await update.message.reply_text(
                "Your flight probably will not be delayed!\n" + url)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5851745353:AAFieExrFoAXNOUHDOA7Ic6s3n7q_ObaTTY").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, predict))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
