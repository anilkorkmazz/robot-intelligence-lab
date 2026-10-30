
# ============================================================
# IMPORTS - Gerekli modüller
# ============================================================

import matplotlib.pyplot as plt
from robot_lab.worlds.house import ROOMS
from pathlib import Path

# ============================================================
# BELIEF HISTORY VISUALIZATION
# Robotun inanç geçmişini görselleştirme
# ============================================================

def plot_belief_history(history):
    """
    Robotun hareket geçmişindeki inanç dağılımlarını
    çizgi grafiği kullanarak görselleştirir.

    Bu fonksiyon:
    1. Figure ve Axes nesnelerini oluşturur.
    2. Hareket geçmişindeki zaman adımlarını toplar.
    3. Her oda için olasılık değerlerini toplar.
    4. Her odanın olasılık değişimini çizgiyle gösterir.
    5. Grafik başlığını ve eksenlerini düzenler.
    6. Oluşturulan Figure nesnesini döndürür.

    Args:
        history (list):
            RobotSimulation.get_history() metodundan
            elde edilen hareket kayıtları.

    Returns:
        matplotlib.figure.Figure:
            Oluşturulan grafik nesnesi.

    Grafik:
        X ekseni -> Hareket adımı (Discrete Time)
        Y ekseni -> Odada bulunma olasılığı

    Önemli:
        Bu fonksiyon grafiği ekranda açmaz.

        Grafiğin gösterilmesi, kaydedilmesi veya
        test edilmesi çağıran kodun sorumluluğudur.
    """

    # ========================================================
    # 1. CREATE FIGURE AND AXES
    # Grafik ve eksen nesnelerini oluşturma
    # ========================================================

    # plt.subplots() iki nesne döndürür:
    #
    # fig (Figure):
    # Grafiğin tamamını temsil eder.
    #
    # ax (Axes):
    # Çizgileri, başlıkları ve eksenleri
    # yerleştirdiğimiz grafik alanıdır.
    fig, ax = plt.subplots()

    # ========================================================
    # 2. MOVEMENT STEPS
    # Hareket adımlarını toplama
    # ========================================================

    # Grafiğin X eksenindeki zaman adımlarını
    # saklamak için boş bir liste oluştururuz.
    steps = []

    # Hareket geçmişindeki bütün kayıtları dolaşırız.
    for record in history:

        # Her kaydın zaman adımını listeye ekleriz.
        #
        # Örneğin:
        # steps = [0, 1, 2]
        #
        # 0 -> Başlangıç
        # 1 -> Birinci hareket
        # 2 -> İkinci hareket
        steps.append(record["step"])

    # ========================================================
    # 3. BELIEF PROBABILITIES
    # Her odanın olasılıklarını toplama
    # ========================================================

    # ROOMS içerisindeki bütün odaları dolaşırız.
    #
    # Her oda için ayrı bir çizgi oluşturulacaktır.
    for room in ROOMS:

        # İlgili odanın bütün zaman adımlarındaki
        # olasılıklarını saklayacağımız liste.
        probabilities = []

        # Hareket geçmişindeki bütün kayıtları dolaşırız.
        for record in history:

            # İlgili odanın o adımdaki
            # olasılık değerini alırız.
            #
            # Örneğin:
            # record["belief"]["Office"]
            probability = record["belief"][room]

            # Olasılığı listeye ekleriz.
            probabilities.append(probability)

        # ====================================================
        # 4. PLOT ROOM PROBABILITIES
        # Her oda için olasılık çizgisi oluşturma
        # ====================================================

        # ax.plot() belirlenen Axes üzerine
        # çizgi oluşturur.
        #
        # steps:
        # X eksenindeki zaman adımları.
        #
        # probabilities:
        # Y eksenindeki olasılık değerleri.
        #
        # marker="o":
        # Her veri noktasında daire gösterir.
        #
        # label=room:
        # Çizginin ait olduğu odanın adını saklar.
        #
        # Bu etiket testlerde çizgiyi
        # bulmak için de kullanılacaktır.
        ax.plot(
            steps,
            probabilities,
            marker="o",
            label=room
        )

    # ========================================================
    # 5. GRAPH CONFIGURATION
    # Grafik görünümünü düzenleme
    # ========================================================

    # Grafik başlığını ayarla.
    ax.set_title("Robot Belief History")

    # X ekseni hareket adımlarını temsil eder.
    ax.set_xlabel("Movement Step")

    # Y ekseni olasılıkları temsil eder.
    ax.set_ylabel("Probability")

    # Olasılıkların gösterildiği dikey ekseni
    # 0 ile 1 arasında sınırlandır.
    ax.set_ylim(0, 1)

    # X ekseninde kayıtlı hareket adımlarını göster.
    ax.set_xticks(steps)

    # Çizgilerin hangi odalara ait olduğunu göster.
    ax.legend()

    # Yardımcı çizgileri etkinleştir.
    ax.grid(True)

    # ========================================================
    # 6. RETURN FIGURE
    # Grafik nesnesini döndürme
    # ========================================================

    # Önceki sürüm:
    # plt.show()
    #
    # Yeni sürüm:
    # return fig
    #
    # Grafiği burada açmıyoruz.
    # Oluşturulan Figure nesnesini döndürüyoruz.
    #
    # Böylece grafik:
    # - Ekranda gösterilebilir.
    # - PNG/PDF olarak kaydedilebilir.
    # - Otomatik testlerle kontrol edilebilir.
    return fig



# ============================================================
# SAVE BELIEF PLOT
# İnanç grafiğini PNG dosyasına kaydetme
# ============================================================

def save_belief_plot(fig, file_path):
    """
    Oluşturulan inanç grafiğini PNG dosyasına kaydeder.

    Bu fonksiyon:
    1. Verilen dosya yolunu Path nesnesine dönüştürür.
    2. Kaydetme klasörünün varlığını kontrol eder.
    3. Gerekli klasörler yoksa oluşturur.
    4. Matplotlib Figure nesnesini PNG olarak kaydeder.
    5. Kaydedilen dosyanın yolunu döndürür.

    Args:
        fig (matplotlib.figure.Figure):
            plot_belief_history() tarafından
            oluşturulan grafik nesnesi.

        file_path (str | Path):
            Grafiğin kaydedileceği dosya yolu.

    Returns:
        Path:
            Kaydedilen grafik dosyasının yolu.

    Önemli:
        Bu fonksiyon grafik penceresini açmaz.
        Sadece grafiği dosyaya kaydeder.
    """

    # ========================================================
    # 1. CREATE FILE PATH
    # Dosya yolunu oluşturma
    # ========================================================

    # Path(), verilen dosya yolunu Python'un
    # pathlib.Path nesnesine dönüştürür.
    #
    # Örneğin:
    # "robot_lab/experiments/results/belief_history.png"
    path = Path(file_path)

    # ========================================================
    # 2. CREATE OUTPUT DIRECTORY
    # Kayıt klasörünü oluşturma
    # ========================================================

    # path.parent:
    # Dosyanın kaydedileceği klasörü belirtir.
    #
    # parents=True:
    # Gerekirse üst klasörleri de oluşturur.
    #
    # exist_ok=True:
    # Klasör zaten varsa hata oluşturmaz.
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # ========================================================
    # 3. SAVE FIGURE AS PNG
    # Grafiği PNG dosyasına kaydetme
    # ========================================================

    # fig.savefig():
    # Matplotlib Figure nesnesini dosyaya kaydeder.
    #
    # dpi=150:
    # Grafiğin çözünürlüğünü belirler.
    #
    # bbox_inches="tight":
    # Grafik çevresindeki gereksiz boşlukları azaltır.
    #
    # format="png":
    # Çıktının PNG formatında olmasını sağlar.
    fig.savefig(
        path,
        format="png",
        dpi=150,
        bbox_inches="tight"
    )

    # ========================================================
    # 4. RETURN SAVED FILE PATH
    # Kaydedilen dosyanın yolunu döndürme
    # ========================================================

    # Kaydetme başarılıysa dosyanın
    # bulunduğu konumu döndürürüz.
    return path

