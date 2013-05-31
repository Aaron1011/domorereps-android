PYTHON_DIST_PATH=~/python-for-android/dist/default

VERSION=$1
BUILD_TYPE=$2
INSTALL_TYPE=$3

ANDROIDSDK=$4
ANDROIDNDK=$5

REPO_PATH=$6

if [ -z "$ANDROIDSDK" ]; then export ANDROIDSDK=/home/$USER/android-tools/adt-bundle-linux-x86_64-20130514/sdk; fi
if [ -z "$ANDROIDAPI" ]; then export ANDROIDAPI=8; fi
if [ -z "$ANDROIDNDK" ]; then export ANDROIDNDK=/home/$USER/android-tools/android-ndk-r8e; fi
if [ -z "$ANDROIDNDKVER" ]; then export ANDROIDNDKVER=8; fi

if [ -z "$PYTHON_DIST_PATH" ]; then export PYTHON_DIST_PATH=~/Documents/kivy/python-for-android/dist/default/; fi

if [ -z "$BUILD_TYPE" ]; then export BUILD_TYPE=debug; fi
if [ -z "$VERSION" ]; then export VERSION="1.0.0"; fi
if [ -z "$INSTALL_TYPE" ]; then export INSTALL_TYPE=installr; fi
if [ -z "$REPO_PATH" ]; then export REPO_PATH="~/domorereps-android"; fi

PATH=$ANDROIDNDK:$ANDROIDSDK/tools:$PATH

cd ~/python-for-android/dist/default
echo $VERSION
python build.py --dir $REPO_PATH --package org.domorereps.domorereps --name "Do More Reps" --version $VERSION --orientation portrait --permission INTERNET $BUILD_TYPE $INSTALL_TYPE
