import subprocess,shlex
import time
import logging
from .log_utils import setup_logging

setup_logging()
log = logging.getLogger(__name__)

class Runner():
	""" A class for running executables with arguments,
	save their output to file, then pass its instance
	to a collector.
	"""

	def __init__(self):
		log.info('Initialized new Runner instance %s', self)

	def produce_command(self, bin, input_fname, params, prefix=False):
		""" Produce command to run on a unix shell
		In: 
			bin:		executable (including path),
			input_fname:input file name,
			params:		parameters string,
			prefix:		adds './' prefix to command (unix style)
		
		Out: 
						command (string)
		"""
		run_prefix = ''
		if prefix:
			run_prefix = './'
		cmd_string = "{run_prefix}{bin} {input_fname} {params}" \
		.format(run_prefix=run_prefix, bin=bin, input_fname=input_fname,
				params=params)
		log.info("Produced command: '%s'", cmd_string)
		return cmd_string

	def run(self, cmd, timeout, parsed=False, exit_codes=(0,10,20)):
		""" Run command with subprocess.Popen
		In:
			cmd:		output of produce_command function
			timeout:	timeout in seconds
			parsed:		indicates if to parse command,
					 	e.g., 'ls -l' isn't parsed -
					 	which parsed as ['ls', '-l']
			exit_codes: tuple, skip selected process codes
					 	otherwise raise an exception
		Out:
						{process stdout (utf-8), 'timeout', None on error}
		"""
		if not parsed:
			cmd = shlex.split(cmd)

		try:
			log.info("Trying to run: %s", cmd)
			proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
									universal_newlines=True)		

			out, err = proc.communicate(timeout=timeout)

			# check exit code
			if proc.returncode not in exit_codes:
				raise subprocess.CalledProcessError(proc.returncode, cmd)

			log.info("Succeeded running: %s", cmd)
			return out

		except subprocess.TimeoutExpired as t:
			proc.kill()
			log.warn("Timeout: %lf sec expired for %s", t.timeout, cmd)
			return 'timeout'

		except subprocess.CalledProcessError as e:
			log.warn("Process error, return value: %s, stderr: %s", e.returncode, err, exc_info=True)
			return None

		except OSError as e:
			log.warn("OS Error, cannot run commmand: '%s'", cmd, exc_info=True)
			return None