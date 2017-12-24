# -*- coding: utf-8 -*-

from .context import sampler
from sampler import *
import unittest
from unittest.mock import Mock, patch

class RunnerTestSuite(unittest.TestCase):
	"""Runner test cases."""
	def setUp(self):
		self.instance = Runner()
		self.bin = 'minisat'
		self.input_fname = 'tests/check.cnf'
		self.params = '-var-decay=0.9'
		self.cmd = self.instance.produce_command(self.bin, 
												self.input_fname, 
												self.params, prefix=False)
		self.stdout_file = open('tests/check.cnf.out')

	def test_produce_command(self):
		correct_cmd = 'minisat tests/check.cnf -var-decay=0.9'
		self.assertEqual(self.cmd, correct_cmd)

	def test_popen_with_mock(self):
		correct_out = self.stdout_file.read()
		out = self.instance.run(self.cmd)
		self.assertEqual(correct_out, out)

	def test_popen_with_ls(self):
		cmd = 'ls -l'
		out = self.instance.run(cmd)

if __name__ == '__main__':
	unittest.main()