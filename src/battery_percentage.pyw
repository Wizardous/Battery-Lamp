import threading
import time
import psutil
import sys

from PIL import Image, ImageDraw, ImageFont
import pystray


def battery_info() -> tuple:
    battery = psutil.sensors_battery()
    return (battery.percent, battery.power_plugged)


# A function to create an image with a percent argument in the center in white color 
# and balck background. If the number is less than 20 the foreground color will be red.
# If the charging status param is true, then the image will have a green border.
def create_image(width, height, percent, charging_status):
    image = Image.new('RGB', (width, height), (0, 0, 0))
    dc = ImageDraw.Draw(image)

    if charging_status:
        dc.rectangle([(0, 0), (width, height)], outline='green', width=5)

    font_color = "red" if percent <= 20 else "white"
    font_size = 35 if percent==100 else 40
    font = ImageFont.truetype('consola.ttf', font_size)
    dc.text((width//2, height//2), str(percent), fill=font_color, font=font, anchor='mm')
    return image


def exit_action(icon):
    # print("Exiting...")
    icon.visible = False
    icon.stop()


def update_icon():
    while True:
        battery_level, plugged_status = battery_info()
        # print(f"{time.strftime('%H:%M:%S')} - Battery: {battery_level}%, Plugged: {plugged_status}")
        new_image = create_image(64, 64, battery_level, plugged_status)
        icon.icon = new_image
        time.sleep(1)


if __name__ == "__main__":
    battery_level, plugged_status = battery_info()

    icon = pystray.Icon("Battery Status")
    icon.menu = pystray.Menu(
        pystray.MenuItem('Exit', lambda: exit_action(icon))
    )

    update_thread = threading.Thread(target=update_icon)
    update_thread.daemon = True
    update_thread.start()

    icon.run()
