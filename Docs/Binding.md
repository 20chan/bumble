# Binding

바인딩은 Reactive Programming을 위한 syntatic sugar입니다. 바인드 연산자는 :=이고, 이는 충분히 바뀔 의향이 있습니다.

기존의 변수 개념에서는 다음과 같이 작동이 됩니다. (주석이 결과)
```python
var a = 1
var b = a + 10  # b = 11
var a = 5       # still, b = 11
```

하지만 b에 a+10을 대입이 아닌 바인딩을 하면 결과는 달라집니다.
```python
var a = 1
var b := a + 10 # b = 11
var a = 5       # now b = 15
```

위 바인딩 예제는 아래 C#코드와 같다고 볼 수 있습니다.
```csharp
int a = 1;
int b => a + 10; // b return 11
a = 5;           // now b returns 15
```

바인드된 a는 완벽한 readonly 프로퍼티이고 변경될 수 없습니다.

바인드는 동적인 람다를 생성할 수도 있습니다.
```python
var bar(arg1) := foo(1, 2, arg1)
print(bar(5))
```