# coding=utf-8
"""
Copyright (C) 2015, marazt. All rights reserved.
"""
from typing import List, Dict
from mapper.object_mapper_exception import ObjectMapperException
from mapper.casedict import CaseDict
from inspect import getmembers, isroutine
from datetime import date, datetime

class ObjectMapper(object):
    """
    Base class for mapping class attributes from one class to another one
    Supports mapping conversions too
    """

    primitive_types = { int, str, bool, date, datetime }

    def __init__(self):
        """Constructor

        Args:
          mappings: dictionary of the attribute conversions

        Examples:

            1. Mapping of the properties without mapping definition
            In this case are mapped only these properties of the target class which
            are in target and source classes. Other properties are not mapped.
            Suppose we have class 'A' with attributes 'name' and 'last_name'
            and class 'B' with attribute 'name'.
            Initialization of the ObjectMapper will be:
            mapper = ObjectMapper()
            mapper.create_map(A, B)
            instance_b = mapper.map(A(), B)

            In this case, value of A.name will be copied into B.name.

            2. Mapping with defined mapping functions
            Suppose we have class 'A' with attributes 'first_name' and 'last_name'
            , class 'B' with attribute 'full_name' and class 'C' with attribute reverse_name.
            And want to map it in a way 'B.full_name' = 'A.first_name' + 'A.last_name' and
            'C.reverse_name' = 'A.last_name' + 'A.first_name'
            Initialization of the ObjectMapper will be:
            mapper = ObjectMapper()
            mapper.create_map(A, B, {'name': lambda a : a.first_name + " " + a.last_name})
            mapper.create_map(A, C, {'name': lambda a : a.last_name + " " + a.first_name})

            instance_b = mapper.map(A(), B)
            instance_c = mapper.map(A(), C)

            In this case, to the B.name will be mapped A.first_name + " " + A.last_name
            In this case, to the C.name will be mapped A.last_name + " " + A.first_name

            3. Mapping suppression
            For some purposes, it can be needed to suppress some mapping.
            Suppose we have class 'A' with attributes 'name' and 'last_name'
            and class 'B' with attributes 'name' and 'last_name'.
            And we want to map only the A.name into B.name, but not A.last_name to
            b.last_name
            Initialization of the ObjectMapper will be:
            mapper = ObjectMapper()
            mapper.create_map(A, B, {'last_name': None})

            instance_b = mapper.map(A())

            In this case, value of A.name will be copied into B.name automatically by the attribute name 'name'.
            Attribute A.last_name will be not mapped thanks the suppression (lambda function is None).

            4. Case insensitive mapping
            Suppose we have class 'A' with attributes 'Name' and 'Age' and
            class 'B' with attributes 'name' and 'age' and we want to map 'A' to 'B' in a way
            'A.Name' = 'B.name' and 'A.Age' = 'B.age'
            Initialization of the ObjectMapper will be:
            mapper = ObjectMapper()
            mapper.create_map(A, B)
            instance_b = mapper.map(A(), ignore_case=True)

            In this case, the value of A.Name will be copied into B.name and
            the value of A.Age will be copied into B.age.

        :return: Instance of the ObjectMapper
        """

        # mapping is a 2-layer dict keyed by source type then by dest type, and stores two things in a tuple:
        #  - the destination type class
        #  - custom mapping functions, if any
        self.mappings = {}
        pass

    def create_map(self, type_from: type, type_to: type, mapping: Dict =None):
        """Method for adding mapping definitions

        :param type_from: source type
        :param type_to: target type
        :param mapping: dictionary of mapping definitions in a form {'target_property_name',
                        lambda function from rhe source}

        :return: None
        """

        if (type(type_from) is not type):
            raise ObjectMapperException(f"type_from must be a type")
        if (type(type_to) is not type):
            raise ObjectMapperException(f"type_to must be a type")
        if (mapping is not None and not isinstance(mapping, Dict)):
            raise ObjectMapperException(f"mapping, if provided, must be a Dict type")

        key_from = f"{type_from.__module__}.{type_from.__name__}"
        key_to = f"{type_to.__module__}.{type_to.__name__}"

        if key_from in self.mappings:
            inner_map = self.mappings[key_from]
            if key_to in inner_map:
                raise ObjectMapperException("Mapping for {0} -> {1} already exists".format(key_from, key_to))
            else:
                inner_map[key_to] = (type_to, mapping)
        else:
            self.mappings[key_from] = {}
            self.mappings[key_from][key_to] = (type_to, mapping)


    def map(self, from_obj, to_type: type=type(None), ignore_case: bool=False, allow_none: bool=False, excluded: List[str]=None, included: List[str]=None, allow_unmapped: bool=False):
        """Method for creating target object instance

        :param from_obj: source object to be mapped from
        :param to_type: target type
        :param ignore_case: if set to true, ignores attribute case when performing the mapping
        :param allow_none: if set to true, returns None if the source object is None; otherwise throws an exception
        :param excluded: A list of fields to exclude when performing the mapping
        :param included: A list of fields to force inclusion when performing the mapping
        :param allow_unmapped: if set to true, copy over the non-primitive object that didn't have a mapping defined; otherwise exception

        :return: Instance of the target class with mapped attributes
        """
        if (from_obj is None) and allow_none:
            return None
        else:
            # one of the tests is explicitly checking for an attribute error on __dict__ if it's not set
            from_obj.__dict__

        key_from = f"{from_obj.__class__.__module__}.{from_obj.__class__.__name__}"

        if key_from not in self.mappings:
            raise ObjectMapperException(f"No mapping defined for {key_from}")

        custom_mappings = None
        key_to_cls = type(None)
        
        if to_type is None or to_type is type(None):
            # automatically infer to to_type
            # if this is a nested call and we do not currently support more than one to_types
            assert(len(self.mappings[key_from]) > 0)
            if len(self.mappings[key_from]) > 1:
                raise ObjectMapperException(f"Ambiguous type mapping exists for {key_from}, must specifiy to_type explicitly")
            the_only_key_to = next(iter(self.mappings[key_from]))
            key_to_cls = self.mappings[key_from][the_only_key_to][0]
            custom_mappings = self.mappings[key_from][the_only_key_to][1]
        else:
            key_to = f"{to_type.__module__}.{to_type.__name__}"
            if key_to not in self.mappings[key_from]:
                raise ObjectMapperException(f"No mapping defined for {key_from} to {key_to}")
            key_to_cls = self.mappings[key_from][key_to][0]
            custom_mappings = self.mappings[key_from][key_to][1]

        # Currently, all target class data members need to have default value
        # Object with __init__ that carries required non-default arguments are not supported
        inst = key_to_cls()

        def not_private(s):
            return not s.startswith('_')

        def not_excluded(s):
            return not (excluded and s in excluded)

        def is_included(s):
            return included and s in included

        from_obj_attributes = getmembers(from_obj, lambda a: not isroutine(a))
        from_obj_dict = {k: v for k, v in from_obj_attributes}

        to_obj_attributes = getmembers(inst, lambda a: not isroutine(a))
        to_obj_dict = {k: v for k, v in to_obj_attributes if not_excluded(k) and (not_private(k) or is_included(k))}

        if ignore_case:
            from_props = CaseDict(from_obj_dict)
            to_props = CaseDict(to_obj_dict)
        else:
            from_props = from_obj_dict
            to_props = to_obj_dict

        def map_obj(o, allow_unmapped):
            if o is not None:
                key_from_child_cls = o.__class__
                key_from_child = f"{key_from_child_cls.__module__}.{key_from_child_cls.__name__}"
                if (key_from_child in self.mappings):
                    # if key_to has a mapping defined, nests the map() call
                    return self.map(o, type(None), ignore_case, allow_none, excluded, included, allow_unmapped)
                elif (key_from_child_cls in ObjectMapper.primitive_types):
                    # allow primitive types without mapping
                    return o
                else:
                    # fail complex type conversion if mapping was not defined, unless explicitly allowed
                    if allow_unmapped:
                        return o
                    else:
                        raise ObjectMapperException(f"No mapping defined for {key_from_child}")
            else:
                return None

        for prop in to_props:
            
            val = None
            suppress_mapping = False

            # mapping function take precedence over complex type mapping
            if custom_mappings is not None and prop in custom_mappings:
                try:
                    fnc = custom_mappings[prop]
                    if fnc is not None:
                        val = fnc(from_obj)
                    else:
                        suppress_mapping = True
                except Exception:
                    raise ObjectMapperException("Invalid mapping function while setting property {0}.{1}".
                                                format(inst.__class__.__name__, prop))

            elif prop in from_props:
                # try find property with the same name in the source
                from_obj_child = from_props[prop]
                if isinstance(from_obj_child, List):
                    val = [map_obj(from_obj_child_i, allow_unmapped) for from_obj_child_i in from_obj_child]
                else:
                    val = map_obj(from_obj_child, allow_unmapped)
            
            else:
                suppress_mapping = True

            if not suppress_mapping:
                setattr(inst, prop, val)

        return inst
