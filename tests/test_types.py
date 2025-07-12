"""Test Deluge data types."""

import pytest
from datetime import datetime
import json

from deluge_compat.types import Map, List, DelugeString, deluge_string


class TestMap:
    """Test Deluge Map type."""
    
    def test_creation(self):
        """Test Map creation and basic operations."""
        m = Map()
        assert len(m) == 0
        assert m.isEmpty() is True
    
    def test_put_and_get(self):
        """Test put and get operations."""
        m = Map()
        m.put("key1", "value1")
        m.put("key2", 42)
        
        assert m.get("key1") == "value1"
        assert m.get("key2") == 42
        assert m.get("nonexistent") is None
        assert len(m) == 2
    
    def test_containKey(self):
        """Test containKey method."""
        m = Map()
        m.put("existing", "value")
        
        assert m.containKey("existing") is True
        assert m.containKey("nonexistent") is False
    
    def test_containValue(self):
        """Test containValue method."""
        m = Map()
        m.put("key", "value")
        
        assert m.containValue("value") is True
        assert m.containValue("nonexistent") is False
    
    def test_keys(self):
        """Test keys method."""
        m = Map()
        m.put("a", 1)
        m.put("b", 2)
        
        keys = m.keys()
        assert isinstance(keys, List)
        assert "a" in keys
        assert "b" in keys
        assert len(keys) == 2
    
    def test_putAll(self):
        """Test putAll method."""
        m1 = Map()
        m1.put("a", 1)
        
        m2 = Map()
        m2.put("b", 2)
        m2.put("c", 3)
        
        m1.putAll(m2)
        assert len(m1) == 3
        assert m1.get("a") == 1
        assert m1.get("b") == 2
        assert m1.get("c") == 3


class TestList:
    """Test Deluge List type."""
    
    def test_creation(self):
        """Test List creation."""
        l = List()
        assert len(l) == 0
        assert l.isEmpty() is True
        assert l.isempty() is True  # Test alias
    
    def test_add_and_get(self):
        """Test add and get operations."""
        l = List()
        l.add("item1")
        l.add(42)
        
        assert l.get(0) == "item1"
        assert l.get(1) == 42
        assert l.get(10) is None  # Out of bounds
        assert l.size() == 2
    
    def test_removeElement(self):
        """Test removeElement method."""
        l = List()
        l.add("a")
        l.add("b")
        l.add("a")
        
        l.removeElement("a")
        assert l.size() == 2
        assert l.get(0) == "b"
        assert l.get(1) == "a"
    
    def test_addAll(self):
        """Test addAll method."""
        l1 = List()
        l1.add(1)
        l1.add(2)
        
        l2 = List()
        l2.add(3)
        l2.add(4)
        
        l1.addAll(l2)
        assert l1.size() == 4
        assert l1.get(2) == 3
        assert l1.get(3) == 4
    
    def test_sort(self):
        """Test sort method."""
        l = List()
        l.add(3)
        l.add(1)
        l.add(2)
        
        l.sort(True)  # Ascending
        assert l.get(0) == 1
        assert l.get(1) == 2
        assert l.get(2) == 3
        
        l.sort(False)  # Descending
        assert l.get(0) == 3
        assert l.get(1) == 2
        assert l.get(2) == 1
    
    def test_distinct(self):
        """Test distinct method."""
        l = List()
        l.add(1)
        l.add(2)
        l.add(1)
        l.add(3)
        l.add(2)
        
        distinct = l.distinct()
        assert distinct.size() == 3
        assert 1 in distinct
        assert 2 in distinct
        assert 3 in distinct
    
    def test_intersect(self):
        """Test intersect method."""
        l1 = List()
        l1.add(1)
        l1.add(2)
        l1.add(3)
        
        l2 = List()
        l2.add(2)
        l2.add(3)
        l2.add(4)
        
        intersection = l1.intersect(l2)
        assert intersection.size() == 2
        assert 2 in intersection
        assert 3 in intersection
    
    def test_sublist(self):
        """Test sublist method."""
        l = List()
        for i in range(5):
            l.add(i)
        
        sub = l.sublist(1, 3)
        assert sub.size() == 2
        assert sub.get(0) == 1
        assert sub.get(1) == 2
        
        # Test without end index
        sub2 = l.sublist(2)
        assert sub2.size() == 3
        assert sub2.get(0) == 2
    
    def test_indexOf(self):
        """Test indexOf and lastindexOf methods."""
        l = List()
        l.add("a")
        l.add("b")
        l.add("a")
        
        assert l.indexOf("a") == 0
        assert l.lastindexOf("a") == 2
        assert l.indexOf("c") == -1
        assert l.lastindexOf("c") == -1


class TestDelugeString:
    """Test Deluge String type."""
    
    def test_creation(self):
        """Test string creation."""
        s = deluge_string("Hello World")
        assert isinstance(s, DelugeString)
        assert str(s) == "Hello World"
    
    def test_contains(self):
        """Test contains method."""
        s = deluge_string("Hello World")
        assert s.contains("World") is True
        assert s.contains("world") is False  # Case sensitive
        assert s.containsIgnoreCase("world") is True
        assert s.contains("xyz") is False
    
    def test_startsWith_endsWith(self):
        """Test startsWith and endsWith methods."""
        s = deluge_string("Hello World")
        assert s.startsWith("Hello") is True
        assert s.startsWith("World") is False
        assert s.endsWith("World") is True
        assert s.endsWith("Hello") is False
    
    def test_case_conversion(self):
        """Test case conversion methods."""
        s = deluge_string("Hello World")
        assert s.toUpperCase() == "HELLO WORLD"
        assert s.toLowerCase() == "hello world"
        assert isinstance(s.toUpperCase(), DelugeString)
    
    def test_length(self):
        """Test length method."""
        s = deluge_string("Hello")
        assert s.length() == 5
        
        empty = deluge_string("")
        assert empty.length() == 0
    
    def test_substring(self):
        """Test substring methods."""
        s = deluge_string("Hello World")
        
        assert s.substring(0, 5) == "Hello"
        assert s.substring(6) == "World"
        assert s.subString(0, 5) == "Hello"  # Test alias
        assert s.subText(0, 5) == "Hello"  # Test alias
        
        assert isinstance(s.substring(0, 5), DelugeString)
    
    def test_indexOf(self):
        """Test indexOf and lastIndexOf methods."""
        s = deluge_string("Hello Hello World")
        
        assert s.indexOf("Hello") == 0
        assert s.lastIndexOf("Hello") == 6
        assert s.indexOf("xyz") == -1
    
    def test_replace_methods(self):
        """Test replace methods."""
        s = deluge_string("Hello Hello World")
        
        assert s.replaceAll("Hello", "Hi") == "Hi Hi World"
        assert s.replaceFirst("Hello", "Hi") == "Hi Hello World"
        assert isinstance(s.replaceAll("Hello", "Hi"), DelugeString)
    
    def test_remove_methods(self):
        """Test remove methods."""
        s = deluge_string("Hello Hello World")
        
        assert s.remove("Hello ") == "World"
        assert s.removeFirstOccurence("Hello ") == "Hello World"
        assert s.removeLastOccurence(" Hello") == "Hello World"
    
    def test_prefix_suffix(self):
        """Test prefix and suffix methods."""
        s = deluge_string("user@example.com")
        
        assert s.getPrefix("@") == "user"
        assert s.getSuffix("@") == "example.com"
        assert isinstance(s.getPrefix("@"), DelugeString)
    
    def test_character_filtering(self):
        """Test character filtering methods."""
        s = deluge_string("Hello123!@#")
        
        alpha = s.getAlpha()
        assert alpha == "Hello"
        assert alpha.length() == 5
        
        alphanum = s.getAlphaNumeric()
        assert alphanum == "Hello123"
        assert alphanum.length() == 8
    
    def test_occurrence_methods(self):
        """Test occurrence counting."""
        s = deluge_string("Hello Hello World")
        
        assert s.getOccurence("Hello") == 2
        assert s.getOccurence("o") == 3
        assert s.getOccurence("xyz") == 0
    
    def test_equality_methods(self):
        """Test equality methods."""
        s = deluge_string("Hello")
        
        assert s.equalsIgnoreCase("hello") is True
        assert s.equalsIgnoreCase("HELLO") is True
        assert s.equalsIgnoreCase("world") is False
    
    def test_toList(self):
        """Test toList method."""
        s = deluge_string("a,b,c")
        
        list_result = s.toList(",")
        assert isinstance(list_result, List)
        assert list_result.size() == 3
        assert list_result.get(0) == "a"
        assert list_result.get(1) == "b"
        assert list_result.get(2) == "c"
        
        # Test character splitting
        char_list = deluge_string("abc").toList("")
        assert char_list.size() == 3
        assert char_list.get(0) == "a"
    
    def test_toMap(self):
        """Test toMap method."""
        json_str = deluge_string('{"key": "value", "number": 42}')
        
        map_result = json_str.toMap()
        assert isinstance(map_result, Map)
        assert map_result.get("key") == "value"
        assert map_result.get("number") == 42
        
        # Test invalid JSON
        invalid_str = deluge_string("not json")
        with pytest.raises(ValueError):
            invalid_str.toMap()
    
    def test_toJSONList(self):
        """Test toJSONList method."""
        json_str = deluge_string('[1, 2, 3]')
        
        list_result = json_str.toJSONList()
        assert isinstance(list_result, List)
        assert list_result.size() == 3
        assert list_result.get(0) == 1
    
    def test_toLong(self):
        """Test toLong method."""
        s = deluge_string("123")
        assert s.toLong() == 123
        
        hex_s = deluge_string("0x1F")
        assert hex_s.toLong() == 31
        
        invalid_s = deluge_string("not a number")
        with pytest.raises(ValueError):
            invalid_s.toLong()
    
    def test_toDate(self):
        """Test toDate method."""
        date_str = deluge_string("2024-01-01")
        date_obj = date_str.toDate()
        assert isinstance(date_obj, datetime)
        assert date_obj.year == 2024
        assert date_obj.month == 1
        assert date_obj.day == 1
        
        # Test invalid date
        invalid_date = deluge_string("not a date")
        with pytest.raises(ValueError):
            invalid_date.toDate()
    
    def test_padding(self):
        """Test padding methods."""
        s = deluge_string("hello")
        
        left_padded = s.leftPad("0", 8)
        assert left_padded == "000hello"
        assert isinstance(left_padded, DelugeString)
        
        right_padded = s.rightPad("!", 8)
        assert right_padded == "hello!!!"
    
    def test_trim(self):
        """Test trim method."""
        s = deluge_string("  hello world  ")
        trimmed = s.trim()
        assert trimmed == "hello world"
        assert isinstance(trimmed, DelugeString)
    
    def test_regex_matches(self):
        """Test regex matching."""
        s = deluge_string("hello123")
        
        assert s.matches(r"hello\d+") is True
        assert s.matches(r"world\d+") is False