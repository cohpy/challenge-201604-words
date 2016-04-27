# This .py is an AWS Lambda function, not a standalone .py

The 'requests' library is not included in the repo due to size and cross platform line feed issues.

But, it needs to be deployed with the Lambda function, since the Amazon Machine Image that backs Lambda does not have the requests library installed.  Will explain this when discussing the solution.

>Note that you can define "word" as you wish, however, your definition of "word" MUST be fully specified in text

in this implementation a 'word' is defined by the following conventions:

1.  any series of contiguous chars, separated by one or more spaces.
2.  any escape chars (e.g. \n \r etc) are stripped from the input string
2.  uppercase chars are converted to lowercase chars, to prevent capitalized occurrences of a word from creating duplicates.
3.  any chars in the Python set(string.punctuation) are stripped, to prevent words that are immediately followed by punctuation with no space in between from creating duplicates.  This has the undesirable side effect of hyphenated and apostrophed words being converted to words that are not real, but still serves to count those words correctly.

Example:
'One day, the day was a better one than that day.'
day = 3
one = 2

>your definition of "word" and word counts must be tested,

see doctest bit in Test function.  Test is rather strict, only a-z allowed.  This limits words to strict set of English words with no special chars.  This has no effect on 10 most used words in a book, but decreases accuracy for some lesser used words that contain special chars.
