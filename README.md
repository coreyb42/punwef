# punwef
Potentially UNwanted WEbsite Filter
==
## Test Types

* Ad real estate - how much % of the page is ads? Can we diff with adblocker? Detect things that look like ads? Like if they load after the page is done loading. Score page based on that.
* Takeover popups on mobile (“congrats you’re the 1000th iPhone user”)
* Pop ups that happen upon clicking in white space or following an internal link on the page
* Lighthouse times - how long to responsiveness

## Models

###Examination

A series of tests of a given URL.

* url
* is_spam
* spam_detection_version
* spam_score
* start_time
* finish_time

###ExaminationMeasure

The result of an individual test for a given URL.

* examination
* numeric_value
* string_value
* examination_measure_type

###ExaminationMeasureType

A type of individual measurement - be it render time, size of page, etc.

* name
* description

###RedditItem

A comment or post on Reddit.

* reddit_post_id
* reddit_comment_id
* submitting_user
* commented_back - whether or not the bot has commented at this
* subreddit

###RedditItemExamination

An instance of checking a URL from a post or comment on Reddit. Many to many relationship.

* reddit_item_id
* examination_id

###SubReddit

A community on Reddit. The bot will check a given community for new posts at a given interval in seconds.

* name
* url
* update_interval

###Test

A given instance of running a suite of measurements for a given, URL, along with overall results.

* type
* result_code
* examination

###TestType

A suite of measurements.

* name
* description

###ResultType

An overall result of a suite of tests.

* name
* description
* importance_weight

###RedditIgnoreUser

A request for not testing the URLs submitted by a given user. If overridden, 
is ignored; this can be used for obvious spambots who request to be ignored.

* username
* date_created
* override - whether or not we should override the ignoring of this user
* override_readon - why we're overriding the ignore
