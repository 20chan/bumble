# Syntax
- [Literal](#literal)
    - [Integer](#integer)
    - [Real](#real)
    - [Boolean](#boolean)
    - [Character](#character)
    - [String](#string)
- [Variable](#variable)
- [Function](#function)
- [Comment](#comment)
## Literal
### Integer
```
print 0b0101001
print 0o01276
print 0xffffff
```
### Real
```
print 3.14159265
print .99999999
```
### Boolean
```
print true
print false
```
### Character
```
print 'c'
print '뷁'
```
### String
```
print "Lorem ipsum"
print "아무말 대잔치 만쉐이"
```
## Variable
변수는 `(변수명) = (값)` 으로 선언, 대입합니다.
```
a = 1
b = (plus a 2)
b = (plus a b)
```
## Function
함수 선언도 변수 선언과 다른게 없습니다.
```
plus1 a = plus a 1
print (plus1 a)
```
## Comment
인라인 주석은 `//` 을 사용합니다.
```
print (plus 1 2) // 2
```
여러줄의 주석은 `/* */` 을 사용합니다.
```
print /* 요기에 출력할걸 넣으세욤~~~ */ "Like THIS"
```
