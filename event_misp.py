class EventMisp:
    # Define an MISP Event with all the informations needed

    def __init__(self, idEvent, firstUpdate, infoEvent, timestampUpdate, isPublished, creatorOrgName):
        self.idEvent = idEvent
        self.firstUpdate = firstUpdate
        self.infoEvent = infoEvent
        self.timestampUpdate = timestampUpdate
        self.isPublished = isPublished
        self.creatorOrgName = creatorOrgName

    def prettyPrint(self):
        print("__________________")
        print("Event : ")
        print(self.idEvent)
        print(self.firstUpdate)
        print(self.infoEvent)
        print(self.timestampUpdate)
        print(self.isPublished)
        print(self.creatorOrgName)
        print("__________________")


def printEvents(events):
    for e in events:
        e.prettyPrint()
