# Search contract

`search(records, limit=None)` returns the first records in their original order.
None defaults to 100. A zero limit returns an empty list. Positive integer limits
return at most that many records. Negative and noninteger limits are outside scope.
