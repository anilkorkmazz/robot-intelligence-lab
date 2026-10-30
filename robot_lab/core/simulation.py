
# ============================================================
# IMPORTS - Gerekli modüller
# ============================================================

from robot_lab.core.robot import Robot
from robot_lab.belief.belief_state import BeliefState
from robot_lab.belief.belief_update import predict_belief
from robot_lab.motion.actions import ACTIONS


# ============================================================
# ROBOT SIMULATION
# Robot simülasyonunu yöneten sınıf
# ============================================================

class RobotSimulation:
    """
    Robotun gerçek hareketlerini ve inanç durumunu yönetir.

    Bu sınıf:
    1. Robotun gerçek konumunu takip eder.
    2. İnanç dağılımını (Belief State) saklar.
    3. Gerçekleştirilen hareket sayısını takip eder.
    4. Başlangıç durumunu ve hareket geçmişini kaydeder.
    5. Kayıtlı hareket geçmişinin güvenli kopyasını döndürür.

    Gerçek konum ile inanç durumu birbirinden
    bağımsız olarak güncellenir.
    """

    # ========================================================
    # SECTION 1 - INITIALIZATION
    # Simülasyonun başlangıç durumunu oluşturma
    # ========================================================

    def __init__(self, start_room="Office"):
        """
        Robot simülasyonunu başlatır.

        Args:
            start_room (str):
                Robotun başlangıç odası.
                Varsayılan değer "Office".

        Başlangıçta:
        - Robot belirtilen odada bulunur.
        - Başlangıç inancı kesin olarak bilinir.
        - Hareket sayacı sıfırdır.
        - Hareket geçmişi oluşturulur.
        - Başlangıç durumu geçmişe kaydedilir.
        """

        # 1. GERÇEK ROBOTU OLUŞTUR
        # Robot nesnesi gerçek konumu saklar.
        self.robot = Robot(start_room=start_room)

        # 2. BAŞLANGIÇ İNANCINI OLUŞTUR
        # Başlangıçta robotun hangi odada olduğu
        # kesin olarak bilinmektedir.
        #
        # Örneğin:
        # P(Office) = 1.0
        belief = BeliefState(start_room=start_room)

        # 3. İNANÇ DAĞILIMINI SAKLA
        # Olasılık dağılımını simülasyonun
        # güncel inanç durumu olarak saklarız.
        self.current_belief = belief.get_probabilities()

        # 4. ZAMAN ADIMINI SIFIRLA
        # Henüz hiçbir hareket gerçekleştirilmemiştir.
        #
        # t = 0 -> Başlangıç durumu
        self.step_count = 0

        # 5. HAREKET GEÇMİŞİNİ OLUŞTUR
        # Her hareketin sonucu bu listede saklanır.
        #
        # Liste içerisinde her hareket için
        # ayrı bir sözlük (dict) bulunacaktır.
        self.history = []

        # 6. BAŞLANGIÇ DURUMUNU KAYDET
        # Robot hareket etmeden önceki durumu
        # başlangıç kaydı olarak oluştururuz.
        #
        # step = 0:
        # Henüz hareket gerçekleşmedi.
        #
        # action = START:
        # Bu kayıt bir hareket değil,
        # simülasyonun başlangıç durumudur.
        initial_record = {
            "step": 0,
            "action": "START",
            "true_position": self.robot.get_position(),
            "belief": self.current_belief.copy()
        }

        # 7. BAŞLANGIÇ KAYDINI GEÇMİŞE EKLE
        # append() listeye yeni bir eleman ekler.
        #
        # history[0] artık başlangıç durumunu tutar.
        self.history.append(initial_record)

    # ========================================================
    # SECTION 2 - SIMULATION STEP
    # Bir hareket gerçekleştirme ve sonucu kaydetme
    # ========================================================

    def step(self, action):
        """
        Robot simülasyonunda bir zaman adımı gerçekleştirir.

        İşlem sırası:
        1. Hareket komutunun geçerliliğini kontrol eder.
        2. Robotun gerçek hareket sonucunu örnekler.
        3. Gerçek konumu günceller.
        4. İnanç dağılımını günceller.
        5. Zaman adımını artırır.
        6. Hareket sonucunu geçmişe kaydeder.
        7. Sonuç sözlüğünü döndürür.

        Args:
            action (str):
                Robota verilen hareket komutu.

        Returns:
            dict:
                Hareketin adım numarası, komutu,
                gerçek konumu ve inanç dağılımı.

        Raises:
            ValueError:
                Geçersiz hareket komutu verildiğinde.
        """

        # 1. HAREKET KOMUTUNU DOĞRULA
        # Geçersiz komutlar herhangi bir durum
        # güncellemesinden önce reddedilir.
        #
        # Örneğin "JUMP" geçerli değilse
        # ValueError hatası oluşturulur.
        if action not in ACTIONS:
            raise ValueError(
                f"Geçersiz hareket komutu: {action}"
            )

        # 2. ROBOTUN GERÇEK KONUMUNU GÜNCELLE
        # Verilen hareket komutunun olası
        # sonuçlarından biri rastgele örneklenir.
        #
        # Örnek:
        # Office -> Hallway : %80
        # Office -> Office  : %20
        #
        # Yalnızca bir gerçek sonuç gerçekleşir.
        new_position = self.robot.move_probabilistic(
            action
        )

        # 3. İNANÇ DAĞILIMINI GÜNCELLE
        # Önceki inanç dağılımı ve hareket modeli
        # kullanılarak yeni dağılım hesaplanır.
        #
        # Gerçek konum doğrudan kullanılmaz.
        # Tüm olası hareket sonuçları dikkate alınır.
        self.current_belief = predict_belief(
            self.current_belief,
            action
        )

        # 4. ZAMAN ADIMINI ARTIR
        # Robot aynı odada kalsa bile geçerli bir
        # hareket komutu gerçekleştiği için
        # zaman adımı ilerler.
        #
        # t = 0 -> t = 1 -> t = 2 -> ...
        self.step_count += 1

        # 5. HAREKET KAYDINI OLUŞTUR
        # Hareket sonucunu bir sözlükte toplarız.
        #
        # belief.copy():
        # Güncel inanç dağılımının o andaki
        # değerlerini ayrı bir sözlükte saklar.
        record = {
            "step": self.step_count,
            "action": action,
            "true_position": new_position,
            "belief": self.current_belief.copy()
        }

        # 6. KAYDI HAREKET GEÇMİŞİNE EKLE
        # Yeni kayıt history listesinin sonuna eklenir.
        #
        # Örneğin:
        # history[0] -> Başlangıç
        # history[1] -> Birinci hareket
        # history[2] -> İkinci hareket
        self.history.append(record)

        # 7. SONUCU DÖNDÜR
        # Önceki aşamalardaki kullanım korunur.
        #
        # result = simulation.step("RIGHT")
        return record

    # ========================================================
    # SECTION 3 - MOVEMENT HISTORY
    # Hareket geçmişini güvenli şekilde okuma
    # ========================================================

    def get_history(self):
        """
        Robotun kayıtlı hareket geçmişini döndürür.

        Hareket geçmişi:
        - Başlangıç durumunu içerir.
        - Her hareketin komutunu içerir.
        - Her hareket sonrası gerçek konumu içerir.
        - Her adımdaki inanç dağılımını içerir.

        Kayıtlar kopyalanarak döndürülür.

        Böylece get_history() sonucunda yapılan
        değişiklikler simülasyonun kendi geçmişini
        etkilemez.

        Returns:
            list:
                Hareket kayıtlarının bağımsız kopyaları.
        """

        # 1. BOŞ BİR GEÇMİŞ LİSTESİ OLUŞTUR
        # Orijinal self.history listesi değiştirilmez.
        history_copy = []

        # 2. TÜM KAYITLARI DOLAŞ
        # Her kayıt bir sözlüktür.
        for record in self.history:

            # 3. KAYIT SÖZLÜĞÜNÜ KOPYALA
            # record.copy() dış sözlüğü kopyalar.
            #
            # Ancak sözlük içerisindeki belief
            # sözlüğü henüz ortak referanstır.
            copied_record = record.copy()

            # 4. İÇTEKİ BELIEF SÖZLÜĞÜNÜ KOPYALA
            # İç içe bulunan olasılık dağılımını
            # ayrıca kopyalayarak bağımsızlaştırırız.
            copied_record["belief"] = (
                record["belief"].copy()
            )

            # 5. KOPYALANMIŞ KAYDI LİSTEYE EKLE
            history_copy.append(copied_record)

        # 6. KOPYALANMIŞ GEÇMİŞİ DÖNDÜR
        # Dışarıdan yapılan değişiklikler
        # orijinal history kayıtlarını etkilemez.
        return history_copy
