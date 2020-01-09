<img src="logo.png" align="left" style="width:128px; margin-right: 20px;" />

# Object Mapper

**Version**
1.1.0

**Author**
marazt

**Copyright**
marazt

**License**
The MIT License (MIT)

**Last updated**
13 July 2019

**Package Download**
https://pypi.python.org/pypi/object-mapper

**Build Status**
[![Build Status](https://travis-ci.com/marazt/object-mapper.svg?branch=master)](https://travis-ci.com/marazt/object-mapper)

---

## Versions

**1.1.0 - 2019/07/13**

* Add basic support for nested object, thanks [@direbearform](https://github.com/direbearform)

**1.0.7 - 2019/06/19**

* Fix type name inside mapper dict to avoid collision, thanks [@renanvieira](https://github.com/renanvieira)

**1.0.6 - 2018/10/28**

* Added ability to specify excluded fields, thanks [@uralov](https://github.com/uralov)

**1.0.5 - 2018/02/21**

* Support for dynamic properties [@nijm](https://github.com/nijm)

**1.0.4 - 2017/11/03**

* Migration to new Pypi.org deployment

**1.0.3 - 2015/05/15**

* Added support for None mapping [@ramiabughazaleh](https://github.com/ramiabughazaleh)


**1.0.2 - 2015/05/06**

* Added support for case insensitivity mapping [@ramiabughazaleh](https://github.com/ramiabughazaleh)


**1.0.1 - 2015/02/19**

* Fix of the package information


**1.0.0 - 2015/02/19**

* Initial version


## About

**ObjectMapper** is a class for automatic object mapping inspired by .NET **AutoMapper**.
It helps you to create objects between project layers (data layer, service layer, view) in a simple, transparent way.

## Example

1. **Mapping of the properties without mapping definition**

  In this case are mapped only these properties of the target class which
  are in target and source classes. Other properties are not mapped.
  Suppose we have class `A` with attributes `name` and `last_name`
  and class `B` with attribute `name`.
  Initialization of the ObjectMapper will be:

  ```python
  mapper = ObjectMapper()
  mapper.create_map(A, B)
  instance_b = mapper.map(A(), B)
  ```

  In this case, value of A.name will be copied into B.name.

2. **Mapping with defined mapping functions**

  Suppose we have class `A` with attributes `first_name` and `last_name`
  , class `B` with attribute `full_name` and class `C` with attribute reverse_name.
  And want to map it in a way `B.full_name = A.first_name + A.last_name` and
  `C.reverse_name = A.last_name + A.first_name`
  Initialization of the ObjectMapper will be:

  ```python
  mapper = ObjectMapper()
  mapper.create_map(A, B, {'name': lambda a : a.first_name + " " + a.last_name})
  mapper.create_map(A, C, {'name': lambda a : a.last_name + " " + a.first_name})

  instance_b = mapper.map(A(), B)
  instance_c = mapper.map(A(), C)
  ```

  In this case, to the `B.name` will be mapped `A.first_name + " " + A.last_name`
  In this case, to the `C.name` will be mapped `A.last_name + " " + A.first_name`

3. **Mapping suppression**

  For some purposes, it can be needed to suppress some mapping.
  Suppose we have class `A` with attributes `name` and `last_name`
  and class `B` with attributes `name` and `last_name`.
  And we want to map only the `A.name` into `B.name`, but not `A.last_name` to
  `B.last_name`
  Initialization of the ObjectMapper will be:

  ```python
  mapper = ObjectMapper()
  mapper.create_map(A, B, {'last_name': None})

  instance_b = mapper.map(A(), B)
  ```

  In this case, value of A.name will be copied into `B.name` automatically by the attribute name `name`.
  Attribute `A.last_name` will be not mapped thanks the suppression (lambda function is None).

4. **Case insensitive mapping**

  Suppose we have class `A` with attributes `Name` and `Age` and
  class `B` with attributes `name` and `age` and we want to map `A` to `B` in a way
  `B.name` = `A.Name` and `B.age` = `A.Age`
  Initialization of the ObjectMapper will be:

  ```python
  mapper = ObjectMapper()
  mapper.create_map(A, B)
  instance_b = mapper.map(A(), B, ignore_case=True)
  ```

  In this case, the value of A.Name will be copied into B.name and
  the value of A.Age will be copied into B.age.

  **Note:** You can find more examples in tests package

5. **Mapping with nested objects**

Suppose you have two classes `Person` and `MyPerson`, each one of them contains an `address` field of types `Address` and `MyAdress` respectively. And you want to map from `Person` to `MyPerson`. Initialization of the `ObjectMapper` will be:

```
class MyPerson:
    def __init__(self):
        self.address = None
class MyAdress:
    def __init__(self):
        self.city = None
        self.street = None
class Address:
    def __init__(self):
        self.line = "Amman-Maka Street"
class Person:
    def __init__(self):
        self.address = Address()

mapper = ObjectMapper()
mapper.create_map(
    Address, 
    MyAdress, 
    {
        'city': lambda add: add.line.split('-')[0],
        'street': lambda add: add.line.split('-')[1]
    }
)
mapper.create_map(Person, MyPerson)
person = mapper.map(Person(), MyPerson)
assert type(person.address) is MyAdress
assert '{}-{}'.format(person.address.city, person.address.street) == Person().address.line
```

## Installation

* Download this project
* Download from Pypi: https://pypi.python.org/pypi/object-mapper

### ENJOY IT!
