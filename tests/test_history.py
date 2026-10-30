
# ============================================================
# IMPORTS - Gerekli modüller
# ============================================================

import unittest

from robot_lab.core.simulation import RobotSimulation


# ============================================================
# TEST CLASS - SIMULATION HISTORY TESTS
# Robotun hareket geçmişi birim testleri
# ============================================================

class TestSimulationHistory(unittest.TestCase):
    """
    RobotSimulation sınıfının hareket geçmişini test eder.

    Bu sınıfta dört temel özellik doğrulanır:

    1. Initial History:
       Simülasyon başladığında başlangıç kaydının
       doğru oluşturulması.

    2. History Growth:
       Her hareketin geçmişe yeni bir kayıt eklemesi.

    3. Belief History:
       Önceki hareketlere ait inanç dağılımlarının
       sonraki hareketlerde değişmeden korunması.

    4. History Copy Protection:
       Dışarıya döndürülen geçmiş kopyasında yapılan
       değişikliklerin asıl kayıtları etkilememesi.

    unittest.TestCase:
    Python'un birim test altyapısını sağlar.
    """

    # ========================================================
    # TEST 1 - INITIAL HISTORY
    # Başlangıç geçmişini doğrulama
    # ========================================================

    def test_initial_history(self):
        """
        Simülasyonun başlangıç kaydını kontrol eder.

        Beklenen sonuçlar:
        - Geçmişte yalnızca 1 kayıt bulunmalıdır.
        - Kayıt adımı 0 olmalıdır.
        - Hareket komutu START olmalıdır.
        - Gerçek konum Office olmalıdır.
        - P(Office) = 1.0 olmalıdır.

        Başlangıç kaydı henüz bir hareket
        gerçekleştirilmeden oluşturulur.
        """

        # 1. ROBOT SİMÜLASYONUNU OLUŞTUR
        # Robot Office odasında başlatılır.
        #
        # __init__() içerisinde başlangıç kaydı
        # otomatik olarak history listesine eklenir.
        simulation = RobotSimulation(
            start_room="Office"
        )

        # 2. HAREKET GEÇMİŞİNİ AL
        # get_history() kayıtların bağımsız
        # kopyalarını içeren bir liste döndürür.
        history = simulation.get_history()

        # 3. KAYIT SAYISINI KONTROL ET
        # Henüz hareket yapılmadığından
        # yalnızca başlangıç kaydı bulunmalıdır.
        #
        # len(history) = 1
        self.assertEqual(
            len(history),
            1
        )

        # 4. İLK KAYDA ERİŞ
        # Python listelerinde indeksler 0'dan başlar.
        #
        # history[0] -> Başlangıç kaydı
        first_record = history[0]

        # 5. ZAMAN ADIMINI KONTROL ET
        # Başlangıç durumunda t = 0 olmalıdır.
        self.assertEqual(
            first_record["step"],
            0
        )

        # 6. HAREKET KOMUTUNU KONTROL ET
        # START gerçek bir hareket komutu değildir.
        # Simülasyonun başlangıcını temsil eder.
        self.assertEqual(
            first_record["action"],
            "START"
        )

        # 7. GERÇEK KONUMU KONTROL ET
        # Robotun başlangıç odası Office olmalıdır.
        self.assertEqual(
            first_record["true_position"],
            "Office"
        )

        # 8. BAŞLANGIÇ İNANCINI KONTROL ET
        # Robotun Office odasında bulunduğu
        # başlangıçta kesin olarak bilinmektedir.
        #
        # P(Office) = 1.0
        self.assertAlmostEqual(
            first_record["belief"]["Office"],
            1.0
        )

    # ========================================================
    # TEST 2 - HISTORY GROWTH
    # Her hareketin geçmişe kayıt eklemesini doğrulama
    # ========================================================

    def test_history_grows(self):
        """
        Hareket geçmişinin büyümesini kontrol eder.

        Hareket dizisi:
        RIGHT -> RIGHT -> UP

        Beklenen sonuçlar:
        - 3 hareket gerçekleştirilmelidir.
        - Hareket sayacı 3 olmalıdır.
        - Geçmişte toplam 4 kayıt bulunmalıdır.
        - Hareket komutları doğru sırada saklanmalıdır.

        Başlangıç kaydı hareket sayısına dahil değildir.

        Kayıt sayısı = Hareket sayısı + 1
        """

        # 1. SİMÜLASYONU BAŞLAT
        # Başlangıç kaydı otomatik oluşturulur.
        simulation = RobotSimulation(
            start_room="Office"
        )

        # 2. BİRİNCİ HAREKETİ GERÇEKLEŞTİR
        # t = 0 -> t = 1
        #
        # history[1] kaydı oluşturulur.
        simulation.step("RIGHT")

        # 3. İKİNCİ HAREKETİ GERÇEKLEŞTİR
        # t = 1 -> t = 2
        #
        # history[2] kaydı oluşturulur.
        simulation.step("RIGHT")

        # 4. ÜÇÜNCÜ HAREKETİ GERÇEKLEŞTİR
        # t = 2 -> t = 3
        #
        # history[3] kaydı oluşturulur.
        simulation.step("UP")

        # 5. HAREKET GEÇMİŞİNİ AL
        history = simulation.get_history()

        # 6. TOPLAM KAYIT SAYISINI KONTROL ET
        #
        # Başlangıç kaydı = 1
        # Hareket kayıtları = 3
        #
        # Toplam kayıt = 4
        self.assertEqual(
            len(history),
            4
        )

        # 7. HAREKET SAYACINI KONTROL ET
        # Üç geçerli hareket komutu
        # gerçekleştirildiği için sayaç 3 olmalıdır.
        self.assertEqual(
            simulation.step_count,
            3
        )

        # 8. HAREKET KOMUTLARININ SIRASINI KONTROL ET
        #
        # history[0] -> START
        # history[1] -> RIGHT
        # history[2] -> RIGHT
        # history[3] -> UP
        self.assertEqual(
            history[1]["action"],
            "RIGHT"
        )

        self.assertEqual(
            history[2]["action"],
            "RIGHT"
        )

        self.assertEqual(
            history[3]["action"],
            "UP"
        )

        # 9. SON KAYDIN ZAMAN ADIMINI KONTROL ET
        # Son kayıt üçüncü hareketi temsil etmelidir.
        self.assertEqual(
            history[3]["step"],
            3
        )

    # ========================================================
    # TEST 3 - BELIEF HISTORY PRESERVATION
    # Önceki inanç dağılımlarının korunmasını doğrulama
    # ========================================================

    def test_belief_history(self):
        """
        Geçmiş inanç dağılımlarının korunmasını test eder.

        Hareket dizisi:
        RIGHT -> RIGHT

        Beklenen inanç dağılımları:

        Başlangıç (t = 0):
        P(Office) = 1.0

        Birinci RIGHT (t = 1):
        P(Office)  = 0.2
        P(Hallway) = 0.8

        İkinci RIGHT (t = 2):
        P(Office)      = 0.04
        P(Hallway)     = 0.32
        P(Dining Room) = 0.64

        Her kayıt, oluşturulduğu zamandaki
        olasılık dağılımını korumalıdır.
        """

        # 1. SİMÜLASYONU BAŞLAT
        simulation = RobotSimulation(
            start_room="Office"
        )

        # 2. İKİ ARDIŞIK RIGHT HAREKETİ GERÇEKLEŞTİR
        # Her hareketten sonra yeni bir inanç
        # dağılımı hesaplanır ve geçmişe kaydedilir.
        simulation.step("RIGHT")
        simulation.step("RIGHT")

        # 3. HAREKET GEÇMİŞİNİ AL
        # Geçmişte üç kayıt bulunmalıdır:
        #
        # history[0] -> Başlangıç
        # history[1] -> Birinci RIGHT
        # history[2] -> İkinci RIGHT
        history = simulation.get_history()

        # 4. BAŞLANGIÇ İNANCINI KONTROL ET
        # İki hareket gerçekleştirilmiş olsa bile
        # başlangıç kaydı değişmemiş olmalıdır.
        #
        # P(Office) = 1.0
        self.assertAlmostEqual(
            history[0]["belief"]["Office"],
            1.0
        )

        # 5. BİRİNCİ RIGHT SONRASI İNANCI KONTROL ET
        #
        # P(Office)  = 0.2
        # P(Hallway) = 0.8
        #
        # Bu değerler ikinci hareket
        # gerçekleştirildikten sonra da korunmalıdır.
        self.assertAlmostEqual(
            history[1]["belief"]["Office"],
            0.2
        )

        self.assertAlmostEqual(
            history[1]["belief"]["Hallway"],
            0.8
        )

        # 6. İKİNCİ RIGHT SONRASI İNANCI KONTROL ET
        #
        # P(Office)      = 0.04
        # P(Hallway)     = 0.32
        # P(Dining Room) = 0.64
        #
        # Bu dağılım ikinci hareketin
        # tahmin edilen sonucudur.
        self.assertAlmostEqual(
            history[2]["belief"]["Office"],
            0.04
        )

        self.assertAlmostEqual(
            history[2]["belief"]["Hallway"],
            0.32
        )

        self.assertAlmostEqual(
            history[2]["belief"]["Dining Room"],
            0.64
        )

        # 7. HER KAYDIN OLASILIK TOPLAMINI KONTROL ET
        # Geçerli bir inanç dağılımında
        # olasılıkların toplamı 1 olmalıdır.
        for record in history:
            self.assertAlmostEqual(
                sum(record["belief"].values()),
                1.0
            )

    # ========================================================
    # TEST 4 - HISTORY COPY PROTECTION
    # Dışarıdan yapılan değişikliklere karşı veri koruması
    # ========================================================

    def test_history_copy_protection(self):
        """
        get_history() metodunun veri korumasını test eder.

        Bu testte:
        1. Simülasyon oluşturulur.
        2. Bir RIGHT hareketi gerçekleştirilir.
        3. Hareket geçmişinin kopyası alınır.
        4. Kopyadaki başlangıç inancı değiştirilir.
        5. Simülasyonun orijinal geçmişi tekrar okunur.
        6. Orijinal değerin korunup korunmadığı kontrol edilir.

        Beklenen:
        Dışarıdan yapılan değişiklikler
        simülasyonun kendi geçmişini etkilememelidir.
        """

        # 1. SİMÜLASYONU BAŞLAT
        simulation = RobotSimulation(
            start_room="Office"
        )

        # 2. BİR RIGHT HAREKETİ GERÇEKLEŞTİR
        # Geçmişte artık iki kayıt vardır:
        #
        # history[0] -> START
        # history[1] -> RIGHT
        simulation.step("RIGHT")

        # 3. HAREKET GEÇMİŞİNİN KOPYASINI AL
        # get_history() dış listeyi, kayıt sözlüklerini
        # ve belief sözlüklerini kopyalayarak döndürür.
        history_copy = simulation.get_history()

        # 4. KOPYADAKİ İNANÇ DEĞERİNİ DEĞİŞTİR
        # Başlangıçta:
        # P(Office) = 1.0
        #
        # Test amacıyla bu değeri 0.5 yapıyoruz.
        #
        # Bu değişiklik yalnızca kopyayı etkilemelidir.
        history_copy[0]["belief"]["Office"] = 0.5

        # 5. ORİJİNAL GEÇMİŞİ TEKRAR OKU
        # Simülasyonun sakladığı kayıtlar
        # değiştirilmemiş olmalıdır.
        original_history = simulation.get_history()

        # 6. ORİJİNAL BAŞLANGIÇ İNANCINI KONTROL ET
        # Kopyada P(Office) = 0.5 yapılmış olsa bile
        # orijinal değer 1.0 kalmalıdır.
        self.assertAlmostEqual(
            original_history[0]["belief"]["Office"],
            1.0
        )


# ============================================================
# MAIN - Test Runner
# Testleri doğrudan çalıştırma
# ============================================================

if __name__ == "__main__":
    unittest.main()
