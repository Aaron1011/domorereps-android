ANDROIDSDK=~/android-tools/adt-bundle-linux-x86_64-20130514/sdk
ANDROIDNDK=~/android-tools/android-ndk-r8e
PYTHON_DIST_PATH=~/python-for-android/dist/default

PATH=$ANDROIDNDK:$ANDROIDSDK/tools:$PATH

BUILD_TYPE=release
VERSION=$1

if [ -z "$ANDROIDSDK" ]; then export ANDROIDSDK=~/Downloads/adt-bundle-linux-x86_64-20130219/sdk/; fi
if [ -z "$ANDROIDAPI" ]; then export ANDROIDAPI=8; fi
if [ -z "$ANDROIDNDK" ]; then export ANDROIDNDK=~/Downloads/android-ndk-r8e; fi
if [ -z "$ANDROIDNDKVER" ]; then export ANDROIDNDKVER=8; fi

if [ -z "$PYTHON_DIST_PATH" ]; then export PYTHON_DIST_PATH=~/Documents/kivy/python-for-android/dist/default/; fi

if [ -z "$BUILD_TYPE" ]; then export BUILD_TYPE=debug; fi
if [ -z "$VERSION" ]; then export VERSION="1.0.0"; fi

cd ~/python-for-android/dist/default
echo $VERSION
python build.py --dir ~/domorereps-android/ --package org.domorereps.domorereps --name "Do More Reps" --version $VERSION --orientation portrait --permission INTERNET $BUILD_TYPE release
