# Notes

## To retrieve data from a Objective C FrozenDict

```python
@staticmethod
def get_ffd(fdict, key):
    """ Retrieve the object with the specified key from the frozen dict.
    """
    NSString = autoclass('NSString')
    string_key = NSString.stringWithUTF8String_(key)
    return fdict.objectForKey_(string_key)
```

## To retrieve the keys from an FrozenDict

```python
all_keys = frozen_dict.allKeys()  # NSArrayI
try:
    k = 0
    while True:
        obj = all_keys.objectAtIndex_(k)
        print(f"object at {k} = {obj.UTF8String()}")
        k += 1
except Exception as _e:
    pass
```

