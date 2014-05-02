from app_tt.engine.model import Model
import unittest
from unittest import TestCase
from app_tt.application import app as application


class test_model(TestCase):

    def setUp(self):
        self.model = Model()
        self.BOOK_ID = "test_short_name1"
        self.PAGE_ID = 1
        self.TABLE_ID = 1
        self.FATOR = 40
        app = application
        app.config['TESTING'] = True
        self.app = application.test_client()

    def tearDown(self):
        return
        self.model.del_where("cell", "table_id", self.TABLE_ID)
        self.model.del_where("page_table", "page_id", self.PAGE_ID)
        self.model.del_where("page", "book_id", self.BOOK_ID)
        self.model.del_where("book", "id", self.BOOK_ID)

    def test_insert(self):
        insert = self.model.insert_db(table="book", id=self.BOOK_ID,
                                      title="title_test",
                                      publisher="publisher_test",
                                      contributor="contributor_test")
        self.assertTrue(insert)

        insert = self.model.insert_db(table="page", id=self.PAGE_ID,
                                      url="http://localhost/page_url_test.png",
                                      book_id=self.BOOK_ID)
        self.assertTrue(insert)

        insert = self.model.insert_db(
            table="page_table", id=self.TABLE_ID,
            book_id=self.BOOK_ID,
            url="http://localhost/table_url_test.png",
            top_pos=0, left_pos=0, page_id=self.PAGE_ID,
            source="teste_library", title="test table1",
            subtitle="subtitle table1", context="made to test")

        self.assertTrue(insert)

        FATOR = self.FATOR

        for i in range(10):
            insert = self.model.insert_db(
                table="cell", table_id=self.TABLE_ID,
                book_id=self.BOOK_ID, page_id=self.PAGE_ID,
                x0=i*FATOR, y0=i*FATOR, x1=(i*FATOR) + FATOR,
                y1=(i*FATOR) + FATOR, text="texto_" + chr(97 + i))
            self.assertTrue(insert)

    def test_get_cells(self):
        cells = self.model.get_cells(self.BOOK_ID, self.PAGE_ID, self.TABLE_ID)
        FATOR = self.FATOR
        print range(len(cells))
        points = [[
            i*FATOR, i*FATOR,
            (i*FATOR) + FATOR, (i*FATOR) + FATOR,
            "texto_" + chr(97 + i)] for i in range(len(cells))]

        for i in range(len(cells)):
            self.assertEquals(
                tuple(points[i]), cells[i],
                "cell should be equal to %s" %
                str(tuple(points[i])))


if __name__ == "__main__":
    unittest.main()
