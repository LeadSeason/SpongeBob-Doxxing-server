from sanic import Sanic
from sanic import response as res

from os.path import isfile
from PIL import Image
from PIL import ImageFont, ImageDraw

app = Sanic(__name__)


async def gen_img(ip):
    """
        Adds the ip to the image for funny laughs
    """
    text = str(ip)
    print(f"Genarating File for {ip}")
    file_path = f"Images/{text}.jpg"
    # Image Size
    width = 800
    height = 450

    img = Image.open("SpongeBob-Doxxing.jpg")
    font = ImageFont.truetype("FreeSans.otf", 100)
    draw = ImageDraw.Draw(img)
    w, h = draw.textsize(text, font=font)
    h += int(h * 0.21)
    draw.text(((width - w) / 2, (height - h) / 2), text=text, fill=0, font=font)
    img.save(file_path)
    return file_path


@app.route("/api/img")
async def img_api(req):
    text = str(req.ip)
    if isfile(f"Images/{text}.jpg"):
        return await res.file(f"Images/{text}.jpg")
    else:
        response_file = await gen_img(req.ip)
        return await res.file(response_file)


@app.route("/")
async def root(req):
    return await res.file("src/index.html")


@app.route("/favicon.ico")
async def favicon(req):
    return await res.file("src/favicon.ico")


@app.route("/robots.txt")
async def robots(req):
    return await res.file("src/robots.txt")


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
