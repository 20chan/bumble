# Macro

다음과 같은 파이썬 코드가 있다고 합시다
```python
a = iter(range(10))
print(next(a))
```

이때 다음 next(a)를 호출하면 그 전의 값은 알 수 없습니다. 그래서 우리는 다음과 같이 변수를 선언해서 쓰죠:
```python
cur = next(a)
print(cur)
```

이를 인라인으로 선언하면
```python
print(next(a)@cur)
```
가 됩니다.