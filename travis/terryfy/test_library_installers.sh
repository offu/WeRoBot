# Check library installer routines

# Re-create testing directory
rm -rf library-testing
mkdir library-testing

# terryfy directory location
source library_installers.sh
terryfy_pwd=$PWD
if [[ $TERRYFY_DIR != $terryfy_pwd ]]; then
    echo "TERRYFY_DIR != $terryfy_pwd"
    RET=1
fi

# Still correct after changing directory?
cd library-testing
# terryfy directory location
source ../library_installers.sh
if [[ $TERRYFY_DIR != $terryfy_pwd ]]; then
    echo "TERRYFY_DIR != $terryfy_pwd"
    RET=1
fi

# prefixes
set_32_prefix
if [[ $ARCH_FLAGS != '-arch i386' ]]; then
    echo "ARCH_FLAGS != '-arch i386"
    RET=1
fi
if [[ $CPATH != $PWD/build32/include ]]; then
    echo "CPATH is $CPATH, should be $PWD/build32/include"
    RET=1
fi
set_64_prefix
if [[ $ARCH_FLAGS != '-arch x86_64' ]]; then
    echo "ARCH_FLAGS != '-arch x86_64"
    RET=1
fi
if [[ $CPATH != $PWD/build64/include ]]; then
    echo "CPATH is $CPATH, should be $PWD/build64/include"
    RET=1
fi
set_dual_prefix
if [[ $ARCH_FLAGS != '-arch i386 -arch x86_64' ]]; then
    echo "ARCH_FLAGS != '-arch i386 -arch x86_64"
    RET=1
fi
if [[ $CPATH != $PWD/build/include ]]; then
    echo "CPATH is $CPATH, should be $PWD/build64/include"
    RET=1
fi

# Clean up after
cd ..
rm -rf library-testing
