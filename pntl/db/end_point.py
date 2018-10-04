"""
EntryPoint will be act as interface
medium for acessing the db api (sqlalchemy).

.. warning::

    Please install `SQL Database driver` for python
    manully `driver link <https://docs.sqlalchemy.org/en/latest/dialects/>`

Hash Value's
-------------

Hash will be saved on to the database based
on the hash value return by the function.
As the hash function depends on the system's
property, so that hash value must be dependent
on the system's such as seed values.
To avoid so unnessary general confussion,
"Is it possible to distribute the db backup for another's system
without any problem?"
It is highly recomment not to make any dependency
based on hash value (such as searching or filtering).

.. note::

    Simplest form of the about paragraph, relay hash value
    if you and only you be the one to be
    using db.

Change the class name in the .env to `DistPackage` to
accessing the table which is related to the elasticserach
stores and set bash for the enviroment variable
`ELASTICSEARCH_HOST`
(follow `link <http://elasticsearch-dsl.readthedocs.io/>`).

"""

from sqlalchemy.exc import IntegrityError

from pntl.db.config import SessionMaker
from pntl.db.utils import import_class, env_str

package = "pntl.db.model.{}".format(env_str("DB_CLASS"))


class EntryPoint:

    """EntryPoint class define as access point
    for the class in `db.model` file.

    """

    def __init__(self):

        self.db = import_class(package)
        self.session = SessionMaker()
        self.create_table()

    def create_table(self):

        from pntl.db.config import Base, engine

        return Base.metadata.create_all(engine)

    def insert(self, tagged=None):

        if not isinstance(tagged, dict) and not tagged:

            ValueError("given value must `dict` with non empty..")

        tagged["words"] = " ".join(tagged["words"])

        try:

            self.session.add(self.db(**tagged))

        except IntegrityError as e:
            print("duplicate sentence")

    def filter(self):
        # arg will be selected soon..
        # In RoadMap
        raise NotImplementedError("This function has not been implemented")

    def save(self):

        self.session.commit()

    def roll_back(self):

        self.session.rollback()
