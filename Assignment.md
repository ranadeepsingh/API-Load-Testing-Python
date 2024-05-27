## Assignment Details
Write a program that serves as a general-purpose HTTP load-testing and benchmarking library.
Bare minimum requirements:
- Reports latencies and error rates
- Support a --qps flag to generate requests at a given fixed QPS
- Make a buildable Docker image

## Restrictions:
You may not use any existing load test or benchmarking library as a dependency.
Evaluation criteria:
Must provide accurate results. Your results will be compared against a reference implementation.
Thoughtful design of what features such a library should provide. You are expected to implement additional features and functionality beyond the bare minimum requirements.
Code, test, and documentation quality

## Time limit:
 ~24 hours

## FAQs: 
Would I need to submit a GitHub repo with documentation ? Can I have multiple files? Should I also put my code in pypi?
GitHub, PyPI, and multiple files are not required, but are all allowed. Use them to the extent you feel they demonstrate good software engineering.
Can I take it that beyond the bare minimum the assignment is open-ended?
Absolutely, this is encouraged.
If I plan on putting my code up on pypi would I still need a docker image? Or is the goal to mainly containerize all my code from a github repository?
Yes, a Docker image is required. No need to host/submit the image itself, but at least have instructions for how to build one.
