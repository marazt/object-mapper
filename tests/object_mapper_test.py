# Copyright (C) 2015, marazt. All rights reserved.
import unittest

from datetime import datetime
from mapper.object_mapper import ObjectMapper
from mapper.object_mapper_exception import ObjectMapperException


class ToTestClass:
    def __init__(self):
        self.name = ''
        self.date = ''
        pass


class ToTestClassTwo:
    def __init__(self):
        self.all = ''
        pass


class ToTestClassEmpty:
    def __init__(self):
        pass


class FromTestClass:
    def __init__(self):
        self.name = "Igor"
        self.surname = "Hnizdo"
        self.date = datetime(2015, 1, 1, 0, 0)
        pass


class ObjectMapperTest(unittest.TestCase):
    """
    Unit tests for the `ObjectMapper` module.
    """

    def setUp(self):
        pass

    def test_mapping_creation_without_mappings_correct(self):

        # Arrange
        from_class = FromTestClass()
        mapper = ObjectMapper()
        mapper.create_map(FromTestClass, ToTestClass)

        # Act
        result = mapper.map(FromTestClass(), ToTestClass)

        # Assert
        self.assertTrue(isinstance(result, ToTestClass), "Target types must be same")
        self.assertEqual(result.name, from_class.name, "Name mapping must be equal")
        self.assertEqual(result.date, from_class.date, "Date mapping must be equal")
        self.assertNotIn('surname', result.__dict__, "To class must not contain surname")

    def test_mapping_creation_with_mappings_correct(self):

        # Arrange
        from_class = FromTestClass()
        mapper = ObjectMapper()
        mapper.create_map(FromTestClass, ToTestClass,
                          {'name': lambda x: "{0} {1}".format(x.name, x.surname),
                           'date': lambda x: "{0} Hi!".format(str(x.date))})
        mapper.create_map(FromTestClass, ToTestClassTwo,
                          {'all': lambda x: "{0}{1}{2}".format(x.name, x.surname, x.date)})
        mapper.create_map(ToTestClassTwo, ToTestClassEmpty)

        # Act
        result1 = mapper.map(from_class, ToTestClass)
        result2 = mapper.map(from_class, ToTestClassTwo)
        result3 = mapper.map(result2, ToTestClassEmpty)

        # Assert
        self.assertTrue(isinstance(result1, ToTestClass), "Type must be ToTestClass")
        self.assertEqual(result1.name, "{0} {1}".format(from_class.name, from_class.surname),
                         "Name mapping must be equal")
        self.assertEqual(result1.date, "{0} Hi!".format(from_class.date), "Date mapping must be equal")
        self.assertNotIn('surname', result1.__dict__, "To class must not contain surname")

        self.assertTrue(isinstance(result2, ToTestClassTwo), "Type must be ToTestClassTwo")
        self.assertEqual(result2.all,
                         "{0}{1}{2}".format(from_class.name, from_class.surname, from_class.date),
                         "There must be concatenated all properties of fromTestClass")
        self.assertNotIn('name', result2.__dict__, "To class must not contain name")
        self.assertNotIn('surname', result2.__dict__, "To class must not contain surname")
        self.assertNotIn('date', result2.__dict__, "To class must not contain date")

        self.assertTrue(isinstance(result3, ToTestClassEmpty), "Type must be ToTestClassEmpty")
        self.assertTrue(len(result3.__dict__) == 0, "There must be no attributes")

    def test_mapping_creation_duplicate_mapping(self):

        # Arrange
        exc = False
        msg = 'Mapping for FromTestClass -> ToTestClass already exists'
        mapper = ObjectMapper()

        # Act
        try:
            mapper.create_map(FromTestClass, ToTestClass)
            mapper.create_map(FromTestClass, ToTestClass, {})
        except ObjectMapperException as ex:
            self.assertEqual(ex.message, msg, "Exception message must be correct")
            exc = True

        # Assert
        self.assertTrue(exc, "Exception must be thrown")

    def test_mapping_creation_invalid_mapping_function(self):

        # Arrange
        exc = False
        msg = 'Invalid mapping function while setting property ToTestClass.date'
        mapper = ObjectMapper()
        mapper.create_map(FromTestClass, ToTestClass, {'date': lambda x: x.be + x.de})

        # Act
        try:
            mapper.map(FromTestClass(), ToTestClass)
        except ObjectMapperException as ex:
            self.assertEqual(ex.message, msg, "Exception message must be correct")
            exc = True

        # Assert
        self.assertTrue(exc, "Exception must be thrown")


    def test_mapping_creation_none_target(self):
        # Arrange
        exc = False
        from_class = None
        mappings = \
            {
                'name': lambda x: x.name + " " + x.surname,
                'date': lambda x: str(x.date) + " Happy new year!"
            }

        mapper = ObjectMapper()

        # Act
        try:
            mapper.create_map(FromTestClass, ToTestClass, mappings)
            mapper.map(from_class, ToTestClass)
        except AttributeError:
            exc = True

        # Assert
        self.assertTrue(exc, "AttributeError must be thrown")

    def test_mapping_creation_no_mapping_defined(self):
        # Arrange
        exc = False
        msg = 'No mapping defined for FromTestClass -> ToTestClass'
        from_class = FromTestClass()

        mapper = ObjectMapper()

        # Act
        try:
            mapper.map(from_class, ToTestClass)
        except ObjectMapperException as ex:
            self.assertEqual(ex.message, msg, "Exception message must be correct")
            exc = True

        # Assert
        self.assertTrue(exc, "Exception must be thrown")

    def test_mapping_creation_with_mapping_suppression(self):

        # Arrange
        from_class = FromTestClass()
        mapper = ObjectMapper()
        mapper.create_map(FromTestClass, ToTestClass,
                          {'name': None})

        # Act
        result1 = mapper.map(from_class, ToTestClass)

        # Assert
        self.assertTrue(isinstance(result1, ToTestClass), "Type must be ToTestClass")
        self.assertEqual(result1.name, '', "Name must not be mapped")
        self.assertEqual(result1.date, from_class.date, "Date is set by property name")
        self.assertNotIn('surname', result1.__dict__, "To class must not contain surname")