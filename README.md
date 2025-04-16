# bqe

A query construction toolkit for [Pipe SQL](https://storage.googleapis.com/gweb-research2023-media/pubtools/1004848.pdf)

## why

Pipe SQL has a unique "prefix property":

> Each prefix of a query (up to a pipe character) is also a valid query.

The bet is that this property makes it possible to write tools that *generate* SQL without compromising on the experience of *writing* SQL.

Traditionally, SQL interfaces require the developer to work with an expression API most of the time, only dropping into raw SQL when more expressive power is required. `bqe` aims to invert this relationship: the developer should write SQL most of the time, only dropping into the expression API when interpolation is required. We think this more accurately reflects the distribution of effort when working with SQL in data applications.

## parser

`bqe` understands a restricted subset of Pipe SQL:

- All pipe operator syntax is fully supported
- All traditional syntax with an equivalent pipe operator is unsupported

## devlog

- [x] Parser
- [ ] AST
- [ ] Expression API
- [ ] Placeholders