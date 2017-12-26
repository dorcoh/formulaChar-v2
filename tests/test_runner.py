# -*- coding: utf-8 -*-

from .context import sampler
from sampler import *
import unittest
import subprocess

class RunnerTestSuite(unittest.TestCase):
	"""Runner test cases."""
	def sample_command(self):
		bin = 'minisat'
		input_fname = 'tests/check.cnf'
		params = '-var-decay=0.9'
		# produce command call
		cmd = self.instance.produce_command(bin, input_fname, params, prefix=False)
		return cmd

	def setUp(self):
		# create instance
		self.instance = Runner()
	

	def test_produce_command(self):
		cmd = self.sample_command()
		correct_cmd = 'minisat tests/check.cnf -var-decay=0.9'
		self.assertEqual(cmd, correct_cmd)

	# FAILS
	# still exit status 10 somehow..
	def test_run_with_correct_stdout_file(self):
		stdout_file = open('tests/check.cnf.out')
		correct_out = stdout_file.read()
		cmd = self.sample_command()
		out = self.instance.run(cmd, timeout=10)
		self.assertEqual(correct_out, out)

	def test_run_with_ls(self):
		cmd = 'ls -l'
		out = self.instance.run(cmd, timeout=10)
	
	def test_run_file_not_found(self):
		cmd = 'wee'
		out = self.instance.run(cmd, timeout=10, parsed=True)
		self.assertRaises(OSError)
		self.assertEqual(None, out)
	
	def test_run_expired_timeout(self):
		args = ['echo', 'hello world']
		out = self.instance.run(args, timeout=0, parsed=True)
		self.assertRaises(subprocess.TimeoutExpired)

	def test_run_nonzero_exit_status(self):
		args = ['minisat', 'wee']
		timeout = 10
		out = self.instance.run(args, timeout, parsed=True)
		self.assertRaises(subprocess.CalledProcessError)

if __name__ == '__main__':
	unittest.main()