def volume():
    length = float(input("Length: "))
    r1 = float(input("Actual R1: "))
    r2 = float(input("Actual R2: "))
    r3 = float(input("Actual R3: "))
    compound = input("Composition (iron / bronze): ")
    if compound.lower().strip() == "bronze":
        # bronze
        density = 8030 * 0.000001
    elif compound.lower().strip() == "iron":
        density = 7870 * 0.000001
    cut_cone = (1/3) * 3.14159 * length * (sqr(r3) + (r3 * r1) + sqr(r1))
    cylinder = 3.14159 * sqr(r2) * length
    volume = cut_cone - cylinder
    print("Cannon volume = {0}".format(volume))
    mass = volume * density
    water_displaced = volume * 997 * 0.000001
    water_weight = (mass - water_displaced) * 9.8
    print("Cannon weight = {0}".format(water_weight))

if __name__ == '__main__':
    volume()
