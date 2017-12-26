import subprocess,shlex
from threading import Timer
import logging
from .log_utils import setup_logging

setup_logging(default_level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Runner():
	"""
	A class for running binaries with arguments,
	and save their stdout to file
	"""
	def __init__(self):
		logger.info('Initialized new Runner instance %s', self)

	def produce_command(self, bin, input_fname, params, prefix=False):
		"""
			Produce command to run on a unix shell
			In: 
				bin - executable (including path),
				input_fname - input file name,
				params - parameters string,
				prefix - adds ./ to command (unix style)
						 needed only when bin in same dir as script
			Out: 
				command to run
		"""
		run_prefix = ''
		if prefix:
			run_prefix = './'
		cmd_string = "{run_prefix}{bin} {input_fname} {params}" \
		.format(run_prefix=run_prefix, bin=bin, input_fname=input_fname,
				params=params)
		logger.debug("Produced command: '%s'", cmd_string)
		return cmd_string

	def run(self, cmd, timeout, parsed=False):
		"""
			Run command with subprocess Popen

			In:
				cmd - output of produce_command function
			Out:
				output (stdout) in utf-8
				'timeout' on timeout
				None on error

		"""
		if not parsed:
			cmd = shlex.split(cmd)

		try:
			logger.info("Trying to run: %s", cmd)
			proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
									universal_newlines=True)
			
			out, err = proc.communicate(timeout=timeout)
			
			# check return code
			if proc.returncode:
				raise subprocess.CalledProcessError(proc.returncode, cmd)

			logger.info("Succeeded running: %s", cmd)
			return out

		except subprocess.TimeoutExpired as t:
			proc.kill()
			logger.warn("Timeout: %lf sec expired for %s", t.timeout, cmd)
			return 'timeout'

		except subprocess.CalledProcessError as e:
			logger.warn("Terminated with return value: %s", e.returncode, exc_info=True)
			return None

		except OSError as e:
			logger.warn("Cannot run commmand: '%s'", cmd, exc_info=True)
			return None

		# if reached here it's an error
		logger.warn("Cannot run commmand: '%s'", cmd)
		return None



