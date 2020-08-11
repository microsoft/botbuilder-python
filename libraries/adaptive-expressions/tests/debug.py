from adaptive.expressions import Expression

scope = {
    "one": 1.0,
    "two": 2.0,
    "hello": "hello",
    "nullObj": None,
    "null": None,
    "bag": {"three": 3.0, "name": "mybag"},
    "items": ["zero", "one", "two"],
    "nestedItems": [{"x": 1}, {"x": 2}, {"x": 3},],
    "dialog": {
        "x": 3,
        "instance": {"xxx": "instance", "yyy": {"instanceY": "instanceY"}},
        "options": {"xxx": "options", "yyy": ["optionY1", "optionY2"]},
        "title": "Dialog Title",
        "subTitle": "Dialog Sub Title",
    },
    "timestamp": "2018-03-15T13:00:00.000Z",
    "notISOTimestamp": "2018/03/15 13:00:00",
    "unixTimestamp": 1521118800,
    "unixTimestampFraction": 1521118800.5,
    "ticks": 637243624200000000,
    "doubleNestedItems": [[{"x": 1}, {"x: 2"}], [{"x": 3}]],
}
print("syp, debug")
parsed = Expression.parse("getProperty(bag, concat('na','me'))")
assert parsed is not None

value, error = parsed.try_evaluate(scope)

print(value, error)
