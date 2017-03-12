# Basics
## Table of Contents
- [데이터 타입](#데이터-타입)
  - [Integers](#integers)
  - [Floats](#floats)
  - [Booleans](#booleans)
  - [Characters](#characters)
  - [Strings](#strings)
- 연산자
  - [Arithmetic](#arithmetic)
  - [Boolean](#boolean)
  - [Comparison](#comparison)
  - [List](#list)

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

## 연산자
### Arithmetic
기본적인 사칙연산 연산자 `+`, `-`, `*`, `/` 가 있고 나머지 연산인 `%`과 거듭제곱 연산 `**`가 있습니다.
연산 우선순위는 `(**) > (*) = (/) = (%) > (+) = (-)` 입니다.

### Boolean
부울 연산에 and or not xor 말고 뭐가 있겠어요 ㅇㅅㅇ
and 연산자는 `&&`, or 연산자는 `||`, not 연산자는 `!`, xor 연산자는 `^` 입니다.
각 연산자는 정수형 변수에도 똑같이 적용됩니다.

### Comparison
비교 연산자 `>`, `<`, `>=`, `<=`, `==`, `!=` 가 있습니다.

### List
리스트(문자열 포함) 연산자에는 리스트를 이어 붙이는 `++` 연산자가 있습니다.
리스트에 원소를 붙이는 `:` 연산자도 있습니다.
예를 들어, 리스트 `[2, 3, 4]`의 처음에 1을 추가하려면 다음과 같은 코드가 됩니다.
```python
1:[2, 3, 4] == [1] ++ [2, 3, 4]
```