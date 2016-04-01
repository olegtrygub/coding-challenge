import sys, json, time
import heapq

class DegreeCalculator:
    tweetsHeap = []
    hashtagsGraph = {}

    @staticmethod
    def tweets_belong_to_the_same_window(timestamp1, timestamp2):
         difference = time.mktime(timestamp2) - time.mktime(timestamp1)
         return  difference <= 60.0 and difference >= 0

    def add_vertex_to_the_graph(self, hashtag1, hashtag2):
        if hashtag1 not in self.hashtagsGraph:
            self.hashtagsGraph[hashtag1] = {hashtag2: 1}
        elif hashtag2 not in self.hashtagsGraph[hashtag1]:
            self.hashtagsGraph[hashtag1][hashtag2] = 1
        else:
            self.hashtagsGraph[hashtag1][hashtag2] += 1

    def remove_vertex_from_the_graph(self, hashtag1, hashtag2):
        connected_nodes = self.hashtagsGraph[hashtag1]
        edge_weight = connected_nodes[hashtag2]
        if edge_weight <= 1:
            del connected_nodes[hashtag2]
        else:
            connected_nodes[hashtag2] = edge_weight - 1
        if not connected_nodes:
            del self.hashtagsGraph[hashtag1]

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
        while self.tweetsHeap and not DegreeCalculator.tweets_belong_to_the_same_window(timestamp, self.tweetsHeap[0][0]):
            tweet_data = heapq.heappop(self.tweetsHeap)
            self.remove_hashtags_from_the_graph(tweet_data[1])
        if len(hashtags) > 1:
            heapq.heappush(self.tweetsHeap, (timestamp, hashtags))
            self.add_hashtags_to_the_graph(hashtags)

        print self.hashtagsGraph

    def get_average_degree(self):
        sum = 0
        vertices = self.hashtagsGraph.keys()
        for vertex in vertices:
            sum += len(self.hashtagsGraph[vertex])
        return sum / len(vertices)




input_path = sys.argv[1]
output_path = sys.argv[2]

degreeCalculator = DegreeCalculator()

with open(input_path) as input_file:
    for line in input_file:
        data = json.loads(line)
        currentHashtags = map(lambda hash: hash[u"text"], data[u"entities"][u"hashtags"])
        currentTimestamp = time.strptime(data[u"created_at"], "%a %b %d %H:%M:%S +0000 %Y")
        print currentHashtags
        degreeCalculator.process_tweet_data(currentHashtags, currentTimestamp)
        print degreeCalculator.get_average_degree()










