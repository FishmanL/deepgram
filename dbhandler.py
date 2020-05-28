import psycopg2
import yaml

from wavprocessor import processfile, savetotemp

from psycopg2.extras import RealDictCursor

selectsql = """SELECT * FROM wavfiles WHERE (nframes = %(nframes)s OR %(nframes)s IS NULL)
      AND (samplewidth = %(samplewidth)s OR %(samplewidth)s IS NULL)
      AND (framerate = %(framerate)s OR %(framerate)s IS NULL)
      AND (filename = %(filename)s OR %(filename)s IS NULL)
      AND (numchannels = %(numchannels)s OR %(numchannels)s IS NULL)
      AND (userid = %(userid)s OR %(userid)s IS NULL)
      AND (seconds = %(seconds)s OR %(seconds)s IS NULL)"""

insertsql = """insert into wavfiles (nframes, samplewidth, userid, content, numchannels, filename, seconds, framerate) 
VALUES (%(nframes)s, %(samplewidth)s, %(userid)s, %(content)s, %(numchannels)s, %(filename)s, %(seconds)s, %(framerate)s)"""

selectbynamesql = "SELECT * from wavfiles where (filename = %(filename)s OR %(filename)s IS NULL) AND (userid = %(userid)s OR %(userid)s IS NULL)"


class Dict2Obj(object):
    """
    Turns a dictionary into a class
    """

    # ----------------------------------------------------------------------
    def __init__(self, dictionary):
        """Constructor"""
        for key in dictionary:
            setattr(self, key, dictionary[key])


with open("config.yaml", "r") as f:
    configfile = yaml.load(f, Loader=yaml.FullLoader)


def preprocessdict(indict):
    retdict = indict
    if "userid" not in indict:
        retdict["userid"] = 1
    keylst = ["nframes", "samplewidth", "userid", "numchannels", "filename", "seconds", "framerate"]
    for key in keylst:
        if key not in indict:
            retdict[key] = None
    return retdict


def searchformatches(inreq):
    """
    finds al rows corresponding to a given request
    :param inreq: incoming request args
    :return: all matching wav files + metadata (to be split)
    """
    newreq = preprocessdict(inreq)
    conn = psycopg2.connect(user='postgres', password=configfile["password"], database='deepgram')

    with conn.cursor(cursor_factory = RealDictCursor) as cur:
        try:
            cur.execute(selectsql, newreq)
            return [dict(item) for item in cur.fetchall()]
        except Exception as e:
            print(e)
        finally:
            conn.commit()




def insertmatch(member):
    """
    given a row from wavprocessor. saves it
    :param member: the member object
    :return: a boolean indicating successful or failed saving

    """

    if "userid" not in member:
        member["userid"] = 1
    conn = psycopg2.connect(user='postgres', password=configfile["password"], database='deepgram')
    with conn.cursor() as cur:
        try:
            cur.execute(insertsql, member)
            conn.commit()
            return True
        except Exception as e:
            conn.commit()
            raise e


if __name__ == "__main__":
    savetotemp(searchformatches(dict())[0])
    print(searchformatches(dict()))
