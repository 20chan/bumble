# Match

bumble은 타입매칭도 지원합니다! 세상에나 이렇게 좋은 언어가...
```python
match(x, y) {
    1, _    then print('one');
    _, True then {
                print ('wow');
                do_something();
            }
    _, _    then print('nah');
}
```
