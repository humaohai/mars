# Copyright 1999-2020 Alibaba Group Holding Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import os

from mars.learn.contrib.tensorflow import run_tensorflow_script
from mars.session import new_session
from mars.tests.core import ExecutorForTest

try:
    import tensorflow
except ImportError:
    tensorflow = None


@unittest.skipIf(tensorflow is None, 'tensorflow not installed')
class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.session = new_session().as_default()
        self._old_executor = self.session._sess._executor
        self.executor = self.session._sess._executor = \
            ExecutorForTest('numpy', storage=self.session._sess._context)

    def tearDown(self) -> None:
        self.session._sess._executor = self._old_executor

    def testLocalRunTensorFlowScript(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tf_distributed_sample.py')
        self.assertEqual(run_tensorflow_script(
            path, n_workers=2, command_argv=['multiple'],
            port=2222, run_kwargs={'n_parallel': 2}
        )['status'], 'ok')

        with self.assertRaises(ValueError):
            run_tensorflow_script(path, n_workers=0)

        with self.assertRaises(ValueError):
            run_tensorflow_script(path, 2, n_ps=-1)
