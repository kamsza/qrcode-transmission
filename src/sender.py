from qrGenerator import generate
from qrGUI import show
from cleaner import clean
import easygui

print("SENDER starts working")
print("Generate QR codes")

generate(easygui.fileopenbox(default="../img/*"))

print("QR codes ready")
print("Sending data")

show()
clean()
