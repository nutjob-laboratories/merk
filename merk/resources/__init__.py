
# Load in resource file
globals()["merk.resources.resources"] = __import__("merk.resources.resources")

# Load in major and minor version
f = open("./merk/data/major.txt","r")
major = f.read()
f.close()

f = open("./merk/data/minor.txt","r")
minor = f.read()
f.close()

# Format minor version so it is always
# at least three digits long
if len(minor)==1:
	minor = f"00{minor}"
elif len(minor)==2:
	minor = f"0{minor}"

APPLICATION_VERSION = major+"."+minor
APPLICATION_NAME = "mƏrk"

MDI_BACKGROUND = ":/gui-background.png"

BUNDLED_FONT = ":/font-FiraMono-Regular.ttf"
OTHER_BUNDLED_FONTS = [
	":/font-FiraMono-Medium.ttf",
	":/font-FiraMono-Bold.ttf",
]
BUNDLED_FONT_SIZE = 9

# Icons

APPLICATION_ICON = ":/icon-app.png"