class AmbiguousTrie:
    def __init__(self, key=None, value=None):
        self.children = {}
        self.key = key
        self.value = value

    def __getitem__(self, key):
        node = self
        while True:
            if not key:
                return node
            prefix, rest = key[0], key[1:]
            node = node.children[prefix]
            key = rest

    def __setitem__(self, key, value):
        node = self
        while True:
            prefix, rest = key[0], key[1:]
            node = node.children.setdefault(prefix, AmbiguousTrie(prefix))
            if not rest:
                node.value = value
                break
            key = rest

    def get_matches(self, key):
        next_visit = (key, self)
        to_visit = []

        while True:
            key, node = next_visit
            prefix, rest = key[0], key[1:]
            if not rest:
                if prefix in node.children and node.children[prefix].value:
                    yield node.children[prefix].value
            else:
                if prefix in node.children:
                    to_visit.append((rest, node.children[prefix]))
                if 'N' in node.children:
                    to_visit.append((rest, node.children['N']))
                if prefix == 'N':
                    to_visit.extend((rest, c) for c in node.children.values())

            try:
                next_visit = to_visit.pop()
            except IndexError:
                break
