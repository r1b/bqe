# bqe

A query language for BigQuery that compiles to Pipe SQL.

## goals

- Encourage developers to Just Write SQL
- Enable safe, robust expression interpolation when query generation is required
- Procedural and metaprogramming extensions for common data transformation tasks

## non-goals

- Types, catalogs and schemas
- Query execution and orchestration, including result processing

## why

`bqe` is designed to be used on the read side of big data workloads. By cleaving off the data definition and mutation parts of SQL, it becomes feasible to write a small parser that enables and extends the transformation part of SQL. 

## usage

For the most part, `bqe` is just Pipe SQL with some extensions.

### metaprogramming

Metaprogramming in `bqe` is inspired by the macro system in `sqlmesh`.

The most common use cases we've seen for metaprogramming include:

- Injection of externally generated expressions (especially predicates)
- Conditional rendering of statements, clauses and column expressions

Remember that metaprogramming rewrites the query _before_ compilation to Pipe SQL.

#### expression interpolation

AST nodes or python expressions can be injected into the generated query with the syntax `@(expr)`. In general, nodes can be interpolated into any position of the query where an expression or identifier is expected. Python values are automatically rendered as query parameters.

Expressions are generated with the expression API. It should feel familiar for users coming from SQLAlchemy.

```python
# TODO: Flesh this out
from bqe.builtins import search
from bqe.compiler import compile
from bqe.query import column, func, null, param, table, text

query = "FROM @(table) |> WHERE @(dsl) |> SELECT d"
dsl = (search(column("a"), param("foobar"), text_analyzer=text("NOOP_ANALYZER")) & column("b") != param(2)) | column("c").is(null())
sql, params = compile(path_or_str, context={"dsl": dsl, "table": table("table1")}, options={"paramstyle": "at"})
print(sql, params)
```

```sql
FROM table1
    |> WHERE (
        SEARCH(a, @param1, text_analyzer => 'NOOP_ANALYZER')
        AND b != @param2
    ) OR c IS NULL
```

To interpolate a column list, use the syntax @@(expr):

```sql
FROM table1
    |> SELECT a, @@(table1_extra_columns)
```

If you provide no context value for an expression, it will be omitted

#### conditional rendering: statements and clauses

`bqe` extends Pipe SQL with a conditional pipe operator:

The operator can be used at the top level to conditionally render statements:

```sql
|? WHEN @(condition) THEN
    FROM table1
        |> TO TEMP TABLE table2
|? END
```

Or within a pipeline to conditionally render individual pipeline steps:

```sql
FROM table1
    |? WHEN NOT @(condition) THEN
        |> SELECT a
    |? ELSE
        |> SELECT b
    |? END
```

### procedural extensions

In general, we think that avoiding side effects and state is a Good Thing. However, there are many real-world use cases where these features are necessary. For these cases, `bqe` prefers procedural features over sessions or external orchestration because this allows the developer to keep all of their business logic in one place.

All procedural extensions are _terminal_ - no additional pipeline operators can be added to the statement after a procedural pipeline operator.

#### materialization

It can be necessary to materialize intermediate results (for example, to reuse them in multiple downstream queries). `bqe` extends Pipe SQL with the `TO TEMP TABLE` form, which writes the pipeline results to a temporary table.

```sql
FROM table1
    |> SELECT column1, column2
    |> TO TEMP TABLE table2;
```

This compiles to:

```sql
CREATE TEMP TABLE table2 AS (
    FROM table1
        |> SELECT column1, column2
);
```

#### variable definition

In most cases, variables can be substituted with query parameters. However, there are some rare situations where a large value needs to be available at statement analysis time. For example, it is possible to get pruning from clustering with a query like:

```sql
FROM table
    |> WHERE column1 IN UNNEST(<array>)
```

Where `<array>` has up to 1,000 values and can be statically analyzed (i.e: not the result of a query). Depending on the size and provenance of the values, it may be cumbersome to pass the array as a query parameter.

To support this use case, `bqe` extends Pipe SQL with the `TO VARIABLE` form, which writes the results of a scalar table to a named variable.

```sql
SELECT [1, 2]
    |> TO VARIABLE var1 ARRAY<INT64>
```

This complies to:

```sql
DECLARE var1 ARRAY<INT64>;

SET var1 = (SELECT [1, 2]);
```

Note that currently the type of the variable must always be specified, even where it could be inferred from context.

The `DECLARE` statements are always lifted to the top of the compiled SQL, while the `SET` statements remain in the defined position. Chained variable definitions work as expected:

```sql
SELECT [1, 2]
    |> TO VARIABLE var1 INT64;

SELECT var1[0]
    |> TO VARIABLE var2 STRING;
```

This compiles to:

```sql
DECLARE var1 ARRAY<INT64>;
DECLARE var2 STRING;
        
SET var1 = (SELECT [1, 2]);
SET var2 = (SELECT CAST(var1[0] AS STRING));
```

#### merge

We have observed serving-side workloads that merge the results of a query into a state table.

To support this use case, `bqe` extends pipe SQL with a `MERGE` pipe operator:

```sql
FROM table1
    |> MERGE INTO table2
        USING src
        ON table2.col1 = src.col1
        WHEN MATCHED THEN
            UPDATE SET table2.col2 = src.col2;
```

This compiles to:

```sql
MERGE INTO table2
USING (FROM table1) AS src
ON table2.col1 = src.col1
WHEN MATCHED THEN
    UPDATE SET table2.col2 = src.col2;
```