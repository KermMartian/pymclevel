import materials
from materials import alphaMaterials
from numpy import arange, zeros


def genericVerticalFlip(cls):
    rotation = arange(16, dtype='uint8')
    if hasattr(cls, "Up") and hasattr(cls, "Down"):
        rotation[cls.Up] = cls.Down
        rotation[cls.Down] = cls.Up

    if hasattr(cls, "TopNorth") and hasattr(cls, "TopWest") and hasattr(cls, "TopSouth") and hasattr(cls, "TopEast"):
        rotation[cls.North] = cls.TopNorth
        rotation[cls.West] = cls.TopWest
        rotation[cls.South] = cls.TopSouth
        rotation[cls.East] = cls.TopEast
        rotation[cls.TopNorth] = cls.North
        rotation[cls.TopWest] = cls.West
        rotation[cls.TopSouth] = cls.South
        rotation[cls.TopEast] = cls.East

    return rotation


def genericRotation(cls):
    rotation = arange(16, dtype='uint8')
    rotation[cls.North] = cls.West
    rotation[cls.West] = cls.South
    rotation[cls.South] = cls.East
    rotation[cls.East] = cls.North
    if hasattr(cls, "TopNorth") and hasattr(cls, "TopWest") and hasattr(cls, "TopSouth") and hasattr(cls, "TopEast"):
        rotation[cls.TopNorth] = cls.TopWest
        rotation[cls.TopWest] = cls.TopSouth
        rotation[cls.TopSouth] = cls.TopEast
        rotation[cls.TopEast] = cls.TopNorth

    return rotation


def genericEastWestFlip(cls):
    rotation = arange(16, dtype='uint8')
    rotation[cls.West] = cls.East
    rotation[cls.East] = cls.West
    if hasattr(cls, "TopWest") and hasattr(cls, "TopEast"):
        rotation[cls.TopWest] = cls.TopEast
        rotation[cls.TopEast] = cls.TopWest

    return rotation


def genericNorthSouthFlip(cls):
    rotation = arange(16, dtype='uint8')
    rotation[cls.South] = cls.North
    rotation[cls.North] = cls.South
    if hasattr(cls, "TopNorth") and hasattr(cls, "TopSouth"):
        rotation[cls.TopSouth] = cls.TopNorth
        rotation[cls.TopNorth] = cls.TopSouth

    return rotation


rotationClasses = []


def genericFlipRotation(cls):
    cls.rotateLeft = genericRotation(cls)

    cls.flipVertical = genericVerticalFlip(cls)
    cls.flipEastWest = genericEastWestFlip(cls)
    cls.flipNorthSouth = genericNorthSouthFlip(cls)
    rotationClasses.append(cls)
    return cls


# Note, directions are based on the old north. North in here is East ingame.
class Torch:
    blocktypes = [
        alphaMaterials.Torch.ID,
        alphaMaterials.RedstoneTorchOn.ID,
        alphaMaterials.RedstoneTorchOff.ID,
    ]

    South = 1
    North = 2
    West = 3
    East = 4


genericFlipRotation(Torch)


class Ladder:
    blocktypes = [alphaMaterials.Ladder.ID]

    East = 2
    West = 3
    North = 4
    South = 5


genericFlipRotation(Ladder)


class Stair:
    blocktypes = [b.ID for b in alphaMaterials.AllStairs]

    South = 0
    North = 1
    West = 2
    East = 3
    TopSouth = 4
    TopNorth = 5
    TopWest = 6
    TopEast = 7


genericFlipRotation(Stair)


class HalfSlab:
    blocktypes = [alphaMaterials.StoneSlab.ID]

    StoneSlab = 0
    SandstoneSlab = 1
    WoodenSlab = 2
    CobblestoneSlab = 3
    BrickSlab = 4
    StoneBrickSlab = 5
    TopStoneSlab = 8
    TopSandstoneSlab = 9
    TopWoodenSlab = 10
    TopCobblestoneSlab = 11
    TopBrickSlab = 12
    TopStoneBrickSlab = 13


HalfSlab.flipVertical = arange(16, dtype='uint8')
HalfSlab.flipVertical[HalfSlab.StoneSlab] = HalfSlab.TopStoneSlab
HalfSlab.flipVertical[HalfSlab.SandstoneSlab] = HalfSlab.TopSandstoneSlab
HalfSlab.flipVertical[HalfSlab.WoodenSlab] = HalfSlab.TopWoodenSlab
HalfSlab.flipVertical[HalfSlab.CobblestoneSlab] = HalfSlab.TopCobblestoneSlab
HalfSlab.flipVertical[HalfSlab.BrickSlab] = HalfSlab.TopBrickSlab
HalfSlab.flipVertical[HalfSlab.StoneBrickSlab] = HalfSlab.TopStoneBrickSlab
HalfSlab.flipVertical[HalfSlab.TopStoneSlab] = HalfSlab.StoneSlab
HalfSlab.flipVertical[HalfSlab.TopSandstoneSlab] = HalfSlab.SandstoneSlab
HalfSlab.flipVertical[HalfSlab.TopWoodenSlab] = HalfSlab.WoodenSlab
HalfSlab.flipVertical[HalfSlab.TopCobblestoneSlab] = HalfSlab.CobblestoneSlab
HalfSlab.flipVertical[HalfSlab.TopBrickSlab] = HalfSlab.BrickSlab
HalfSlab.flipVertical[HalfSlab.TopStoneBrickSlab] = HalfSlab.StoneBrickSlab
rotationClasses.append(HalfSlab)


class WallSign:
    blocktypes = [alphaMaterials.WallSign.ID, alphaMaterials.WallBanner.ID]

    East = 2
    West = 3
    North = 4
    South = 5


genericFlipRotation(WallSign)


class FurnaceDispenserChest:
    blocktypes = [
        alphaMaterials.Furnace.ID,
        alphaMaterials.LitFurnace.ID,
        alphaMaterials.Chest.ID,
        alphaMaterials.EnderChest.ID
    ]
    East = 2
    West = 3
    North = 4
    South = 5


genericFlipRotation(FurnaceDispenserChest)


class Pumpkin:
    blocktypes = [
        alphaMaterials.Pumpkin.ID,
        alphaMaterials.JackOLantern.ID,
    ]

    East = 0
    South = 1
    West = 2
    North = 3


genericFlipRotation(Pumpkin)


class Rail:
    blocktypes = [alphaMaterials.Rail.ID]

    EastWest = 0
    NorthSouth = 1
    South = 2
    North = 3
    East = 4
    West = 5

    Northeast = 6
    Southeast = 7
    Southwest = 8
    Northwest = 9


def generic8wayRotation(cls):
    cls.rotateLeft = genericRotation(cls)
    cls.rotateLeft[cls.Northeast] = cls.Northwest
    cls.rotateLeft[cls.Southeast] = cls.Northeast
    cls.rotateLeft[cls.Southwest] = cls.Southeast
    cls.rotateLeft[cls.Northwest] = cls.Southwest

    cls.flipEastWest = genericEastWestFlip(cls)
    cls.flipEastWest[cls.Northeast] = cls.Northwest
    cls.flipEastWest[cls.Northwest] = cls.Northeast
    cls.flipEastWest[cls.Southwest] = cls.Southeast
    cls.flipEastWest[cls.Southeast] = cls.Southwest

    cls.flipNorthSouth = genericNorthSouthFlip(cls)
    cls.flipNorthSouth[cls.Northeast] = cls.Southeast
    cls.flipNorthSouth[cls.Southeast] = cls.Northeast
    cls.flipNorthSouth[cls.Southwest] = cls.Northwest
    cls.flipNorthSouth[cls.Northwest] = cls.Southwest
    rotationClasses.append(cls)


generic8wayRotation(Rail)
Rail.rotateLeft[Rail.NorthSouth] = Rail.EastWest
Rail.rotateLeft[Rail.EastWest] = Rail.NorthSouth


def applyBit(apply):
    def _applyBit(class_or_array):
        if hasattr(class_or_array, "rotateLeft"):
            for a in (class_or_array.flipEastWest,
                      class_or_array.flipNorthSouth,
                      class_or_array.rotateLeft):
                apply(a)
        else:
            array = class_or_array
            apply(array)

    return _applyBit


@applyBit
def applyBit8(array):
    array[8:16] = array[0:8] | 0x8


@applyBit
def applyBit4(array):
    array[4:8] = array[0:4] | 0x4
    array[12:16] = array[8:12] | 0x4


@applyBit
def applyBits48(array):
    array[4:8] = array[0:4] | 0x4
    array[8:16] = array[0:8] | 0x8


applyThrownBit = applyBit8


class PoweredDetectorRail(Rail):
    blocktypes = [alphaMaterials.PoweredRail.ID, alphaMaterials.DetectorRail.ID, alphaMaterials.ActivatorRail.ID]


PoweredDetectorRail.rotateLeft = genericRotation(PoweredDetectorRail)

PoweredDetectorRail.rotateLeft[PoweredDetectorRail.NorthSouth] = PoweredDetectorRail.EastWest
PoweredDetectorRail.rotateLeft[PoweredDetectorRail.EastWest] = PoweredDetectorRail.NorthSouth

PoweredDetectorRail.flipEastWest = genericEastWestFlip(PoweredDetectorRail)
PoweredDetectorRail.flipNorthSouth = genericNorthSouthFlip(PoweredDetectorRail)
applyThrownBit(PoweredDetectorRail)
rotationClasses.append(PoweredDetectorRail)


class Lever:
    blocktypes = [alphaMaterials.Lever.ID]
    ThrownBit = 0x8
    Up = 0
    South = 1
    North = 2
    West = 3
    East = 4
    EastWest = 5
    NorthSouth = 6
    Down = 7


Lever.rotateLeft = genericRotation(Lever)
Lever.rotateLeft[Lever.NorthSouth] = Lever.EastWest
Lever.rotateLeft[Lever.EastWest] = Lever.NorthSouth
Lever.rotateLeft[Lever.Up] = Lever.Down
Lever.rotateLeft[Lever.Down] = Lever.Up
Lever.flipEastWest = genericEastWestFlip(Lever)
Lever.flipNorthSouth = genericNorthSouthFlip(Lever)
applyThrownBit(Lever)
rotationClasses.append(Lever)


class Button:
    blocktypes = [alphaMaterials.Button.ID, alphaMaterials.WoodenButton.ID]
    PressedBit = 0x8
    South = 1
    North = 2
    West = 3
    East = 4


Button.rotateLeft = genericRotation(Button)
Button.flipEastWest = genericEastWestFlip(Button)
Button.flipNorthSouth = genericNorthSouthFlip(Button)
applyThrownBit(Button)
rotationClasses.append(Button)


class SignPost:
    blocktypes = [alphaMaterials.Sign.ID, alphaMaterials.MobHead.ID, alphaMaterials.StandingBanner.ID]

    South = 0
    SouthSouthWest = 1
    SouthWest = 2
    SouthWestWest = 3
    West = 4
    NorthWestWest = 5
    NorthWest = 6
    NorthNorthWest = 7
    North = 8
    NorthNorthEast = 9
    NorthEast = 10
    NorthEastEast = 11
    East = 12
    SouthEastEast = 13
    SouthEast = 14
    SouthSouthEast = 15
    
    #rotate by increasing clockwise
    rotateLeft = arange(16, dtype='uint8')
    rotateLeft -= 4
    rotateLeft &= 0xf

SignPost.flipNorthSouth = arange(16, dtype='uint8')
SignPost.flipNorthSouth[SignPost.East] = SignPost.West
SignPost.flipNorthSouth[SignPost.West] = SignPost.East
SignPost.flipNorthSouth[SignPost.SouthWestWest] = SignPost.SouthEastEast
SignPost.flipNorthSouth[SignPost.SouthEastEast] = SignPost.SouthWestWest
SignPost.flipNorthSouth[SignPost.SouthWest] = SignPost.SouthEast
SignPost.flipNorthSouth[SignPost.SouthEast] = SignPost.SouthWest
SignPost.flipNorthSouth[SignPost.SouthSouthWest] = SignPost.SouthSouthEast
SignPost.flipNorthSouth[SignPost.SouthSouthEast] = SignPost.SouthSouthWest
SignPost.flipNorthSouth[SignPost.NorthEastEast] = SignPost.NorthWestWest
SignPost.flipNorthSouth[SignPost.NorthWestWest] = SignPost.NorthEastEast
SignPost.flipNorthSouth[SignPost.NorthEast] = SignPost.NorthWest
SignPost.flipNorthSouth[SignPost.NorthWest] = SignPost.NorthEast
SignPost.flipNorthSouth[SignPost.NorthNorthEast] = SignPost.NorthNorthWest
SignPost.flipNorthSouth[SignPost.NorthNorthWest] = SignPost.NorthNorthEast


SignPost.flipEastWest = arange(16, dtype='uint8')
SignPost.flipEastWest[SignPost.North] = SignPost.South
SignPost.flipEastWest[SignPost.South] = SignPost.North
SignPost.flipEastWest[SignPost.SouthSouthEast] = SignPost.NorthNorthEast
SignPost.flipEastWest[SignPost.NorthNorthEast] = SignPost.SouthSouthEast
SignPost.flipEastWest[SignPost.NorthEast] = SignPost.SouthEast
SignPost.flipEastWest[SignPost.SouthEast] = SignPost.NorthEast
SignPost.flipEastWest[SignPost.SouthEastEast] = SignPost.NorthEastEast
SignPost.flipEastWest[SignPost.NorthEastEast] = SignPost.SouthEastEast
SignPost.flipEastWest[SignPost.NorthNorthWest] = SignPost.SouthSouthWest
SignPost.flipEastWest[SignPost.SouthSouthWest] = SignPost.NorthNorthWest
SignPost.flipEastWest[SignPost.NorthWest] = SignPost.SouthWest
SignPost.flipEastWest[SignPost.SouthWest] = SignPost.NorthWest
SignPost.flipEastWest[SignPost.NorthWestWest] = SignPost.SouthWestWest
SignPost.flipEastWest[SignPost.SouthWestWest] = SignPost.NorthWestWest

rotationClasses.append(SignPost)


class Bed:
    blocktypes = [alphaMaterials.Bed.ID]
    West = 0
    North = 1
    East = 2
    South = 3


genericFlipRotation(Bed)
applyBit8(Bed)
applyBit4(Bed)

class EndPortal:
    blocktypes = [alphaMaterials.PortalFrame.ID]
    West = 0
    North = 1
    East = 2
    South = 3


genericFlipRotation(EndPortal)
applyBit4(EndPortal)

class Door:
    blocktypes = [
        alphaMaterials.IronDoor.ID,
        alphaMaterials.WoodenDoor.ID,
        alphaMaterials.SpruceDoor.ID,
        alphaMaterials.BirchDoor.ID,
        alphaMaterials.JungleDoor.ID,
        alphaMaterials.AcaciaDoor.ID,
        alphaMaterials.DarkOakDoor.ID,
        alphaMaterials.WoodenDoor.ID,
    ]
    South = 0
    West = 1
    North = 2
    East = 3
    SouthOpen = 4
    WestOpen = 5
    NorthOpen = 6
    EastOpen = 7
    Left = 8
    Right = 9

    rotateLeft = arange(16, dtype='uint8')

Door.rotateLeft[Door.South] = Door.West
Door.rotateLeft[Door.West] = Door.North
Door.rotateLeft[Door.North] = Door.East
Door.rotateLeft[Door.East] = Door.South
Door.rotateLeft[Door.SouthOpen] = Door.WestOpen
Door.rotateLeft[Door.WestOpen] = Door.NorthOpen
Door.rotateLeft[Door.NorthOpen] = Door.EastOpen
Door.rotateLeft[Door.EastOpen] = Door.SouthOpen
    
#applyBit4(Door.rotateLeft)

Door.flipEastWest = arange(16, dtype='uint8')
Door.flipEastWest[Door.Left] = Door.Right
Door.flipEastWest[Door.Right] = Door.Left
Door.flipEastWest[Door.East] = Door.West
Door.flipEastWest[Door.West] = Door.East
Door.flipEastWest[Door.EastOpen] = Door.WestOpen
Door.flipEastWest[Door.WestOpen] = Door.EastOpen

Door.flipNorthSouth = arange(16, dtype='uint8')
Door.flipNorthSouth[Door.Left] = Door.Right
Door.flipNorthSouth[Door.Right] = Door.Left
Door.flipNorthSouth[Door.North] = Door.South
Door.flipNorthSouth[Door.South] = Door.North
Door.flipNorthSouth[Door.NorthOpen] = Door.SouthOpen
Door.flipNorthSouth[Door.SouthOpen] = Door.NorthOpen

rotationClasses.append(Door)

class Log:
    blocktypes = [
        alphaMaterials.Wood.ID,
        alphaMaterials.Wood2.ID,
    ]
    Type1Up = 0
    Type2Up = 1
    Type3Up = 2
    Type4Up = 3
    Type1NorthSouth = 4
    Type2NorthSouth = 5
    Type3NorthSouth = 6
    Type4NorthSouth = 7
    Type1EastWest = 8
    Type2EastWest = 9
    Type3EastWest = 10
    Type4EastWest = 11

    rotateLeft = arange(16, dtype='uint8')

Log.rotateLeft[Log.Type1NorthSouth] = Log.Type1EastWest
Log.rotateLeft[Log.Type1EastWest] = Log.Type1NorthSouth
Log.rotateLeft[Log.Type2NorthSouth] = Log.Type2EastWest
Log.rotateLeft[Log.Type2EastWest] = Log.Type2NorthSouth
Log.rotateLeft[Log.Type3NorthSouth] = Log.Type3EastWest
Log.rotateLeft[Log.Type3EastWest] = Log.Type3NorthSouth
Log.rotateLeft[Log.Type4NorthSouth] = Log.Type4EastWest
Log.rotateLeft[Log.Type4EastWest] = Log.Type4NorthSouth

rotationClasses.append(Log)


class RedstoneRepeater:
    blocktypes = [
        alphaMaterials.RedstoneRepeaterOff.ID,
        alphaMaterials.RedstoneRepeaterOn.ID
    ]

    East = 0
    South = 1
    West = 2
    North = 3


genericFlipRotation(RedstoneRepeater)

#high bits of the repeater indicate repeater delay, and should be preserved
applyBits48(RedstoneRepeater)


class Trapdoor:
    blocktypes = [alphaMaterials.Trapdoor.ID, alphaMaterials.IronTrapdoor.ID]

    West = 0
    East = 1
    South = 2
    North = 3
    TopWest = 4
    TopEast = 5
    TopSouth = 6
    TopNorth = 7


genericFlipRotation(Trapdoor)
applyOpenedBit = applyBit8
applyOpenedBit(Trapdoor)


class PistonBody:
    blocktypes = [alphaMaterials.StickyPiston.ID, alphaMaterials.Piston.ID]

    Down = 0
    Up = 1
    East = 2
    West = 3
    North = 4
    South = 5


genericFlipRotation(PistonBody)
applyPistonBit = applyBit8
applyPistonBit(PistonBody)


class PistonHead(PistonBody):
    blocktypes = [alphaMaterials.PistonHead.ID]


rotationClasses.append(PistonHead)


#Mushroom types:
#Value     Description     Textures
#0     Fleshy piece     Pores on all sides
#1     Corner piece     Cap texture on top, directions 1 (cloud direction) and 2 (sunrise)
#2     Side piece     Cap texture on top and direction 2 (sunrise)
#3     Corner piece     Cap texture on top, directions 2 (sunrise) and 3 (cloud origin)
#4     Side piece     Cap texture on top and direction 1 (cloud direction)
#5     Top piece     Cap texture on top
#6     Side piece     Cap texture on top and direction 3 (cloud origin)
#7     Corner piece     Cap texture on top, directions 0 (sunset) and 1 (cloud direction)
#8     Side piece     Cap texture on top and direction 0 (sunset)
#9     Corner piece     Cap texture on top, directions 3 (cloud origin) and 0 (sunset)
#10     Stem piece     Stem texture on all four sides, pores on top and bottom


class HugeMushroom:
    blocktypes = [alphaMaterials.HugeRedMushroom.ID, alphaMaterials.HugeBrownMushroom.ID]
    Northeast = 1
    East = 2
    Southeast = 3
    South = 6
    Southwest = 9
    West = 8
    Northwest = 7
    North = 4


generic8wayRotation(HugeMushroom)


class Vines:
    blocktypes = [alphaMaterials.Vines.ID]

    WestBit = 1
    NorthBit = 2
    EastBit = 4
    SouthBit = 8

    rotateLeft = arange(16, dtype='uint8')
    flipEastWest = arange(16, dtype='uint8')
    flipNorthSouth = arange(16, dtype='uint8')

#Hmm... Since each bit is a direction, we can rotate by shifting!
Vines.rotateLeft = 0xf & ((Vines.rotateLeft >> 1) | (Vines.rotateLeft << 3))
# Wherever each bit is set, clear it and set the opposite bit
EastWestBits = (Vines.EastBit | Vines.WestBit)
Vines.flipEastWest[(Vines.flipEastWest & EastWestBits) > 0] ^= EastWestBits

NorthSouthBits = (Vines.NorthBit | Vines.SouthBit)
Vines.flipNorthSouth[(Vines.flipNorthSouth & NorthSouthBits) > 0] ^= NorthSouthBits

rotationClasses.append(Vines)


class Anvil:
    blocktypes = [alphaMaterials.Anvil.ID]

    East = 0
    South = 1
    West = 2
    North = 3


genericFlipRotation(Anvil)
applyAnvilBit = applyBit8
applyAnvilBit(Anvil)


@genericFlipRotation
class Hay:
    blocktypes = [alphaMaterials.HayBlock.ID]

    East = 4
    West = 4
    North = 8
    South = 8


@genericFlipRotation
class QuartzPillar:
    blocktypes = [alphaMaterials.BlockofQuartz.ID]

    East = 3
    West = 3
    North = 4
    South = 4

@genericFlipRotation
class NetherPortal:
    blocktypes = [alphaMaterials.NetherPortal.ID]

    East = 1
    West = 1
    North = 2
    South = 2

class Wood:
    blocktypes = [alphaMaterials.Wood.ID, alphaMaterials.Wood2.ID]

    East = 0
    South = 1
    West = 2
    North = 3


genericFlipRotation(Anvil)
applyAnvilBit = applyBit8
applyAnvilBit(Anvil)


class FenceGate:
    blocktypes = [alphaMaterials.FenceGate.ID]

    South = 0
    West = 1
    North = 2
    East = 3


@genericFlipRotation
class EnderPortal:
    blocktypes = [alphaMaterials.EnderPortal.ID]

    South = 0
    West = 1
    North = 2
    East = 3


@genericFlipRotation
class CocoaPlant:
    blocktypes = [alphaMaterials.CocoaPlant.ID]

    North = 0
    East = 1
    South = 2
    West = 3


applyBits48(CocoaPlant)  # growth state


@genericFlipRotation
class TripwireHook:
    blocktypes = [alphaMaterials.TripwireHook.ID]

    South = 0
    West = 1
    North = 2
    East = 3


applyBits48(TripwireHook)  # activation/ready state


@genericFlipRotation
class MobHead:
    blocktypes = [alphaMaterials.MobHead.ID]

    East = 2
    West = 3
    North = 4
    South = 5


@genericFlipRotation
class Hopper:
    blocktypes = [alphaMaterials.Hopper.ID]
    Down = 0
    East = 2
    West = 3
    North = 4
    South = 5


@genericFlipRotation 
class Dropper:
    blocktypes = [alphaMaterials.Dropper.ID, alphaMaterials.Dispenser.ID]
    Down = 0
    Up = 1
    East = 2
    West = 3
    North = 4
    South = 5

applyBit8(Dropper)


@genericFlipRotation 
class RedstoneComparator:
    blocktypes = [alphaMaterials.RedstoneComparatorInactive.ID, alphaMaterials.RedstoneComparatorActive.ID]

    East = 0
    South = 1
    West = 2
    North = 3


applyBits48(RedstoneComparator)


def masterRotationTable(attrname):
    # compute a materials.id_limitx16 table mapping each possible blocktype/data combination to
    # the resulting data when the block is rotated
    table = zeros((materials.id_limit, 16), dtype='uint8')
    table[:] = arange(16, dtype='uint8')
    for cls in rotationClasses:
        if hasattr(cls, attrname):
            blocktable = getattr(cls, attrname)
            for blocktype in cls.blocktypes:
                table[blocktype] = blocktable

    return table


def rotationTypeTable():
    table = {}
    for cls in rotationClasses:
        for b in cls.blocktypes:
            table[b] = cls

    return table


class BlockRotation:
    rotateLeft = masterRotationTable("rotateLeft")
    flipEastWest = masterRotationTable("flipEastWest")
    flipNorthSouth = masterRotationTable("flipNorthSouth")
    flipVertical = masterRotationTable("flipVertical")
    typeTable = rotationTypeTable()


def SameRotationType(blocktype1, blocktype2):
    #use different default values for typeTable.get() to make it return false when neither blocktype is present
    return BlockRotation.typeTable.get(blocktype1.ID) == BlockRotation.typeTable.get(blocktype2.ID, BlockRotation)


def FlipVertical(blocks, data):
    data[:] = BlockRotation.flipVertical[blocks, data]


def FlipNorthSouth(blocks, data):
    data[:] = BlockRotation.flipNorthSouth[blocks, data]


def FlipEastWest(blocks, data):
    data[:] = BlockRotation.flipEastWest[blocks, data]


def RotateLeft(blocks, data):
    data[:] = BlockRotation.rotateLeft[blocks, data]
