from unittest import TestCase
from rucola import Rucola
from rucola_collections import Collections


class Test(TestCase):

    def test_all(self):

        app = Rucola()

        app.create('posts/cat.md')
        app.create('posts/apple.md')
        grape = app.create('posts/grape.md')
        banana = app.create('posts/banana.md')
        orange = app.create('posts/orange.md')

        app.use(
            Collections(
                fruits={
                    'pattern': '**/*.md',
                    'sort_by': 'path',
                    'reverse': True,
                    'metadata': {'foo': 'bar'},
                    'limit': 3,
                    'filter': lambda x: x.path != 'posts/cat.md'
                })
        )

        expected = [orange, grape, banana]
        self.assertListEqual(expected, app.metadata['fruits'])

        for i in expected:
            self.assertEqual('bar', i['foo'])

    def test_metadata_collection(self):

        app = Rucola()

        app.create('index.html')
        f = app.create('foo', collection='posts')

        app.use(Collections())

        self.assertTrue('posts' in app.metadata)
        self.assertListEqual([f], app.metadata['posts'])

    def test_metadata_and_pattern(self):

        app = Rucola()

        a = app.create('apple.md')
        b = app.create('banana.txt', collection='posts')
        c = app.create('carrot.md', collection='posts')

        app.use(
            Collections(
                posts={'pattern': '*.md',
                       'sort_by': 'path'}
            )
        )

        self.assertTrue('posts' in app.metadata)
        self.assertListEqual([a, b, c], app.metadata['posts'])

    def test_empty_collection(self):

        app = Rucola()
        app.use(Collections(pages={}))

        self.assertTrue('pages' in app.metadata)
        self.assertListEqual([], app.metadata['pages'])

    # next / previous

    def test_next_previous(self):

        app = Rucola()
        a = app.create('a.html', collection='pages')
        b = app.create('b.html', collection='pages')
        c = app.create('c.html', collection='pages')

        app.use(Collections())

        self.assertIsNone(a['previous'])
        self.assertEqual(b, a['next'])
        self.assertEqual(a, b['previous'])
        self.assertEqual(c, b['next'])
        self.assertIsNone(c['next'])
        self.assertEqual(b, c['previous'])

    # Parameters

    def test_pattern(self):

        app = Rucola()
        a = app.create('apple.html')
        b = app.create('post/hello.html')
        app.create('banana.md')

        app.use(
            Collections(pages={'pattern': '**/*.html'})
        )

        self.assertListEqual([a, b], app.metadata['pages'])

    def test_sort(self):

        app = Rucola()
        c = app.create('carrot.html')
        a = app.create('apple.html')
        b = app.create('banana.html')

        app.use(
            Collections(pages={
                'pattern': '*.html',
                'sort_by': 'path'})
        )

        self.assertListEqual([a, b, c], app.metadata['pages'])

        app.use(
            Collections(pages={
                'pattern': '*.html',
                'sort_by': 'path',
                'reverse': True})
        )

        self.assertListEqual([c, b, a], app.metadata['pages'])

    def test_metadata(self):

        app = Rucola()
        f = app.create('test.html', collection='pages')

        app.use(Collections(pages={'metadata': {'foo': 'bar'}}))

        self.assertEqual('bar', f['foo'])

    def test_limit(self):

        app = Rucola()
        for i in range(10):
            app.create(str(i) + '.html')

        app.use(
            Collections(pages={
                'pattern': '*.html',
                'limit': 5})
        )

        self.assertEqual(5, len(app.metadata['pages']))

    def test_filter(self):

        def filter_(f):
            return f.path != 'test.html'

        app = Rucola()
        app.create('test.html')

        app.use(
            Collections(pages={'filter': filter_})
        )

        self.assertListEqual([], app.metadata['pages'])

