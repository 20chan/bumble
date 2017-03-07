# Inline Declaration

다음과 같이 [cond](/Cond.md)문이 있습니다.
```python
cond(weight height){
    weight / height ** 2 <= 18.5 then return "underweight"
    weight / height ** 2 <= 25.0 then return "normal"
    weight / height ** 2 <= 30.0 then return "fat"
    otherwise then return "whale"
}
```

`weight / height ** 2`가 반복되어 사용되어지는건 바람직하지 않습니다!

```python
cond(weight height){
    (weight / height ** 2)@bmi <= 18.5 then return "underweight"
    bmi <= 25.0 then return "normal"
    bmi <= 30.0 then return "fat"
    otherwise then return "whale"
}
```

`(weight / height ** 2)@bmi` 가 계산될때 bmi 에는 `weight / height ** 2`를 계산한 값이 대입됩니다.
