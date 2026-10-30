
# ============================================================
# IMPORTS - Gerekli modüller
# ============================================================

import unittest
import tempfile

from pathlib import Path

import matplotlib

# Test sırasında grafik penceresi açılmaması için
# Matplotlib'in Agg backend'ini kullanıyoruz.
#
# Bu ayar pyplot importundan önce yapılmalıdır.
matplotlib.use("Agg")

import matplotlib.pyplot as plt

from robot_lab.core.simulation import RobotSimulation

from robot_lab.visualization.belief_plot import (
    plot_belief_history,
    save_belief_plot
)



# ============================================================
# TEST CLASS - VISUALIZATION TESTS
# Robot inanç grafiği birim testleri
# ============================================================

class TestVisualization(unittest.TestCase):
    """
    Robotun inanç geçmişini gösteren grafiği test eder.

    Bu sınıfta iki temel özellik doğrulanır:

    1. Five Room Lines:
       Her oda için ayrı bir çizgi oluşturulması.

    2. Office Line Values:
       Office odasının olasılıklarının grafik
       üzerinde doğru gösterilmesi.

    Testler grafik penceresi açılmadan çalıştırılır.
    """

    # ========================================================
    # TEST 1 - FIVE ROOM LINES
    # Beş oda için beş çizgi oluşturulması
    # ========================================================

    def test_five_room_lines(self):
        """
        Grafikte beş oda için beş çizgi olup
        olmadığını doğrular.

        Beklenen davranış:
        - Simülasyon Office odasında başlar.
        - Bir RIGHT hareketi gerçekleştirilir.
        - Hareket geçmişinden grafik oluşturulur.
        - Grafikte toplam 5 çizgi bulunmalıdır.

        Her çizgi bir odayı temsil eder.
        """

        # 1. SİMÜLASYONU OLUŞTUR
        # Robot Office odasında başlatılır.
        simulation = RobotSimulation(
            start_room="Office"
        )

        # 2. BİR RIGHT HAREKETİ GERÇEKLEŞTİR
        # Gerçek konum ve inanç dağılımı güncellenir.
        # Hareket sonucu geçmişe kaydedilir.
        simulation.step("RIGHT")

        # 3. HAREKET GEÇMİŞİNİ AL
        # Başlangıç ve birinci hareket kayıtları bulunur.
        history = simulation.get_history()

        # 4. GRAFİĞİ OLUŞTUR
        # Figure nesnesi döndürülür.
        # Grafik penceresi açılmaz.
        fig = plot_belief_history(history)

        # 5. GRAFİK NESNESİNİ TEST ET
        try:

            # Figure içerisindeki ilk Axes nesnesini al.
            #
            # fig.axes:
            # Figure içerisindeki eksen alanları.
            #
            # fig.axes[0]:
            # İlk grafik alanı.
            ax = fig.axes[0]

            # ax.lines:
            # Grafik üzerindeki çizgilerin listesi.
            #
            # Beş odamız olduğu için
            # toplam beş çizgi bekliyoruz.
            self.assertEqual(
                len(ax.lines),
                5
            )

        finally:

            # 6. GRAFİĞİ KAPAT
            # Test başarılı veya başarısız olsa da
            # Figure nesnesi kapatılır.
            #
            # Böylece gereksiz açık grafik
            # nesnelerinin birikmesi önlenir.
            plt.close(fig)

    # ========================================================
    # TEST 2 - OFFICE LINE VALUES
    # Office olasılık çizgisini doğrulama
    # ========================================================

    def test_office_line_values(self):
        """
        Office odasının çizgi değerlerini doğrular.

        Başlangıç:
        P(Office) = 1.0

        Birinci RIGHT sonrası:
        P(Office) = 0.2

        İkinci RIGHT sonrası:
        P(Office) = 0.04

        Beklenen grafik değerleri:
        [1.0, 0.2, 0.04]

        Grafik hesaplanan inanç dağılımlarını
        doğru göstermelidir.
        """

        # 1. SİMÜLASYONU OLUŞTUR
        simulation = RobotSimulation(
            start_room="Office"
        )

        # 2. İKİ RIGHT HAREKETİ GERÇEKLEŞTİR
        #
        # t = 0 -> Başlangıç
        # t = 1 -> Birinci RIGHT
        # t = 2 -> İkinci RIGHT
        simulation.step("RIGHT")
        simulation.step("RIGHT")

        # 3. HAREKET GEÇMİŞİNİ AL
        history = simulation.get_history()

        # 4. GRAFİĞİ OLUŞTUR
        fig = plot_belief_history(history)

        try:

            # 5. İLK GRAFİK ALANINI AL
            ax = fig.axes[0]

            # 6. OFFICE ÇİZGİSİNİ BUL
            # Başlangıçta çizgi bulunmadığını
            # belirtmek için None kullanıyoruz.
            office_line = None

            # Grafik üzerindeki bütün çizgileri dolaş.
            for line in ax.lines:

                # get_label():
                # Çizginin etiketini döndürür.
                #
                # Office etiketli çizgiyi arıyoruz.
                if line.get_label() == "Office":
                    office_line = line
                    break

            # 7. OFFICE ÇİZGİSİNİN VARLIĞINI DOĞRULA
            #
            # assertIsNotNone():
            # Değişkenin None olmadığını kontrol eder.
            #
            # Office çizgisi bulunamazsa
            # test başarısız olur.
            self.assertIsNotNone(office_line)

            # 8. BEKLENEN OLASILIKLARI TANIMLA
            #
            # t = 0 -> 1.0
            # t = 1 -> 0.2
            # t = 2 -> 0.04
            expected = [1.0, 0.2, 0.04]

            # 9. GRAFİKTEKİ GERÇEK DEĞERLERİ AL
            #
            # get_ydata():
            # Çizginin dikey eksenindeki
            # bütün değerleri döndürür.
            actual = office_line.get_ydata()

            # 10. VERİ SAYISINI DOĞRULA
            # Üç zaman adımı için üç olasılık
            # değeri bulunmalıdır.
            self.assertEqual(
                len(actual),
                len(expected)
            )

            # 11. OLASILIKLARI KARŞILAŞTIR
            # Her zaman adımındaki grafik değeri
            # beklenen olasılıkla karşılaştırılır.
            #
            # assertAlmostEqual():
            # Ondalıklı sayıların karşılaştırılmasında
            # küçük hassasiyet farklarını tolere eder.
            for index in range(len(expected)):

                self.assertAlmostEqual(
                    actual[index],
                    expected[index]
                )

        finally:

            # 12. GRAFİĞİ KAPAT
            # Testin sonucundan bağımsız olarak
            # grafik nesnesinin kapatılmasını sağlar.
            plt.close(fig)




    # ========================================================
    # TEST 3 - SAVE BELIEF PLOT AS PNG
    # İnanç grafiğini PNG olarak kaydetme testi
    # ========================================================

    def test_save_belief_plot(self):
        """
        save_belief_plot() fonksiyonunu test eder.

        Bu test:
        1. Örnek robot simülasyonu oluşturur.
        2. İki RIGHT hareketi gerçekleştirir.
        3. Hareket geçmişini alır.
        4. İnanç grafiğini oluşturur.
        5. Geçici bir klasör oluşturur.
        6. Grafiği PNG dosyasına kaydeder.
        7. Dosyanın gerçekten oluştuğunu doğrular.
        8. Dosyanın boş olmadığını doğrular.
        9. PNG dosya imzasını kontrol eder.
        10. Test sonunda kaynakları temizler.

        Beklenen sonuç:
        - PNG dosyası oluşturulmalıdır.
        - Dosya boyutu sıfırdan büyük olmalıdır.
        - Dosyanın ilk 8 baytı PNG imzasıyla
          eşleşmelidir.
        """

        # ====================================================
        # 1. CREATE ROBOT SIMULATION
        # Örnek robot simülasyonunu oluşturma
        # ====================================================

        # Robot Office odasında başlatılır.
        simulation = RobotSimulation(
            start_room="Office"
        )

        # İki RIGHT hareketi gerçekleştirilir.
        #
        # Her hareket:
        # - Gerçek robot konumunu günceller.
        # - İnanç dağılımını günceller.
        # - Hareket geçmişine kaydedilir.
        simulation.step("RIGHT")
        simulation.step("RIGHT")

        # ====================================================
        # 2. GET MOVEMENT HISTORY
        # Hareket geçmişini alma
        # ====================================================

        # Başlangıç durumu ve iki hareket kaydı alınır.
        #
        # history:
        # [record_0, record_1, record_2]
        history = simulation.get_history()

        # ====================================================
        # 3. CREATE BELIEF HISTORY FIGURE
        # İnanç geçmişi grafiğini oluşturma
        # ====================================================

        # Figure nesnesi oluşturulur.
        #
        # plot_belief_history() grafiği oluşturur
        # ancak ekranda göstermez.
        fig = plot_belief_history(history)

        try:

            # ================================================
            # 4. CREATE TEMPORARY DIRECTORY
            # Geçici klasör oluşturma
            # ================================================

            # TemporaryDirectory():
            # Test için geçici bir klasör oluşturur.
            #
            # with bloğundan çıkıldığında klasör
            # ve içindeki dosyalar temizlenir.
            with tempfile.TemporaryDirectory() as temp_dir:

                # ============================================
                # 5. CREATE PNG FILE PATH
                # PNG dosyasının yolunu oluşturma
                # ============================================

                # Path(temp_dir):
                # Geçici klasörün yolunu temsil eder.
                #
                # / operatörü:
                # Dosya yolu parçalarını birleştirir.
                #
                # Örneğin:
                # /tmp/abc123/test_belief.png
                file_path = Path(temp_dir) / "test_belief.png"

                # ============================================
                # 6. SAVE BELIEF PLOT
                # Grafiği PNG dosyasına kaydetme
                # ============================================

                # save_belief_plot():
                # Figure nesnesini belirtilen
                # dosya yoluna PNG olarak kaydeder.
                #
                # Kaydedilen dosyanın Path
                # nesnesini geri döndürür.
                saved_path = save_belief_plot(
                    fig,
                    file_path
                )

                # ============================================
                # 7. CHECK FILE EXISTENCE
                # Dosyanın oluştuğunu doğrulama
                # ============================================

                # assertTrue():
                # Verilen koşulun True olmasını bekler.
                #
                # is_file():
                # Belirtilen konumda gerçek bir dosya
                # bulunup bulunmadığını kontrol eder.
                self.assertTrue(
                    saved_path.is_file()
                )

                # ============================================
                # 8. CHECK FILE SIZE
                # Dosyanın boş olmadığını doğrulama
                # ============================================

                # stat().st_size:
                # Dosyanın boyutunu bayt cinsinden verir.
                #
                # assertGreater():
                # Birinci değerin ikinci değerden
                # büyük olmasını bekler.
                #
                # Böylece dosyanın en az bir miktar
                # veri içerdiğini doğrularız.
                self.assertGreater(
                    saved_path.stat().st_size,
                    0
                )

                # ============================================
                # 9. CHECK PNG FILE SIGNATURE
                # PNG dosyasının biçimini doğrulama
                # ============================================

                # PNG dosyalarının başlangıcında
                # standart 8 baytlık imza bulunur.
                #
                # PNG signature:
                # b"\x89PNG\r\n\x1a\n"
                #
                # rb:
                # Dosyayı binary (ikili) okuma
                # modunda açar.
                with saved_path.open("rb") as file:

                    # Dosyanın ilk 8 baytını oku.
                    signature = file.read(8)

                # Beklenen PNG imzasını tanımla.
                expected_signature = b"\x89PNG\r\n\x1a\n"

                # assertEqual():
                # Gerçek ve beklenen imzanın
                # eşit olduğunu doğrular.
                #
                # Eşleşme olmazsa test başarısız olur.
                self.assertEqual(
                    signature,
                    expected_signature
                )

        finally:

            # ================================================
            # 10. CLOSE FIGURE
            # Grafik nesnesini kapatma
            # ================================================

            # Test başarılı veya başarısız olsa bile
            # Matplotlib Figure nesnesi kapatılır.
            #
            # Böylece gereksiz grafik nesnelerinin
            # açık kalması önlenir.
            plt.close(fig)



# ============================================================
# MAIN - Test Runner
# Testleri doğrudan çalıştırma
# ============================================================

if __name__ == "__main__":
    unittest.main()
