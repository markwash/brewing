import argparse

# inputs:
# - mash 1 vol
# - mash 1 sg
# - mash 2 vol
# - mash 2 sg
# variable input:
# - swap volume
# outputs:
# - mash 1 new sg
# - mash 2 new sg



def main():
    args = parse_args()
    if args.test_sg:
        brix = sg_to_brix(args.test_sg)
        sg = brix_to_sg(brix)
        print "%0.3f SG -> %0.3f Brix -> %0.3f SG" % (args.test_sg, brix, sg)
        return
    mash1, mash2 = convert_args(args)
    mash1, mash2 = calculate(mash1, mash2, args.swap1, args.swap2)
    display(mash1, mash2)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--vol1', type=float)
    parser.add_argument('--sg1', type=float)
    parser.add_argument('--vol2', type=float)
    parser.add_argument('--sg2', type=float)
    parser.add_argument('--swap1', type=float)
    parser.add_argument('--swap2', type=float)
    parser.add_argument('--test-sg', type=float)
    return parser.parse_args()

def convert_args(args):
    mash1 = Mash.from_volume_and_sg(args.vol1, args.sg1)
    mash2 = Mash.from_volume_and_sg(args.vol2, args.sg2)
    return mash1, mash2

def calculate(mash1, mash2, swap1, swap2):
    main1, xfer1 = mash1.split(swap1)
    main2, xfer2 = mash2.split(swap2)
    mash1 = main1.add(xfer2)
    mash2 = main2.add(xfer1)
    return mash1, mash2

def display(mash1, mash2):
    print 'Mash1: %0.3f gallons at %0.3f SG' % (mash1.volume, mash1.sg)
    print 'Mash2: %0.3f gallons at %0.3f SG' % (mash2.volume, mash2.sg)

def brix_to_sg(brix):
    return (brix / (258.6 - ((brix / 258.2)*227.1))) + 1

def sg_to_brix(sg):
    return (((182.4601 * sg - 775.6821) * sg + 1262.7794) * sg - 669.5622)

class Mash(object):
    @classmethod
    def from_water_and_sugar(cls, water, sugar):
        return Mash(water, sugar)

    @classmethod
    def from_volume_and_sg(cls, volume, sg):
        mass = volume * sg
        brix = sg_to_brix(sg)
        sugar = brix * mass / 100.0
        water = (mass - sugar) / 8.0
        return Mash(water, sugar)

    def __init__(self, water, sugar):
        self.water = water  # gallons
        self.sugar = sugar  # lbs

    @property
    def volume(self):
        # volume = mass / density
        return self.mass / self.sg

    @property
    def sg(self):
        return brix_to_sg(self.brix)

    @property
    def brix(self):
        return  100.0 * self.sugar / self.mass

    @property
    def mass(self):
        # 8 lbs per gallon of water
        return 8 * self.water + self.sugar

    def add(self, other):
        water = self.water + other.water
        sugar = self.sugar + other.sugar
        return Mash.from_water_and_sugar(water, sugar)

    def split(self, volume):
        sg = self.sg
        vol1 = self.volume - volume
        vol2 = volume
        mash1 = Mash.from_volume_and_sg(vol1, sg)
        mash2 = Mash.from_volume_and_sg(vol2, sg)
        return mash1, mash2


if __name__ == '__main__':
    main()
