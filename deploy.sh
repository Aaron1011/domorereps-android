$ANDROIDSDK || export ANDROIDSDK=~/Downloads/adt-bundle-linux-x86_64-20130219/sdk/
$ANDROIDAPI || export ANDROIDAPI=8
$ANDROIDNDK || export ANDROIDNDK=~/Downloads/android-ndk-r8e
$ANDROIDNDKVER || export ANDROIDNDKVER=8

$PYTHON_DIST_PATH || export PYTHON_DIST_PATH=~/Documents/kivy/python-for-android/dist/default/

$BUILD_TYPE || export BUILD_TYPE=debug

cd $PYTHON_DIST_PATH

./build.py --dir ~/repos/domorereps-android/ --package org.domorereps.domorereps --name "Do More Reps" --version 1.0.0 --orientation portrait --permission INTERNET $BUILD_TYPE installd
