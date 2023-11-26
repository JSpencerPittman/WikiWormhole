class WikipageTable(object):
    def __init__(self, root):
        self.root = root
        self.table = dict()
        self.size = 1

    def spot(self, subject, source=""):
        if subject in self.table:
            self.table[subject][0] += 1
            
            if source != "" and self.table[subject][1] == "":
                self.table[subject][1] = source
        
        else:
            self.table[subject] = [1, source]
            self.size += 1

    def entry_exists(self, subject):
        return subject in self.table
    
    def hits(self, subject):
        if subject in self.table:
            return self.table[subject][0]
        else:
            return 0
        
    def parent(self, subject):
        if subject not in self.table:
            return ""
        return self.table[subject][1]
    
    def unravel(self, subject):
        pathway = [subject]
        
        while self.parent(subject) != self.root:
            if subject == "":
                raise Exception("NULL SUBJECT")
            subject = self.parent(subject)
            pathway.append(subject)
        pathway.append(self.root)

        return pathway[::-1]

    def keys(self):
        return list(self.table.keys())
    
    def __len__(self):
        return self.size
    
