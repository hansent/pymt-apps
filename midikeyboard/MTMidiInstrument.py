from pymt import *


MIDI_instruments = [
#  Piano
	"Acoustic Grand Piano",
	"Bright Acoustic Piano",
	"Electric Grand Piano",
	"Honkytonk Piano",
	"Electric Piano 1",
	"Electric Piano 2",
	"Harpsichord",
	"Clavi",
#  Chromatic Percussion
	"Celesta",
	"Glockenspiel",
	"Music Box",
	"Vibraphone",
	"Marimba",
	"Xylophone",
	"Tubular Bells",
	"Dulcimer",
#  Organ 
	"Drawbar Organ",
	"Percussive Organ",
	"Rock Organ",
	"Church Organ",
	"Reed Organ",
	"Accordion",
	"Harmonica",
	"Tango Accordion",
#  Guitar 
	"Acoustic Guitar (nylon)",
	"Acoustic Guitar (steel)",
	"Electric Guitar (jazz)",
	"Electric Guitar (clean)",
	"Electric Guitar (muted)",
	"Overdriven Guitar",
	"Distortion Guitar",
	"Guitar Harmonics",
#  Bass 
	"Acoustic Bass",
	"Electric Bass (finger)",
	"Electric Bass (pick)",
	"Fretless Bass",
	"Slap Bass 1",
	"Slap Bass 2",
	"Synth Bass 1",
	"Synth Bass 2",
#  Strings 
	"Violin",
	"Viola",
	"Cello",
	"Contrabass",
	"Tremolo Strings",
	"Pizzicato Strings",
	"Orchestral Harp",
	"Timpani",
#  Ensemble 
	"String Ensemble 1",
	"String Ensemble 2",
	"SynthStrings 1",
	"SynthStrings 2",
	"Choir Aahs",
	"Voice Oohs",
	"Synth Voice",
	"Orchestra Hit",
#  Brass 
	"Trumpet",
	"Trombone",
	"Tuba",
	"Muted Trumpet",
	"French Horn",
	"Brass Section",
	"SynthBrass 1",
	"SynthBrass 2",
#  Reed 
	"Soprano Sax",
	"Alto Sax",
	"Tenor Sax",
	"Baritone Sax",
	"Oboe",
	"English Horn",
	"Bassoon",
	"Clarinet",
#  Pipe 
	"Piccolo",
	"Flute",
	"Recorder",
	"Pan Flute",
	"Blown Bottle",
	"Shakuhachi",
	"Whistle",
	"Ocarina",
#  Synth Lead 
	"Lead 1 (square)",
	"Lead 2 (sawtooth)",
	"Lead 3 (calliope)",
	"Lead 4 (chiff)",
	"Lead 5 (charang)",
	"Lead 6 (voice)",
	"Lead 7 (fifths)",
	"Lead 8 (bass + lead)",
#  Synth Pad 
	"Pad 1 (new age)",
	"Pad 2 (warm)",
	"Pad 3 (polysynth)",
	"Pad 4 (choir)",
	"Pad 5 (bowed)",
	"Pad 6 (metallic)",
	"Pad 7 (halo)",
	"Pad 8 (sweep)",
#  Synth FM 
	"FX 1 (rain)",
	"FX 2 (soundtrack)",
	"FX 3 (crystal)",
	"FX 4 (atmosphere)",
	"FX 5 (brightness)",
	"FX 6 (goblins)",
	"FX 7 (echoes)",
	"FX 8 (sci-fi)",
#  Ethnic Instruments 
	"Sitar",
	"Banjo",
	"Shamisen",
	"Koto",
	"Kalimba",
	"Bag Pipe",
	"Fiddle",
	"Shanai",
#  Percussive Instruments 
	"Tinkle Bell",
	"Agogo",
	"Steel Drums",
	"Woodblock",
	"Taiko Drum",
	"Melodic Tom",
	"Synth Drum",
	"Reverse Cymbal",
#  Sound Effects 
	"Guitar Fret Noise",
	"Breath Noise",
	"Seashore",
	"Bird Tweet",
	"Telephone Ring",
	"Helicopter",
	"Applause",
	"Gunshot"
]


class MTMidiInstrument(MTScatterWidget):
	def __init__(self, **kwargs):
		super(MTMidiInstrument, self).__init__(**kwargs)
		self.do_scale=False
		self.do_rotation=False
		self.channel = kwargs['channel']
		self.midi_out = kwargs['midi_out']
		self.instrument = kwargs['instrument']
		
		self.midi_out.set_instrument(self.instrument, channel=self.channel)
		
		self.register_event_type('note_on')
		self.register_event_type('note_off')
		
		a = MTAnchorLayout(size=self.size, pos=(0,0))
		self.button = MTButton(label=MIDI_instruments[self.instrument], size=(180,80))
		self.button.connect('on_press', self.open_choose_instrument)
		a.add_widget(self.button)
		self.add_widget(a)
		
	
	def note_on(self, note):
		self.midi_out.note_on(note,127,self.channel)
	
	def note_off(self, note):
		self.midi_out.note_off(note,127,self.channel)

	def draw(self):
		#background
		set_color(0.6,0.6,0.6, 1)
		drawRoundedRectangle(
			pos = (0,0),
			size = self.size,
			radius = 10
		)

	def open_choose_instrument(self,*largs):
		w = self.get_parent_window()
		m = MTModalWindow()
		a = MTAnchorLayout(size=w.size)
		k = MTKineticList(size=(400, 500), searchable=False,
						  deletable=False, title="Instrument")

		def choose_instrument(item, name, *largs):
			w.remove_widget(m)
			self.instrument = MIDI_instruments.index(name)
			self.button.label = name
			self.midi_out.set_instrument(self.instrument, channel=self.channel)

		for x in MIDI_instruments:
			item = MTKineticItem(label=x, size=(400, 50))
			item.connect('on_press', curry(choose_instrument, item, x))
			k.add_widget(item)
		a.add_widget(k)
		m.add_widget(a)
		w.add_widget(m)
