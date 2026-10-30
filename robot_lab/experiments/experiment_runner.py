
# ============================================================
# IMPORTS - Gerekli modüller
# ============================================================

from pathlib import Path

import matplotlib.pyplot as plt

from robot_lab.core.simulation import RobotSimulation

from robot_lab.visualization.belief_plot import (
    plot_belief_history,
    save_belief_plot
)

from robot_lab.experiments.csv_export import (
    export_history_to_csv
)

from robot_lab.experiments.report_generator import (
    generate_experiment_report
)


# ============================================================
# INTEGRATED EXPERIMENT RUNNER
# Bütünleşik robot deneyi yürütme
# ============================================================

def run_experiment(actions, output_folder):
    """
    Robot deneyini gerçekleştirir ve sonuçlarını kaydeder.

    Bu fonksiyon:
    1. Yeni bir RobotSimulation nesnesi oluşturur.
    2. Hareket komutlarını sırayla gerçekleştirir.
    3. Deneyin bütün hareket geçmişini alır.
    4. Sonuçların kaydedileceği klasörü oluşturur.
    5. PNG, CSV ve Markdown dosya yollarını belirler.
    6. İnanç grafiğini PNG dosyasına kaydeder.
    7. Simülasyon geçmişini CSV dosyasına kaydeder.
    8. Markdown deney raporunu oluşturur.
    9. Deney geçmişini ve çıktı yollarını döndürür.

    Args:
        actions (list):
            Robotun gerçekleştireceği hareket komutları.

            Örnek:
            ["RIGHT", "RIGHT", "UP"]

        output_folder (str | Path):
            Deney sonuçlarının kaydedileceği klasör.

    Returns:
        dict:
            Deney sonuçlarını içeren sözlük.

            {
                "history": list,
                "png_path": Path,
                "csv_path": Path,
                "report_path": Path
            }

    Önemli:
        PNG, CSV ve Markdown dosyalarının tamamı
        aynı simülasyon geçmişinden oluşturulur.

        Böylece dosyalar arasındaki deney verileri
        tutarlı kalır.
    """

    # ========================================================
    # 1. CREATE ROBOT SIMULATION
    # Robot simülasyonunu oluşturma
    # ========================================================

    # Yeni bir RobotSimulation nesnesi oluştururuz.
    #
    # Robot Office odasında başlatılır.
    #
    # Başlangıçta:
    # - Gerçek konum Office'dir.
    # - P(Office) = 1.0
    # - Zaman adımı 0'dır.
    # - Başlangıç kaydı history listesine eklenir.
    simulation = RobotSimulation(
        start_room="Office"
    )

    # ========================================================
    # 2. EXECUTE MOVEMENT SEQUENCE
    # Hareket komutlarını gerçekleştirme
    # ========================================================

    # actions:
    # Deneyde kullanılacak hareket komutlarının listesi.
    #
    # Örneğin:
    # ["RIGHT", "RIGHT", "UP"]
    #
    # Komutlar sırayla uygulanır.
    for action in actions:

        # step():
        # 1. Hareket komutunu doğrular.
        # 2. Robotun gerçek hareketini örnekler.
        # 3. Gerçek konumu günceller.
        # 4. İnanç dağılımını günceller.
        # 5. Zaman adımını artırır.
        # 6. Hareket sonucunu geçmişe kaydeder.
        simulation.step(action)

    # ========================================================
    # 3. GET EXPERIMENT HISTORY
    # Deneyin hareket geçmişini alma
    # ========================================================

    # get_history():
    # Simülasyonun bütün hareket kayıtlarını alır.
    #
    # Başlangıç kaydı da geçmişe dahildir.
    #
    # Örneğin:
    # history[0] -> START
    # history[1] -> RIGHT
    # history[2] -> RIGHT
    # history[3] -> UP
    #
    # Tek bir history listesi oluşturulur.
    # Bütün çıktı dosyaları bu listeyi kullanır.
    history = simulation.get_history()

    # ========================================================
    # 4. CREATE OUTPUT DIRECTORY
    # Deney sonuçlarının kaydedileceği klasörü oluşturma
    # ========================================================

    # Path():
    # Verilen klasör yolunu Path nesnesine dönüştürür.
    folder = Path(output_folder)

    # mkdir():
    # Sonuç klasörünü oluşturur.
    #
    # parents=True:
    # Gerekli üst klasörleri de oluşturur.
    #
    # exist_ok=True:
    # Klasör zaten bulunuyorsa hata üretmez.
    folder.mkdir(
        parents=True,
        exist_ok=True
    )

    # ========================================================
    # 5. DEFINE OUTPUT FILE PATHS
    # Çıktı dosyalarının yollarını belirleme
    # ========================================================

    # PNG:
    # Robotun inanç dağılımının zaman içindeki
    # değişimini gösteren çizgi grafiği.
    png_path = folder / "belief_history.png"

    # CSV:
    # Her hareketin komutunu, gerçek konumunu
    # ve bütün oda olasılıklarını saklayan tablo.
    csv_path = folder / "simulation_history.csv"

    # Markdown:
    # Deney amacı, hareket kayıtları ve
    # son inanç dağılımını açıklayan rapor.
    report_path = folder / "experiment_001.md"

    # ========================================================
    # 6. GENERATE AND SAVE BELIEF PLOT
    # İnanç grafiğini oluşturma ve PNG kaydetme
    # ========================================================

    # plot_belief_history():
    # Hareket geçmişindeki olasılıkları kullanarak
    # Matplotlib Figure nesnesi oluşturur.
    #
    # Grafik penceresini açmaz.
    fig = plot_belief_history(history)

    try:

        # save_belief_plot():
        # Figure nesnesini belirtilen dosyaya
        # PNG biçiminde kaydeder.
        save_belief_plot(
            fig,
            png_path
        )

    finally:

        # plt.close(fig):
        # Grafik nesnesini kapatır.
        #
        # Kaydetme sırasında hata oluşsa bile
        # Matplotlib kaynakları temizlenir.
        #
        # Bu fonksiyon grafik penceresi açmaz.
        plt.close(fig)

    # ========================================================
    # 7. EXPORT SIMULATION HISTORY TO CSV
    # Simülasyon geçmişini CSV dosyasına kaydetme
    # ========================================================

    # export_history_to_csv():
    # Her hareket kaydını CSV satırına dönüştürür.
    #
    # Her oda için ayrı bir olasılık sütunu bulunur.
    #
    # Aynı history listesi kullanıldığı için
    # CSV verileri PNG grafiğiyle tutarlıdır.
    export_history_to_csv(
        history,
        csv_path
    )

    # ========================================================
    # 8. GENERATE MARKDOWN EXPERIMENT REPORT
    # Markdown deney raporunu oluşturma
    # ========================================================

    # generate_experiment_report():
    # Hareket geçmişinden okunabilir bir
    # Markdown deney raporu üretir.
    #
    # Hareket komutları, gerçek konumlar ve
    # son inanç dağılımı rapora eklenir.
    #
    # Bu rapor da aynı history listesini kullanır.
    generate_experiment_report(
        history,
        report_path
    )

    # ========================================================
    # 9. RETURN EXPERIMENT RESULTS
    # Deney sonuçlarını döndürme
    # ========================================================

    # Oluşturulan üç dosyanın yollarını ve
    # deneyin bütün hareket geçmişini döndürürüz.
    #
    # Böylece diğer fonksiyonlar veya otomatik
    # testler deney sonuçlarına erişebilir.
    return {
        "history": history,
        "png_path": png_path,
        "csv_path": csv_path,
        "report_path": report_path
    }
