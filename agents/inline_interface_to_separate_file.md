Here is my in-line Vyper Interface:

```
interface Favorites:
    def store():
    def retrieve() -> uint256: view
```

Convert it to a Vyper file interface. Here is an example:


Inline Vyper interaface:
```
interface AggregatorV3Interface:
    def decimals() -> uint8: view
    def description() -> String[1000]: view
    def version() -> uint256: view
    def latestAnswer() -> int256: view
```

Vyper file interface:
`AggregatorV3Interface.vyi`
```
@external
@view
def decimals() -> uint8:
    ...

@external
@view
def description() -> String[1000]:
    ...

@external
@view
def version() -> uint256:
    ...

@external
@view
def latestAnswer() -> int256:
    ...
```