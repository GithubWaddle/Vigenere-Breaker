import unittest
from Vigenere_Breaker.index_of_coincidence import find_likely_key_length


def test_find_likely_key_length():
	ciphertext = "UHVT WVML OF A IFRL MOAH PVFCR PF PJPUFRGFXG. JT GBLXT AOPUG QRNDTVDAYMY NOYGIIAH. TUJS VT A GFSG UO FFE VG TUF IAEEK PF PPIADIQFNPF CNO CBSRRDTYZ FVOD GIIF THVU. OU ZENI. DRGIAJTRMY GSYVOG GP FVOD VU."
	assert find_likely_key_length(ciphertext, 10) == 3
