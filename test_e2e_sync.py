from pathlib import Path
from sync import sync

# def sync(source, dest, filesystem=FileSystem()):  #(1)
#     source_hashes = filesystem.read(source)  #(2)
#     dest_hashes = filesystem.read(dest)  #(2)

#     for sha, filename in source_hashes.items():
#         if sha not in dest_hashes:
#             sourcepath = Path(source) / filename
#             destpath = Path(dest) / filename
#             filesystem.copy(sourcepath, destpath)  #(3)

#         elif dest_hashes[sha] != filename:
#             olddestpath = Path(dest) / dest_hashes[sha]
#             newdestpath = Path(dest) / filename
#             filesystem.move(olddestpath, newdestpath)  #(3)

#     for sha, filename in dest_hashes.items():
#         if sha not in source_hashes:
#             filesystem.delete(dest / filename)  #(3)

class FakeFilesystem:
    def __init__(self, path_hashes):  #(1)
        self.path_hashes = path_hashes
        self.actions = []  #(2)

    def read(self, path):
        return self.path_hashes[path]  #(1)

    def copy(self, source, dest):
        self.actions.append(('COPY', source, dest))  #(2)

    def move(self, source, dest):
        self.actions.append(('MOVE', source, dest))  #(2)

    def delete(self, dest):
        self.actions.append(('DELETE', dest))  #(2)



def test_when_a_file_exists_in_the_source_but_not_the_destination():
    fakefs = FakeFilesystem({
        '/src': {"hash1": "fn1"},
        '/dst': {},
    })
    sync('/src', '/dst', filesystem=fakefs)
    assert fakefs.actions == [("COPY", Path("/src/fn1"), Path("/dst/fn1"))]


def test_when_a_file_has_been_renamed_in_the_source():
    fakefs = FakeFilesystem({
        '/src': {"hash1": "fn1"},
        '/dst': {"hash1": "fn2"},
    })
    sync('/src', '/dst', filesystem=fakefs)
    assert fakefs.actions == [("MOVE", Path("/dst/fn2"), Path("/dst/fn1"))]