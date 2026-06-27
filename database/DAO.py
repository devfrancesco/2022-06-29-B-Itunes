from database.DB_connect import DBConnect
from model.album import Album
from model.arco import Arco


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllAlbum(n):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ select a.*, t.durata as Durata
                    from (
                        select t.AlbumId, sum(t.Milliseconds )/1000 as Durata
                        from track t
                        group by t.AlbumId 
                        having durata > %s
                    ) as t, album a 
                    where a.AlbumId = t.albumid 
                    order by a.Title """
        cursor.execute(query, (n,))
        for row in cursor:
            results.append(Album(**row))
        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllEdges(n, idMapA):
        conn = DBConnect.get_connection()
        results = []
        cursor = conn.cursor(dictionary=True)
        query = """ with durata as (
                    select t.AlbumId, sum(t.Milliseconds )/1000 as Durata
                    from track t
                    group by t.AlbumId 
                    having durata > %s
                    )
                select d.albumid as id1, d2.albumid as id2, (d.durata + d2.durata) as peso
                from durata d
                join durata d2 on d.albumid <> d2.albumid 
                where d.durata < d2.durata 
                having peso > 4 * %s """
        cursor.execute(query, (n,n))
        for row in cursor:
            results.append(Arco(idMapA[row['id1']], idMapA[row['id2']], row['peso']))
        cursor.close()
        conn.close()
        return results