# bqe

A query construction toolkit for [Pipe SQL](https://storage.googleapis.com/gweb-research2023-media/pubtools/1004848.pdf)

## why

Pipe SQL has a unique "prefix property":

> Each prefix of a query (up to a pipe character) is also a valid query.

The bet is that this property makes it possible to write tools that *generate* SQL without compromising on the experience of *writing* SQL.

Traditionally, SQL interfaces require the developer to work with an expression API most of the time, only dropping into raw SQL when more expressive power is required. `bqe` aims to invert this relationship: the developer should write SQL most of the time, only dropping into the expression API when interpolation is required. This more accurately reflects the distribution of effort when working with SQL in data applications.

## language

`bqe` understands a restricted subset of **BigQuery** Pipe SQL syntax:

- All pipe operator syntax is fully supported
- All traditional syntax that is redundant in Pipe SQL is either constrained or unsupported
  - Constrained syntax
    - Top-level SELECT is preserved to support DISTINCT and projection of values
    - All FROM clauses must have exactly one table expression
      - PIVOT, UNPIVOT, TABLESAMPLE and JOIN (including comma CROSS JOIN) are unsupported
  - Unsupported syntax
    - WHERE
    - GROUP BY
    - HAVING
    - ORDER BY
    - QUALIFY
    - WINDOW
    - UNION / INTERSECT / EXCEPT
    - LIMIT / OFFSET
    - CTEs
- All DDL, DML, DCL statements are unsupported
- Otherwise, all BigQuery SQL syntax is fully supported
  - Lexical forms
  - Types
  - Operators
  - Functions
  - Expressions

There are no plans to support any other dialect of Pipe SQL or any other database engine.

## devlog

- [x] Parser
- [ ] AST
- [ ] Generator
- [ ] Expression API
- [ ] Placeholders