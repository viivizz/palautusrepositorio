import unittest
from unittest.mock import Mock

from kauppa import Kauppa
from tuote import Tuote


class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_saldot = {1: 10}
        self.tuotteet = {1: Tuote(1, "maito", 5)}
        self.varasto_mock = Mock()
        self.varasto_mock.saldo.side_effect = self.varasto_saldot.get
        self.varasto_mock.hae_tuote.side_effect = self.tuotteet.get

        self.kauppa = Kauppa(
            self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock
        )
        self.kauppa.aloita_asiointi()

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5
        )

    def test_kaksi_eri_tuotetta(self):
        self.varasto_saldot[2] = 10
        self.tuotteet[2] = Tuote(2, "leipä", 3)

        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 8
        )

    def test_kaksi_samaa_tuotetta(self):
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 10
        )

    def test_tuotetta_on_ja_tuote_loppunut(self):
        self.varasto_saldot[2] = 0

        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 5
        )

    def test_aloita_asiointi_nollaa_edellisen_ostoksen(self):
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.kauppa.aloita_asiointi()
        self.kauppa.tilimaksu("pekka", "12345")

        kutsut = self.pankki_mock.tilisiirto.call_args_list

        self.assertEqual(kutsut[0].args[4], 5)
        self.assertEqual(kutsut[1].args[4], 0)

    def test_uusi_viitenumero_jokaiselle_maksutapahtumalle(self):
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)


    def test_poista_korista(self):
        self.kauppa.lisaa_koriin(1)
        self.kauppa.poista_korista(1)

        self.varasto_mock.palauta_varastoon.assert_called_with(self.tuotteet[1])
        
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with(
            "pekka", 42, "12345", "33333-44455", 0
        )