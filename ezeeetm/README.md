# This .py is an AWS Lambda function, not a standalone .py

The 'requests' library is not included in the repo due to size and cross platform line feed issues.

But, it needs to be deployed with the Lambda function, since the Amazon Machine Image that backs Lambda does not have the requests library installed.  Will explain this when discussing the solution.
