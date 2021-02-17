class EventMisp:
    def __init__(self, idEvent, dateEvent, infoEvent, timestampUpdate, isPublished, creatorOrgName):
        self.idEvent = idEvent
        self.dateEvent = dateEvent
        self.infoEvent = infoEvent
        self.timestampUpdate = timestampUpdate
        self.isPublished = isPublished
        self.creatorOrgName = creatorOrgName

    def prettyPrint(self):
        print("__________________________________________________________")
        print("Event : ")
        print(self.idEvent)
        print(self.dateEvent)
        print(self.infoEvent)
        print(self.timestampUpdate)
        print(self.isPublished)
        print(self.creatorOrgName)
        print("__________________________________________________________")
