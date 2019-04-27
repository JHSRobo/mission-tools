# take input of scale length in pixel
# divide that by IRL distance of length (just leave it blank for now)
# take input of cannon length in pixels
# divide that by IRL ratio calculated before

SCALE_LENGTH = 12

scale_length_in_pixels = input("What is the scale length in pixels\n")
cannon_diameter_in_pixels = input("What is the cannon diameter in pixels\n")


cannon_length_in_pixels = input("What is the cannon length in pixels\n")

ratio = float(scale_length_in_pixels) / float(SCALE_LENGTH)
print(ratio)
cannon_length = float(cannon_length_in_pixels) / ratio

cannon_diameter = float(cannon_diameter_in_pixels) / ratio
print ("Cannon length in pixels: " + str(cannon_length))
print ("Cannon diameter in pixels: " + str(cannon_diameter))
