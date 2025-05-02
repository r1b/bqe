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
- All traditional syntax is either restricted or unsupported
  - Restricted syntax
    - SELECT clauses cannot contain ALL or DISTINCT
      - Instead, use the DISTINCT pipe operator
    - FROM clauses cannot contain PIVOT, UNPIVOT, TABLESAMPLE or JOIN (including comma CROSS JOIN)
      - Instead, chain the corresponding pipe operator(s)
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

It should be true that all transformations that can be expressed in the traditional syntax can also be expressed in the restricted syntax without impacting the result or the mechanics of the underlying query plan.

**If this is not true, please file an issue**.

There are no plans to support any other dialect of Pipe SQL or any other database engine.

## devlog

- [x] Parser
- [ ] AST
- [ ] Generator
- [ ] Expression API
- [ ] Placeholders