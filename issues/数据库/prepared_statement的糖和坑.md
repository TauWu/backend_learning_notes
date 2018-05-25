# Prepare Statement的糖和坑

## 报错信息
调用接口执行SQL查询的时候，数据库报错max_prepared_stmt_count超过最大值。
```
mysql_stmt_prepare failed! error(1461) Can't create more than max_prepared_stmt_count statements (current value: 16382)
```

## 排错方案
问题出现在prepared statement的使用上面，执行以下SQL语句查询当前statement的使用情况。
```sql
show global status like 'com_stmt%';
```
查询到的内容如下：
Variable_name | Value 
--- | ---
Com_stmt_execute |1
Com_stmt_close |1
Com_stmt_fetch |0
Com_stmt_prepare | 1
Com_stmt_reset | 0
Com_stmt_send_long_data | 0
Com_stmt_reprepare | 0

倘若`Com_stmt_close`的数值要远远小于`Com_stmt_execute`和`Com_stmt_fetch`的值，则可以定位到错误是执行SQL语句的时候，应用端的session没有关闭prepared导致数量溢出最大值（默认最大值是16382），最终导致SQL查询无法进行而报错。

## 解决方案
- 治标方案
迅速解决的办法是手动调整db中max_prepared_stmt_count的值
```sql
set global max_prepared_stmt_count=1000000; 
-- 可以是0～1048576之间的任意值
```
- 治本方案
检查代码中带占位符`？`的SQL执行语句中，对于创建出的stmt和查询连接等是否手动关闭。如果均合理关闭，可以对底层调用的第三方、标准库中的代码进行检查，在使用prepare语句的时候，是否有做关闭处理（Go在1.4版本前的标准库中存在过这种隐患。=>[传送门](https://studygolang.com/articles/1795)）

## 源码分析
以本次出现问题的Go为例，使用到了sqlx的第三方库。当前项目中，select操作使用到的方法是`Select`（针对列表数据）和`Get`（针对单行数据），update和insert使用到的方式是`Exec`。
以Exec为例，因为存在
```go
defer ds.Close()
```
所以这种方法执行的SQL是安全的，不需要考虑关闭ds和rows等的问题。
sqlx中的代码如下：
```go
func (db *DB) exec(ctx context.Context, query string, args []interface{}, strategy connReuseStrategy) (res Result, err error) {
    dc, err := db.conn(ctx, strategy)

    // ... 略

    var si driver.Stmt
    // 执行prepare语句： SQL中prepare其实是存储过程
    withLock(dc, func() {
        si, err = ctxDriverPrepare(ctx, dc.ci, query)
    })
    if err != nil {
        return nil, err
    }
    // 创建driverStmt
    ds := &driverStmt{Locker: dc, si: si}
    // Exec方法中会自带关闭ds，因此该方法是安全的
    defer ds.Close()
    // 填充args参数
    return resultFromStatement(ctx, ds, args...)
}

func resultFromStatement(ctx context.Context, ds *driverStmt, args ...interface{}) (Result, error) {
    want := driverNumInput(ds)

    // -1 means the driver doesn't know how to count the number of
    // placeholders, so we won't sanity check input here and instead let the
    // driver deal with errors.
    if want != -1 && len(args) != want {
        return nil, fmt.Errorf("sql: expected %d arguments, got %d", want, len(args))
    }

    // 获取参数
    dargs, err := driverArgs(ds, args)
    if err != nil {
        return nil, err
    }

    ds.Lock()
    defer ds.Unlock()

    // 通过driver执行SQL
    resi, err := ctxDriverStmtExec(ctx, ds.si, dargs)
    if err != nil {
        return nil, err
    }
    return driverResult{ds.Locker, resi}, nil
}

```
而旧版本中获取多行数据采取了使用的是Go标准库中自带的`"database/sql"`。具体代码是先调用`Query()`，然后再调用`Scan()`的方案。这种方案需要手动关闭rows，如果遗忘便会有风险连接数超额或者stmt超额。
```go
SQL = `select id from test_table where age = ?`
rows, err1 := db.Query(SQL)

if err1 == nil {
    // 手动在运行完毕的时候执行Close
    defer rows.Close()

    for rows.Next() {
        data := new(TestStruct)
        err = rows.Scan(&data)
        if err != nil {
            log.Error("scan failed,err=", err.Error())
            continue
        }
        list = append(list, *data)
    }

```

## 选择PreparedStatement的原因
- 代码的可读性和可维护性
    - 虽然用PreparedStatement来代替Statement会使代码多出几行,但这样的代码无论从可读性还是可维护性上来说，都比直接用Statement的代码要好
```java
    // 方法1：拼接SQL
    stmt.executeUpdate("insert into tb_name (col1,col2,col2,col4)values('"+var1+"','"+var2+"',"+var3+",'"+var4+"')");
    // 方法2：采用PreparedStatement
    perstmt=con.prepareStatement("insert into tb_name (col1,col2,col2,col4)values(?,?,?,?)");
    perstmt.setString(1,var1);
    perstmt.setString(2,var2);
    perstmt.setString(3,var3);
    perstmt.setString(4,var4);
    perstmt.executeUpdate();
```
- 尽最大可能提高性能
    - 每一种数据库都会尽最大努力对预编译语句提供最大的性能优化，因为**预编译语句有可能被重复调用**。所以语句在被DB的编译器编译后的执行代码被缓存下来，那么下次调用时只要是相同的预编译语句就不需要编译，只要将参数直接传入编译过的语句执行代码中（相当于一个函数）就会得到执行。这并不是说只有一个Connection中多次执行的预编译语句被缓存，而是对于整个DB中，只要预编译的语句语法和缓存中匹配，那么在任何时候就可以不需要再次编译而可以直接执行。而statement的语句中，即使是相同一操作，而由于每次操作的数据不同所以使整个语句相匹配的机会极小,几乎不太可能匹配。比如：
    ```sql
    　　insert into tb_name(col1,col2) values('11','22');
    　　insert into tb_name(col1,col2) values('11','23');
    ```
    - 即使是相同操作但因为数据内容不一样，所以整个个语句本身不能匹配，没有缓存语句的意义。事实是没有数据库会对普通语句编译后的执行代码缓存。当然并不是所有预编译语句都一定会被缓存，数据库本身会用一种策略，比如使用频度等因素来决定什么时候不再缓存已有的预编译结果。以保存有更多的空间存储新的预编译语句。
- 提高了安全性，阻止SQL注入
    - 对于
    ```java
    　　Stringsql="select * from tb_name where name = '"+varname+"' and passwd = '"+varpasswd+"'";
    ```
    - 如果我们把['or'1'='1]作为varpasswd传入进来，用户名随意，就会变成
    ```sql
        select * from tb_name where name = '随意' and passwd = '' or '1'='1';
    ```
    - 因为'1'='1'肯定成立，所以可以任何通过验证。如果把[';droptabletb_name;]作为varpasswd传入进来,则会是：
    ```sql
    　　select * from tb_name = '随意' and passwd = ''; drop table tb_name;
    ```
    - 有些数据库是不会让你成功的,但也有很多数据库就可以使这些语句得到执行。而如果你使用预编译语句，你传入的任何内容就不会和原来的语句发生任何匹配的关系，只要全使用预编译语句，你就用不着对传入的数据做任何过滤。