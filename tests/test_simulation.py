# ============================================================
# IMPORTS - Gerekli modüller
# ============================================================

import unittest

from robot_lab.core.simulation import RobotSimulation
from robot_lab.worlds.house import ROOMS


# ============================================================
# TEST CLASS - Robot Simulation Tests
# Robot simülasyonu birim testleri
# ============================================================

class TestRobotSimulation(unittest.TestCase):
    """
    RobotSimulation sınıfının doğru çalıştığını test eder.

    Bu sınıfta dört temel özellik doğrulanır:

    1. Initial State:
       Robotun başlangıç konumu ve inanç durumu.

    2. Single Motion:
       Tek hareketten sonraki gerçek konum
       ve inanç dağılımı.

    3. Consecutive Motions:
       Ardışık hareketlerden sonraki
       gerçek konum ve inanç dağılımı.

    4. Invalid Action:
       Geçersiz komutların reddedilmesi
       ve simülasyon durumunun korunması.

    unittest.TestCase:
    Python'un birim test altyapısını sağlar.
    """

    # ========================================================
    # TEST 1 - INITIAL STATE
    # Başlangıç durumunu doğrulama
    # ========================================================

    def test_initial_state(self):
        """
        Robotun başlangıç durumunu kontrol eder.

        Beklenen sonuçlar:
        - Gerçek konum Office olmalıdır.
        - Zaman adımı 0 olmalıdır.
        - P(Office) = 1.0 olmalıdır.

        Başlangıçta robotun Office odasında
        bulunduğu kesin olarak bilinmektedir.
        """

        # 1. Simülasyonu Office odasında başlat.
        simulation = RobotSimulation(
            start_room="Office"
        )

        # 2. GERÇEK KONUMU KONTROL ET
        # get_position() robotun gerçek konumunu döndürür.
        #
        # assertEqual():
        # Gerçek değer ile beklenen değerin
        # birbirine eşit olduğunu doğrular.
        self.assertEqual(
            simulation.robot.get_position(),
            "Office"
        )

        # 3. ZAMAN ADIMINI KONTROL ET
        # Henüz hareket gerçekleştirilmediği için
        # step_count değeri 0 olmalıdır.
        self.assertEqual(
            simulation.step_count,
            0
        )

        # 4. BAŞLANGIÇ İNANCINI KONTROL ET
        # Robotun Office'de olduğu kesin biliniyor.
        #
        # P(Office) = 1.0
        #
        # assertAlmostEqual():
        # Ondalıklı sayıları küçük hesaplama
        # farklılıklarını dikkate alarak karşılaştırır.
        self.assertAlmostEqual(
            simulation.current_belief["Office"],
            1.0
        )

        # 5. TOPLAM OLASILIĞI KONTROL ET
        # Geçerli bir olasılık dağılımının
        # toplamı 1 olmalıdır.
        self.assertAlmostEqual(
            sum(simulation.current_belief.values()),
            1.0
        )

    # ========================================================
    # TEST 2 - SINGLE PROBABILISTIC MOTION
    # Tek olasılıksal hareket testi
    # ========================================================

    def test_one_right(self):
        """
        Tek bir RIGHT hareketini test eder.

        Başlangıç:
        Robot Office odasındadır.

        Hareket:
        RIGHT

        Beklenen inanç dağılımı:
        P(Office)  = 0.2
        P(Hallway) = 0.8

        Gerçek hareket sonucu rastgele seçildiğinden
        robot Office veya Hallway odasında olabilir.

        İnanç dağılımı ise hareket modelinden
        hesaplandığı için belirli bir sonuç üretir.
        """

        # 1. Simülasyonu oluştur.
        simulation = RobotSimulation(
            start_room="Office"
        )

        # 2. BİR RIGHT HAREKETİ GERÇEKLEŞTİR
        #
        # step() metodu:
        # - Gerçek hareket sonucunu örnekler.
        # - Gerçek konumu günceller.
        # - İnanç dağılımını günceller.
        # - Zaman adımını artırır.
        result = simulation.step("RIGHT")

        # 3. ZAMAN ADIMINI KONTROL ET
        # Bir hareket gerçekleştirildiği için
        # zaman adımı 1 olmalıdır.
        self.assertEqual(
            result["step"],
            1
        )

        # 4. HAREKET KOMUTUNU KONTROL ET
        # Gerçekleştirilen komut RIGHT olmalıdır.
        self.assertEqual(
            result["action"],
            "RIGHT"
        )

        # 5. GERÇEK KONUMU KONTROL ET
        #
        # Olasılıksal hareket modeli:
        # Office -> Hallway : %80
        # Office -> Office  : %20
        #
        # Hareket sonucu rastgele olduğu için
        # belirli bir oda beklemiyoruz.
        #
        # assertIn():
        # Gerçek konumun izin verilen
        # odalardan biri olduğunu doğrular.
        self.assertIn(
            result["true_position"],
            ["Office", "Hallway"]
        )

        # 6. ROBOT NESNESİNİN KONUMUNU KONTROL ET
        # Döndürülen gerçek konum ile robotun
        # sakladığı konum aynı olmalıdır.
        self.assertEqual(
            simulation.robot.get_position(),
            result["true_position"]
        )

        # 7. BELIEF STATE DEĞERLERİNİ KONTROL ET
        #
        # Başlangıçta:
        # P(Office) = 1.0
        #
        # RIGHT hareketinden sonra:
        # P(Office)  = 0.2
        # P(Hallway) = 0.8
        self.assertAlmostEqual(
            result["belief"]["Office"],
            0.2
        )

        self.assertAlmostEqual(
            result["belief"]["Hallway"],
            0.8
        )

        # 8. TOPLAM OLASILIĞI KONTROL ET
        # Tüm odaların olasılıkları toplamı
        # 1.0 olmalıdır.
        self.assertAlmostEqual(
            sum(result["belief"].values()),
            1.0
        )

    # ========================================================
    # TEST 3 - CONSECUTIVE PROBABILISTIC MOTIONS
    # İki ardışık RIGHT hareketi
    # ========================================================

    def test_two_rights(self):
        """
        Ardışık iki RIGHT hareketini test eder.

        Başlangıç:
        Robot Office odasındadır.

        Hareket dizisi:
        RIGHT -> RIGHT

        Beklenen inanç dağılımı:
        P(Office)      = 0.04
        P(Hallway)     = 0.32
        P(Dining Room) = 0.64

        Beklenen zaman adımı:
        step_count = 2

        Gerçek konum rastgele olabilir.
        Ancak inanç dağılımı hareket modeli
        kullanılarak hesaplanır.
        """

        # 1. Simülasyonu başlat.
        simulation = RobotSimulation(
            start_room="Office"
        )

        # 2. BİRİNCİ RIGHT HAREKETİ
        # Gerçek konum ve inanç durumu güncellenir.
        # t = 0 -> t = 1
        simulation.step("RIGHT")

        # 3. İKİNCİ RIGHT HAREKETİ
        # Birinci hareketten sonraki gerçek konum
        # ve inanç dağılımı kullanılır.
        #
        # t = 1 -> t = 2
        result = simulation.step("RIGHT")

        # 4. ZAMAN ADIMINI KONTROL ET
        # İki hareket gerçekleştirildiği için
        # zaman adımı 2 olmalıdır.
        self.assertEqual(
            result["step"],
            2
        )

        self.assertEqual(
            simulation.step_count,
            2
        )

        # 5. GERÇEK KONUMU KONTROL ET
        # Robot geçerli odalardan birinde
        # bulunmalıdır.
        #
        # ROOMS:
        # Robotun dünyasında tanımlı odalar.
        self.assertIn(
            result["true_position"],
            ROOMS
        )

        # 6. İKİNCİ HAREKET SONRASI BELIEF STATE
        #
        # P(Office) = 0.04
        #
        # P(Hallway) = 0.32
        #
        # P(Dining Room) = 0.64
        #
        # Bu olasılıklar iki ardışık
        # hareket modelinden hesaplanır.
        self.assertAlmostEqual(
            result["belief"]["Office"],
            0.04
        )

        self.assertAlmostEqual(
            result["belief"]["Hallway"],
            0.32
        )

        self.assertAlmostEqual(
            result["belief"]["Dining Room"],
            0.64
        )

        # 7. OLASILIK TOPLAMINI KONTROL ET
        #
        # 0.04 + 0.32 + 0.64 = 1.0
        #
        # Geçerli olasılık dağılımında
        # toplam değer 1 olmalıdır.
        self.assertAlmostEqual(
            sum(result["belief"].values()),
            1.0
        )

    # ========================================================
    # TEST 4 - INVALID ACTION HANDLING
    # Geçersiz hareket komutu testi
    # ========================================================

    def test_invalid_action(self):
        """
        Geçersiz hareket komutlarını test eder.

        Geçersiz komut:
        JUMP

        Beklenen davranış:
        1. ValueError hatası oluşmalıdır.
        2. Robot Office odasında kalmalıdır.
        3. Zaman adımı 0 olarak kalmalıdır.
        4. İnanç dağılımı değişmemelidir.

        Böylece geçersiz komutların
        simülasyonun durumunu bozması önlenir.
        """

        # 1. Simülasyonu oluştur.
        simulation = RobotSimulation(
            start_room="Office"
        )

        # 2. GEÇERSİZ KOMUT GÖNDER
        #
        # JUMP tanımlı bir hareket komutu değildir.
        #
        # assertRaises(ValueError):
        # Kodun ValueError hatası üretmesini bekler.
        #
        # Eğer hata oluşmazsa test başarısız olur.
        with self.assertRaises(ValueError):
            simulation.step("JUMP")

        # 3. GERÇEK KONUMU KONTROL ET
        # Geçersiz hareket robotun
        # gerçek konumunu değiştirmemelidir.
        self.assertEqual(
            simulation.robot.get_position(),
            "Office"
        )

        # 4. ZAMAN ADIMINI KONTROL ET
        # Geçersiz komut kabul edilmediğinden
        # zaman adımı artırılmamalıdır.
        self.assertEqual(
            simulation.step_count,
            0
        )

        # 5. BELIEF STATE DEĞERİNİ KONTROL ET
        # Robotun Office odasında bulunduğuna
        # ilişkin başlangıç inancı korunmalıdır.
        self.assertAlmostEqual(
            simulation.current_belief["Office"],
            1.0
        )

        # 6. TOPLAM OLASILIĞI KONTROL ET
        # Hatalı komut sonrasında da
        # olasılık dağılımı geçerli kalmalıdır.
        self.assertAlmostEqual(
            sum(simulation.current_belief.values()),
            1.0
        )


# ============================================================
# MAIN - Test Runner
# Testleri doğrudan çalıştırma
# ============================================================

if __name__ == "__main__":
    unittest.main()

