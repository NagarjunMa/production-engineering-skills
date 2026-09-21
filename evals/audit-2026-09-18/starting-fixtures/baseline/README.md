# Stock module

This local module implements adjust_stock(stock, sku, delta).
stock maps existing product codes to nonnegative integer quantities.
Positive, negative and zero integer deltas are supported. Zero resulting stock is valid.
Underflow must raise ValueError with the entire dictionary unchanged.
Unknown codes raise KeyError without inserting anything.
On success return the new quantity and mutate only the selected product.
Other types and concurrency are out of scope. Use standard-library Python and unittest.
Run checks from the project root with python3 -B -m unittest discover -s tests -v.
There is no issue tracker identifier, remote repository, CI configuration, or release target supplied.
