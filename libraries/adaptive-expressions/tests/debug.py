from adaptive.expressions import Expression

scope = {"bag": {"three": 3.0}, "items": ["zero", "one", "two"]}

parsed = Expression.parse("contains(items, 'zero')")

value, error = parsed.try_evaluate(scope)

print(value)
