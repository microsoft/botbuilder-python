from expression import Expression

parsed = Expression.parse('1+1')
value, error = parsed.try_evaluate()

print(value)
