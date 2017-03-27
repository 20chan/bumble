# Collections
## Table of Contents
- [Lists](#lists)
- [Tuples](#tuples)
- [Maps](#maps)

# Lists
리스트는 다양한 타입의 변수를 여러 개 저장할 수 있습니다.
리스트의 선언은 변수의 나열, [리스트 노테이션](https://wiki.haskell.org/List_notation),
[LINQ](https://msdn.microsoft.com/library/bb397676.aspx), [리스트 컴프리헨션](https://en.wikipedia.org/wiki/List_comprehension)을 통해 선언가능합니다.
```python
// List notation
var a = [1, 2, 3, 4];
var a2 = [1..4];
var b = [2, 4, 6, 8, 10];
var b2 = [2..10 by 2];

// LINQ
var c = [select x
         from x in [1..10]
         where isprime(x)];

// List comprehension
[x for x in [1..10] if isprime(x)]
```

리스트의 원소는 리스트의 선언시 원소의 앞에 `&`를 붙여 변수의 레퍼런스가 될 수 있습니다.
예를 들어, 다음과 같은 코드는 10을 출력합니다.
```python
var a = 5;
var ref_list = [&a, 1, 2];
ref_list[0] *= 2;
print(a);
```

# Tuples
튜플은 리스트와 비슷하게 콤마로 구분되는 변수들의 집합입니다. 하지만 튜플의 원소는 변경될 수 없다는 차이점이 있습니다.
```python
var a = [1, 2, 3, 4];
var b = (1, 2, 3, 4);
a[1] = 10; // OK
b[1] = 10; // ERROR
```

# Maps
맵은 키워드와 일대일 대응하는 밸류값을 가지는 자료구조입니다.
```python
var a = {1:10, 2:20, 3:30, "s":None};
print(a[1]); // 10
a["s"] = 40;
print(a["s"]); // 40
```
맵도 마찬가지로 레퍼런스를 원소로 추가할 수 있습니다. 하지만, 키는 상수여야 하고 밸류만 레퍼런스가 될 수 있습니다.
```python
var a = 100;
var b = {1:10, 2:20, 10:&a};
b[10] = "yeah";
print(a);
```
역시, 위 코드는 `yeah`를 출력합니다.
