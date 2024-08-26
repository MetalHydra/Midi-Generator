import argparse
from .Rythms.Rythm_Builder import Rythm_Builder
from .Notes.Note_Builder import Note_Builder
import random
import uuid

R_Builder = Rythm_Builder()
N_Builder = Note_Builder()

parser = argparse.ArgumentParser(description='A parser for creating midi Files based an a given Rythm_string and Notes')
parser.add_argument('-prs', '--rythm_string',           type=str,   metavar='', required=True,                  help='Rythm String which describes the Rythmic specifications e.g. q_q for Rythm of 2 quarter Notes')
parser.add_argument('-ars', '--alternate_rythm_string', type=str,   metavar='',                                 help='creates an alternative Rythm string based on a given Rythm string')
parser.add_argument('-bpm', '--bpm',                    type=int,   metavar='', nargs='?', const=60,            help='specifies the tempo in BPM')
parser.add_argument('-rbpm',   '--random_bpm',          type=str,   metavar='',                                 help='crate random tempo')
parser.add_argument('-f',   '--filename',               type=str,   metavar='', nargs='?', const=uuid.uuid4(),  help='filename for the midi file. If not specified it will be an random uuid')
parser.add_argument('-nstr',   '--note_string',         type=str,   metavar='',                                 help='Names of Note and Chord names. e.g. A4_C#5_Bb2 or C4:maj_C4:5')

args = parser.parse_args()

if __name__ == '__main__':
    tempo = args.tempo
    rythm_string = args.rythm_string
    if args.random_bpm == 'yes':
        tempo = random.randint(45,260)
    if args.alternate_rythm_string:
        rythm_string = R_Builder.create_alternative_rythm(rythm_string=args.rythm_string)
    parsed_rythm_string = R_Builder.parse_rythm_string(rythm_string, tempo)
    list_of_elements = N_Builder.create_list_of_elements(elements=args.note_string, rythm_list=parsed_rythm_string)
    N_Builder.create_midi_from_elements(elements=list_of_elements, tempo=tempo, name=args.filename)


