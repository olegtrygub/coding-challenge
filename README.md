##Solution

Solution is developed in Python 2.7 using only standard libraries: sys, json, time, heapq.

General approach is based on using min-heap to store tweets using timestamp as key and storing hashtag graph using
adjanceny lists representation. Every time tweet is processed, it's being added to the heap if its timestamp falls in
the 60-second window (or ignored if it falls behind) and tweets older then 60 seconds are removed. Min heap is used
to quickly find and delete tweets with older timestamps.

Every time new tweet is processed its hashtags are added to hashtag graph. If corresponding edge between tags already exists edge
weight is incremented. If tweet becomes older than 60 seconds weights of graph edges that correspond to its hashtags are decremented.
If edge's weight reaches zero, it's removed from the graph entirely. To calculate average degree we ignore weights (which basically serve
as reference counters) and just sum adjacency list lengths.

While developing this script I considered another approach suggested by one of answers in the FAQ - to keep track of hashtag graph
edges timestamps, but I considered this approach less beneficial, because it requires the same algorithmic complexity (some sort of
priority queue for tweets plus checking and updatind graph edges when adding or removing tweets) yet timestamps seems to be
less useful piece of information to store. If one thinks of future applications of this script, one can argue that storing
weights of the edges can be very natural and useful for counting other statistics. So I rejected this approach.