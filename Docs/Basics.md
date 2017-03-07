# Basics
## Table of Contents
- [데이터 타입](##데이터-타입)
  - [Integers](###Integers)
  - [Floats](###Floats)
  - [Booleans](###Booleans)
  - [Characters](###Characters)
  - [Strings](###Strings)
- 연산자
  - Arithmetic
  - Boolean
  - Comparison
  - List

## 데이터 타입
### Integers
2진수, 8진수, 16진수를 지원합니다.
```python
print(0b0101001);
print(0o01276);
print(0xffffff);
```
### Floats
실수는 64비트 double을 사용합니다. 근데 왜 헤더는 float일까 꺄르륵
```python
print(3.141592);
```

### Booleans
불리언에는 두가지 값이 있습니다 : true, false
```python
print(true);
print(false);
```

### Characters
문자는 기본적으로 utf-8 유니코드 인코딩을 사용합니다. 따옴표로 감싸서 한글자의 문자를 나타냅니다.
```python
print('c'.type())
print('뷁')
print('死')
```

### Strings
문자열은 문자의 배열 클래스입니다. 역시 utf-8 유니코드 인코딩을 기본으로 사용하며, 다양한 연산을 지원합니다.
쌍따옴표로 감싸서 문자열을 나타냅니다.
```python
print("This is STRING!")
print("死死死死死死死死死")
```