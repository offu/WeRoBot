# Tests for manylinux utils

# cpython path calculator
[ "$(cpython_path 2.6)" == "/opt/python/cp26-cp26mu" ] || ingest "cp 2.6"
[ "$(cpython_path 2.6 32)" == "/opt/python/cp26-cp26mu" ] || ingest "cp 2.6 32"
[ "$(cpython_path 2.6 16)" == "/opt/python/cp26-cp26m" ] || ingest "cp 2.6 16"
[ "$(cpython_path 2.7)" == "/opt/python/cp27-cp27mu" ] || ingest "cp 2.7"
[ "$(cpython_path 2.7 32)" == "/opt/python/cp27-cp27mu" ] || ingest "cp 2.7 32"
[ "$(cpython_path 2.7 16)" == "/opt/python/cp27-cp27m" ] || ingest "cp 2.7 16"
[ "$(cpython_path 3.3)" == "/opt/python/cp33-cp33m" ] || ingest "cp 3.3"
[ "$(cpython_path 3.3 32)" == "/opt/python/cp33-cp33m" ] || ingest "cp 3.3 32"
[ "$(cpython_path 3.3 16)" == "/opt/python/cp33-cp33m" ] || ingest "cp 3.3 16"
[ "$(cpython_path 3.4)" == "/opt/python/cp34-cp34m" ] || ingest "cp 3.4"
[ "$(cpython_path 3.4 32)" == "/opt/python/cp34-cp34m" ] || ingest "cp 3.4 32"
[ "$(cpython_path 3.4 16)" == "/opt/python/cp34-cp34m" ] || ingest "cp 3.4 16"
[ "$(cpython_path 3.5)" == "/opt/python/cp35-cp35m" ] || ingest "cp 3.5"
[ "$(cpython_path 3.5 32)" == "/opt/python/cp35-cp35m" ] || ingest "cp 3.5 32"
[ "$(cpython_path 3.5 16)" == "/opt/python/cp35-cp35m" ] || ingest "cp 3.5 16"
