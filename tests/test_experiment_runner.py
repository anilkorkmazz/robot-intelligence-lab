# ============================================================
# IMPORTS - Gerekli modüller
# ============================================================

import csv
import tempfile
import unittest

from robot_lab.experiments.experiment_runner import (
    run_experiment
)


# ============================================================
# TEST CLASS - INTEGRATED EXPERIMENT RUNNER
# Bütünleşik deney yürütücüsü testleri
# ============================================================

class TestExperimentRunner(unittest.TestCase):
    """
    run_experiment() fonksiyonunun doğru
    çalıştığını test eder.

    Bu sınıfta dört temel özellik doğrulanır:

    1. Output Files:
       PNG, CSV ve Markdown dosyalarının oluşturulması.

    2. History Length:
       Başlangıç durumu ve hareket kayıtlarının
       doğru sayıda bulunması.

    3. CSV and Report Consistency:
       CSV ve Markdown raporunun aynı deneyin
       gerçek hareket sonuçlarını içermesi.

    4. Final Belief State:
       Son inanç dağılımının beklenen
       Markov olasılıklarıyla eşleşmesi.

    Testlerde TemporaryDirectory kullanılır.

    Böylece gerçek deney sonuçları değiştirilmez.
    """

    # ========================================================
    # TEST 1 - OUTPUT FILES CREATED
    # Deney çıktı dosyalarının oluşturulması
    # ========================================================

    def test_output_files_created(self):
        """
        Bütünleşik deneyin üç çıktı dosyasını
        oluşturduğunu doğrular.

        Beklenen dosyalar:
        - belief_history.png
        - simulation_history.csv
        - experiment_001.md

        Ayrıca dosyaların boş olmadığını kontrol eder.

        Bu test dosyaların varlığını doğrular;
        içeriklerinin tamamını doğrulamaz.
        """

        # 1. GEÇİCİ KLASÖR OLUŞTUR
        # Deney dosyaları geçici klasöre kaydedilir.
        #
        # with bloğu tamamlandığında klasör
        # ve bütün dosyalar otomatik temizlenir.
        with tempfile.TemporaryDirectory() as temp_dir:

            # 2. BÜTÜNLEŞİK DENEYİ ÇALIŞTIR
            #
            # run_experiment():
            # - Tek bir simülasyon oluşturur.
            # - Üç RIGHT/UP hareketini gerçekleştirir.
            # - PNG, CSV ve Markdown dosyalarını üretir.
            #
            # Sonuçlar bir sözlük olarak döndürülür.
            result = run_experiment(
                ["RIGHT", "RIGHT", "UP"],
                temp_dir
            )

            # 3. ÇIKTI DOSYALARINI KONTROL ET
            # Üç dosyanın Path nesnelerini dolaşırız.
            for key in ["png_path", "csv_path", "report_path"]:

                # İlgili dosyanın yolunu al.
                path = result[key]

                # 4. DOSYANIN VARLIĞINI DOĞRULA
                # is_file():
                # Belirtilen konumda dosya bulunmalıdır.
                self.assertTrue(
                    path.is_file()
                )

                # 5. DOSYANIN BOŞ OLMADIĞINI DOĞRULA
                # stat().st_size:
                # Dosyanın boyutunu bayt cinsinden verir.
                self.assertGreater(
                    path.stat().st_size,
                    0
                )

    # ========================================================
    # TEST 2 - HISTORY LENGTH
    # Deney geçmişi ve hareket sayısı testi
    # ========================================================

    def test_history_length(self):
        """
        Üç hareketin dört geçmiş kaydı
        oluşturduğunu doğrular.

        Hareket dizisi:
        RIGHT -> RIGHT -> UP

        Beklenen kayıtlar:
        history[0] -> START
        history[1] -> RIGHT
        history[2] -> RIGHT
        history[3] -> UP

        Başlangıç kaydı hareket sayısına
        dahil edilmez.
        """

        # 1. GEÇİCİ DENEY KLASÖRÜ OLUŞTUR
        with tempfile.TemporaryDirectory() as temp_dir:

            # 2. DENEYİ ÇALIŞTIR
            result = run_experiment(
                ["RIGHT", "RIGHT", "UP"],
                temp_dir
            )

            # 3. HAREKET GEÇMİŞİNİ AL
            # history başlangıç dahil bütün kayıtları tutar.
            history = result["history"]

            # 4. KAYIT SAYISINI DOĞRULA
            #
            # 1 başlangıç + 3 hareket = 4 kayıt
            self.assertEqual(
                len(history),
                4
            )

            # 5. BAŞLANGIÇ KAYDINI DOĞRULA
            # İlk kaydın adım numarası sıfırdır.
            self.assertEqual(
                history[0]["step"],
                0
            )

            # İlk kaydın komutu START olmalıdır.
            self.assertEqual(
                history[0]["action"],
                "START"
            )

            # Başlangıç konumu Office olmalıdır.
            self.assertEqual(
                history[0]["true_position"],
                "Office"
            )

            # 6. SON ADIM NUMARASINI DOĞRULA
            # Üç hareket sonunda zaman adımı 3 olur.
            self.assertEqual(
                history[-1]["step"],
                3
            )

            # 7. HAREKET SIRASINI DOĞRULA
            # Bütün kayıtlardaki komutları sırayla alırız.
            actual_actions = [
                record["action"]
                for record in history
            ]

            expected_actions = [
                "START",
                "RIGHT",
                "RIGHT",
                "UP"
            ]

            self.assertEqual(
                actual_actions,
                expected_actions
            )

    # ========================================================
    # TEST 3 - CSV AND REPORT CONSISTENCY
    # CSV ve Markdown raporunun tutarlılığı
    # ========================================================

    def test_csv_report_consistency(self):
        """
        CSV dosyası ve Markdown raporunun
        aynı hareket geçmişini içerdiğini doğrular.

        Bu test:
        1. Bütünleşik deneyi gerçekleştirir.
        2. CSV dosyasını okur.
        3. Markdown raporunu okur.
        4. CSV satırlarından beklenen Markdown
           tablo satırlarını oluşturur.
        5. Her satırın raporda bulunduğunu doğrular.

        Önemli:
        Gerçek konumlar rastgele olabilir.

        Bu nedenle belirli bir konum beklemek yerine
        iki dosyanın aynı sonuçları içerdiğini
        kontrol ediyoruz.
        """

        # 1. GEÇİCİ KLASÖR OLUŞTUR
        with tempfile.TemporaryDirectory() as temp_dir:

            # 2. BÜTÜNLEŞİK DENEYİ ÇALIŞTIR
            result = run_experiment(
                ["RIGHT", "RIGHT", "UP"],
                temp_dir
            )

            # ====================================================
            # 3. READ CSV FILE
            # CSV dosyasını okuma
            # ====================================================

            # csv_path:
            # run_experiment() tarafından döndürülen
            # CSV dosyasının Path nesnesidir.
            with result["csv_path"].open(
                "r",
                newline="",
                encoding="utf-8-sig"
            ) as file:

                # csv.DictReader():
                # CSV satırlarını sütun isimleriyle
                # erişilebilen sözlüklere dönüştürür.
                csv_rows = list(
                    csv.DictReader(file)
                )

            # ====================================================
            # 4. READ MARKDOWN REPORT
            # Markdown raporunu okuma
            # ====================================================

            # read_text():
            # Markdown dosyasının bütün içeriğini
            # string olarak döndürür.
            report_text = result["report_path"].read_text(
                encoding="utf-8"
            )

            # ====================================================
            # 5. COMPARE CSV AND MARKDOWN RECORDS
            # Hareket kayıtlarının tutarlılığını kontrol etme
            # ====================================================

            # Öncelikle CSV'deki veri satırı sayısının
            # geçmiş kayıt sayısıyla eşit olduğunu doğrula.
            self.assertEqual(
                len(csv_rows),
                len(result["history"])
            )

            # CSV içerisindeki bütün kayıtları dolaş.
            for row in csv_rows:

                # CSV sütunlarındaki:
                # - Step
                # - Action
                # - True Position
                #
                # değerlerinden Markdown tablo satırı oluştur.
                #
                # Örneğin:
                # | 1 | RIGHT | Hallway |
                #
                # Gerçek konum rastgele olabilir.
                # Ancak CSV ve Markdown'da aynı olmalıdır.
                expected_line = (
                    f"| {row['Step']} | "
                    f"{row['Action']} | "
                    f"{row['True Position']} |"
                )

                # assertIn():
                # Beklenen Markdown satırının
                # rapor içerisinde bulunmasını doğrular.
                self.assertIn(
                    expected_line,
                    report_text
                )

    # ========================================================
    # TEST 4 - FINAL BELIEF STATE
    # Son Markov inanç dağılımı testi
    # ========================================================

    def test_final_belief(self):
        """
        Son inanç dağılımının beklenen Markov
        olasılıklarına eşit olduğunu doğrular.

        Başlangıç:
        Robot Office odasındadır.

        Hareket dizisi:
        RIGHT -> RIGHT -> UP

        Beklenen:
        Living Room = 0.256
        Kitchen     = 0.512
        Office      = 0.040
        Hallway     = 0.064
        Dining Room = 0.128

        Robotun gerçek hareketi olasılıksaldır.

        Ancak Belief Prediction işlemi
        bütün olası hareket sonuçlarını
        hesapladığı için aynı hareket dizisi
        aynı inanç dağılımını üretir.
        """

        # 1. GEÇİCİ KLASÖR OLUŞTUR
        with tempfile.TemporaryDirectory() as temp_dir:

            # 2. DENEYİ ÇALIŞTIR
            result = run_experiment(
                ["RIGHT", "RIGHT", "UP"],
                temp_dir
            )

            # 3. SON İNANÇ DAĞILIMINI AL
            #
            # history[-1]:
            # Son hareket kaydını temsil eder.
            #
            # ["belief"]:
            # Son zaman adımındaki olasılık dağılımıdır.
            final_belief = result["history"][-1]["belief"]

            # 4. BEKLENEN OLASILIKLARI TANIMLA
            # Bu değerler projemizde kullanılan
            # Markov hareket modeline aittir.
            expected = {
                "Living Room": 0.256,
                "Kitchen": 0.512,
                "Office": 0.04,
                "Hallway": 0.064,
                "Dining Room": 0.128
            }

            # 5. HER ODANIN OLASILIĞINI DOĞRULA
            #
            # assertAlmostEqual():
            # Ondalıklı sayı karşılaştırmalarında
            # küçük kayan nokta hatalarını tolere eder.
            for room, probability in expected.items():

                self.assertAlmostEqual(
                    final_belief[room],
                    probability
                )

            # 6. TOPLAM OLASILIĞI DOĞRULA
            #
            # Geçerli bir inanç dağılımında
            # bütün odaların olasılıkları toplamı
            # 1.0 olmalıdır.
            self.assertAlmostEqual(
                sum(final_belief.values()),
                1.0
            )


# ============================================================
# MAIN - Test Runner
# Testleri doğrudan çalıştırma
# ============================================================

if __name__ == "__main__":
    unittest.main()
