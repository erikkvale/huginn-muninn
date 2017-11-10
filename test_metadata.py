import unittest
from metadata import (
    BEA_API_ROOT_URL,
    BEA_API_USER_KEY,
    MetaRequestHandle
)


class TestMetadataHandler(unittest.TestCase):

    def test_init_good_result_format_arg(self):
        """
        Pass in 'JSON' as result_format arg,
        should NOT raise a ValueError
        """
        try:
            obj = MetaRequestHandle(
                base_url=BEA_API_ROOT_URL,
                user_key=BEA_API_USER_KEY,
                result_format='JSON'
            )
        except ValueError:
            self.fail("This should not have produced a ValueError")


    def test_init_bad_result_format_arg(self):
        """
        Pass in 'XML' as result_format arg,
        should raise ValueError
        """
        with self.assertRaises(ValueError):
            obj = MetaRequestHandle(
                base_url=BEA_API_ROOT_URL,
                user_key=BEA_API_USER_KEY,
                result_format='XML'
            )


    def test_init_state_variables_are_set_correctly(self):
        """
        T
        """

    def test_init_good_request(self):
        pass


    def test_init_bad_request(self):
        pass






