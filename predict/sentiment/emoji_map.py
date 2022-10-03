class EmojiMap():

    def buildEmojiMap(self):
        emoji_maps = list()
        emoji_map = {}
        with open('sentiment/emoji_map.txt', 'r') as data:
            for line in data.read().split("\n"):
                if len(line) > 2:
                    emoji_map["unicode"] = line.split()[1]
                    emoji_map["name"] = self.findMiddleText("name: ", " sentiment:", line)
                    emoji_map["sentiment"] = self.findMiddleText("sentiment: ", " tags:", line)
                    emoji_map["tags"] = self.findMiddletoEndLine("tags: ", line)
                    emoji_maps.append(emoji_map)
                    emoji_map = {}
        return emoji_maps

    def findMiddleText(self, start, end, line):
        foundWord = ""
        if line.find(start):
            startAndword = line[line.find(start):line.rfind(end)]
            foundWord = startAndword[len(start):]
            return foundWord


    def findMiddletoEndLine(self, start, line):
        foundWord = ""
        if line.find(start):
            startAndword = line[line.find(start):]
            foundWord = startAndword[len(start):]
            return foundWord
