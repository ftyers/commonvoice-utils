# Copyright (c) 2020, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# Copyright (c) 2020, SeanNaren.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#	 http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# To convert mp3 files to wav using sox, you must have installed sox with mp3 support
# For example sudo apt-get install libsox-fmt-mp3
import csv
import json
import logging
import multiprocessing
import os
import subprocess
import sys
import tarfile
from multiprocessing.pool import ThreadPool
from pathlib import Path
from typing import List

import sox
from sox import Transformer
from tqdm import tqdm

class NemoExporter:
	def __init__(self, validator, alphabet):
		self.validator = validator
		self.validate_label = validator.validate
		self.alphabet = alphabet
		try:
			import sox
		except ModuleNotFoundError:
			print('The NemoExporter needs pysox installed.', file=sys.stderr)
			print('You can install it with: pip3 install sox', file=sys.stderr)
			return

	
	def create_manifest(self, data: List[tuple], output_name: str, manifest_path: str):
		output_file = Path(manifest_path) / output_name
		output_file.parent.mkdir(exist_ok=True, parents=True)
	
		with output_file.open(mode='w') as f:
			for wav_path, duration, text in tqdm(data, total=len(data)):
				if wav_path != '':
					# skip invalid input files that could not be converted
					f.write(
						json.dumps({'audio_filepath': os.path.abspath(wav_path), "duration": duration, 'text': text})
						+ '\n'
					)
	
	
	def process_files(self, tsv_file, data_root, num_workers):
		""" Read *.csv file description, convert mp3 to wav, process text.
			Save results to data_root.
	
		Args:
			tsv_file: str, path to *.csv file with data description, usually start from 'cv-'
			data_root: str, path to dir to save results; wav/ dir will be created
		"""
		wav_dir = os.path.join(data_root, 'wav/')
		os.makedirs(wav_dir, exist_ok=True)
		audio_clips_path = os.path.dirname(tsv_file) + '/clips/'
	
		def process(x):
			file_path, text = x
			file_name = os.path.splitext(os.path.basename(file_path))[0]
			text = text.lower().strip()
			audio_path = os.path.join(audio_clips_path, file_path)
			if os.path.getsize(audio_path) == 0:
				logging.warning(f'Skipping empty audio file {audio_path}')
				return '', '', ''
	
			output_wav_path = os.path.join(wav_dir, file_name + '.wav')
	
			if not os.path.exists(output_wav_path):
				tfm = Transformer()
				tfm.rate(samplerate=16000)
				tfm.channels(n_channels=1)
				tfm.build(input_filepath=audio_path, output_filepath=output_wav_path)
	
			duration = sox.file_info.duration(output_wav_path)
			return output_wav_path, duration, text
	
		logging.info('Converting mp3 to wav for {}.'.format(tsv_file))
		with open(tsv_file) as csvfile:
			reader = csv.DictReader(csvfile, delimiter='\t')
			next(reader, None)  # skip the headers
			data = []
			for row in reader:
				file_name = row['path']
				# add the mp3 extension if the tsv entry does not have it
				if not file_name.endswith('.mp3'):
					file_name += '.mp3'
				
				label = self.validator.validate(row['sentence'])
				if label:
					data.append((file_name, label))
			with ThreadPool(num_workers) as pool:
				data = list(tqdm(pool.imap(process, data), total=len(data)))
		return data
	
	def main(self, tsv_dir):
		logging.basicConfig(level=logging.INFO)
	
		manifest_dir = tsv_dir
	
		if os.path.exists(tsv_dir):
			logging.info('Find existing folder {}'.format(tsv_dir))
		else: 
			logging.info('Folder {} not found'.format(tsv_dir))
	
		for tsv_file in ['test.tsv', 'dev.tsv', 'train.tsv']:
			data = self.process_files(
				tsv_file=os.path.join(tsv_dir, tsv_file),
				data_root=os.path.join(tsv_dir, os.path.splitext(tsv_file)[0]),
				num_workers=multiprocessing.cpu_count()
			)
			logging.info('Creating manifests...')
			self.create_manifest(
				data=data,
				output_name=f'commonvoice_{os.path.splitext(tsv_file)[0]}_manifest.json',
				manifest_path=manifest_dir,
			)
	
	def process(self, tsv_dir, audio_dir):
		self.main(tsv_dir)

