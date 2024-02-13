import datetime

"""esto hay que chequear todo."""

class Logger:
    def __init__(self):
        self.travel_history = {}
        self.encounter_history = {}
        self.text_list = {}

    def add_dead_history():
        return 1
    
    def add_travel_history(self, location, party):
        if location not in self.travel_history:
            self.travel_history[location] = [party]
        else:
            self.travel_history[location].append(party)

    def add_encounter_history(self, location, party, deads): 
        if location not in self.travel_history:
            self.travel_history[location] = [(party, deads)]
        else:
            self.travel_history[location].append((party, deads))   

    def prepare_encounter_history(self):
        for x in self.encounter_history:
            confrontations = (", ").join(self.encounter_history[x][0]) + " fought at " + x + " and " + (", ").join(self.encounter_history[x][1]) + " died."
            if x not in self.text_list:
                self.text_list[x] = [confrontations]
            else:
                self.text_list[x].append(confrontations) 

    def prepare_travel_write(self):
        for x in self.travel_history:
            arrived = (", ").join(self.travel_history[x]) + " arrived at " + x
            if x not in self.text_list:
                self.text_list[x] = [arrived]
            else:
                self.text_list[x].append(arrived)   

    def add_plain_text(self, msg):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('dungeon_crawl.log', 'a') as log_file:
            for msg in self.text_list:
                log_file.write(f'{timestamp} - {msg}\n')

    def resolve_round(self):
        """
        Logs messages related to the dungeon crawl.
        """
        self.prepare_travel_write()
        self.prepare_encounter_history()
        

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open('dungeon_crawl.log', 'a') as log_file:
            for location in self.text_list:
                for msg in self.text_list[location]:
                    log_file.write(f'{timestamp} - {msg}\n')
