from mdx.tag_attribute_parser import attributes_to_element, parse_attribute_string


def test_empty_attribute_string_returns_none():
    assert parse_attribute_string("") is None
    assert parse_attribute_string("   ") is None


def test_braces_only_return_default_parse():
    parsed = parse_attribute_string("{}")
    assert parsed["tagname"] is None
    assert parsed["classes"] == []


def test_classes_id_tagname_and_attrs_are_parsed():
    parsed = parse_attribute_string('{.a .b #main /section width="400"}')
    assert parsed["classes"] == ["a", "b"]
    assert parsed["id"] == "main"
    assert parsed["tagname"] == "section"
    assert parsed["attrs"]["width"] == "400"


def test_bare_word_becomes_class():
    assert parse_attribute_string(" Danger  ")["classes"] == ["Danger"]


def test_self_closing_tag_is_parsed():
    parsed = parse_attribute_string("{/hr/}")
    assert parsed["tagname"] == "hr"
    assert parsed["closed"] is True


def test_attributes_to_element_sets_tag_class_and_id():
    el = attributes_to_element(parse_attribute_string("{.warn #x}"), default="div")
    assert el.tag == "div"
    assert el.get("class") == "warn"
    assert el.get("id") == "x"


def test_attributes_to_element_uses_default_tagname():
    el = attributes_to_element(parse_attribute_string("{}"), default="span")
    assert el.tag == "span"
