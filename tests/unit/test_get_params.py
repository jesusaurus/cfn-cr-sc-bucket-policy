import unittest

from policy_maker import app


class TestGetParams(unittest.TestCase):

  def test_bucketname_present(self):
    bucket_name = 'some-bucket'
    event = {
      'ResourceProperties': {
        'BucketName': bucket_name
      }
    }
    result = app.get_params(event)
    self.assertEqual(len(result), 3)
    self.assertEqual(result[0], bucket_name)
    self.assertEqual(result[1], [])
    self.assertFalse(result[2])


  def test_bucketname_missing(self):
    with self.assertRaises(Exception):
      event = { 'ResourceProperties': {} }
      result = app.get_params(event)


  def test_principals_present(self):
    principals = ['foo', 'bar']
    event = {
      'ResourceProperties': {
        'BucketName': 'some-bucket',
        'ExtraPrincipalArns': principals
      }
    }
    result = app.get_params(event)
    self.assertCountEqual(principals, result[1])


  def test_string_principals_converted_to_list(self):
    principals = 'foobar'
    event = {
      'ResourceProperties': {
        'BucketName': 'some-bucket',
        'ExtraPrincipalArns': principals
      }
    }
    result = app.get_params(event)
    self.assertCountEqual([principals], result[1])


  def test_require_encryption(self):
    truthies = ['true', 'True', 'TRUE', True]
    falsies = ['false', 'False', 'FALSE', '', 'foo', False, 0 ]
    for truthy in truthies:
      event = {
        'ResourceProperties': {
          'BucketName': 'some-bucket',
          'RequireEncryption': truthy
        }
      }
      result = app.get_params(event)
      self.assertTrue(result[2])
    for falsey in falsies:
      event = {
        'ResourceProperties': {
          'BucketName': 'some-bucket',
          'RequireEncryption': falsey
        }
      }
      result = app.get_params(event)
      self.assertFalse(result[2])
