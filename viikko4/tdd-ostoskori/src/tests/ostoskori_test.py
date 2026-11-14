import unittest
from ostoskori import Ostoskori
from tuote import Tuote

class TestOstoskori(unittest.TestCase):
    def setUp(self):
        self.kori = Ostoskori()

    def test_ostoskorin_hinta_ja_tavaroiden_maara_alussa(self):
        self.assertEqual(self.kori.hinta(), 0)
        self.assertEqual(self.kori.tavaroita_korissa(), 0)

    def test_yhden_tuotteen_lisaamisen_jalkeen_korissa_yksi_tavara(self):
        tuote = Tuote("Maito", 3)
        self.kori.lisaa_tuote(tuote)
        self.assertEqual(self.kori.tavaroita_korissa(), 1)

    def test_yhden_tuotteen_lisaamisen_jalkeen_ostokset_listaan_yksi_ostos(self):
        tuote = Tuote("Maito", 3)
        self.kori.lisaa_tuote(tuote)
        self.assertEqual(len(self.kori.ostokset()), 1)

    def test_kahden_eri_tuotteen_lisaamisen_jalkeen_ostokset_listassa_kaksi_ostosta(self):
        maito = Tuote("Maito", 3)
        leipa = Tuote("Leipä", 2)
        self.kori.lisaa_tuote(maito)
        self.kori.lisaa_tuote(leipa)
        self.assertEqual(len(self.kori.ostokset()), 2)

    def test_kahden_saman_tuotteen_lisaamisen_jalkeen_ostokset_listassa_yksi_ostos(self):
        tuote = Tuote("Maito", 3)
        self.kori.lisaa_tuote(tuote)
        self.kori.lisaa_tuote(tuote)
        self.assertEqual(len(self.kori.ostokset()), 1)

    def test_kahden_saman_tuotteen_lisaamisen_jalkeen_ostoksen_nimi_ja_lukumaara_oikein(self):
        tuote = Tuote("Maito", 3)
        self.kori.lisaa_tuote(tuote)
        self.kori.lisaa_tuote(tuote)
        ostos = self.kori.ostokset()[0]
        self.assertEqual(ostos.tuotteen_nimi(), tuote.nimi())
        self.assertEqual(ostos.lukumaara(), 2)

    def test_yhden_tuotteen_lisaamisen_jalkeen_ostoksen_tuote_ja_lukumaara_oikein(self):
        tuote = Tuote("Maito", 3)
        self.kori.lisaa_tuote(tuote)
        ostos = self.kori.ostokset()[0]
        self.assertEqual(ostos.tuotteen_nimi(), tuote.nimi())
        self.assertEqual(ostos.lukumaara(), 1)

    def test_yhden_tuotteen_lisaamisen_jalkeen_ostoskorin_hinta(self):
        tuote = Tuote("Maito", 3)
        self.kori.lisaa_tuote(tuote)
        self.assertEqual(self.kori.hinta(), 3)

    def test_kahden_eri_tuotteen_lisaamisen_jalkeen_korissa_kaksi_tavaraa(self):
        maito = Tuote("Maito", 3)
        leipa = Tuote("Leipä", 2)
        self.kori.lisaa_tuote(maito)
        self.kori.lisaa_tuote(leipa)
        self.assertEqual(self.kori.tavaroita_korissa(), 2)

    def test_kahden_eri_tuotteen_lisaamisen_jalkeen_ostoskorin_hinta_on_sama_kuin_tuotteiden_hintojen_summa(self):
        maito = Tuote("Maito", 3)
        leipa = Tuote("Leipä", 2)
        self.kori.lisaa_tuote(maito)
        self.kori.lisaa_tuote(leipa)
        self.assertEqual(self.kori.hinta(), 5)

    def test_kahden_saman_tuotteen_lisaamisen_jalkeen_korissa_kaksi_tavaraa(self):
        maito = Tuote("Maito", 3)
        self.kori.lisaa_tuote(maito)
        self.kori.lisaa_tuote(maito)
        self.assertEqual(self.kori.tavaroita_korissa(), 2)

    def test_kahden_saman_tuotteen_lisaamisen_jalkeen_ostoskorin_hinta_on_sama_kuin_2_kertaa_tuotteiden_hinta(self):
        maito = Tuote("Maito", 3)
        self.kori.lisaa_tuote(maito)
        self.kori.lisaa_tuote(maito)
        self.assertEqual(self.kori.hinta(), 6)
