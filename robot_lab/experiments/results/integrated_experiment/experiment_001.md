# Robot Intelligence Lab - Deney 001

## Deney Amacı

Olasılıksal robot hareketlerini ve Markov inanç dağılımlarını incelemek.

## Başlangıç Koşulları

Başlangıç odası: Office

## Hareket Komutları

RIGHT → RIGHT → UP

## Deney Sonuçları

| Adım | Komut | Gerçek Konum |
|---|---|---|
| 0 | START | Office |
| 1 | RIGHT | Hallway |
| 2 | RIGHT | Dining Room |
| 3 | UP | Kitchen |

## Son İnanç Dağılımı

- Living Room: 0.2560
- Kitchen: 0.5120
- Office: 0.0400
- Hallway: 0.0640
- Dining Room: 0.1280

## Değerlendirme

Toplam 3 hareket gerçekleştirildi.

Son gerçek konum: Kitchen

En yüksek olasılığa sahip oda: Kitchen (0.5120)

Son inanç dağılımının toplamı: 1.0000

İnanç dağılımı, robotun hangi odada bulunabileceğini olasılıksal olarak temsil eder.

Gerçek konum, hareket modelinden örneklenirken inanç dağılımı bütün olası hareket sonuçları dikkate alınarak hesaplanır.
