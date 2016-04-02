import sys, json, time
import heapq

class DegreeCalculator:
    tweets_heap = []
    hashtags_graph = {}

    @staticmethod
    def tweets_belong_to_the_same_window(timestamp1, timestamp2):
         difference = time.mktime(timestamp2) - time.mktime(timestamp1)
         return  difference <= 60.0 and difference >= 0

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
                    self.remove_hashtags_from_the_graph(hashtag_start, hashtag_end)

    def process_tweet_data(self, hashtags, timestamp):
        while self.tweets_heap and not DegreeCalculator.tweets_belong_to_the_same_window(timestamp, self.tweets_heap[0][0]):
            tweet_data = heapq.heappop(self.tweets_heap)
            self.remove_hashtags_from_the_graph(tweet_data[1])
        if len(hashtags) > 1:
            heapq.heappush(self.tweets_heap, (timestamp, hashtags))
            self.add_hashtags_to_the_graph(hashtags)

        #print self.hashtags_graph

    def get_average_degree(self):
        sum = 0
        vertices = self.hashtags_graph.keys()
        for vertex in vertices:
            sum += len(self.hashtags_graph[vertex])
        return sum / float(len(vertices))


input_path = sys.argv[1]
output_path = sys.argv[2]

degree_calculator = DegreeCalculator()

with open(input_path) as input_file, open(output_path, 'w') as output_file:
    for line in input_file:
        data = json.loads(line)
        if not data[u"entities"] or not data[u"entities"][u"hashtags"] or not data[u"created_at"]:
            continue
        current_hashtags = map(lambda hashtag: hashtag[u"text"], data[u"entities"][u"hashtags"])
        current_timestamp = time.strptime(data[u"created_at"], "%a %b %d %H:%M:%S +0000 %Y")
        #print current_hashtags

        degree_calculator.process_tweet_data(current_hashtags, current_timestamp)
        average_degree = degree_calculator.get_average_degree()
        #print average_degree
        output_file.write('%.2f' % average_degree + '\n')

    output_file.close()















