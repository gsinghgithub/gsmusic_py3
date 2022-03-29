#!/usr/bin/env python
"""

natural notes: SRGMPDN
altered notes: Lower case: rgdnm
higher octave: ' after note
lower octave: . after note
equally divided sub interval of single beat: (...) - under parenthesis
Note continuation: -
Note silence: ,
Notation: one cycle (measure or bar per line)
Note without parenthesis => 1 beat note
121 = - = continue
120 = , = pause/stop note
"""
from GsMidiFile import MIDIFile
from GsMidiFile import TICKSPERBEAT_CONFIG
import re
import struct
import os
import logging
import logging.handlers
#from datetime import datetime
import time, datetime
from time import gmtime, strftime
import random
print strftime("%Y-%m-%d %H:%M:%S", time.localtime())

CURRENT_MIDI = "midiout.mid"
CURRENT_BEAT = "beatout.mid"

def time_stamp(): # with microsecond
    #return strftime("%y%m%d_%H%M%S_%f", datetime.now())
    return datetime.datetime.now().strftime("%y%m%d_%H%M%S_%f")
print time_stamp()
 # create midi out directory
if not os.path.exists("midi_out_dir"): os.mkdir("midi_out_dir", 0o755)
if not os.path.exists("beat_out_dir"): os.mkdir("beat_out_dir", 0o755)
logger = logging.getLogger(__name__)
LOGFILE = 'log_midi.txt'
logger.setLevel(logging.DEBUG)
t = time.localtime()
#formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
formatter = logging.Formatter('%(asctime)s: %(message)s')
# logging: http://stackoverflow.com/questions/21591748/how-do-i-get-logger-to-delete-existing-log-file-before-writing-to-it-again
#filehandler_dbg = logging.FileHandler(logger.name + '-debug.log', mode='w')
handler = logging.handlers.RotatingFileHandler(
    LOGFILE, maxBytes=(1048576*5), backupCount=7, mode='w'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.debug('::LOG START ...')
logger.debug('::LOG START ...')
# TICKSPERBEAT is set to 1 for minimum change purpose
# TICKSPERBEAT in heade = TICKSPERBEAT_CONFIG
# Midi format
'''
# To do:
# 4 items
1. strip whitespaces for bars
#note: song structure = bars separated by spaces. number of new lines, #, and spaces does not matter
2. duration add for: -
3. Time add for: ,
-4. remove remove-note feature for splitted notes: it makes notes continuous: probably already there


====
https://www.csie.ntu.edu.tw/~r92092/ref/midi/

1. midi file common structure is: type:length:data
2. Two types of chunks: A. header chunk, B. Track chunk
3. Header chunk:
   A. 4 bytes-MThd (4D 54 68 64), B. 4 bytes - for length of header chunk after the length value
   : which is very small this time and midi 1.0 fills only 1 byte that and the value is 6 : MSB first
    4D 54 68 64  00 00 00 06  00 01 00 01  03 C0 4D 54: MThd..........MT
    M   T h  d             6 [6 byte long header]M  T
    Byte-14: header chnunk ends. header data: 2 byte = format, 2 byte = tracks, 2 bytes = ticks per quarter note
    example: ticks/quarter = 03 C0 = 960
    Important metadata: Metadata starts with FF as: FF <type> <length> <data>
    End of track: FF 2F 00
    Tempo: FF 51 03 tt tt tt
    Lyric: FF 05 <len> <text>
    Instrument: FF 04 <len> <text>
    Time signature: FF 58 04 nn dd cc bb

    Track chunk: track chunk length is exact number of bytes this chunk contains. after the word
    MTrk (4D 54 72 6B), length is placed. Track length counting starts after length bytes. Structure is MTrk-length-delta time ticks
    Bytes for track length: 4 bytes atthe enf of MTrk

    note on = 0x90 + note : MSB set
    note off = 0x80 + note : MSB = 0

    # specified time is multiplied by ticks per beat
'''


# ==== generate tune ==== Start

# numbers: .P = 55: P' =  79: continue = - = 80: pause = , = 81 # in the program the extendend note=: 48...83

# range : 55-81



exclude_1 = [55,65]
def generate_tune(exclude_list):
    my_randoms = []
    for i in range(32):
        rand_list = []
        rand_len = random.randint(1,4)
        #rand_len = 0
        for i in range(rand_len):
            rand_found = False
            while not rand_found:
                rand_num = random.randint(55,81)
                if rand_num not in exclude_list: rand_found = True
                #print "exclude note found"
            rand_list.append(rand_num)
        if rand_len == 1:
            my_randoms.append(rand_list[0])
        else:
            my_randoms.append(tuple(rand_list))
    print (my_randoms)

# ==== generate tune ==== End




# ==== play midi ==== Start

# play .mid music files using PyGame on your computer's sound card
# PyGame is free from: http://www.pygame.org/news.html
# tested with Python25 and PyGame171      vegaseat     27aug2007
import pygame
import os

def play_music(music_file):
    """
    stream music with mixer.music module in blocking manner
    this will stream the sound from disk while playing
    """
    clock = pygame.time.Clock()
    try:
        pygame.mixer.music.load(music_file)
        print "Music file %s loaded!" % music_file
    except pygame.error:
        print "File %s not found! (%s)" % (music_file, pygame.get_error())
        return
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)
# pick a midi music file you have ...
# (if not in working folder use full path)

def play_midi_file(file_name):
    freq = 44100    # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2    # 1 is mono, 2 is stereo
    buffer = 1024    # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)
    play_music(file_name)

def music_files():
    music_dir = "midi_out_dir/"
    midi_files = os.listdir(music_dir)
    for one in midi_files:
        yield music_dir + one


def play_midi():
    freq = 44100    # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2    # 1 is mono, 2 is stereo
    buffer = 1024    # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    # optional volume 0 to 1.0
    pygame.mixer.music.set_volume(0.8)
    for music_file in music_files():
        try:
            play_music(music_file)
        except KeyboardInterrupt:
            # if user hits Ctrl/C then exit
            # (works only in console mode)
            while True:
                action = raw_input('Enter Q to Quit, Enter to Skip. ').lower()
                if action == 'q':
                    pygame.mixer.music.fadeout(1000)
                    pygame.mixer.music.stop()
                    raise SystemExit
                else:
                    break

# ==== play midi ==== End

class Song(object):
    def __init__(self):

        self.srgm_base = ['S', 'r', 'R', 'g', 'G', 'M', 'm', 'P', 'd', 'D', 'n', 'N']
        self.notes_list = self.extended_note_list() # notes = 12 ... 119

        self.note_enum = enumerate(self.notes_list, start = 12)
    #self.bars = self.read_song()
        self.tracks = 1 # single track midi
        self.tempo = 120
        self.volume = 127
        self.duration = 1 # 1 beat long
        self.track = 0 # mono track
        self.time = 0 # t on beat - 0
        self.channel = 0
        self.program = 0
        self.pitch = 60 # C4 = Middle C
        self.track_name = 'Base Track'
        self.midifile = MIDIFile(self.tracks)
        self.midifile.addTrackName(self.track, self.time, self.track_name)
        self.midifile.addTempo(self.track, self.time, self.tempo)
        self.midifile.addProgramChange(self.track, self.channel, self.time, self.program)

    def create_midi_file(self, file_name, midifile):
        with open(file_name, 'wb') as outf:
            midifile.writeFile(outf)

    def create_default_midi(self):
        for i in range(1, 4):
            self.midifile.addNote(self.track, self.channel, self.pitch, self.time, self.duration, self.volume)
            self.time += 2
            self.pitch += 2
            print i
        self.create_midi_file(self.midifile)

    def read_song(self):
        # space = bar or measure or cycle separator
        # May be first few measures or beats empty as song may start ayt any bit of a drum cycle (hindi->taala)
        # :V = volume, :R = rhythm, :C = chord
        # Check if song.txt exist
        valid_notes = 'SsrRgGMmPpdDnN,\(\)-\'. '
        if os.path.exists('song.txt'):
            with open('song.txt') as fp:
                notes = []
                # read notes and duration
                #raw_song = fp.readlines()
                raw_song = [self.generate_tune('SrRgmMdDnN', 4)]
                print raw_song
           
                # filter song comments:
                songs_lines_srgm = [line.strip() for line in raw_song if (('#' not in line) and (line.strip() != '') and (':' not in line))]
                # check for valid characters
                check = [x for x in songs_lines_srgm[0] if x not in valid_notes]   
                if len(check) > 0:
                    print 'Invalid characters in the song notation: ' + repr(check)
                    exit(0)
                # find total cycles
                cycles = len(songs_lines_srgm)
                # find total bars
                temp_bars = [x.split(' ') for x in songs_lines_srgm]
                #.replace('s', 'S').replace('p', 'P') # for accidental typing  s and p
                # S and P are always natural, so lowercase letters are allowedof
                bars = [item.replace('s', 'S').replace('p', 'P') for sublist in temp_bars for item in sublist if item != '']
        
                return bars
        else:
            print 'song.txt does not exist. No Midi file will be created.'
            exit(0)


    def read_midi(self, midi_file = 'output.mid'):
        # space = bar or measure or cycle separator
        # May be first few measures or beats empty as song may start ayt any bit of a drum cycle (hindi->taala)
        # :V = volume, :R = rhythm, :C = chord
        # Check if song.txt exist
        #midi_file = '1.mid'
        if os.path.exists(midi_file):
            with open(midi_file) as fp:
                bytes_read = fp.read()
    
                print '\nFile Size: ' + repr(len(bytes_read))       
                print 'Midi Format: ' + repr(self.bytes_to_number([bytes_read[8], bytes_read[9]]))
                print 'Midi Tracks: ' + repr(self.bytes_to_number([bytes_read[10], bytes_read[11]]))
                print 'Midi ticks per beat: ' + repr(self.bytes_to_number([bytes_read[12], bytes_read[13]]))
           
                # Read tracks start positions: # Starting from position-0
                track_signature = '\x4D\x54\x72\x6B'
                track_positions = self.binary_string_search(bytes_read, track_signature)
                print track_positions
            # Find track size
   
   
        else:
            print 'Midi file ' + midi_file + ' does not exist.'
            exit(0)

    def bar_to_tuple(self, bar, time_signature):
        accent_str = '\'.'
        # Due to fraction ans preciseness issue: only 2,3 and 4 subnotes are recommended per beat
        # Check 1. if 1/2, 1/3,1/4 beat times work in the library implementation, 2. if there note off, note continue implementation is possible
        equal_time_notes = re.findall('\(.*?\)|.', bar)
        true_length_equal_notes = len([x for x in equal_time_notes if x not in accent_str])
        equal_time = (time_signature * TICKSPERBEAT_CONFIG) / true_length_equal_notes
        list_note = []
        skip_loop = False
        for i in range(0, len(equal_time_notes)):
            if skip_loop:
                skip_loop = False
                continue
            if not '(' in equal_time_notes[i]:
                if (i < len(equal_time_notes) - 1) and equal_time_notes[i + 1] in accent_str:
                    list_note.append((self.get_note_num(equal_time_notes[i] + equal_time_notes[i + 1]), equal_time))
                    skip_loop = True
                else:
                    list_note.append((self.get_note_num(equal_time_notes[i]), equal_time))
            else:
                sub_notes = equal_time_notes[i].replace('(', '').replace(')', '')
                sub_notes_length = len([x for x in sub_notes if x not in accent_str])
                for y in range(0, len(sub_notes)):
                    if skip_loop:
                        skip_loop = False
                        continue
                    if (y < len(sub_notes) - 1) and sub_notes[y + 1] in accent_str:
                        list_note.append(
                            (self.get_note_num(sub_notes[y] + sub_notes[y + 1]), equal_time / sub_notes_length))
                        skip_loop = True
                    else:
                        list_note.append((self.get_note_num(sub_notes[y]), equal_time / sub_notes_length))

        return list_note


    def get_note_num(self, note_name):
        self.note_num = None
        #for index, item in self.note_enum:
        for index, item in  enumerate(self.notes_list, start = 12):       
            if note_name == item:
                self.note_num = index
                return self.note_num
        return self.note_num


    def get_note_name(self, note_num):
        self.note_name = None
        for index, item in enumerate(self.notes_list, start=12):
            if note_num == index:
                self.note_name = item
                return self.note_name
        return self.note_name

    def get_note_name2(self, note_num):
        self.note_name = None
        for index, item in self.note_enum:
            if note_num == index:
                self.note_name = item
                break
        return self.note_name

    def extended_note_list(self):
        # maximum 88 key piano: A0 - A8: A4 = 440
        # https://en.wikipedia.org/wiki/Piano_key_frequencies: A0 = 27.5: C8 = 4186.01: immediate key ratio = 1.06
        # C4 = 261.626: Octave count starts from 0: if counted from 1 the middle octave is the 5th octave
        # S = C
        # C4 = 60: C0 = S0 = 12
        srgm_base = ['S', 'r', 'R', 'g', 'G', 'M', 'm', 'P', 'd', 'D', 'n', 'N']
        note_list = []
        suffix_1 = '.....'
        suffix_2 = ''
        for x in range(0,9):
            if x < 4:
                suffix = suffix_1[:-x-1]

            if x == 4: suffix = ''

            if x > 4:
                suffix += '\''

            for i in srgm_base:
                #note_list.append(i + repr(x) + suffix)
                note_list.append(i + suffix)
                #print i + repr(x)
            # 120(,) = S10, 121(-) = r10
        #print note_list
        return note_list + [',', '-'] # , and - may not be be required to be added because they are filtered out later

    def binary_string_search(self, bytes_list, bytes_search_string):
        list_find_positions = []
        pattern = re.compile(bytes_search_string)
        for match in pattern.finditer(bytes_list):
            list_find_positions.append(match.start()) #print m.start(), m.group()   
            return list_find_positions

    def text_to_byte_str(self, str): # comma separated bytes
        # do not expect binary data to be printed on console
        return bytearray(split(str, ','))  # byte array is mutable : string is not mutable

    def write_binary1(self, file_name, list_data):
        with open(file_name, 'w') as fp:
            fp.write(bytearray(list_data))

    def write_binary2(self, file_name, list_data):
        with open(file_name, 'w') as fp:
            for x in list_data:
                fp.write(struct.pack('B',x)) # pack converts number to binary

    def bytelist_to_numberlist(self, byte_list):
        list_number = []
        for byte in byte_list:
            list_number.append(ord(byte))
        return list_number

    def bytelist_to_hexlist(self, byte_list):
        list_number = []
        for byte in byte_list:
            list_number.append(hex(ord(byte)))
        return list_number

    def bytelist_to_hexstring(self, byte_list): # Gives formatted value
        list_number = []
        for byte in byte_list:
            list_number.append(byte.encode('hex'))
        return list_number 

    def byte_string_from_number_list(self, number_list): # input argument = a number list
        return bytearray(number_list)           

    def byte_to_number(self, byte): # argument as single byte: \x02
        return ord(byte)

    def number_to_byte(self, number): # Do nit expect visible print on the screen
        return struct.pack('B',number)           
                  
    def bytes_to_number(self, bytes_list):
        bytes = ''.join(bytes_list)
        return int(bytes.encode('hex'), 16)

    # Read midi data
    def get_midi_format(self, file_name):
        return self.read_file(file_name, 8, 2)

    def get_total_tracks(self, file_name):
        return self.read_file(file_name, 10, 2)

    def get_ticks_config(self, file_name):
        return self.read_file(file_name, 12, 2)

    def read_file(self, file_name, start_position, bytes_to_read):
        with open(file_name) as fp:
            fp.seek(start_position, 0)
            bytes_read = fp.read(bytes_to_read)
            return self.bytes_to_number(bytes_read)   

    def get_file_size(self, file_name):
        return os.path.getsize(file_name)   

    def read_track_data(self, file_name):
        print 'GOT IT'

    def get_ticks(self):
        pass


    def create_test_midi(self, file_name):
        file_name = 'midi_out_dir/tune' + time_stamp() + '.mid'
        notes_str =  ''
        notes = [60, 60, 64, 65, 67, 69, 71]
        duration = [480 for x in range(0, 7)]
        time = [960*x for x in range(0, 7)]
        volume = [127 for x in range(0, 7)]

        # create your MIDI object
        midifile = MIDIFile(1)     # only 1 track
        track = 0   # the only track
        program = 1
        midifile.addTrackName(track, 0, "Sample Track")
        midifile.addTempo(track, 0, 120)

        channel = 0
        midifile.addProgramChange(track,channel, 0, program)
        for i in range(0, len(notes)):
            print time[i]
            midifile.addNote(track, channel, notes[i], time[i], duration[i], volume[i])

        self.create_midi_file(file_name, midifile)

    def midi_from_notation(self, file_name = 'output.mid', time_signature = 4):
        file_name = 'midi_out_dir/tune_' + time_stamp() + '.mid'
        #current_midi = file_name
        markers = [121,120]
        print 'Ticks per beat: ' + repr(TICKSPERBEAT_CONFIG)
        print 'BPB: Beats per bar: ' + repr(time_signature)
        print 'BAR LENGTH: ' + repr(time_signature*TICKSPERBEAT_CONFIG) + ' ticks'
        notes_list = []
        bars = self.read_song()
        print 'BARS: ' + repr(len(bars))
        for bar in bars:
            notes_list += self.bar_to_tuple(bar, time_signature)  # One note per beat: is the assumption: => 4 beat per measure => measure = cycle
        print notes_list
        note_position = 0
        duration = 0
        volume = 0
        note = 1 # Representation of empty note: Also volume = 0
        note_hold = 1
        duration_hold = 0
        note_position_hold = -1
    
        notes_list_length = len(notes_list)
        # Consideration last - or ,
    
        for count in range(0, notes_list_length):
            logger.debug('Line-1: Note: ' + repr(notes_list[count][0]) + ': Note position: ' + repr(note_position))
            print('Line-1: Note: ' + repr(notes_list[count][0]) + ': Note position: ' + repr(note_position))
                # < notes_list_length - 1: takes care all notes except last note   
            if count < notes_list_length - 1 and notes_list[count + 1][0] in markers:
                if duration_hold == 0: duration_hold = notes_list[count][1] # duration hold
                if note_hold == 1: note_hold = notes_list[count][0] # note hold
                if note_position_hold == -1: note_position_hold = note_position # note position hold for - and ,
                if notes_list[count + 1][0] == 121 and notes_list[count][0] != 120: # to address the ,- order and combination
                    duration_hold += notes_list[count + 1][1] # duration hold for current note
                note_position += notes_list[count][1] # this position will continue increasing as usual
                continue

                # last note is already covered in the last loop
                    # Known issues:
                # 1. - or , does not work when song start with - or ,

                '''
                    # last note handling   
                if count == notes_list_length - 1:
                if notes_list[count][0] in markers:
                    if note_hold != 1: # if previous note is already on hold
                    if notes_list[count][0] == 121: # if -, current note duration should change
                        duration_hold += notes_list[count][1]
                '''
            if note_hold != 1: # If last note is - or , : let it be handles by hold operation
                # not by writing unnecessary code
                self.midifile.addNote(self.track, self.channel, note_hold, note_position_hold, duration_hold, self.volume)
                note_position += notes_list[count][1] # update note position
                note_hold = 1 # disable note hold
                note_position_hold = -1 # disable note position hold
                duration_hold = 0 # disable duration hold
                logger.debug('Line-2: Note: ' + repr(notes_list[count][0]) + ': Note position: ' + repr(note_position))
            else:
                self.midifile.addNote(self.track, self.channel, notes_list[count][0], note_position, notes_list[count][1], self.volume)
                note_position += notes_list[count][1]
                logger.debug('Line-3: Note: ' + repr(notes_list[count][0]) + ': Note position: ' + repr(note_position))
        self.create_midi_file(file_name, self.midifile)  # Create unique file
        self.create_midi_file(CURRENT_MIDI, self.midifile)  # Create unique file


    def midi_from_notation2(self, file_name = 'output.mid', time_signature = 4):
        print 'Ticks per beat: ' + repr(TICKSPERBEAT_CONFIG)
        print 'BPB: Beats per bar: ' + repr(time_signature)
        print 'BAR LENGTH: ' + repr(time_signature*TICKSPERBEAT_CONFIG) + ' ticks'
        notes_list = []
        bars = self.read_song()
        print 'BARS: ' + repr(len(bars))
        for bar in bars:
            notes_list += self.bar_to_tuple(bar, time_signature)  # One note per beat: is the assumption: => 4 beat per measure => measure = cycle
            print notes_list
            note_position = 0
            for note in notes_list:
                self.midifile.addNote(self.track, self.channel, note[0], note_position, note[1], self.volume)
                note_position += note[1]
        self.create_midi_file(file_name, self.midifile)


    def midi_to_notation(self, midi_file = 'output.mid', song_file = 'song_extract.txt'):
        self.read_midi()

    # numbers: .P = 55: P' =  79: continue = - = 81: pause = , = 80 # in the program the extendend note=: 48...83

    # range : 55-81

    def generate_tune(self, exclude_list, bar_beats):
        counter = 0
        str_tune = ''
        for i in range(32): # 1-bar music
            rand_list = []
            rand_len = random.randint(1,4)
            for i in range(rand_len):
                rand_found = False
                while not rand_found:
                    rand_num = random.randint(55,81)
                    if rand_num == 80: rand_note = ','
                    if rand_num == 81: rand_note = '-'
                    rand_note = self.get_note_name(rand_num)
                    if rand_note.replace('.', '').replace('\'', '') not in exclude_list: rand_found = True
                    #if rand_num not in exclude_list: rand_found = True
                rand_list.append(rand_note)

            if counter >= bar_beats:
                counter = 0
                str_tune += ' '
            counter += 1
            if rand_len == 1: str_tune += ''.join(rand_list)
            else: str_tune += '(' + ''.join(rand_list) + ')'
        return str_tune

    def make_beats(self, file_name='beatout.mid', time_signature=4):
        file_name = 'beat_out_dir/beat_' + time_stamp() + '.mid'
        # current_midi = file_name
        markers = [121, 120]
        print 'Ticks per beat: ' + repr(TICKSPERBEAT_CONFIG)
        print 'BPB: Beats per bar: ' + repr(time_signature)
        print 'BAR LENGTH: ' + repr(time_signature * TICKSPERBEAT_CONFIG) + ' ticks'
        notes_list = []
        bars = self.read_beats()
        print 'BARS: ' + repr(len(bars))
        for bar in bars:
            notes_list += self.bar_to_tuple(bar,
                                            time_signature)  # One note per beat: is the assumption: => 4 beat per measure => measure = cycle
        print notes_list
        note_position = 0
        duration = 0
        volume = 0
        note = 1  # Representation of empty note: Also volume = 0
        note_hold = 1
        duration_hold = 0
        note_position_hold = -1

        notes_list_length = len(notes_list)
        # Consideration last - or ,

        for count in range(0, notes_list_length):
            logger.debug('Line-1: Note: ' + repr(notes_list[count][0]) + ': Note position: ' + repr(note_position))
            print('Line-1: Note: ' + repr(notes_list[count][0]) + ': Note position: ' + repr(note_position))
            # < notes_list_length - 1: takes care all notes except last note
            if count < notes_list_length - 1 and notes_list[count + 1][0] in markers:
                if duration_hold == 0: duration_hold = notes_list[count][1]  # duration hold
                if note_hold == 1: note_hold = notes_list[count][0]  # note hold
                if note_position_hold == -1: note_position_hold = note_position  # note position hold for - and ,
                if notes_list[count + 1][0] == 121 and notes_list[count][
                    0] != 120:  # to address the ,- order and combination
                    duration_hold += notes_list[count + 1][1]  # duration hold for current note
                note_position += notes_list[count][1]  # this position will continue increasing as usual
                continue

                # last note is already covered in the last loop
                # Known issues:
                # 1. - or , does not work when song start with - or ,

                '''
                    # last note handling   
                if count == notes_list_length - 1:
                if notes_list[count][0] in markers:
                    if note_hold != 1: # if previous note is already on hold
                    if notes_list[count][0] == 121: # if -, current note duration should change
                        duration_hold += notes_list[count][1]
                '''
            if note_hold != 1:  # If last note is - or , : let it be handles by hold operation
                # not by writing unnecessary code
                self.midifile.addNote(self.track, self.channel, note_hold, note_position_hold, duration_hold,
                                      self.volume)
                note_position += notes_list[count][1]  # update note position
                note_hold = 1  # disable note hold
                note_position_hold = -1  # disable note position hold
                duration_hold = 0  # disable duration hold
                logger.debug('Line-2: Note: ' + repr(notes_list[count][0]) + ': Note position: ' + repr(note_position))
            else:
                self.midifile.addNote(self.track, self.channel, notes_list[count][0], note_position,
                                      notes_list[count][1], self.volume)
                note_position += notes_list[count][1]
                logger.debug('Line-3: Note: ' + repr(notes_list[count][0]) + ': Note position: ' + repr(note_position))
        self.create_midi_file(file_name, self.midifile)  # Create unique file
        self.create_midi_file(CURRENT_BEAT, self.midifile)  # Create unique file

    def read_beats(self):
        # space = bar or measure or cycle separator
        # May be first few measures or beats empty as song may start ayt any bit of a drum cycle (hindi->taala)
        # :V = volume, :R = rhythm, :C = chord
        # Check if song.txt exist
        valid_notes = 'SsrRgGMmPpdDnN,\(\)-\'. '
        if os.path.exists('song.txt'):
            with open('song.txt') as fp:
                notes = []
                # read notes and duration
                # raw_song = fp.readlines()
                raw_song = [self.generate_beat('SrRgmMdDnN', 4)]
                print raw_song

                # filter song comments:
                songs_lines_srgm = [line.strip() for line in raw_song if
                                    (('#' not in line) and (line.strip() != '') and (':' not in line))]
                # check for valid characters
                check = [x for x in songs_lines_srgm[0] if x not in valid_notes]
                if len(check) > 0:
                    print 'Invalid characters in the song notation: ' + repr(check)
                    exit(0)
                # find total cycles
                cycles = len(songs_lines_srgm)
                # find total bars
                temp_bars = [x.split(' ') for x in songs_lines_srgm]
                # .replace('s', 'S').replace('p', 'P') # for accidental typing  s and p
                # S and P are always natural, so lowercase letters are allowedof
                bars = [item.replace('s', 'S').replace('p', 'P') for sublist in temp_bars for item in sublist if
                        item != '']

                return bars
        else:
            print 'song.txt does not exist. No Midi file will be created.'
            exit(0)

    # numbers: .P = 55: P' =  79: continue = - = 81: pause = , = 80 # in the program the extendend note=: 48...83

    # range : 55-81

    def generate_beat(self, exclude_list, bar_beats):
        counter = 0
        str_tune = ''
        for i in range(32): # 1-bar music
            rand_list = []
            rand_len = random.randint(1,4)
            for i in range(rand_len):
                rand_found = False
                while not rand_found:
                    rand_num = random.randint(55,81)
                    if rand_num == 80: rand_note = ','
                    if rand_num == 81: rand_note = '-'
                    rand_note = self.get_note_name(rand_num)
                    if rand_note.replace('.', '').replace('\'', '') not in exclude_list: rand_found = True
                    #if rand_num not in exclude_list: rand_found = True
                rand_list.append(rand_note)

            if counter >= bar_beats:
                counter = 0
                str_tune += ' '
            counter += 1
            if rand_len == 1: str_tune += ''.join(rand_list)
            else: str_tune += '(' + ''.join(rand_list) + ')'
        return str_tune

def main():
    song = Song()
    """
    song.midi_from_notation()
    play_midi_file(CURRENT_MIDI)
    """
    song.make_beats(8)
    play_midi_file(CURRENT_BEAT)
    print 'DONE'
if __name__ == '__main__':
    main()