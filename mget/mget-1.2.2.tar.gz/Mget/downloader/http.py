#!/usr/bin/env python3

import time
from . import FileDownloader
from ..utils import common, DownloadError, ContentTooShortError

class MGetDownloader(FileDownloader):
	def __init__(self, urlObj, fileObj, info):
		FileDownloader.__init__(self)

		self.info = info
		self.urlObj = urlObj
		self.fileObj = fileObj
		self.start_time = info.get('start_time')
		self.filename = info.get('filename')
		self.cursize = int(info.get('cursize'))
		self.filesize = info.get('filesize', -1)
		self.expected = info.get('expected', -1)
		self.chunk = info.get('buffersize', 1024)
		self.quit_size = info.get('quit_size', 100.0)

		self.resume_len = self.cursize
		self.remaining = (self.expected - self.resume_len)

	def start(self):
		while True:
			if self.quit_size != 100.0 and self._progress() >= self.quit_size:
				if self.info.get('debug_mget'):
					common._stderr('')
					common.report("Quit size reached!")
				break

			get_time = time.time()
			buffer = self.urlObj.read(self.chunk if self.chunk > 1024 else 1024)
			end_time = time.time()

			if len(buffer) == 0: 
				if self.info.get('debug_mget'):
					common._stderr('')
					common.report("Buffer == 0!")
				break

			try: self.fileObj.write(buffer)
			except (IOError, OSError) as err: detail.report_error(err); break

			self.cursize += len(buffer)
			if self.info.get('buffersize') == 1024 and not self.info.get('noresize'):
				self.chunk = self.best_block_size(end_time - get_time, len(buffer))

			args = {'s_dif': time.time() - self.start_time,
				'progress': self.progress(self.cursize,self.filesize),
				'bytes': len(buffer), 'dif': end_time - get_time}

			self._progress_bar(**args)

		if self._progress() >= self.quit_size: return True
		else: raise ContentTooShortError(self.cursize,self.info.get('expected'))
