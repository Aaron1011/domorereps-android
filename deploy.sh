export ANDROIDSDK=~/Downloads/adt-bundle-linux-x86_64-20130219/sdk/
export ANDROIDAPI=8
export ANDROIDNDK=~/Downloads/android-ndk-r8e
export ANDROIDNDKVER=8

export PYTHON_DIST_PATH=~/Documents/kivy/python-for-android/dist/default/

cd $PYTHON_DIST_PATH
./build.py --dir ~/repos/domorereps-android/ --package org.domorereps.domorereps --name "Do More Reps" --version 1.0.0 --orientation portrait --permission INTERNET debug installd
