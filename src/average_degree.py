#For readme see README.md
import sys
import json
import datetime
import heapq

# #class that encapsulates hashtag graph and counting logic
class DegreeCalculator:
    tweets_heap = []
    hashtags_graph = {}
    max_timestamp = datetime.datetime.min

    # #method that adds "hashtag" edge to the hashtags graph either by adding it or by incrementing existing weight
    def add_vertex_to_the_graph(self, hashtag1, hashtag2):
        if hashtag1 not in self.hashtags_graph:
            self.hashtags_graph[hashtag1] = {hashtag2: 1}
        elif hashtag2 not in self.hashtags_graph[hashtag1]:
            self.hashtags_graph[hashtag1][hashtag2] = 1
        else:
            self.hashtags_graph[hashtag1][hashtag2] += 1

    # #method that removes "hashtag" edge to the hashtags graph either by deleting it or by incrementing existing weight
    def remove_vertex_from_the_graph(self, hashtag1, hashtag2):
        connected_nodes = self.hashtags_graph[hashtag1]
        edge_weight = connected_nodes[hashtag2]
        if edge_weight <= 1:
            del connected_nodes[hashtag2]
        else:
            connected_nodes[hashtag2] = edge_weight - 1
        if not connected_nodes:
            del self.hashtags_graph[hashtag1]

    # #method that adds a set of hashtags for some particular tweet to the graph
    def add_hashtags_to_the_graph(self, hashtags):
         for hashtag_start in hashtags:
            for hashtag_end in hashtags:
                if hashtag_start != hashtag_end:
                    self.add_vertex_to_the_graph(hashtag_start, hashtag_end)

    # #method that removes a set of hashtags for some particular tweet to the graph
    def remove_hashtags_from_the_graph(self, hashtags):
        for hashtag_start in hashtags:
            for hashtag_end in hashtags:
                if hashtag_start != hashtag_end:
                    self.remove_vertex_from_the_graph(hashtag_start, hashtag_end)

    # #method that processes newly added tweet
    def process_tweet_data(self, hashtags, timestamp):
        def get_time_difference_in_seconds(timestamp1, timestamp2):
            return (timestamp1 - timestamp2).total_seconds()

        # #if tweet is 59 or more seconds older than maximum processes tweet than skip it
        if get_time_difference_in_seconds(self.max_timestamp, timestamp) > 59.0:
            return

        # #update maximum timestamp
        if timestamp > self.max_timestamp:
            self.max_timestamp = timestamp

        # #remove tweets older that 59 seconds than current from tweets heap
        while self.tweets_heap and get_time_difference_in_seconds(timestamp, self.tweets_heap[0][0]) > 59.0:
            tweet_data = heapq.heappop(self.tweets_heap)
            self.remove_hashtags_from_the_graph(tweet_data[1])

        # #push tweet on the heap and add hashtags to the graph if it contains more than 2 hashtags
        heapq.heappush(self.tweets_heap, (timestamp, hashtags))
        if len(hashtags) > 1:
            self.add_hashtags_to_the_graph(hashtags)

    # #method that calculates current average degree for the graph
    def get_average_degree(self):
        number_edges = 0
        vertices = self.hashtags_graph.keys()
        for vertex in vertices:
            number_edges += len(self.hashtags_graph[vertex])
        n_vertices = len(vertices)
        return 0 if n_vertices == 0 else number_edges / float(n_vertices)


# #main script
# #collect parameters
input_path = sys.argv[1]
output_path = sys.argv[2]

degree_calculator = DegreeCalculator()

with open(input_path) as input_file, open(output_path, 'w') as output_file:
    for line in input_file:
        data = json.loads(line)

        # #if tweet data is not correct skip it
        if u"entities" not in data or u"created_at" not in data or u"hashtags" not in data[u"entities"]:
            continue

        # #extract hashtags from tweet data
        current_hashtags = map(lambda hashtag: hashtag[u"text"], data[u"entities"][u"hashtags"])
        current_timestamp = datetime.datetime.strptime(data[u"created_at"], "%a %b %d %H:%M:%S +0000 %Y")

        # #process tweet and calculate average degree
        degree_calculator.process_tweet_data(current_hashtags, current_timestamp)
        average_degree = degree_calculator.get_average_degree()

        output_file.write('%.2f' % average_degree + '\n')

    output_file.close()















