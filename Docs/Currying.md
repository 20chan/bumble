# Currying

bumble에서는 초라하지만 함수 커링을 지원합니다.

```python
func foo(a, b, c){
    // Do Something
    return something;
}

var bar = foo(1, 2);
bar(3) // bar(3) = foo(1, 2)(3) = foo(1, 2, 3);
```

바인딩을 사용하여 다음과 같이 작성할 수도 있습니다.
```python
var bar(c) := foo(1, 2, c);
bar(3) // bar(3) = foo(1, 2, 3);
```
