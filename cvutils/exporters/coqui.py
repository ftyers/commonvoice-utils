import sys
import csv
import os
import subprocess
import unicodedata
from multiprocessing import Pool

from collections import Counter

FIELDNAMES = ["wav_filename", "wav_filesize", "transcript"]
SAMPLE_RATE = 16000
CHANNELS = 1
MAX_SECS = 10
PARAMS = None
FILTER_OBJ = None

# Increase maximum size of field in the csv processing 
# module (for TSVs with long fields)
csv.field_size_limit(sys.maxsize)

class LabelFilter:
	def __init__(self, normalise, alphabet, validator):
		self.normalise = normalise
		self.validator = validator
		self.alphabet = alphabet.get_alphabet()
		self.validate_fun = validator.validate

	def filter(self, label):
		#print('???', label)
		stuff = self.validator.check(label)
		label = self.validate_fun(label)
		#print('+++', label)
		#print('>>>', stuff)
		return label
	
class CoquiExporter:
	def __init__(self, validator, alphabet):
		self.validator = validator
		self.validate_label = validator.validate
		self.alphabet = alphabet
		try:
			import sox
		except ModuleNotFoundError:
			print('The CoquiExporter needs pysox installed.', file=sys.stderr)
			print('You can install it with: pip3 install sox', file=sys.stderr)
			return

	def get_counter(self):
		return Counter(
			{
				"all": 0,
				"failed": 0,
				"invalid_label": 0,
				"too_short": 0,
				"too_long": 0,
				"imported_time": 0,
				"total_time": 0,
			}
		)
	
	def get_imported_samples(self, counter):
		return (
			counter["all"]
			- counter["failed"]
			- counter["too_short"]
			- counter["too_long"]
			- counter["invalid_label"]
		)
	

	def init_worker(self):
		global FILTER_OBJ  # pylint: disable=global-statement
		FILTER_OBJ = LabelFilter(False, self.alphabet, self.validator)
	
	def one_sample(self, sample):
		""" Take an audio file, and optionally convert it to 16kHz WAV """
		mp3_filename = sample[0]
		if not os.path.splitext(mp3_filename.lower())[1] == ".mp3":
			mp3_filename += ".mp3"
		# Storing wav files next to the mp3 ones - just with a different suffix
		wav_filename = os.path.splitext(mp3_filename)[0] + ".wav"
		self._maybe_convert_wav(mp3_filename, wav_filename)
		file_size = -1
		frames = 0
		if os.path.exists(wav_filename):
			file_size = os.path.getsize(wav_filename)
			frames = int(
				subprocess.check_output(
					["soxi", "-s", wav_filename], stderr=subprocess.STDOUT
				)
			)
		label = FILTER_OBJ.filter(sample[1])
		rows = []
		counter = self.get_counter()
		if file_size == -1:
			# Excluding samples that failed upon conversion
			counter["failed"] += 1
		elif label is None:
			# Excluding samples that failed on label validation
			counter["invalid_label"] += 1
		elif int(frames / SAMPLE_RATE * 1000 / 10 / 2) < len(str(label)):
			# Excluding samples that are too short to fit the transcript
			counter["too_short"] += 1
		elif frames / SAMPLE_RATE > MAX_SECS:
			# Excluding very long samples to keep a reasonable batch-size
			counter["too_long"] += 1
		else:
			# This one is good - keep it for the target CSV
			rows.append((os.path.split(wav_filename)[-1], file_size, label, sample[2]))
			counter["imported_time"] += frames
		counter["all"] += 1
		counter["total_time"] += frames
	
		return (counter, rows)
	
	def _maybe_convert_set(self, 
		dataset,
		tsv_dir,
		audio_dir,
		filter_obj,
		space_after_every_character=None,
		rows=None,
		exclude=None,
	):
		exclude_transcripts = set()
		exclude_speakers = set()
		if exclude is not None:
			for sample in exclude:
				exclude_transcripts.add(sample[2])
				exclude_speakers.add(sample[3])
	
		if rows is None:
			rows = []
			input_tsv = os.path.join(os.path.abspath(tsv_dir), dataset + ".tsv")
			if not os.path.isfile(input_tsv):
				return rows
			print("Loading TSV file: ", input_tsv)
			# Get audiofile path and transcript for each sentence in tsv
			samples = []
			with open(input_tsv, encoding="utf-8") as input_tsv_file:
				reader = csv.DictReader(input_tsv_file, delimiter="\t")
				for row in reader:
					samples.append(
						(
							os.path.join(audio_dir, row["path"]),
							row["sentence"],
							row["client_id"],
						)
					)
	
			counter = self.get_counter()
			num_samples = len(samples)
	
			print("  Importing mp3 files...")
			pool = Pool(initializer=self.init_worker, initargs=())
			#bar = progressbar.ProgressBar(max_value=num_samples, widgets=SIMPLE_BAR)
			for i, processed in enumerate(
				pool.imap_unordered(self.one_sample, samples), start=1
			):
				counter += processed[0]
				rows += processed[1]
				#bar.update(i)
			#bar.update(num_samples)
			pool.close()
			pool.join()
	
			imported_samples = self.get_imported_samples(counter)
			assert counter["all"] == num_samples
			assert len(rows) == imported_samples
			self.print_import_report(counter, SAMPLE_RATE, MAX_SECS)
	
		output_csv = os.path.join(os.path.abspath(audio_dir), dataset + ".csv")
		print("  Saving new Coqui STT-formatted CSV file to: ", output_csv)
		with open(output_csv, "w", encoding="utf-8", newline="") as output_csv_file:
			print("  Writing CSV file for train.py as: ", output_csv)
			writer = csv.DictWriter(output_csv_file, fieldnames=FIELDNAMES)
			writer.writeheader()
			#bar = progressbar.ProgressBar(max_value=len(rows), widgets=SIMPLE_BAR)
			#for filename, file_size, transcript, speaker in bar(rows):
			for filename, file_size, transcript, speaker in rows:
				if transcript in exclude_transcripts or speaker in exclude_speakers:
					continue
				if space_after_every_character:
					writer.writerow(
						{
							"wav_filename": filename,
							"wav_filesize": file_size,
							"transcript": " ".join(transcript),
						}
					)
				else:
					writer.writerow(
						{
							"wav_filename": filename,
							"wav_filesize": file_size,
							"transcript": transcript,
						}
					)
		return rows

	def secs_to_hours(self, secs):
		hours, remainder = divmod(secs, 3600)
		minutes, seconds = divmod(remainder, 60)
		return "%d:%02d:%02d" % (hours, minutes, seconds)
	
	
	
	def print_import_report(self,counter, sample_rate, max_secs):
		print("  Imported %d samples." % (self.get_imported_samples(counter)))
		if counter["failed"] > 0:
			print("  Skipped %d samples that failed upon conversion." % counter["failed"])
		if counter["invalid_label"] > 0:
			print(
				"  Skipped %d samples that failed on transcript validation."
				% counter["invalid_label"]
			)
		if counter["too_short"] > 0:
			print(
				"  Skipped %d samples that were too short to match the transcript."
				% counter["too_short"]
			)
		if counter["too_long"] > 0:
			print(
				"  Skipped %d samples that were longer than %d seconds."
				% (counter["too_long"], max_secs)
			)
		print(
			"  Final amount of imported audio: %s from %s."
			% (
				self.secs_to_hours(counter["imported_time"] / sample_rate),
				self.secs_to_hours(counter["total_time"] / sample_rate),
			)
		)


	
	def _maybe_convert_wav(self, mp3_filename, wav_filename):
		if not os.path.exists(wav_filename):
			import sox
			transformer = sox.Transformer()
			transformer.convert(samplerate=SAMPLE_RATE, n_channels=CHANNELS)
			try:
				transformer.build(mp3_filename, wav_filename)
			except sox.core.SoxError:
				pass
	
	def _preprocess_data(self, tsv_dir, audio_dir, space_after_every_character=False):
		exclude = []
		for dataset in ["test", "dev", "train", "validated", "other"]:
			set_samples = self._maybe_convert_set(
				dataset, tsv_dir, audio_dir, space_after_every_character
			)
			if dataset in ["test", "dev"]:
				exclude += set_samples
			if dataset == "validated":
				self._maybe_convert_set(
					"train-all",
					tsv_dir,
					audio_dir,
					space_after_every_character,
					rows=set_samples,
					exclude=exclude,
				)
		
	def process(self, tsv_dir, audio_dir, space_after_every_character=False):
		self._preprocess_data(tsv_dir, audio_dir, space_after_every_character)
	
