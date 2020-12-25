class Job:
    # The init method or constructor
    def __init__(self, position, description, link):
        self.position = position
        self.description = description
        self.link = link

    def __repr__(self):
        return "position: {0}\ndescription: {1}\nlink: {2}\n".format(self.position, self.description, self.link)
