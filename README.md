# punwef
Potentially UNwanted WEbsite Filter
==
## Test Types

* Ad real estate - how much % of the page is ads? Can we diff with adblocker? Detect things that look like ads? Like if they load after the page is done loading. Score page based on that.
* Takeover popups on mobile (“congrats you’re the 1000th iPhone user”)
* Pop ups that happen upon clicking in white space or following an internal link on the page

## Models 


###Examination


* url
* submitting_user
* is_spam
* spam_detection_version
* spam_score
* subreddit
* reddit post id
* reddit comment id

###SubReddit

* name
* url
* update_interval

###Test

* type
* result_code
* examination

###TestType

* name
* description

###ResultType

* name
* description
* importance_weight
