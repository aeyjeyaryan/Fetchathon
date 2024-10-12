class Memory:
    def __init__(self):
        self.memories = {}

    def add(self, text, user_id):
        """Adds a memory for a specific user."""
        if user_id not in self.memories:
            self.memories[user_id] = []
        self.memories[user_id].append({"text": text})

    def search(self, query, user_id):
        """Searches for memories that match the query for a specific user."""
        if user_id not in self.memories:
            return []
        return [m for m in self.memories[user_id] if query.lower() in m["text"].lower()]
