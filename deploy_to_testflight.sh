ssh ubuntu@50.16.231.161 /bin/sh << 'EOF'
. ./secrets.sh;
#. ./vars.sh

cd ~/domorereps-android
git pull
cd ~/

ANDROIDSDK=~/android-tools/adt-bundle-linux-x86_64-20130514/sdk;
ANDROIDNDK=~/android-tools/android-ndk-r8e;
PYTHON_DIST_PATH=~/python-for-android/dist/default;

PATH=$ANDROIDNDK:$ANDROIDSDK/tools:$PATH;

BUILD_TYPE=release;

~/domorereps-android/deploy.sh

jarsigner -verbose -keypass $KEYSTORE_PASS -storepass $KEYSTORE_PASS -sigalg SHA1withRSA -digestalg SHA1 -keystore ~/.my-keystore.keystore ~/python-for-android/dist/default/bin/DoMoreReps-1.0.0-release-unsigned.apk mykey;

zipalign -f -v 4 ~/python-for-android/dist/default/bin/DoMoreReps-1.0.0-release-unsigned.apk DoMoreReps.apk;

curl "http://testflightapp.com/api/builds.json" \
  -F file=@DoMoreReps.apk \
  -F api_token="$TESTFLIGHT_API_TOKEN" \
  -F team_token="$TESTFLIGHT_TEAM_TOKEN" \
  -F notes="`git --git-dir=/home/$USER/domorereps-android/.git log -1 --pretty=%B`" \
  -F notify=True \
  -F distribution_lists='Testers'

EOF
