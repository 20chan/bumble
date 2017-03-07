# Cond, Conds

cond문은 if ~ else if ~ else if ~ else 문의 지옥으로부터 우리를 구원해줄 어메이징한 구문입니다.
```python
a = "yeah"
cond(a) {
    a.startswith("y") then print("yes")
    a.startswith("m") then print("nooo")
    otherwise print(";ㅅ;")
}
```
위 코드는 yes를 출력하고 cond문을 탈출하게 됩니다. 반면 conds 문은 참인 조건을 만나도 cond문을 탈출하지 않습니다.
```python
a = "yeah"
conds(a) {
    a.startswith("y") then print("yes")
    a[1] == "e" then print("wow")
    a.endswith("h") then print("amazing")
    otherwise print("never")
}
```
위 코드는 yes/wow/amazing을 전부 출력합니다.