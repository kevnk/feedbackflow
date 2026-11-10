"""show_notification() must pass its text to osascript as data, never through a
shell. A stub `osascript` on PATH records its arguments; no notification shows.

    python3 -m unittest discover -s tests
"""
import importlib.util
import os
import platform
import shutil
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = ['add_feedback_to_composer.py', 'watch_and_add_feedback.py']


def load(name):
    spec = importlib.util.spec_from_file_location(name[:-3], os.path.join(ROOT, 'scripts', name))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@unittest.skipUnless(platform.system() == 'Darwin', 'macOS notification path')
class NotificationTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir)
        self.argv_log = os.path.join(self.dir, 'argv')
        stub = os.path.join(self.dir, 'osascript')
        with open(stub, 'w') as f:
            f.write(f'#!/bin/sh\nfor a in "$@"; do printf "%s\\0" "$a"; done > "{self.argv_log}"\n')
        os.chmod(stub, 0o755)
        old_path = os.environ['PATH']
        os.environ['PATH'] = f'{self.dir}:/usr/bin:/bin'
        self.addCleanup(os.environ.__setitem__, 'PATH', old_path)

    def test_quotes_in_text_stay_text(self):
        title = 'Feedback "Flow"'
        for script in SCRIPTS:
            with self.subTest(script=script):
                pwned = os.path.join(self.dir, 'pwned-' + script)
                message = f"done'; touch {pwned}; echo '"
                load(script).show_notification(title, message)
                self.assertFalse(os.path.exists(pwned))
                with open(self.argv_log) as f:
                    argv = f.read().split('\0')[:-1]
                self.assertEqual(argv[-2:], [title, message])


if __name__ == '__main__':
    unittest.main()
