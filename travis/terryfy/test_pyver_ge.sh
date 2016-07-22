# Test python version comparison utility
if [ -n "$(pyver_ge 2.7.8 3.4.0)" ]; then RET=1; fi
if [ -z "$(pyver_ge 3.8.2 3.4.0)" ]; then RET=1; fi
if [ -n "$(pyver_ge 3.3.8 3.4.0)" ]; then RET=1; fi
if [ -z "$(pyver_ge 2.7.8 2.6.9)" ]; then RET=1; fi
if [ -z "$(pyver_ge 3.4.0 3.4.0)" ]; then RET=1; fi
if [ -n "$(pyver_ge 3.4.0 3.4.1)" ]; then RET=1; fi
if [ -n "$(pyver_ge 2.1.1 3.0.0)" ]; then RET=1; fi
if [ -n "$(pyver_ge 3.0.0 3.0.1)" ]; then RET=1; fi
if [ -n "$(pyver_ge 3.0.1 3.1.0)" ]; then RET=1; fi
