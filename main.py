
# ============================================================
# IMPORTS - Gerekli modüller
# ============================================================

from robot_lab.worlds.house import ROOMS, ROOM_CONNECTIONS
from robot_lab.core.robot import Robot

from robot_lab.motion.actions import ACTIONS
from robot_lab.motion.movement_rules import get_target_room
from robot_lab.motion.motion_model import (
    get_motion_probabilities,
    sample_motion
)
from robot_lab.motion.transition_matrix import create_transition_matrix

from robot_lab.belief.belief_state import BeliefState
from robot_lab.belief.belief_update import (
    predict_belief,
    predict_belief_with_matrix
)

from robot_lab.experiments.report_generator import generate_experiment_report
from robot_lab.core.simulation import RobotSimulation
from robot_lab.experiments.csv_export import export_history_to_csv
from robot_lab.visualization.belief_plot import (
    plot_belief_history,
    save_belief_plot
)

import matplotlib.pyplot as plt
from robot_lab.experiments.experiment_runner import run_experiment

# ============================================================
# HELPER FUNCTIONS - Yardımcı fonksiyonlar
# ============================================================

def print_section(title):
    """
    Terminal çıktısını başlıklara ayırır.

    Her bölümün başlangıcını daha okunabilir
    hale getirmek için kullanılır.
    """
    print("\n" + "=" * 55)
    print(title)
    print("=" * 55)


def print_probabilities(probabilities):
    """
    Olasılık dağılımını ekrana yazdırır.

    Her odanın olasılığını ve toplam
    olasılık değerini gösterir.

    Geçerli bir olasılık dağılımında
    toplam değer 1 olmalıdır.
    """
    for room, probability in probabilities.items():
        print(f"{room}: {probability:.4f}")

    total = sum(probabilities.values())
    print(f"Toplam olasılık: {total:.4f}")


# ============================================================
# SECTION 1 - WORLD MODEL
# Robotun bulunduğu dünya
# ============================================================

def show_world():
    """
    Robotun hareket edebileceği dünyayı gösterir.

    - Odaları listeler.
    - Odalar arasındaki bağlantıları gösterir.
    - Kullanılabilir hareket komutlarını listeler.
    """
    print_section("1. WORLD MODEL")

    print("\nOdalar:")

    for room in ROOMS:
        print("-", room)

    print("\nOdalar arasındaki bağlantılar:")

    for room, neighbors in ROOM_CONNECTIONS.items():
        print(room, "->", ", ".join(neighbors))

    print("\nHareket komutları:")

    for action in ACTIONS:
        print("-", action)


# ============================================================
# SECTION 2 - DETERMINISTIC MOTION
# Kesin hareket modeli
# ============================================================

def show_deterministic_motion():
    """
    Kesin (deterministic) hareketi test eder.

    Bu modelde:
    - Hareket komutu bir hedef oda belirler.
    - Robot hareketi gerçekleştirdiğinde
      belirlenen hedefe geçer.

    Hareket sonucunda belirsizlik yoktur.
    """
    print_section("2. DETERMINISTIC MOTION")

    robot = Robot(start_room="Office")

    action = "RIGHT"
    current_room = robot.get_position()

    # 1. Hareketin hedef odasını hesapla.
    # Bu işlem robotun konumunu değiştirmez.
    target = get_target_room(current_room, action)

    print("\nHareket yönü testi:")
    print("Mevcut oda:", current_room)
    print("Komut:", action)
    print("Hedef oda:", target)
    print("Gerçek konum:", robot.get_position())

    # 2. Gerçek hareketi gerçekleştir.
    # move() robotun konumunu günceller.
    new_room = robot.move(action)

    print("\nHareket sonrası:")
    print("Yeni konum:", new_room)


# ============================================================
# SECTION 3 - PROBABILISTIC MOTION MODEL
# Olasılıksal hareket modeli
# ============================================================

def show_probabilistic_motion():
    """
    Hareket sonuçlarının olasılıklarını gösterir.

    Deterministic modelden farklı olarak,
    verilen bir hareket komutunun birden fazla
    olası sonucu bulunabilir.

    Örneğin robot RIGHT komutuyla:
    - Hedef odaya geçebilir.
    - Bulunduğu odada kalabilir.

    Burada yalnızca olasılıklar hesaplanır.
    Gerçek robot hareket ettirilmez.
    """
    print_section("3. PROBABILISTIC MOTION MODEL")

    current_room = "Office"
    action = "RIGHT"

    probabilities = get_motion_probabilities(
        current_room,
        action
    )

    print("\nBaşlangıç:", current_room)
    print("Komut:", action)

    print("\nOlası hareket sonuçları:")
    print_probabilities(probabilities)


# ============================================================
# SECTION 4 - MOTION SAMPLING
# Olasılıksal hareket örnekleme
# ============================================================

def show_motion_sampling():
    """
    Olasılıksal hareket sonuçlarını örnekler.

    Sampling:
    Olasılık dağılımına göre tek bir
    hareket sonucunun seçilmesidir.

    Aynı komut tekrarlandığında
    farklı sonuçlar elde edilebilir.
    """
    print_section("4. MOTION SAMPLING")

    # 1. Bağımsız örnekleme denemeleri.
    # Her deneme Office odasından başlar.
    print("\n10 bağımsız örnekleme:")

    for i in range(10):
        result = sample_motion("Office", "RIGHT")
        print(f"Deneme {i + 1}: {result}")

    # 2. Robot üzerinde tek hareket.
    print("\nRobotun gerçek hareketi:")

    robot = Robot(start_room="Office")

    print("Başlangıç:", robot.get_position())

    new_position = robot.move_probabilistic("RIGHT")

    print("Komut: RIGHT")
    print("Gerçek konum:", new_position)

    # 3. Ardışık hareketler.
    # Her hareket bir öncekinin sonucundan başlar.
    print("\nArdışık 5 hareket:")

    sequence_robot = Robot(start_room="Office")

    print("Başlangıç:", sequence_robot.get_position())

    for step in range(5):
        new_room = sequence_robot.move_probabilistic(
            "RIGHT"
        )

        print(f"Adım {step + 1}: {new_room}")


# ============================================================
# SECTION 5 - BELIEF STATE PREDICTION
# İnanç durumu güncelleme
# ============================================================

def show_belief_prediction():
    """
    Robotun inanç dağılımını günceller.

    Belief State:
    Robotun hangi odada bulunabileceğine
    ilişkin olasılık dağılımıdır.

    Predict Belief:
    Önceki inanç dağılımını ve verilen
    hareket komutunu kullanarak yeni
    dağılımı hesaplar.

    Bu işlem gerçek hareket sonucunu
    bilmeden yapılır.
    """
    print_section("5. BELIEF STATE PREDICTION")

    # 1. Başlangıç inancı.
    # Robotun Office odasında olduğu biliniyor.
    belief = BeliefState(start_room="Office")

    current_belief = belief.get_probabilities()

    print("\nBaşlangıç inanç dağılımı:")
    print_probabilities(current_belief)

    # 2. İlk RIGHT hareketinin tahmini.
    # Tek bir gerçek sonuç seçilmez.
    # Bütün olası sonuçlar hesaplanır.
    current_belief = predict_belief(
        current_belief,
        "RIGHT"
    )

    print("\n1. RIGHT sonrası:")
    print_probabilities(current_belief)

    # 3. İkinci RIGHT hareketinin tahmini.
    # Önceki dağılım yeni başlangıçtır.
    current_belief = predict_belief(
        current_belief,
        "RIGHT"
    )

    print("\n2. RIGHT sonrası:")
    print_probabilities(current_belief)


# ============================================================
# SECTION 6 - TRANSITION MATRIX
# Durum geçiş matrisi
# ============================================================

def show_transition_matrix():
    """
    RIGHT hareketinin geçiş matrisini oluşturur.

    Transition Matrix:
    Hareket modelindeki geçiş olasılıklarını
    matris biçiminde temsil eder.

    Bu matris, Belief Prediction işlemini
    matris çarpımıyla gerçekleştirmek
    için kullanılabilir.
    """
    print_section("6. TRANSITION MATRIX")

    action = "RIGHT"

    transition_matrix = create_transition_matrix(
        action
    )

    print("\nRIGHT geçiş matrisi:")

    for row in transition_matrix:
        print(row)


# ============================================================
# SECTION 7 - BELIEF UPDATE COMPARISON
# İnanç güncelleme yöntemlerinin karşılaştırılması
# ============================================================

def compare_belief_methods():
    """
    İki farklı Belief Prediction yöntemini karşılaştırır.

    Yöntem 1:
    Olasılıkları döngüler kullanarak hesaplar.

    Yöntem 2:
    Geçiş matrisi kullanarak hesaplar.

    Her iki yöntem de aynı hareket modelini
    kullandığından sonuçları eşit olmalıdır
    (küçük kayan nokta farkları hariç).
    """
    print_section("7. BELIEF UPDATE COMPARISON")

    belief = BeliefState(start_room="Office")

    initial_belief = belief.get_probabilities()

    action = "RIGHT"

    # Yöntem 1: Döngü tabanlı hesaplama.
    result_1 = predict_belief(
        initial_belief,
        action
    )

    # Yöntem 2: Matris tabanlı hesaplama.
    result_2 = predict_belief_with_matrix(
        initial_belief,
        action
    )

    print("\nDöngü yöntemi:")
    print_probabilities(result_1)

    print("\nMatris yöntemi:")
    print_probabilities(result_2)

    # Odalar bazında mutlak farkları hesapla.
    print("\nYöntemler arasındaki fark:")

    for room in ROOMS:
        difference = abs(
            result_1[room] - result_2[room]
        )

        print(f"{room}: {difference:.10f}")


# ============================================================
# SECTION 8 - MATRIX BELIEF PREDICTION
# Matris yöntemiyle ardışık inanç güncelleme
# ============================================================

def show_matrix_prediction():
    """
    Matris yöntemiyle iki hareket tahmini yapar.

    Her adımda:
    - Önceki inanç dağılımı alınır.
    - Hareketin geçiş modeli uygulanır.
    - Yeni inanç dağılımı hesaplanır.

    Hesaplanan dağılım sonraki adıma aktarılır.
    """
    print_section("8. MATRIX BELIEF PREDICTION")

    belief = BeliefState(start_room="Office")

    current_belief = belief.get_probabilities()

    print("\nBaşlangıç:")
    print_probabilities(current_belief)

    for step in range(2):
        current_belief = predict_belief_with_matrix(
            current_belief,
            "RIGHT"
        )

        print(f"\n{step + 1}. RIGHT sonrası:")
        print_probabilities(current_belief)


# ============================================================
# SECTION 9 - INTEGRATED ROBOT SIMULATION
# Birleşik robot simülasyonu
# ============================================================

def run_robot_simulation():
    """
    Gerçek robot hareketi ile Belief State
    güncellemesini birlikte gerçekleştirir.

    RobotSimulation.step(action):
    1. Gerçek hareket sonucunu örnekler.
    2. Robotun gerçek konumunu günceller.
    3. İnanç dağılımını günceller.
    4. Zaman adımını artırır.
    5. Sonuçları sözlük olarak döndürür.

    Gerçek konum ile inanç dağılımı
    birbirinden ayrı tutulur.
    """
    print_section("9. INTEGRATED ROBOT SIMULATION")

    simulation = RobotSimulation(
        start_room="Office"
    )

    print("\nBaşlangıç gerçek konumu:")
    print(simulation.robot.get_position())

    print("\nBaşlangıç inancı:")
    print_probabilities(simulation.current_belief)

    # Bir zaman adımı gerçekleştir.
    result = simulation.step("RIGHT")

    print("\nHareket sonucu:")

    print("Adım:", result["step"])
    print("Komut:", result["action"])
    print("Gerçek konum:", result["true_position"])

    print("\nGüncellenmiş inanç dağılımı:")
    print_probabilities(result["belief"])



# ============================================================
# SECTION 10 - CONSECUTIVE ROBOT SIMULATION
# Ardışık robot simülasyonu
# ============================================================

def run_consecutive_robot_simulation():
    """
    Robotun art arda iki hareket gerçekleştirmesini simüle eder.

    Bu fonksiyon:
    1. Robotu Office odasında başlatır.
    2. İlk RIGHT hareketini gerçekleştirir.
    3. İkinci RIGHT hareketini gerçekleştirir.
    4. Her hareketin gerçek sonucunu gösterir.
    5. İkinci hareket sonrası inanç dağılımını gösterir.
    6. Toplam zaman adımını gösterir.

    Önemli:
    Her hareket, bir önceki hareketin sonucundan başlar.

    Gerçek konum:
    Olasılıksal hareket modelinden örneklenerek belirlenir.

    Belief State:
    Tüm olası hareket sonuçları dikkate alınarak
    hesaplanır.

    Böylece gerçek konum ile inanç dağılımının
    zaman içerisinde nasıl değiştiğini gözlemleriz.
    """

    print_section("10. CONSECUTIVE ROBOT SIMULATION")

    # 1. SİMÜLASYONU BAŞLAT
    # Robotun gerçek başlangıç konumu Office'dir.
    # Başlangıç inancı da robotun Office'de
    # bulunduğunu kesin olarak kabul eder.
    simulation = RobotSimulation(start_room="Office")

    print("\nBaşlangıç konumu:")
    print(simulation.robot.get_position())

    print("\nBaşlangıç inanç dağılımı:")
    print_probabilities(simulation.current_belief)

    # 2. BİRİNCİ RIGHT HAREKETİ
    # Robot olasılıksal olarak hareket eder.
    # Gerçek konum ve inanç dağılımı güncellenir.
    # Zaman adımı 0'dan 1'e ilerler.
    result_1 = simulation.step("RIGHT")

    # 3. İKİNCİ RIGHT HAREKETİ
    # Robot ilk hareketten sonraki gerçek
    # konumundan hareket etmeye çalışır.
    #
    # İnanç dağılımı da ilk hareketten sonraki
    # dağılım kullanılarak yeniden hesaplanır.
    #
    # Zaman adımı 1'den 2'ye ilerler.
    result_2 = simulation.step("RIGHT")

    # 4. GERÇEK HAREKET SONUÇLARINI GÖSTER
    # Her hareketten sonra gerçekleşen
    # gerçek konumları ekrana yazdırırız.
    print("\nİki ardışık RIGHT hareketi:")

    print(
        "1. hareket gerçek konum:",
        result_1["true_position"]
    )

    print(
        "2. hareket gerçek konum:",
        result_2["true_position"]
    )

    # 5. İKİNCİ HAREKET SONRASI BELIEF STATE
    # İkinci hareketin ardından robotun
    # her odada bulunma olasılığını gösterir.
    #
    # Buradaki olasılıklar yalnızca gerçek
    # hareket sonucuna göre hesaplanmaz.
    #
    # Önceki inanç dağılımı ve hareket
    # modeli kullanılarak hesaplanır.
    print("\nİkinci hareket sonrası inanç:")

    print_probabilities(result_2["belief"])

    # 6. TOPLAM ZAMAN ADIMINI GÖSTER
    # İki hareket komutu gerçekleştirildiği
    # için step_count değeri 2 olacaktır.
    #
    # Robot herhangi bir harekette aynı odada
    # kalsa bile zaman adımı ilerler.
    print("\nToplam adım:", result_2["step"])



# ============================================================
# SECTION 11 - ROBOT MOVEMENT HISTORY
# Robotun hareket geçmişini kaydetme
# ============================================================

def show_movement_history():
    """
    Robotun gerçekleştirdiği hareketlerin geçmişini gösterir.

    Bu fonksiyon:
    1. Robot simülasyonunu başlatır.
    2. Birden fazla hareket gerçekleştirir.
    3. Her hareketin sonucunu geçmişe kaydeder.
    4. Hareket geçmişini get_history() ile okur.
    5. Her adımın komutunu, gerçek konumunu
       ve inanç dağılımını ekrana yazdırır.

    Böylece robotun zaman içerisindeki
    gerçek ve tahmin edilen durumlarını
    karşılaştırabiliriz.
    """

    print_section("11. ROBOT MOVEMENT HISTORY")

    # 1. ROBOT SİMÜLASYONUNU BAŞLAT
    # Başlangıç durumu otomatik olarak
    # history listesine kaydedilir.
    simulation = RobotSimulation(
        start_room="Office"
    )

    # 2. HAREKET KOMUTLARINI TANIMLA
    # Robotun sırayla gerçekleştireceği
    # komutları bir liste içerisinde tutarız.
    actions = ["RIGHT", "RIGHT"]

    # 3. HAREKETLERİ GERÇEKLEŞTİR
    # Her step() çağrısı:
    # - Gerçek konumu günceller.
    # - İnanç dağılımını günceller.
    # - Zaman adımını artırır.
    # - Sonucu history listesine kaydeder.
    for action in actions:
        simulation.step(action)

    # 4. HAREKET GEÇMİŞİNİ AL
    # get_history() geçmişin bağımsız
    # bir kopyasını döndürür.
    history = simulation.get_history()

    # 5. GEÇMİŞTEKİ TÜM KAYITLARI GÖSTER
    # İlk kayıt başlangıç durumudur (step = 0).
    # Sonraki kayıtlar gerçekleştirilen hareketlerdir.
    print("\nRobotun hareket geçmişi:")

    for record in history:

        print("\n------------------------------")

        print("Adım:", record["step"])
        print("Komut:", record["action"])
        print("Gerçek konum:", record["true_position"])

        print("\nİnanç dağılımı:")

        print_probabilities(record["belief"])

    # 6. TOPLAM HAREKET SAYISINI GÖSTER
    # Başlangıç kaydı hareket sayısına dahil değildir.
    print("\nToplam hareket:", simulation.step_count)

    # 7. TOPLAM KAYIT SAYISINI GÖSTER
    # Başlangıç kaydı da geçmişte tutulduğu için:
    #
    # Kayıt sayısı = Hareket sayısı + 1
    print("Toplam kayıt:", len(history))



# ============================================================
# SECTION 12 - BELIEF HISTORY VISUALIZATION
# İnanç geçmişinin grafikle görselleştirilmesi
# ============================================================

def show_belief_history_plot():
    """
    Robotun hareketleri boyunca inanç dağılımının
    nasıl değiştiğini grafik üzerinde gösterir.

    Bu fonksiyon:
    1. Robot simülasyonunu oluşturur.
    2. Ardışık hareket komutlarını gerçekleştirir.
    3. Hareket geçmişini alır.
    4. İnanç dağılımlarını grafikle gösterir.

    Böylece her odanın olasılığının zaman
    içerisinde nasıl değiştiğini gözlemleyebiliriz.
    """

    print_section("12. BELIEF HISTORY VISUALIZATION")

    # 1. ROBOT SİMÜLASYONUNU BAŞLAT
    # Robot Office odasında başlar.
    simulation = RobotSimulation(
        start_room="Office"
    )

    # 2. HAREKET DİZİSİNİ TANIMLA
    # Robot art arda üç RIGHT komutu alacaktır.
    actions = ["RIGHT", "RIGHT", "RIGHT"]

    # 3. HAREKETLERİ GERÇEKLEŞTİR
    # Her hareket:
    # - Gerçek konumu günceller.
    # - İnanç dağılımını günceller.
    # - Hareket geçmişine kaydedilir.
    for action in actions:
        simulation.step(action)


    # ========================================================
    # 4. GET MOVEMENT HISTORY
    # Hareket geçmişini alma
    # ========================================================

    # Başlangıç durumu ve hareket kayıtlarını al.
    history = simulation.get_history()

    # ========================================================
    # 5. CREATE BELIEF HISTORY FIGURE
    # İnanç geçmişi grafiğini oluşturma
    # ========================================================

    # plot_belief_history() grafik nesnesini oluşturur.
    # Ancak grafik penceresini açmaz.
    fig = plot_belief_history(history)

    # ========================================================
    # 6. SAVE BELIEF HISTORY FIGURE
    # İnanç grafiğini PNG olarak kaydetme
    # ========================================================

    # Oluşturulan grafiği belirtilen dosyaya kaydet.
    #
    # Klasör mevcut değilse save_belief_plot()
    # fonksiyonu tarafından oluşturulur.
    saved_path = save_belief_plot(
        fig,
        "robot_lab/experiments/results/belief_history.png"
    )

    # Kaydedilen dosyanın yolunu göster.
    print("\nGrafik kaydedildi:", saved_path)

    # ========================================================
    # 7. DISPLAY BELIEF HISTORY FIGURE
    # İnanç grafiğini ekranda gösterme
    # ========================================================

    # Grafik penceresini açmayı dener.
    # Etkileşimli backend kullanılmıyorsa
    # pencere açılmayabilir.
    plt.show()





# ============================================================
# SECTION 13 - SIMULATION HISTORY CSV EXPORT
# Simülasyon geçmişini CSV dosyasına aktarma
# ============================================================

def show_simulation_history_csv_export():
    """
    Robotun hareket geçmişini CSV dosyasına kaydeder.

    Bu fonksiyon:
    1. Yeni bir RobotSimulation nesnesi oluşturur.
    2. Robotu Office odasında başlatır.
    3. Ardışık hareket komutlarını gerçekleştirir.
    4. Hareket geçmişini alır.
    5. Geçmiş kayıtlarını CSV dosyasına aktarır.
    6. Kaydedilen dosyanın yolunu gösterir.
    7. Toplam hareket ve kayıt sayılarını gösterir.

    Bu işlem diğer simülasyon deneylerinden
    bağımsız olarak gerçekleştirilir.
    """

    print_section("13. SIMULATION HISTORY CSV EXPORT")

    # ========================================================
    # 1. CREATE ROBOT SIMULATION
    # Robot simülasyonunu oluşturma
    # ========================================================

    # Yeni bir RobotSimulation nesnesi oluştururuz.
    #
    # Böylece önceki deneylerin hareketleri
    # bu simülasyonu etkilemez.
    simulation = RobotSimulation(
        start_room="Office"
    )

    # ========================================================
    # 2. DEFINE MOVEMENT SEQUENCE
    # Hareket komutlarını tanımlama
    # ========================================================

    # Robotun gerçekleştireceği hareketleri
    # sıralı bir liste içerisinde tutarız.
    #
    # Bu örnekte üç hareket gerçekleştirilecek.
    actions = [
        "RIGHT",
        "RIGHT",
        "UP"
    ]

    # ========================================================
    # 3. EXECUTE MOVEMENTS
    # Hareketleri gerçekleştirme
    # ========================================================

    # Listedeki hareket komutlarını sırayla uygularız.
    #
    # Her step() çağrısı:
    # - Gerçek konumu günceller.
    # - İnanç dağılımını günceller.
    # - Zaman adımını artırır.
    # - Hareket geçmişine kayıt ekler.
    for action in actions:

        simulation.step(action)

    # ========================================================
    # 4. GET SIMULATION HISTORY
    # Simülasyon geçmişini alma
    # ========================================================

    # get_history():
    # Başlangıç durumu ve bütün hareket
    # kayıtlarının bağımsız kopyalarını döndürür.
    history = simulation.get_history()

    # ========================================================
    # 5. EXPORT HISTORY TO CSV
    # Hareket geçmişini CSV dosyasına kaydetme
    # ========================================================

    # export_history_to_csv():
    # Hareket geçmişini tablo biçiminde
    # belirtilen CSV dosyasına kaydeder.
    #
    # Kayıt klasörü yoksa otomatik oluşturulur.
    csv_path = export_history_to_csv(
        history,
        "robot_lab/experiments/results/simulation_history.csv"
    )

    # ========================================================
    # 6. DISPLAY EXPORT RESULT
    # CSV kaydetme sonucunu gösterme
    # ========================================================

    # Kaydedilen dosyanın yolunu ekrana yazdır.
    print("\nCSV dosyası kaydedildi:", csv_path)

    # ========================================================
    # 7. DISPLAY MOVEMENT COUNT
    # Toplam hareket sayısını gösterme
    # ========================================================

    # step_count:
    # Gerçekleştirilen hareket komutlarının sayısı.
    #
    # Bu örnekte:
    # 3 hareket gerçekleştirildi.
    print(
        "Toplam hareket:",
        simulation.step_count
    )

    # ========================================================
    # 8. DISPLAY RECORD COUNT
    # Geçmiş kayıt sayısını gösterme
    # ========================================================

    # Hareket geçmişi başlangıç durumunu da içerir.
    #
    # Kayıt sayısı = Hareket sayısı + 1
    #
    # Bu örnekte:
    # 3 hareket + 1 başlangıç = 4 kayıt
    print(
        "Geçmiş kayıt sayısı:",
        len(history)
    )



# ============================================================
# SECTION 14 - AUTOMATIC EXPERIMENT REPORT
# Otomatik deney raporu oluşturma
# ============================================================

def show_automatic_experiment_report():
    """
    Robot deneyinin otomatik Markdown raporunu oluşturur.

    Bu fonksiyon:
    1. Yeni bir robot simülasyonu oluşturur.
    2. Robotu Office odasında başlatır.
    3. Ardışık hareket komutlarını gerçekleştirir.
    4. Hareket geçmişini alır.
    5. Deney geçmişinden Markdown raporu oluşturur.
    6. Kaydedilen raporun yolunu gösterir.

    Her rapor deneyi bağımsız bir simülasyon
    üzerinden gerçekleştirilir.
    """

    print_section("14. AUTOMATIC EXPERIMENT REPORT")

    # ========================================================
    # 1. CREATE ROBOT SIMULATION
    # Robot simülasyonunu oluşturma
    # ========================================================

    # Yeni simülasyon oluştururuz.
    #
    # Böylece önceki deneylerin hareketleri
    # rapor sonuçlarını etkilemez.
    simulation = RobotSimulation(
        start_room="Office"
    )

    # ========================================================
    # 2. DEFINE MOVEMENT COMMANDS
    # Hareket komutlarını tanımlama
    # ========================================================

    # Robotun gerçekleştireceği hareket dizisi.
    actions = [
        "RIGHT",
        "RIGHT",
        "UP"
    ]

    # ========================================================
    # 3. EXECUTE MOVEMENTS
    # Hareketleri gerçekleştirme
    # ========================================================

    # Her hareket komutunu sırayla uygularız.
    #
    # step():
    # - Gerçek konumu günceller.
    # - İnanç dağılımını günceller.
    # - Zaman adımını artırır.
    # - Hareket sonucunu geçmişe kaydeder.
    for action in actions:

        simulation.step(action)

    # ========================================================
    # 4. GET EXPERIMENT HISTORY
    # Deney geçmişini alma
    # ========================================================

    # Başlangıç kaydı ve bütün hareketleri al.
    #
    # Başlangıç + 3 hareket = 4 kayıt.
    history = simulation.get_history()

    # ========================================================
    # 5. GENERATE MARKDOWN REPORT
    # Markdown deney raporunu oluşturma
    # ========================================================

    # generate_experiment_report():
    # Hareket geçmişini Markdown biçiminde
    # rapor dosyasına dönüştürür.
    report_path = generate_experiment_report(
        history,
        "robot_lab/experiments/results/experiment_001.md"
    )

    # ========================================================
    # 6. DISPLAY REPORT RESULT
    # Rapor oluşturma sonucunu gösterme
    # ========================================================

    print("\nDeney raporu kaydedildi:", report_path)

    # Toplam hareket sayısını göster.
    print(
        "Toplam hareket:",
        simulation.step_count
    )

    # Başlangıç kaydı dahil toplam kayıt sayısı.
    print(
        "Rapordaki kayıt sayısı:",
        len(history)
    )


# ============================================================
# SECTION 15 - INTEGRATED EXPERIMENT
# Bütünleşik robot deneyi
# ============================================================

def show_integrated_experiment():
    """
    Bütünleşik bir robot deneyini gerçekleştirir.

    Bu fonksiyon:
    1. Hareket dizisini belirler.
    2. run_experiment() fonksiyonunu çağırır.
    3. Tek simülasyondan PNG, CSV ve Markdown üretir.
    4. Kaydedilen dosyaların yollarını gösterir.
    5. Deneyin gerçek konum geçmişini gösterir.

    Deney:
        Başlangıç: Office
        Komutlar: RIGHT -> RIGHT -> UP

    Amaç:
        Tek bir deneyin bütün çıktılarını
        aynı hareket geçmişinden oluşturmak.
    """

    print_section("15. INTEGRATED EXPERIMENT")

    # ========================================================
    # 1. DEFINE EXPERIMENT ACTIONS
    # Deneyde kullanılacak hareketleri belirleme
    # ========================================================

    # Robotun sırasıyla gerçekleştireceği komutlar.
    actions = [
        "RIGHT",
        "RIGHT",
        "UP"
    ]

    # ========================================================
    # 2. RUN INTEGRATED EXPERIMENT
    # Bütünleşik deneyi gerçekleştirme
    # ========================================================

    # run_experiment():
    # Tek bir simülasyon oluşturur.
    #
    # Hareketleri sırayla gerçekleştirir.
    #
    # Aynı geçmişten:
    # - PNG grafiği
    # - CSV tablosu
    # - Markdown raporu
    # üretir.
    experiment_result = run_experiment(
        actions,
        "robot_lab/experiments/results/integrated_experiment"
    )

    # ========================================================
    # 3. DISPLAY OUTPUT FILE PATHS
    # Oluşturulan dosyaların yollarını gösterme
    # ========================================================

    print("\nDeney sonuç dosyaları:")

    print(
        "PNG:",
        experiment_result["png_path"]
    )

    print(
        "CSV:",
        experiment_result["csv_path"]
    )

    print(
        "Rapor:",
        experiment_result["report_path"]
    )

    # ========================================================
    # 4. GET EXPERIMENT HISTORY
    # Deneyin hareket geçmişini alma
    # ========================================================

    # run_experiment() tarafından döndürülen
    # geçmiş kayıtlarını alırız.
    history = experiment_result["history"]

    # Başlangıç + 3 hareket = 4 kayıt.
    print(
        "\nToplam geçmiş kaydı:",
        len(history)
    )

    # ========================================================
    # 5. DISPLAY TRUE POSITION HISTORY
    # Robotun gerçek konum geçmişini gösterme
    # ========================================================

    # Geçmişteki bütün zaman adımlarını dolaşırız.
    #
    # Gerçek konumlar olasılıksal hareket
    # modeline göre değişebilir.
    print("\nDeneyin gerçek konum geçmişi:")

    for record in history:

        # Her satırda:
        # - Zaman adımı
        # - Hareket komutu
        # - Gerçek robot konumu
        # gösterilir.
        print(
            "Adım", record["step"],
            "-", record["action"],
            "-", record["true_position"]
        )

    # ========================================================
    # 6. DISPLAY FINAL BELIEF STATE
    # Deneyin son inanç dağılımını gösterme
    # ========================================================

    # history[-1]:
    # Deneyin son hareket kaydını temsil eder.
    final_record = history[-1]

    print("\nSon inanç dağılımı:")

    # Daha önce oluşturduğumuz yardımcı fonksiyon.
    print_probabilities(
        final_record["belief"]
    )








# ============================================================
# MAIN - Ana program
# ============================================================

def main():
    """
    Robot Intelligence Lab ana programı.
    """

    print("Robot Intelligence Lab")
    print("Robot simülasyon sistemi başlatıldı.")

    # 1. Robotun bulunduğu dünya
    show_world()

    # 2. Kesin hareket modeli
    show_deterministic_motion()

    # 3. Olasılıksal hareket modeli
    show_probabilistic_motion()

    # 4. Olasılıksal hareket örnekleme
    show_motion_sampling()

    # 5. İnanç durumu güncelleme
    show_belief_prediction()

    # 6. Durum geçiş matrisi
    show_transition_matrix()

    # 7. İnanç güncelleme yöntemlerini karşılaştırma
    compare_belief_methods()

    # 8. Matris tabanlı ardışık tahmin
    show_matrix_prediction()

    # 9. Birleşik robot simülasyonu
    run_robot_simulation()

    # 10. Ardışık robot simülasyonu
    run_consecutive_robot_simulation()

    # 11. Robotun hareket geçmişini göster
    show_movement_history()

    # 12. İnanç geçmişini grafikle göster
    show_belief_history_plot()

    # 13. Simülasyon geçmişini CSV dosyasına aktar
    show_simulation_history_csv_export()

    # 14. Otomatik Markdown deney raporu oluştur
    show_automatic_experiment_report()

    # 15. Bütünleşik robot deneyini çalıştır
    show_integrated_experiment()

if __name__ == "__main__":
    main()