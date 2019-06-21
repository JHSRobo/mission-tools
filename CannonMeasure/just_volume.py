def volume():
    length = float(input("Length: "))
    r1 = float(input("Actual R1: "))
    r2 = float(input("Actual R2: "))
    r3 = float(input("Actual R3: "))
    compound = input("Composition (iron (1)/ bronze (2)): ")
    while True:
        if compound == 2:
        # bronze
            density = 8030 * 0.000001
            break
        elif compound == 1:
            density = 7870 * 0.000001
            break
    cut_cone = 0.333333 * 3.14159 * length * ((r3 * r3) + (r3 * r1) + (r1 * r1))

    cylinder = 3.14159 * (r2*r2) * length
    volume = cut_cone - cylinder
    print("Cannon volume = {0}".format(volume))
    mass = volume * density
    water_displaced = volume * 997.0 * 0.000001
    water_weight = (mass - water_displaced) * 9.8
    print("Cannon weight = {0}".format(water_weight))

if __name__ == '__main__':
    volume()
