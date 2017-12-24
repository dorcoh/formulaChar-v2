import subprocess,shlex
from threading import Timer

class Runner():
	"""
	A class for running binaries with arguments,
	and save their stdout to file
	"""
	def __init__(self):
		pass

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
		return cmd_string

	def run(self, cmd):
		"""
			Run command with subprocess module
			In:
				cmd - output of produce_command function
				timeout - timeout in seconds
			Out:
				Returns output (stdout) in utf-8

		"""
		split_string = shlex.split(cmd)
		proc = subprocess.Popen(split_string, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		# handle output
		if proc.poll():
			raise RuntimeError("Failed to terminate")
		out, err = proc.communicate()
		return out.decode()

