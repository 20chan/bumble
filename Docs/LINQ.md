# LINQ

C#의 LINQ를 지원합니다. 하지만 순서는 sql 쿼리와 비슷하게 변경되었습니다.

```csharp
var users_childs = [select childs
                from x in users
                let childs = x.childs
                where x.alive == true
                orderby x.age]
```