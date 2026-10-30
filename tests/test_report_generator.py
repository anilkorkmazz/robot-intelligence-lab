
# ============================================================
# IMPORTS - Gerekli modüller
# ============================================================

import tempfile
import unittest

from pathlib import Path

from robot_lab.core.simulation import RobotSimulation

from robot_lab.experiments.report_generator import (
    generate_experiment_report
)


# ============================================================
# TEST CLASS - EXPERIMENT REPORT TESTS
# Deney raporu birim testleri
# ============================================================

class TestReportGenerator(unittest.TestCase):
    """
    generate_experiment_report() fonksiyonunun
    doğru çalıştığını test eder.

    Bu sınıfta dört temel özellik doğrulanır:

    1. Report File Creation:
       Markdown raporunun oluşturulması.

    2. Report Sections:
       Raporun gerekli başlıkları içermesi.

    3. Movement Records:
       Başlangıç konumu ve hareket kayıtlarının
       doğru yazılması.

    4. Final Belief State:
       Son inanç dağılımının doğru aktarılması.

    Testler geçici klasörler kullanır.

    Böylece mevcut experiment_001.md
    dosyası değiştirilmez.
    """

    # ========================================================
    # TEST 1 - REPORT FILE CREATION
    # Markdown rapor dosyasını oluşturma testi
    # ========================================================

    def test_report_file_created(self):
        """
        Markdown raporunun oluşturulduğunu doğrular.

        Bu test:
        1. Robot simülasyonu oluşturur.
        2. Bir RIGHT hareketi gerçekleştirir.
        3. Hareket geçmişini alır.
        4. Geçici bir klasör oluşturur.
        5. Markdown raporunu kaydeder.
        6. Dosyanın varlığını doğrular.
        7. Dosyanın boş olmadığını kontrol eder.

        Beklenen sonuç:
        - Rapor dosyası bulunmalıdır.
        - Dosyanın boyutu sıfırdan büyük olmalıdır.
        """

        # 1. ROBOT SİMÜLASYONUNU OLUŞTUR
        # Robot Office odasında başlatılır.
        simulation = RobotSimulation(
            start_room="Office"
        )

        # Bir RIGHT hareketi gerçekleştirilir.
        simulation.step("RIGHT")

        # 2. HAREKET GEÇMİŞİNİ AL
        # Başlangıç ve ilk hareket kayıtlarını içerir.
        history = simulation.get_history()

        # 3. GEÇİCİ KLASÖR OLUŞTUR
        # Test tamamlanınca klasör otomatik temizlenir.
        with tempfile.TemporaryDirectory() as temp_dir:

            # Markdown dosyasının yolunu oluştur.
            file_path = Path(temp_dir) / "test_report.md"

            # 4. MARKDOWN RAPORUNU OLUŞTUR
            # generate_experiment_report():
            # Geçmiş kayıtlarını Markdown'a dönüştürür.
            #
            # Kaydedilen dosyanın Path nesnesini döndürür.
            saved_path = generate_experiment_report(
                history,
                file_path
            )

            # 5. DOSYANIN OLUŞTUĞUNU DOĞRULA
            # is_file():
            # Dosyanın belirtilen konumda
            # bulunup bulunmadığını kontrol eder.
            self.assertTrue(
                saved_path.is_file()
            )

            # 6. DOSYANIN BOŞ OLMADIĞINI DOĞRULA
            # stat().st_size:
            # Dosya boyutunu bayt cinsinden döndürür.
            #
            # assertGreater():
            # Birinci değerin ikinci değerden
            # büyük olmasını bekler.
            self.assertGreater(
                saved_path.stat().st_size,
                0
            )

    # ========================================================
    # TEST 2 - REPORT SECTIONS
    # Rapor bölümlerini doğrulama
    # ========================================================

    def test_report_sections(self):
        """
        Markdown raporunda gerekli bölümlerin
        bulunup bulunmadığını kontrol eder.

        Beklenen bölümler:
        - Deney Amacı
        - Başlangıç Koşulları
        - Hareket Komutları
        - Deney Sonuçları
        - Son İnanç Dağılımı
        - Değerlendirme

        Bu test başlıkların varlığını doğrular.
        İçeriklerinin matematiksel doğruluğunu
        tek başına garanti etmez.
        """

        # 1. SİMÜLASYONU OLUŞTUR
        simulation = RobotSimulation(
            start_room="Office"
        )

        # Bir hareket gerçekleştir.
        simulation.step("RIGHT")

        # 2. HAREKET GEÇMİŞİNİ AL
        history = simulation.get_history()

        # 3. GEÇİCİ RAPOR DOSYASI OLUŞTUR
        with tempfile.TemporaryDirectory() as temp_dir:

            file_path = Path(temp_dir) / "test_report.md"

            # Raporu kaydet.
            generate_experiment_report(
                history,
                file_path
            )

            # 4. RAPOR METNİNİ OKU
            # read_text():
            # Dosyanın tamamını string olarak okur.
            #
            # encoding="utf-8":
            # Türkçe karakterlerin doğru okunmasını sağlar.
            content = file_path.read_text(
                encoding="utf-8"
            )

            # 5. DENEY AMACI BAŞLIĞINI KONTROL ET
            #
            # assertIn():
            # Belirtilen metnin rapor içinde
            # bulunup bulunmadığını doğrular.
            self.assertIn(
                "## Deney Amacı",
                content
            )

            # 6. BAŞLANGIÇ KOŞULLARINI KONTROL ET
            self.assertIn(
                "## Başlangıç Koşulları",
                content
            )

            # 7. HAREKET KOMUTLARI BÖLÜMÜNÜ KONTROL ET
            self.assertIn(
                "## Hareket Komutları",
                content
            )

            # 8. DENEY SONUÇLARI BÖLÜMÜNÜ KONTROL ET
            # Önceki aşamada bu başlığı kullanmıştık.
            self.assertIn(
                "## Deney Sonuçları",
                content
            )

            # 9. SON İNANÇ DAĞILIMINI KONTROL ET
            self.assertIn(
                "## Son İnanç Dağılımı",
                content
            )

            # 10. DEĞERLENDİRME BÖLÜMÜNÜ KONTROL ET
            self.assertIn(
                "## Değerlendirme",
                content
            )

    # ========================================================
    # TEST 3 - MOVEMENT RECORDS
    # Başlangıç ve hareket kayıtlarını doğrulama
    # ========================================================

    def test_report_movement_records(self):
        """
        Rapordaki başlangıç koşullarını ve
        hareket kayıtlarını doğrular.

        Hareket dizisi:
        RIGHT -> RIGHT -> UP

        Beklenen:
        - Başlangıç odası Office olmalıdır.
        - Hareket komutları doğru sırada olmalıdır.
        - Başlangıç kaydı raporda bulunmalıdır.
        - Dört zaman adımı tabloya yazılmalıdır.

        Gerçek robot konumu olasılıksal olduğu için
        ara adımlarda belirli bir oda beklenmez.
        """

        # 1. SİMÜLASYONU OLUŞTUR
        simulation = RobotSimulation(
            start_room="Office"
        )

        # 2. ÜÇ HAREKET GERÇEKLEŞTİR
        # t = 0 -> START
        # t = 1 -> RIGHT
        # t = 2 -> RIGHT
        # t = 3 -> UP
        simulation.step("RIGHT")
        simulation.step("RIGHT")
        simulation.step("UP")

        # 3. HAREKET GEÇMİŞİNİ AL
        history = simulation.get_history()

        # 4. GEÇİCİ RAPOR OLUŞTUR
        with tempfile.TemporaryDirectory() as temp_dir:

            file_path = Path(temp_dir) / "test_report.md"

            generate_experiment_report(
                history,
                file_path
            )

            # 5. RAPOR METNİNİ OKU
            content = file_path.read_text(
                encoding="utf-8"
            )

            # 6. BAŞLANGIÇ KOŞULUNU DOĞRULA
            # Robot kesin olarak Office odasında başlar.
            self.assertIn(
                "Başlangıç odası: Office",
                content
            )

            # 7. HAREKET DİZİSİNİ DOĞRULA
            # Komutların sırasını kontrol eder.
            self.assertIn(
                "RIGHT → RIGHT → UP",
                content
            )

            # 8. BAŞLANGIÇ KAYDINI DOĞRULA
            # İlk kayıt:
            # step = 0, action = START
            self.assertIn(
                "| 0 | START | Office |",
                content
            )

            # 9. BİRİNCİ HAREKETİ DOĞRULA
            # Gerçek konum değişebileceği için
            # yalnızca adım ve komutu kontrol ederiz.
            self.assertIn(
                "| 1 | RIGHT |",
                content
            )

            # 10. İKİNCİ HAREKETİ DOĞRULA
            self.assertIn(
                "| 2 | RIGHT |",
                content
            )

            # 11. ÜÇÜNCÜ HAREKETİ DOĞRULA
            self.assertIn(
                "| 3 | UP |",
                content
            )

            # 12. TOPLAM HAREKET SAYISINI KONTROL ET
            self.assertIn(
                "Toplam 3 hareket gerçekleştirildi.",
                content
            )

    # ========================================================
    # TEST 4 - FINAL BELIEF STATE
    # Son inanç dağılımını doğrulama
    # ========================================================

    def test_report_final_belief(self):
        """
        Son inanç dağılımının Markdown raporuna
        doğru yazıldığını doğrular.

        Hareket dizisi:
        RIGHT -> RIGHT -> UP

        Beklenen olasılıklar:
        Living Room = 0.2560
        Kitchen     = 0.5120
        Office      = 0.0400
        Hallway     = 0.0640
        Dining Room = 0.1280

        Bu değerler ilgili Markov hareket
        modelinden elde edilen dağılımdır.

        Rapor dört ondalık basamak kullandığı için
        beklenen değerleri string olarak kontrol ederiz.
        """

        # 1. SİMÜLASYONU OLUŞTUR
        simulation = RobotSimulation(
            start_room="Office"
        )

        # 2. HAREKET DİZİSİNİ GERÇEKLEŞTİR
        simulation.step("RIGHT")
        simulation.step("RIGHT")
        simulation.step("UP")

        # 3. HAREKET GEÇMİŞİNİ AL
        history = simulation.get_history()

        # 4. GEÇİCİ MARKDOWN DOSYASI OLUŞTUR
        with tempfile.TemporaryDirectory() as temp_dir:

            file_path = Path(temp_dir) / "test_report.md"

            generate_experiment_report(
                history,
                file_path
            )

            # 5. RAPOR METNİNİ OKU
            content = file_path.read_text(
                encoding="utf-8"
            )

            # 6. LIVING ROOM OLASILIĞINI KONTROL ET
            self.assertIn(
                "- Living Room: 0.2560",
                content
            )

            # 7. KITCHEN OLASILIĞINI KONTROL ET
            self.assertIn(
                "- Kitchen: 0.5120",
                content
            )

            # 8. OFFICE OLASILIĞINI KONTROL ET
            self.assertIn(
                "- Office: 0.0400",
                content
            )

            # 9. HALLWAY OLASILIĞINI KONTROL ET
            self.assertIn(
                "- Hallway: 0.0640",
                content
            )

            # 10. DINING ROOM OLASILIĞINI KONTROL ET
            self.assertIn(
                "- Dining Room: 0.1280",
                content
            )

            # 11. TOPLAM OLASILIĞI KONTROL ET
            # Mevcut rapor formatımızda bu ifade
            # kullanılıyor.
            self.assertIn(
                "Son inanç dağılımının toplamı: 1.0000",
                content
            )


# ============================================================
# MAIN - Test Runner
# Testleri doğrudan çalıştırma
# ============================================================

if __name__ == "__main__":
    unittest.main()
