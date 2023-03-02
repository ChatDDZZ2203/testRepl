import os
import time
from functions_replicate import RepliGate
import telebot
from flask import Flask, request

TOKENS = [os.getenv("TG_TOKEN"), os.getenv("RE_TOKEN")]
ADMIN_IDS = [652015662, 5412948297]
bot = telebot.TeleBot(TOKENS[0])
app = Flask(__name__)
TIMES_DONE = [0]

@app.before_request
def abuse_api_token():
    if request.headers.get('content-type') == "application/json":
        update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
        if update.message.from_user.id in ADMIN_IDS:
            bot.process_new_updates([update])
    return ""


@bot.message_handler(commands=["set_token"])
def set_api_re_token(m):
    TOKENS[1] = m.text[11:]
    bot.send_message(m.chat.id,
                     f"Setting repl token\n{m.text[11:]}...")

@bot.message_handler(commands=["abuse"])
def zu_abusen(m):
    prompt = m.text[7:]
    image_urls = []
    repclient = RepliGate(TOKENS[1])
    try:
        while True:
            bot.send_message(m.chat.id,
                             f"Starting generate \n{prompt}")
            for i in range(10):
                try:
                    image_urls = repclient.get_image_waifu_diffusion(
                        prompt=prompt,
                        negative_prompt="lowres, bad anatomy hands, text, "
                                        "error, missing fingers, extra digit, fewer digits, "
                                        "cropped, worst quality, low quality, normal quality, "
                                        "jpeg artifacts, signature, watermark, username",
                        width=512, height=768, prompt_strength=None, num_outputs=4, num_inference_steps=10,
                        guidance_scale=12, scheduler=None, seed=None
                    )
                    break
                except Exception as e:
                    bot.send_message(m.chat.id,
                                     f"Some error when getting response:\n{str(e)}")
                    if "NSFW" not in str(e):
                        break

            bot.send_message(m.chat.id,
                             f"Got {len(image_urls)} image(s)")

            for image_url in image_urls:
                upscaled_image_url = repclient.upscale_image_real_esrgan(image_url, 3, True)
                try:
                    bot.send_photo(os.getenv("MAIN_USERNAME"), photo=upscaled_image_url,
                                   caption=f"Upscaled image\n<code>{prompt}</code>"
                                           f'\n\n<a href="{upscaled_image_url}">Url to use as reference</a>\n\n'
                                           f'by <a href="tg://user?id=652015662">AUniqD</a>',
                                   parse_mode="html")
                except Exception as e:
                    if "Bad Request" in str(e):
                        bot.send_message(m.chat.id,
                                         "fucked")
                    else:
                        bot.send_message(m.chat.id,
                                         f"Some interesting error in for image_url:\n\n{str(e)}")

            time.sleep(1000)
            TIMES_DONE[0] += 1

    except Exception as e:
        if "You have reached the free time limit" in str(e):
            bot.send_message(m.chat.id,
                             f"That`s it. Statistics:\nRolled {TIMES_DONE[0]} times")
        else:
            bot.send_message(m.chat.id,
                             f"Some interesting general error:\n\n{str(e)}")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 3000)))



