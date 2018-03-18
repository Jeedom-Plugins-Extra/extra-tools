# -*- coding: utf-8 -*-
import os
import shutil
import tempfile
import unittest

from libs.FeaturesMenu import FeaturesMenu
from libs.MethodData import MethodData


class TestFonctionnalitiesMenu(unittest.TestCase):
    test_dir = None
    empty_file_path = None
    class_file_path = None
    empty_class_path = None
    fonc_menu = None
    no_file_path = None
    method_data = None

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.empty_file_path = self.test_dir + os.sep + 'empty.php'
        self.empty_class_file_path = self.test_dir + os.sep + 'empty_class.php'
        self.class_file_path = self.test_dir + os.sep + 'class.php'
        self.no_file_path = self.test_dir + os.sep + 'no_file.php'
        with open(self.class_file_path, 'w') as class_file:
            class_file.write('<?php\n\n')
            class_file.write('class TestClass\n{\n')
            class_file.write('public function testMethod()\n{\n}\n')
            class_file.write('}\n')
        with open(self.empty_class_file_path, 'w') as class_file:
            class_file.write('<?php\n\n')
            class_file.write('class EmptyClass\n{\n')
            class_file.write('}\n')
        self.method_data = MethodData()
        self.method_data.class_name = 'TestClass'
        self.method_data.method_name = 'testMethod'
        self.fonc_menu = FeaturesMenu(self.test_dir, 'TestClass')

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_check_class_with_empty_file(self):
        result = self.fonc_menu.check_class(self.empty_file_path, 'TestClass')
        self.assertFalse(result)

    def test_check_class_without_file(self):
        result = self.fonc_menu.check_class(self.no_file_path, 'TestClass')
        self.assertFalse(result)

    def test_check_class_with_class(self):
        result = self.fonc_menu.check_class(self.class_file_path, 'TestClass')
        self.assertTrue(result)

    def test_check_if_method_exists_with_empty_file(self):
        result = self.fonc_menu.check_class(self.empty_file_path, 'TestClass')
        self.assertFalse(result)

    def test_check_if_method_exists_without_file(self):
        result = self.fonc_menu.check_class(self.no_file_path, 'TestClass')
        self.assertFalse(result)

    def test_check_if_method_exists_class_with_the_method(self):
        result = self.fonc_menu.check_class(self.class_file_path, 'TestClass')
        self.assertTrue(result)

    def test_check_if_method_exists_class_without(self):
        result = self.fonc_menu.check_class(self.empty_class_file_path,
                                            'TestClass')
        self.assertFalse(result)

    def test_write_class_with_file_doesnt_exists(self):
        result = self.fonc_menu.write_class(self.no_file_path, 'TestClass')
        content = ''
        with open(self.no_file_path, 'r') as file_content:
            content = file_content.read()
        self.assertTrue(result)
        self.assertIn('class TestClass', content)
        self.assertIn('<?php', content)

    def test_write_class_with_empty(self):
        result = self.fonc_menu.write_class(self.empty_file_path, 'TestClass')
        content = ''
        with open(self.empty_file_path, 'r') as file_content:
            content = file_content.read()
        self.assertTrue(result)
        self.assertIn('class TestClass', content)

    def test_write_class_with_class(self):
        result = self.fonc_menu.write_class(self.class_file_path, 'TestClass2')
        content = ''
        with open(self.class_file_path, 'r') as file_content:
            content = file_content.read()
        self.assertTrue(result)
        self.assertIn('class TestClass', content)
        self.assertIn('class TestClass2', content)

    def test_write_method_in_class_with_empty(self):
        self.method_data.class_file_path = self.empty_file_path
        result = self.fonc_menu.write_method_in_class(self.method_data)
        self.assertFalse(result)

    def test_write_method_in_class_without_file(self):
        self.method_data.class_file_path = self.no_file_path
        result = self.fonc_menu.write_method_in_class(self.method_data)
        self.assertFalse(result)

    def test_write_method_in_class_with_empty_class(self):
        self.method_data.class_file_path = self.empty_class_file_path
        self.method_data.class_name = 'EmptyClass'
        result = self.fonc_menu.write_method_in_class(self.method_data)
        content = ''
        with open(self.empty_class_file_path, 'r') as file_content:
            content = file_content.read()
        self.assertTrue(result)
        self.assertIn('testMethod', content)

    def test_write_method_in_class_with_not_empty_class(self):
        self.method_data.class_file_path = self.class_file_path
        self.method_data.class_name = 'TestClass'
        self.method_data.method_name = 'testMethod2'
        result = self.fonc_menu.write_method_in_class(self.method_data)
        content = ''
        with open(self.class_file_path, 'r') as file_content:
            content = file_content.read()
        self.assertTrue(result)
        self.assertIn('testMethod', content)
        self.assertIn('testMethod2', content)

    def test_write_method_in_class_static_method(self):
        self.method_data.class_file_path = self.class_file_path
        self.method_data.method_is_static = True
        self.method_data.method_name = 'testMethod2'
        result = self.fonc_menu.write_method_in_class(self.method_data)
        content = ''
        with open(self.class_file_path, 'r') as file_content:
            content = file_content.read()
        self.assertTrue(result)
        self.assertIn('static function testMethod2', content)

    def test_write_method_in_class_private_method(self):
        self.method_data.class_file_path = self.class_file_path
        self.method_data.method_visibility = 'private'
        self.method_data.method_name = 'testMethod2'
        result = self.fonc_menu.write_method_in_class(self.method_data)
        content = ''
        with open(self.class_file_path, 'r') as file_content:
            content = file_content.read()
        self.assertTrue(result)
        self.assertIn('private function testMethod2', content)

    def test_write_method_in_class_protected_static_method(self):
        self.method_data.class_file_path = self.class_file_path
        self.method_data.method_is_static = True
        self.method_data.method_visibility = 'protected'
        self.method_data.method_name = 'testMethod2'
        result = self.fonc_menu.write_method_in_class(self.method_data)
        content = ''
        with open(self.class_file_path, 'r') as file_content:
            content = file_content.read()
        self.assertTrue(result)
        self.assertIn('protected static function testMethod2', content)
