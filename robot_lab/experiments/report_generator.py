from pathlib import Path

from robot_lab.worlds.house import ROOMS



# ============================================================
# IMPORTS - Gerekli modüller
# ============================================================

from pathlib import Path

from robot_lab.worlds.house import ROOMS


# ============================================================
# GENERATE EXPERIMENT REPORT
# Otomatik deney raporu oluşturma
# ============================================================

def generate_experiment_report(history, file_path):
    """
    Robotun hareket geçmişinden Markdown deney raporu oluşturur.

    Bu fonksiyon:
    1. Rapor dosyasının konumunu hazırlar.
    2. Deney başlığını ve amacını oluşturur.
    3. Başlangıç koşullarını rapora ekler.
    4. Hareket komutlarını listeler.
    5. Hareket sonuçlarını tabloya dönüştürür.
    6. Son inanç dağılımını gösterir.
    7. Deney sonuçlarını değerlendirir.
    8. Raporu Markdown dosyasına kaydeder.

    Args:
        history (list):
            RobotSimulation.get_history() metodundan
            elde edilen hareket kayıtları.

        file_path (str | Path):
            Markdown raporunun kaydedileceği dosya yolu.

    Returns:
        Path:
            Oluşturulan Markdown raporunun dosya yolu.

    Önemli:
        history listesinin boş olmadığı varsayılır.

        Rapordaki gerçek konumlar olasılıksal
        hareket modeline göre değişebilir.
    """

    # ========================================================
    # 1. CREATE REPORT FILE PATH
    # Rapor dosyasının yolunu oluşturma
    # ========================================================

    # Path():
    # Dosya yolunu Path nesnesine dönüştürür.
    path = Path(file_path)

    # Gerekli klasörler yoksa oluşturur.
    #
    # parents=True:
    # Üst klasörleri de oluşturur.
    #
    # exist_ok=True:
    # Klasör zaten varsa hata oluşturmaz.
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # ========================================================
    # 2. INITIALIZE REPORT CONTENT
    # Rapor metnini oluşturmaya başlama
    # ========================================================

    # lines:
    # Markdown dosyasına yazılacak bütün
    # metin satırlarını saklayan listedir.
    lines = []

    # Markdown ana başlığı.
    #
    # # işareti birinci seviye başlık oluşturur.
    lines.append("# Robot Intelligence Lab - Deney 001")
    lines.append("")

    # ========================================================
    # 3. EXPERIMENT OBJECTIVE
    # Deney amacını açıklama
    # ========================================================

    # ## işareti ikinci seviye başlık oluşturur.
    lines.append("## Deney Amacı")
    lines.append("")

    lines.append(
        "Olasılıksal robot hareketlerini ve "
        "Markov inanç dağılımlarını incelemek."
    )

    lines.append("")

    # ========================================================
    # 4. INITIAL CONDITIONS
    # Başlangıç koşullarını rapora ekleme
    # ========================================================

    # history[0]:
    # Simülasyonun başlangıç kaydını temsil eder.
    #
    # step = 0
    # action = START
    first_record = history[0]

    lines.append("## Başlangıç Koşulları")
    lines.append("")

    # Başlangıçtaki gerçek robot konumu.
    lines.append(
        "Başlangıç odası: "
        + first_record["true_position"]
    )

    lines.append("")

    # ========================================================
    # 5. MOVEMENT COMMANDS
    # Hareket komutlarını rapora ekleme
    # ========================================================

    lines.append("## Hareket Komutları")
    lines.append("")

    # history[1:]:
    # Başlangıç kaydını atlayarak
    # gerçekleştirilen hareketleri alır.
    #
    # Örneğin:
    # ["RIGHT", "RIGHT", "UP"]
    actions = []

    for record in history[1:]:
        actions.append(record["action"])

    # Hareket komutlarını birleştirir.
    #
    # Örneğin:
    # RIGHT -> RIGHT -> UP
    if actions:
        action_sequence = " → ".join(actions)
    else:
        action_sequence = "Hareket gerçekleştirilmedi."

    lines.append(action_sequence)
    lines.append("")

    # ========================================================
    # 6. EXPERIMENT RESULTS TABLE
    # Deney sonuçlarını tablo olarak oluşturma
    # ========================================================

    lines.append("## Deney Sonuçları")
    lines.append("")

    # Markdown tablo başlıkları.
    lines.append(
        "| Adım | Komut | Gerçek Konum |"
    )

    # Markdown tablo ayırıcı satırı.
    lines.append(
        "|---|---|---|"
    )

    # Hareket geçmişindeki bütün kayıtları dolaş.
    #
    # Başlangıç kaydı da tabloya dahil edilir.
    for record in history:

        step = record["step"]
        action = record["action"]
        true_position = record["true_position"]

        # f-string:
        # Değişkenlerin değerlerini Markdown
        # tablo satırına yerleştirir.
        lines.append(
            f"| {step} | {action} | {true_position} |"
        )

    lines.append("")

    # ========================================================
    # 7. FINAL BELIEF STATE
    # Son inanç dağılımını rapora ekleme
    # ========================================================

    lines.append("## Son İnanç Dağılımı")
    lines.append("")

    # history[-1]:
    # Listenin son elemanını döndürür.
    #
    # Bu kayıt simülasyonun son durumudur.
    last_record = history[-1]

    # Son zaman adımındaki inanç dağılımı.
    final_belief = last_record["belief"]

    # ROOMS içerisindeki bütün odaları dolaş.
    for room in ROOMS:

        # İlgili odanın son olasılığını al.
        probability = final_belief[room]

        # :.4f:
        # Sayıyı virgülden sonra dört
        # basamakla gösterir.
        #
        # Örneğin:
        # Hallway: 0.0640
        lines.append(
            f"- {room}: {probability:.4f}"
        )

    lines.append("")

    # ========================================================
    # 8. EXPERIMENT EVALUATION
    # Deney sonuçlarını değerlendirme
    # ========================================================

    lines.append("## Değerlendirme")
    lines.append("")

    # Toplam hareket sayısı.
    #
    # Başlangıç kaydı hareket sayılmaz.
    total_steps = len(history) - 1

    lines.append(
        f"Toplam {total_steps} hareket gerçekleştirildi."
    )

    lines.append("")

    # Son gerçek robot konumu.
    lines.append(
        "Son gerçek konum: "
        + last_record["true_position"]
    )

    lines.append("")

    # En yüksek olasılığa sahip odayı belirle.
    #
    # max(..., key=final_belief.get):
    # Olasılık değeri en yüksek olan
    # oda ismini döndürür.
    most_likely_room = max(
        ROOMS,
        key=final_belief.get
    )

    most_likely_probability = final_belief[
        most_likely_room
    ]

    lines.append(
        "En yüksek olasılığa sahip oda: "
        f"{most_likely_room} "
        f"({most_likely_probability:.4f})"
    )

    lines.append("")

    # İnanç dağılımındaki bütün olasılıkların
    # toplamını hesaplar.
    total_probability = sum(
        final_belief.values()
    )

    lines.append(
        "Son inanç dağılımının toplamı: "
        f"{total_probability:.4f}"
    )

    lines.append("")

    # Matematiksel değerlendirme.
    lines.append(
        "İnanç dağılımı, robotun hangi odada "
        "bulunabileceğini olasılıksal olarak temsil eder."
    )

    lines.append("")

    lines.append(
        "Gerçek konum, hareket modelinden örneklenirken "
        "inanç dağılımı bütün olası hareket sonuçları "
        "dikkate alınarak hesaplanır."
    )

    lines.append("")

    # ========================================================
    # 9. GENERATE REPORT TEXT
    # Rapor satırlarını tek metinde birleştirme
    # ========================================================

    # "\n".join(lines):
    # Listedeki bütün metinleri satır sonu
    # karakteriyle birleştirir.
    #
    # Böylece rapor tek bir string olur.
    report_text = "\n".join(lines)

    # ========================================================
    # 10. SAVE MARKDOWN REPORT
    # Markdown raporunu dosyaya kaydetme
    # ========================================================

    # write_text():
    # Rapor metnini belirtilen dosyaya yazar.
    #
    # encoding="utf-8":
    # Türkçe karakterlerin doğru kaydedilmesini sağlar.
    path.write_text(
        report_text,
        encoding="utf-8"
    )

    # ========================================================
    # 11. RETURN REPORT FILE PATH
    # Kaydedilen rapor yolunu döndürme
    # ========================================================

    return path
