from PIL import Image

asset = Image.open("Assets.png")

for y in range(25):
    for x in range(25):
        croped = asset.crop((x*16, y*16, x*16+16, y*16+16))
        croped.save(f"{x}_{y}.png")
