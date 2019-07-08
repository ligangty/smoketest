#!/usr/bin/env python2
#
# Copyright (C) 2011-2018 Red Hat, Inc. (https://github.com/Commonjava)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


from setuptools import setup
import sys

# handle python 3
if sys.version_info >= (3,):
    use_2to3 = True
else:
    use_2to3 = False

setup(
    zip_safe=True,
    use_2to3=use_2to3,
    name='repochange',
    version='0.0.1',
    long_description='Test if repo change log can be popagated successfully between indy and auditquery',
    keywords='indy maven build java',
    author='Gang Li',
    author_email='gli@redhat.com',
    url='https://github.com/ligangty/smoketest',
    license='APL2',
    install_requires=[
      "requests"
    ]
)
