
# ============================================================
# IMPORTS - Gerekli modüller
# ============================================================

import csv

from pathlib import Path

from robot_lab.worlds.house import ROOMS


# ============================================================
# EXPORT SIMULATION HISTORY TO CSV
# Simülasyon geçmişini CSV dosyasına aktarma
# ============================================================

def export_history_to_csv(history, file_path):
    """
    Robotun hareket geçmişini CSV dosyasına kaydeder.

    Bu fonksiyon:
    1. Kaydedilecek dosyanın yolunu oluşturur.
    2. Gerekli klasörler yoksa oluşturur.
    3. CSV sütun başlıklarını belirler.
    4. CSV dosyasını yazma modunda açar.
    5. Hareket geçmişindeki kayıtları satırlara dönüştürür.
    6. Her odanın inanç olasılığını ilgili sütuna ekler.
    7. Kaydedilen dosyanın yolunu döndürür.

    Args:
        history (list):
            RobotSimulation.get_history() metodundan
            elde edilen hareket kayıtları.

        file_path (str | Path):
            CSV dosyasının kaydedileceği konum.

    Returns:
        Path:
            Kaydedilen CSV dosyasının yolu.

    CSV yapısı:
        Step, Action, True Position, ...ROOMS

    Her satır robotun bir zaman adımını temsil eder.

    Önemli:
        Başlangıç durumu da history içerisinde
        bulunduğundan CSV dosyasına dahil edilir.
    """

    # ========================================================
    # 1. CREATE FILE PATH
    # CSV dosyasının yolunu oluşturma
    # ========================================================

    # Path():
    # Verilen dosya yolunu Path nesnesine dönüştürür.
    #
    # Örneğin:
    # "robot_lab/experiments/results/simulation_history.csv"
    #
    # Path nesnesi dosya yollarının işletim sistemine
    # uygun şekilde yönetilmesini sağlar.
    path = Path(file_path)

    # ========================================================
    # 2. CREATE OUTPUT DIRECTORY
    # Kaydetme klasörünü oluşturma
    # ========================================================

    # path.parent:
    # Dosyanın bulunduğu üst klasörü temsil eder.
    #
    # mkdir():
    # Belirtilen klasörü oluşturur.
    #
    # parents=True:
    # Gerekli üst klasörleri de oluşturur.
    #
    # exist_ok=True:
    # Klasör zaten varsa hata oluşturmaz.
    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    # ========================================================
    # 3. CREATE CSV HEADERS
    # CSV sütun başlıklarını oluşturma
    # ========================================================

    # İlk üç sütun hareket bilgilerini saklar.
    #
    # Step:
    # Hareketin zaman adımı.
    #
    # Action:
    # Verilen hareket komutu.
    #
    # True Position:
    # Robotun hareket sonrası gerçek konumu.
    headers = [
        "Step",
        "Action",
        "True Position"
    ]

    # ROOMS listesindeki bütün odaları
    # CSV sütunlarına ekleriz.
    #
    # Her oda için ayrı bir olasılık
    # sütunu oluşturulur.
    #
    # Böylece oda sayısı değiştiğinde
    # sütunlar otomatik olarak güncellenir.
    for room in ROOMS:
        headers.append(room)

    # ========================================================
    # 4. OPEN CSV FILE
    # CSV dosyasını yazma modunda açma
    # ========================================================

    # "w":
    # Dosyayı yazma modunda açar.
    # Dosya mevcutsa eski içeriği yeniden yazar.
    #
    # newline="":
    # CSV yazımında satır sonlarının doğru
    # yönetilmesini sağlar.
    #
    # encoding="utf-8-sig":
    # Türkçe karakterlerin Excel gibi
    # programlarda daha uyumlu açılmasına
    # yardımcı olur.
    #
    # with:
    # İşlem bittiğinde dosyanın otomatik
    # olarak kapatılmasını sağlar.
    with path.open(
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:

        # ====================================================
        # 5. CREATE CSV WRITER
        # CSV yazıcı nesnesini oluşturma
        # ====================================================

        # csv.writer():
        # Python listelerini CSV satırlarına
        # dönüştürmek için kullanılır.
        writer = csv.writer(file)

        # ====================================================
        # 6. WRITE CSV HEADERS
        # Sütun başlıklarını dosyaya yazma
        # ====================================================

        # writerow():
        # Verilen listenin elemanlarını
        # CSV dosyasında tek satıra yazar.
        #
        # İlk satır sütun başlıklarını içerir.
        writer.writerow(headers)

        # ====================================================
        # 7. EXPORT MOVEMENT RECORDS
        # Hareket kayıtlarını CSV satırlarına aktarma
        # ====================================================

        # Hareket geçmişindeki bütün kayıtları dolaş.
        #
        # İlk kayıt başlangıç durumudur:
        # step = 0, action = START
        for record in history:

            # ================================================
            # 8. CREATE RECORD ROW
            # Hareket bilgilerini satıra ekleme
            # ================================================

            # Her satırın ilk üç alanı:
            #
            # 1. Hareket adımı
            # 2. Hareket komutu
            # 3. Gerçek robot konumu
            row = [
                record["step"],
                record["action"],
                record["true_position"]
            ]

            # ================================================
            # 9. ADD BELIEF PROBABILITIES
            # Her odanın olasılığını satıra ekleme
            # ================================================

            # ROOMS içerisindeki her oda için
            # o zaman adımındaki olasılığı alırız.
            #
            # Örneğin:
            # record["belief"]["Office"]
            #
            # Sonuç 0.2 ise Office sütununa
            # bu değer eklenir.
            for room in ROOMS:

                probability = record["belief"][room]

                row.append(probability)

            # ================================================
            # 10. WRITE RECORD TO CSV
            # Oluşturulan satırı dosyaya yazma
            # ================================================

            # Satırdaki hareket bilgileri ve
            # bütün oda olasılıkları CSV'ye yazılır.
            writer.writerow(row)

    # ========================================================
    # 11. RETURN SAVED FILE PATH
    # Kaydedilen dosyanın yolunu döndürme
    # ========================================================

    # with bloğu tamamlandığında dosya kapatılır.
    #
    # Kaydedilen CSV dosyasının Path
    # nesnesini çağıran fonksiyona döndürürüz.
    return path
