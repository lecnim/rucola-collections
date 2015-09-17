class Collections:
    def __init__(self, **keys):
        self.keys = keys

    def neighborhood(self, iterable):
        iterator = iter(iterable)
        prev = None
        item = iterator.__next__() # throws StopIteration if empty.
        for next in iterator:
            yield (prev,item,next)
            prev = item
            item = next
        yield (prev,item,None)

    def __call__(self, app):

        # Find using metadata

        collections = {}

        for f in app.files:
            c = f.get('collection')
            if c:
                if not c in collections:
                    collections[c] = []
                collections[c].append(f)

        # Find using pattern parameter

        for title, config in self.keys.items():

            if not (title in collections):
                collections[title] = []

            pattern = config.get('pattern')
            if pattern:

                for f in app.find(pattern):
                    if f not in collections[title]:
                        collections[title].append(f)

        # Apply config

        for title, files in collections.items():

            config = self.keys.get(title, {})

            for f in files.copy():

                # Filter

                filter_ = config.get('filter')
                if filter_ and not filter_(f):
                    files.remove(f)
                    continue

                # Metadata

                f.update(config.get('metadata', {}))

            # Sorting

            sort_by = config.get('sort_by')
            reverse = config.get('reverse', False)

            if sort_by:
                files = sorted(files, key=lambda x: x[sort_by], reverse=reverse)

            # Limit

            limit = config.get('limit')
            if limit:
                files = files[:limit]

            # Next, previous

            for prev, i, next in self.neighborhood(files):
                i['previous'] = prev
                i['next'] = next

            collections[title] = files

        app.metadata.update(collections)
