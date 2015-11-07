#!/usr/bin/env python

from unittest import TestCase

import os
import shutil
import filecmp
import andle
import andle.sdk
import andle.android
import andle.remote
import andle.gradle


class TestAndle(TestCase):
	CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))
	SDK_PATH = CURRENT_PATH + "/sdk"

	def test_sdk(self):
		"""
		sdk load data test
		"""
		data = andle.sdk.load(self.SDK_PATH)
		print(data)

		self.assertEqual(data['build-tools'], '23.0.1', "build-tools not correct")
		self.assertEqual(data['platforms'], '23', "platforms not correct")
		self.assertEqual(data['dependency']['com.google.android.gms:play-services'], '8.1.0', "depedency not correct")
		self.assertEqual(data['dependency']['com.android.support:appcompat-v7'], '23.0.1', "depedency not correct")

	def test_android(self):
		"""
		update project test
		"""
		data = andle.sdk.load(self.SDK_PATH)
		old = self.CURRENT_PATH + "/src/old.gradle"
		dest = self.CURRENT_PATH + "/dest/build.gradle"
		new = self.CURRENT_PATH + "/src/new.gradle"

		shutil.copyfile(old, dest)
		andle.android.update(self.CURRENT_PATH + "/dest", data)

		self.assertTrue(filecmp.cmp(dest, new), "not change")

	def test_remote(self):
		"""
		remote maven test
		"""
		value = andle.remote.load("com.facebook.android:facebook-android-sdk",
								  "file://" + self.CURRENT_PATH + "/remote/")
		self.assertEqual(value, "4.7.0", "version not match")

	def test_gradle(self):
		"""
		gradle version test
		"""
		value = andle.gradle.load("file://" + self.CURRENT_PATH + "/gradle/version")
		self.assertEqual(value, "2.8", "version not match")
