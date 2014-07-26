#!/usr/bin/env python3

import time
from . import FileDownloader
from ..utils import (common, details, DownloadError, ContentTooShortError)

class MGetDownloader(FileDownloader):
	def __init__(self, urlObj, fileObj, info):
		FileDownloader.__init__(self)

		self.info = info
		self.urlObj = urlObj
		self.fileObj = fileObj
		self.mode = info.get('open_mode')
		self.start_time = info.get('start_time')
		self.filename = info.get('filename')
		self.cursize = int(info.get('cursize'))
		self.filesize = self.expected = info.get('filesize', -1)
		self.chunk = info.get('buffersize', 1024)
		self.quit_size = info.get('quit_size', 100.0)

		self.resume_len = self.cursize
		self.remaining = (self.filesize - self.resume_len)

	def start(self):
		while True:
			if self.quit_size != 100.0 and self.get_progress() * 100.0 >= self.quit_size:
				if self.info.get('debug_mget'):
					details._stderr('')
					details.report("Quit size reached!")
				break

			get_time = time.time()
			buffer = self.urlObj.read(self.chunk if self.chunk > 1024 else 1024)
			end_time = time.time()

			if len(buffer) == 0: 
				if self.info.get('debug_mget'):
					details._stderr('')
					details.report("Buffer == 0!")
				break

			try: self.fileObj.write(buffer)
			except (IOError, OSError) as err: detail.report_error(err); break

			self.cursize += len(buffer)
			if self.info.get('buffersize') == 1024 and not self.info.get('noresize'):
				self.chunk = common.best_block_size(end_time - get_time, len(buffer))

			self._progress_bar(**{	's_dif': time.time() - self.start_time,
						'progress': self.get_progress(),
						'bytes': len(buffer),
						'dif': end_time - get_time})

		if self.get_progress() * 100.0 >= self.quit_size: return True
		else: raise ContentTooShortError(self.cursize,self.info.get('expected'))
