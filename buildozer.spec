[app]
title = Guess The Flag
package.name = guess_the_flag
package.domain = org.ibrahim
source.dir = .
source.include_exts = py,png,jpg,kv
version = 0.1
requirements = python3,kivy,requests
orientation = portrait

[buildozer]
android.ndk_path = /opt/android-ndk
android.sdk_path = /opt/android-sdk
android.api = 31
android.minapi = 21
android.archs = arm64-v8a,armeabi-v7a
