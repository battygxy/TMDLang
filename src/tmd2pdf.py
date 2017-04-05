import TMDScanner as Scan
import re
import sys
from pathlib import Path
import TMDDrawer as Draw
from fractions import Fraction as frac
import cairo
''' necessary variables '''
ReservedInstrument = set({'CHORD', 'GROOVE'})
InstrumentSet = set()
PartSet = set()
Key = ''            # default key is C
Tempo = 120.0       # default tempo 120
SongName = ''       # defult no name
Signature = [4, 4]  # defult to 4/4
PartsContent = []
PartNameList = []
InputFile = ''


def FileChecker(ARGV):
    MarkupTypePattern = r"^\:\:(?P<MarkType>\S+)\:\:\s*?$"
    if len(ARGV) == 1:
        print("usage:\n%s InputFile.tmd\n" % ARGV[0])
        return False

    elif Path(ARGV[1]).is_file() != True:
        print("there is no file named %s!" % ARGV[1])
        return False

    elif re.search(MarkupTypePattern, open(ARGV[1], 'r').readline()) == None:
        print("unknown filetype")
        return False
    else:
        return True


# def Surface(NAME, Size):
    # NAME: Song Name (with page#?)
    # TYPE: {PDF}
    # Size: {A3, A4, B4, B3}
#    if Size == '':
#        Size = 'A4'
#    return cairo.Context(surface(NAME + '.pdf', Size))


def main():
    ARGV = sys.argv

    # Checking File Head #

    if FileChecker(ARGV) == False:
        sys.exit('File Type Error')
    # done Checking File Head #

    # done Checking Header
    InputFile = open(ARGV[1], 'r').read()
    Key = Scan.KeyGetter(InputFile)
    Tempo = float(Scan.TempoGetter(InputFile))
    Signature = Scan.SignatureGetter(InputFile)
    SongName = Scan.SongNameGetter(InputFile)
    PartsContent = Scan.PartContentGetter(InputFile)
    PartNameList = Scan.PartSequenceGetter(InputFile)
    PartSet = Scan.PartSetGetter(PartsContent)
    InstrumentSet = Scan.InstrumentSetGetter(PartsContent)

    # done Confirming Pass 1
    #      Confirming Pass 2
    #      for Chord First
    Scan.ChordListGetter(Scan.PartsContainsChord(PartsContent))


'''
    #  [["6", "♯", "m"], "7-5", ["3", "♭"],  [1, 0.5]]
    #  means 6♯m7-5/3♭ (bass on 3,) with 1 bar before and place at 0.5 * bar_length
    #    Chord :[
    #            Root        -> [ '7' ->  '1~7' ,     #-> full size
    #            pitch       ->   '♯'|'♭'|'' ,       #-> 1/2 size
    #            Quality    ->  'm, aug, dim, alt' ]  #-> 1/2 size
    #            Intrval      ->  'sus, sus4, 7, 11, 6, 9, 13' .etc... , #-> 1/3 size
    #            Bass        ->['4','♭'] ,            #-> 1/2 size bold
    #            Length    -> frac(x,y)                #->  (<basetick *> / (m of <n/m>) ) ???<= confuse now....
    #            ]
    #
'''

if __name__ == '__main__':
    main()
