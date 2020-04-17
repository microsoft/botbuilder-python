import aiounittest

from botbuilder.dialogs import ObjectPath


class Location:
    def __init__(self, lat: float = None, long: float = None):
        self.lat = lat
        self.long = long


class Options:
    def __init__(
        self,
        first_name: str = None,
        last_name: str = None,
        age: int = None,
        boolean: bool = None,
        dictionary: dict = None,
        location: Location = None,
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.boolean = boolean
        self.dictionary = dictionary
        self.location = location


class ObjectPathTests(aiounittest.AsyncTestCase):
    async def test_typed_only_default(self):
        default_options = Options(
            last_name="Smith",
            first_name="Fred",
            age=22,
            location=Location(lat=1.2312312, long=3.234234,),
        )

        overlay = Options()

        result = ObjectPath.assign(default_options, overlay)
        assert result.last_name == default_options.last_name
        assert result.first_name == default_options.first_name
        assert result.age == default_options.age
        assert result.boolean == default_options.boolean
        assert result.location.lat == default_options.location.lat
        assert result.location.long == default_options.location.long

    async def test_typed_only_overlay(self):
        default_options = Options()

        overlay = Options(
            last_name="Smith",
            first_name="Fred",
            age=22,
            location=Location(lat=1.2312312, long=3.234234,),
        )

        result = ObjectPath.assign(default_options, overlay)
        assert result.last_name == overlay.last_name
        assert result.first_name == overlay.first_name
        assert result.age == overlay.age
        assert result.boolean == overlay.boolean
        assert result.location.lat == overlay.location.lat
        assert result.location.long == overlay.location.long

    async def test_typed_full_overlay(self):
        default_options = Options(
            last_name="Smith",
            first_name="Fred",
            age=22,
            location=Location(lat=1.2312312, long=3.234234,),
            dictionary={"one": 1, "two": 2},
        )

        overlay = Options(
            last_name="Grant",
            first_name="Eddit",
            age=32,
            location=Location(lat=2.2312312, long=2.234234,),
            dictionary={"one": 99, "three": 3},
        )

        result = ObjectPath.assign(default_options, overlay)
        assert result.last_name == overlay.last_name
        assert result.first_name == overlay.first_name
        assert result.age == overlay.age
        assert result.boolean == overlay.boolean
        assert result.location.lat == overlay.location.lat
        assert result.location.long == overlay.location.long
        assert "one" in result.dictionary
        assert result.dictionary["one"] == 99
        assert "two" in result.dictionary
        assert "three" in result.dictionary

    async def test_typed_partial_overlay(self):
        default_options = Options(
            last_name="Smith",
            first_name="Fred",
            age=22,
            location=Location(lat=1.2312312, long=3.234234,),
        )

        overlay = Options(last_name="Grant",)

        result = ObjectPath.assign(default_options, overlay)
        assert result.last_name == overlay.last_name
        assert result.first_name == default_options.first_name
        assert result.age == default_options.age
        assert result.boolean == default_options.boolean
        assert result.location.lat == default_options.location.lat
        assert result.location.long == default_options.location.long

    async def test_typed_no_target(self):
        overlay = Options(
            last_name="Smith",
            first_name="Fred",
            age=22,
            location=Location(lat=1.2312312, long=3.234234,),
        )

        result = ObjectPath.assign(None, overlay)
        assert result.last_name == overlay.last_name
        assert result.first_name == overlay.first_name
        assert result.age == overlay.age
        assert result.boolean == overlay.boolean
        assert result.location.lat == overlay.location.lat
        assert result.location.long == overlay.location.long

    async def test_typed_no_overlay(self):
        default_options = Options(
            last_name="Smith",
            first_name="Fred",
            age=22,
            location=Location(lat=1.2312312, long=3.234234,),
        )

        result = ObjectPath.assign(default_options, None)
        assert result.last_name == default_options.last_name
        assert result.first_name == default_options.first_name
        assert result.age == default_options.age
        assert result.boolean == default_options.boolean
        assert result.location.lat == default_options.location.lat
        assert result.location.long == default_options.location.long

    async def test_no_target_or_overlay(self):
        result = ObjectPath.assign(None, None, Options)
        assert result

    async def test_dict_partial_overlay(self):
        default_options = {
            "last_name": "Smith",
            "first_name": "Fred",
            "age": 22,
            "location": Location(lat=1.2312312, long=3.234234,),
        }

        overlay = {
            "last_name": "Grant",
        }

        result = ObjectPath.assign(default_options, overlay)
        assert result["last_name"] == overlay["last_name"]
        assert result["first_name"] == default_options["first_name"]
        assert result["age"] == default_options["age"]
        assert result["location"].lat == default_options["location"].lat
        assert result["location"].long == default_options["location"].long

    async def test_dict_to_typed_overlay(self):
        default_options = Options(
            last_name="Smith",
            first_name="Fred",
            age=22,
            location=Location(lat=1.2312312, long=3.234234,),
        )

        overlay = {
            "last_name": "Grant",
        }

        result = ObjectPath.assign(default_options, overlay)
        assert result.last_name == overlay["last_name"]
        assert result.first_name == default_options.first_name
        assert result.age == default_options.age
        assert result.boolean == default_options.boolean
        assert result.location.lat == default_options.location.lat
        assert result.location.long == default_options.location.long

    async def test_set_value(self):
        test = {}
        ObjectPath.set_path_value(test, "x.y.z", 15)
        ObjectPath.set_path_value(test, "x.p", "hello")
        ObjectPath.set_path_value(test, "foo", {"Bar": 15, "Blat": "yo"})
        ObjectPath.set_path_value(test, "x.a[1]", "yabba")
        ObjectPath.set_path_value(test, "x.a[0]", "dabba")
        ObjectPath.set_path_value(test, "null", None)

        assert ObjectPath.get_path_value(test, "x.y.z") == 15
        assert ObjectPath.get_path_value(test, "x.p") == "hello"
        assert ObjectPath.get_path_value(test, "foo.bar") == 15

        assert not ObjectPath.try_get_path_value(test, "foo.Blatxxx")
        assert ObjectPath.try_get_path_value(test, "x.a[1]") == "yabba"
        assert ObjectPath.try_get_path_value(test, "x.a[0]") == "dabba"

        assert not ObjectPath.try_get_path_value(test, "null")

    async def test_remove_path_value(self):
        test = {}
        ObjectPath.set_path_value(test, "x.y.z", 15)
        ObjectPath.set_path_value(test, "x.p", "hello")
        ObjectPath.set_path_value(test, "foo", {"Bar": 15, "Blat": "yo"})
        ObjectPath.set_path_value(test, "x.a[1]", "yabba")
        ObjectPath.set_path_value(test, "x.a[0]", "dabba")

        ObjectPath.remove_path_value(test, "x.y.z")
        with self.assertRaises(KeyError):
            ObjectPath.get_path_value(test, "x.y.z")

        assert ObjectPath.get_path_value(test, "x.y.z", 99) == 99

        ObjectPath.remove_path_value(test, "x.a[1]")
        assert not ObjectPath.try_get_path_value(test, "x.a[1]")

        assert ObjectPath.try_get_path_value(test, "x.a[0]") == "dabba"
