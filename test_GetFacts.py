import unittest
from GetFacts import SoupObjIgnoreChk
from GetFacts import CleanStr



class GetFactsTestCase(unittest.TestCase):
    """Tests for `GetFacts.py`."""

    def test_is_valid_string_not_ignored(self):
        """Is something not in IgnoreList not ignored?"""
        SoupChild = "Blah"
        MyIgnoreList = ["sortkey", "reference"]        
        self.assertFalse(SoupObjIgnoreChk(SoupChild, MyIgnoreList), msg="Valid string not ignored")
        
    def test_is_invalid_string_ignored(self):
        """Is something in IgnoreList ignored?"""
        SoupChild = "sortkey"
        MyIgnoreList = ["sortkey", "reference"]        
        self.assertTrue(SoupObjIgnoreChk(SoupChild, MyIgnoreList), msg="Invalid string ignored")
        
    def test_cleaned_string_does_not_begin_and_end_with_double_quote(self):
		"""Does cleaned string begin and end with double quote?"""
		MyString = '"blah1"'
		#self.assertRegexpMatches(MyString, "^\"[a-zA-Z0-9]+\"")
		self.assertNotRegexpMatches(CleanStr(MyString), "^\"[a-zA-Z0-9]+\"", msg="String doesn't begin and end with double quotes")
	
    def test_cleaned_string_does_not_begin_with_spaces(self):
        """Does cleaned string begin with one or more spaces?"""
        MyString = ' blah1 '
        #self.assertRegexpMatches(MyString, "^\s+[a-zA-Z0-9]+")
        self.assertNotRegexpMatches(CleanStr(MyString), "^\s+[a-zA-Z0-9]+", msg="String doesn't begin with white space")

    def test_cleaned_string_does_not_end_with_spaces(self):
        """Does cleaned string end with one or more spaces?"""
        MyString = 'blah1 '
        self.assertNotRegexpMatches(CleanStr(MyString), "^[a-zA-Z0-9]\s+", msg="String doesn't end with white space")
        
    def test_cleaned_string_does_not_have_double_spaces(self):
        """Does cleaned string contain double spaces?"""
        MyString = 'blah  blah'
        #self.assertRegexpMatches(MyString, "\s{2}")
        self.assertNotRegexpMatches(CleanStr(MyString), "\s{2}", msg="String doesn't contain double spaces")
        
    def test_cleaned_string_does_not_have_newline_character(self):
        """Does cleaned string contain newline character?"""
        MyString = 'blah\nblah'
        #self.assertRegexpMatches(MyString, "\n{1,}")
        self.assertNotRegexpMatches(CleanStr(MyString), "\n{1}", msg="String doesn't contain newline character")
        
    def test_cleaned_string_does_not_have_linefeed_character(self):
        """Does cleaned string contain linelfeed character?"""
        MyString = 'blah\rblah'
        #self.assertRegexpMatches(MyString, "\r{1,}")
        self.assertNotRegexpMatches(CleanStr(MyString), "\r{1}", msg="String doesn't contain linefeed character")
        
        
        

if __name__ == '__main__':
    unittest.main()
