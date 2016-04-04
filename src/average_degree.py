import sys
import json
import time
import heapq


class DegreeCalculator:
    tweets_heap = []
    hashtags_graph = {}

    def add_vertex_to_the_graph(self, hashtag1, hashtag2):
        if hashtag1 not in self.hashtags_graph:
            self.hashtags_graph[hashtag1] = {hashtag2: 1}
        elif hashtag2 not in self.hashtags_graph[hashtag1]:
            self.hashtags_graph[hashtag1][hashtag2] = 1
        else:
            self.hashtags_graph[hashtag1][hashtag2] += 1

    def remove_vertex_from_the_graph(self, hashtag1, hashtag2):
        connected_nodes = self.hashtags_graph[hashtag1]
        edge_weight = connected_nodes[hashtag2]
        if edge_weight <= 1:
            del connected_nodes[hashtag2]
        else:
            connected_nodes[hashtag2] = edge_weight - 1
        if not connected_nodes:
            del self.hashtags_graph[hashtag1]

    def add_hashtags_to_the_graph(self, hashtags):
         for hashtag_start in hashtags:
            for hashtag_end in hashtags:
                if hashtag_start != hashtag_end:
                    self.add_vertex_to_the_graph(hashtag_start, hashtag_end)

    def remove_hashtags_from_the_graph(self, hashtags):
        for hashtag_start in hashtags:
            for hashtag_end in hashtags:
                if hashtag_start != hashtag_end:
                    self.remove_vertex_from_the_graph(hashtag_start, hashtag_end)

    def process_tweet_data(self, hashtags, timestamp):
        def get_time_difference_in_seconds(timestamp1, timestamp2):
            return time.mktime(timestamp1) - time.mktime(timestamp2)

        if self.tweets_heap and get_time_difference_in_seconds(timestamp, self.tweets_heap[0][0]) < 0:
            return

        while self.tweets_heap and get_time_difference_in_seconds(timestamp, self.tweets_heap[0][0]) > 59:
            tweet_data = heapq.heappop(self.tweets_heap)
            self.remove_hashtags_from_the_graph(tweet_data[1])

        heapq.heappush(self.tweets_heap, (timestamp, hashtags))
        if len(hashtags) > 1:
            self.add_hashtags_to_the_graph(hashtags)

        #print self.hashtags_graph

    def get_average_degree(self):
        number_edges = 0
        vertices = self.hashtags_graph.keys()
        for vertex in vertices:
            number_edges += len(self.hashtags_graph[vertex])
        n_vertices = len(vertices)
        return 0 if n_vertices == 0 else number_edges / float(n_vertices)


input_path = sys.argv[1]
output_path = sys.argv[2]

degree_calculator = DegreeCalculator()

with open(input_path) as input_file, open(output_path, 'w') as output_file:
    for line in input_file:
        data = json.loads(line)

        if u"entities" not in data or u"created_at" not in data or u"hashtags" not in data[u"entities"]:
            continue

        current_hashtags = map(lambda hashtag: hashtag[u"text"], data[u"entities"][u"hashtags"])
        current_timestamp = time.strptime(data[u"created_at"], "%a %b %d %H:%M:%S +0000 %Y")

        degree_calculator.process_tweet_data(current_hashtags, current_timestamp)
        average_degree = degree_calculator.get_average_degree()

        output_file.write('%.2f' % average_degree + '\n')

    output_file.close()















