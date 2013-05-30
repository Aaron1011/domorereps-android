ANDROIDSDK="~/Downloads/adt-bundle-linux-x86_64-20130514/sdk"
ANDROIDNDK="~/Downloads/android-ndk-r8e"
PYTHON_DIST_PATH="~/python-for-android/dist/default"

PATH=$ANDROIDNDK:$ANDROIDSDK/tools:$PATH;

BUILD_TYPE=debug;

./build.sh 1.0.0 debug installr ~/Downloads/adt-bundle-linux-x86_64-20130219/sdk/ ~/Downloads/android-ndk-r8e `pwd`
