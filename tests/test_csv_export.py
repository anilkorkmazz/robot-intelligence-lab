
# ============================================================
# IMPORTS - Gerekli modüller
# ============================================================

import csv
import tempfile
import unittest

from pathlib import Path

from robot_lab.core.simulation import RobotSimulation
from robot_lab.experiments.csv_export import export_history_to_csv
from robot_lab.worlds.house import ROOMS


# ============================================================
# TEST CLASS - CSV EXPORT TESTS
# Simülasyon geçmişini CSV'ye aktarma testleri
# ============================================================

class TestCSVExport(unittest.TestCase):
    """
    export_history_to_csv() fonksiyonunun
    doğru çalıştığını test eder.

    Bu sınıfta üç temel özellik doğrulanır:

    1. CSV File Creation:
       CSV dosyasının oluşturulması ve boş olmaması.

    2. CSV Headers and Rows:
       Sütun başlıklarının, sıralarının ve
       kayıt sayılarının doğrulanması.

    3. CSV Belief Values:
       İnanç dağılımındaki olasılık değerlerinin
       CSV dosyasına doğru aktarılması.

    Testlerde geçici klasörler kullanılır.

    Böylece proje klasöründe gereksiz
    test dosyalarının oluşması önlenir.
    """

    # ========================================================
    # TEST 1 - CSV FILE CREATION
    # CSV dosyasının oluşturulmasını doğrulama
    # ========================================================

    def test_csv_file_created(self):
        """
        CSV dosyasının başarıyla oluşturulduğunu test eder.

        Bu test:
        1. Robot simülasyonu oluşturur.
        2. Bir RIGHT hareketi gerçekleştirir.
        3. Hareket geçmişini alır.
        4. Geçici bir klasör oluşturur.
        5. Hareket geçmişini CSV dosyasına kaydeder.
        6. Dosyanın varlığını kontrol eder.
        7. Dosyanın boş olmadığını doğrular.

        Beklenen sonuç:
        - CSV dosyası oluşturulmalıdır.
        - Dosya boyutu 0 bayttan büyük olmalıdır.
        """

        # ====================================================
        # 1. CREATE ROBOT SIMULATION
        # Robot simülasyonunu oluşturma
        # ====================================================

        # Robot Office odasında başlatılır.
        simulation = RobotSimulation(
            start_room="Office"
        )

        # Bir RIGHT hareketi gerçekleştirilir.
        #
        # Bu hareketin sonucu geçmişe kaydedilir.
        simulation.step("RIGHT")

        # ====================================================
        # 2. GET SIMULATION HISTORY
        # Simülasyon geçmişini alma
        # ====================================================

        # get_history():
        # Başlangıç durumu ve hareket kayıtlarının
        # bağımsız kopyalarını döndürür.
        history = simulation.get_history()

        # ====================================================
        # 3. CREATE TEMPORARY DIRECTORY
        # Geçici klasör oluşturma
        # ====================================================

        # TemporaryDirectory():
        # Test için geçici bir klasör oluşturur.
        #
        # with bloğu tamamlandığında klasör
        # ve içindeki dosyalar otomatik temizlenir.
        with tempfile.TemporaryDirectory() as temp_dir:

            # ================================================
            # 4. CREATE CSV FILE PATH
            # CSV dosyasının yolunu oluşturma
            # ================================================

            # Path(temp_dir):
            # Geçici klasörün yolunu temsil eder.
            #
            # / operatörü:
            # Dosya yolu parçalarını birleştirir.
            #
            # Örneğin:
            # /tmp/abc123/test_history.csv
            file_path = Path(temp_dir) / "test_history.csv"

            # ================================================
            # 5. EXPORT HISTORY TO CSV
            # Hareket geçmişini CSV'ye kaydetme
            # ================================================

            # export_history_to_csv():
            # Hareket geçmişindeki bütün kayıtları
            # CSV dosyasına aktarır.
            #
            # Kaydedilen dosyanın Path nesnesini döndürür.
            saved_path = export_history_to_csv(
                history,
                file_path
            )

            # ================================================
            # 6. CHECK FILE EXISTENCE
            # Dosyanın oluştuğunu doğrulama
            # ================================================

            # assertTrue():
            # Verilen koşulun True olmasını bekler.
            #
            # is_file():
            # Belirtilen konumda bir dosya
            # bulunup bulunmadığını kontrol eder.
            self.assertTrue(
                saved_path.is_file()
            )

            # ================================================
            # 7. CHECK FILE SIZE
            # Dosyanın boş olmadığını doğrulama
            # ================================================

            # stat().st_size:
            # Dosyanın boyutunu bayt cinsinden verir.
            #
            # assertGreater():
            # Birinci değerin ikinci değerden
            # büyük olmasını bekler.
            #
            # Dosya en az bir miktar veri içermelidir.
            self.assertGreater(
                saved_path.stat().st_size,
                0
            )

    # ========================================================
    # TEST 2 - CSV HEADERS AND ROWS
    # CSV sütun başlıkları ve kayıt sayısı testi
    # ========================================================

    def test_csv_headers_and_rows(self):
        """
        CSV dosyasının sütun yapısını ve
        kayıt sayısını doğrular.

        Bu test:
        1. Üç hareket gerçekleştirir.
        2. Hareket geçmişini CSV'ye kaydeder.
        3. CSV dosyasını tekrar okur.
        4. Sütun başlıklarını doğrular.
        5. Sütunların sıralamasını kontrol eder.
        6. Toplam satır ve sütun sayılarını doğrular.

        Beklenen sonuç:
        - 8 sütun bulunmalıdır.
        - 1 başlık satırı bulunmalıdır.
        - 4 veri satırı bulunmalıdır.
        - Toplam 5 satır bulunmalıdır.

        Veri kayıtları:
        0 -> START
        1 -> RIGHT
        2 -> RIGHT
        3 -> UP
        """

        # ====================================================
        # 1. CREATE ROBOT SIMULATION
        # Robot simülasyonunu oluşturma
        # ====================================================

        simulation = RobotSimulation(
            start_room="Office"
        )

        # ====================================================
        # 2. EXECUTE MOVEMENT SEQUENCE
        # Hareket dizisini gerçekleştirme
        # ====================================================

        # Robot üç hareket komutu alır.
        #
        # Her hareket sonucu history
        # listesine yeni bir kayıt eklenir.
        simulation.step("RIGHT")
        simulation.step("RIGHT")
        simulation.step("UP")

        # ====================================================
        # 3. GET MOVEMENT HISTORY
        # Hareket geçmişini alma
        # ====================================================

        # Başlangıç + 3 hareket = 4 kayıt.
        history = simulation.get_history()

        # ====================================================
        # 4. CREATE TEMPORARY CSV FILE
        # Geçici CSV dosyası oluşturma
        # ====================================================

        with tempfile.TemporaryDirectory() as temp_dir:

            file_path = Path(temp_dir) / "test_history.csv"

            # Hareket geçmişini CSV dosyasına kaydet.
            export_history_to_csv(
                history,
                file_path
            )

            # ================================================
            # 5. READ CSV FILE
            # CSV dosyasını okuma
            # ================================================

            # "r":
            # Dosyayı okuma modunda açar.
            #
            # newline="":
            # CSV satırlarının doğru okunmasını sağlar.
            #
            # encoding="utf-8-sig":
            # UTF-8 BOM içeren dosyaların
            # doğru okunmasını sağlar.
            with file_path.open(
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                # csv.reader():
                # CSV satırlarını Python listelerine
                # dönüştürür.
                reader = csv.reader(file)

                # list():
                # Bütün CSV satırlarını belleğe alır.
                rows = list(reader)

            # ================================================
            # 6. CHECK CSV HEADERS
            # CSV sütun başlıklarını doğrulama
            # ================================================

            # CSV dosyasının ilk satırı
            # sütun başlıklarını içerir.
            headers = rows[0]

            # Beklenen ilk üç sütun:
            # Step, Action, True Position
            #
            # Ardından ROOMS listesindeki
            # bütün odalar gelmelidir.
            expected_headers = [
                "Step",
                "Action",
                "True Position"
            ] + list(ROOMS)

            # assertEqual():
            # Gerçek ve beklenen başlıkların
            # isimlerini ve sırasını karşılaştırır.
            self.assertEqual(
                headers,
                expected_headers
            )

            # ================================================
            # 7. CHECK COLUMN COUNT
            # CSV sütun sayısını doğrulama
            # ================================================

            # 3 hareket bilgisi + 5 oda = 8 sütun.
            self.assertEqual(
                len(headers),
                8
            )

            # ================================================
            # 8. CHECK ROW COUNT
            # CSV satır sayısını doğrulama
            # ================================================

            # 1 başlık satırı + 4 veri satırı
            # toplam 5 satır oluşturur.
            self.assertEqual(
                len(rows),
                5
            )

            # ================================================
            # 9. CHECK MOVEMENT RECORDS
            # Hareket kayıtlarını doğrulama
            # ================================================

            # Başlık satırını çıkararak
            # yalnızca veri kayıtlarını alırız.
            data_rows = rows[1:]

            # Başlangıç + 3 hareket = 4 kayıt.
            self.assertEqual(
                len(data_rows),
                4
            )

            # Hareketlerin doğru sırayla
            # kaydedildiğini kontrol ederiz.
            self.assertEqual(
                [row[1] for row in data_rows],
                ["START", "RIGHT", "RIGHT", "UP"]
            )

    # ========================================================
    # TEST 3 - CSV BELIEF VALUES
    # CSV inanç olasılıklarını doğrulama
    # ========================================================

    def test_csv_belief_values(self):
        """
        İnanç dağılımının CSV dosyasına
        doğru aktarılıp aktarılmadığını test eder.

        Başlangıç:
        P(Office) = 1.0

        Birinci RIGHT sonrası:
        P(Office)  = 0.2
        P(Hallway) = 0.8

        İkinci RIGHT sonrası:
        P(Office)      = 0.04
        P(Hallway)     = 0.32
        P(Dining Room) = 0.64

        Bu testte ikinci RIGHT hareketinden
        sonraki inanç dağılımı doğrulanır.

        Robotun gerçek hareket sonucu
        rastgele olabilir.

        Ancak inanç dağılımı aynı başlangıç
        koşulları ve hareket dizisi için sabittir.
        """

        # ====================================================
        # 1. CREATE ROBOT SIMULATION
        # Robot simülasyonunu oluşturma
        # ====================================================

        simulation = RobotSimulation(
            start_room="Office"
        )

        # ====================================================
        # 2. EXECUTE TWO RIGHT MOVEMENTS
        # İki RIGHT hareketi gerçekleştirme
        # ====================================================

        # t = 0 -> Başlangıç
        # t = 1 -> Birinci RIGHT
        # t = 2 -> İkinci RIGHT
        simulation.step("RIGHT")
        simulation.step("RIGHT")

        # ====================================================
        # 3. GET MOVEMENT HISTORY
        # Hareket geçmişini alma
        # ====================================================

        # Başlangıç ve iki hareket kaydını alırız.
        history = simulation.get_history()

        # ====================================================
        # 4. CREATE TEMPORARY CSV FILE
        # Geçici CSV dosyası oluşturma
        # ====================================================

        with tempfile.TemporaryDirectory() as temp_dir:

            file_path = Path(temp_dir) / "test_history.csv"

            # Hareket geçmişini dosyaya kaydet.
            export_history_to_csv(
                history,
                file_path
            )

            # ================================================
            # 5. READ CSV WITH DICTREADER
            # CSV dosyasını sözlük olarak okuma
            # ================================================

            with file_path.open(
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                # csv.DictReader():
                # Her satırı sütun başlıklarını
                # anahtar olarak kullanan
                # bir sözlüğe dönüştürür.
                reader = csv.DictReader(file)

                rows = list(reader)

            # ================================================
            # 6. GET SECOND RIGHT RECORD
            # İkinci RIGHT hareketinin kaydını alma
            # ================================================

            # rows[0] -> START
            # rows[1] -> Birinci RIGHT
            # rows[2] -> İkinci RIGHT
            #
            # DictReader başlık satırını veri
            # listesine dahil etmez.
            second_right = rows[2]

            # ================================================
            # 7. CHECK STEP AND ACTION
            # Adım numarası ve hareket komutunu kontrol etme
            # ================================================

            # CSV verileri metin olarak okunur.
            #
            # Bu yüzden "2" değeri string'dir.
            self.assertEqual(
                second_right["Step"],
                "2"
            )

            self.assertEqual(
                second_right["Action"],
                "RIGHT"
            )

            # ================================================
            # 8. CHECK OFFICE PROBABILITY
            # Office olasılığını doğrulama
            # ================================================

            # float():
            # CSV'den gelen metin değerini
            # ondalıklı sayıya dönüştürür.
            #
            # Beklenen:
            # P(Office) = 0.04
            self.assertAlmostEqual(
                float(second_right["Office"]),
                0.04
            )

            # ================================================
            # 9. CHECK HALLWAY PROBABILITY
            # Hallway olasılığını doğrulama
            # ================================================

            # Beklenen:
            # P(Hallway) = 0.32
            self.assertAlmostEqual(
                float(second_right["Hallway"]),
                0.32
            )

            # ================================================
            # 10. CHECK DINING ROOM PROBABILITY
            # Dining Room olasılığını doğrulama
            # ================================================

            # Beklenen:
            # P(Dining Room) = 0.64
            self.assertAlmostEqual(
                float(second_right["Dining Room"]),
                0.64
            )

            # ================================================
            # 11. CHECK TOTAL PROBABILITY
            # Toplam olasılığı doğrulama
            # ================================================

            # CSV'deki bütün oda olasılıklarını
            # toplarız.
            #
            # Geçerli bir Belief State için
            # toplam olasılık 1 olmalıdır.
            total_probability = sum(
                float(second_right[room])
                for room in ROOMS
            )

            self.assertAlmostEqual(
                total_probability,
                1.0
            )


# ============================================================
# MAIN - Test Runner
# Testleri doğrudan çalıştırma
# ============================================================

if __name__ == "__main__":
    unittest.main()
