#include <FastLED.h>

#define NUM_LEDS 10
CRGB leds1[NUM_LEDS];
CRGB leds2[NUM_LEDS];
CRGB leds3[NUM_LEDS];
CRGB leds4[NUM_LEDS];
CRGB leds5[NUM_LEDS];

#define led_pini_1 13
#define led_pini_2 12
#define led_pini_3 11
#define led_pini_4 10
#define led_pini_5 9

int counter = 0;
int serit_no;
int serit_uzunluk;
int renk;
int serit_array[150][4];
int i = 0;

void setup() {
  
  randomSeed(analogRead(0));
  Serial.begin(9600);
  FastLED.addLeds<WS2812B, led_pini_1, GRB>(leds1, NUM_LEDS);
  FastLED.addLeds<WS2812B, led_pini_2, GRB>(leds2, NUM_LEDS);
  FastLED.addLeds<WS2812B, led_pini_3, GRB>(leds3, NUM_LEDS);
  FastLED.addLeds<WS2812B, led_pini_4, GRB>(leds4, NUM_LEDS);
  FastLED.addLeds<WS2812B, led_pini_5, GRB>(leds5, NUM_LEDS);
}

void loop() {
  if(counter % 3 == 0){
    serit_no = random(1,6);
    serit_uzunluk = random(1, 5);
    renk = random(1, 3);  // 1 kırmızı 2 yeşil
    while(serit_array[i-1][0] == serit_no)
      serit_no = random(1,6);
    serit_array[i][0] = serit_no;
    serit_array[i][1] = serit_uzunluk;
    serit_array[i][2] = renk;
    serit_array[i][3] = 1;  //her bir şeridin tur sayısı
    i++;
  }

    for (int k = 0; k < 100; k++) {
      if (serit_array[k][1] != 0) {  // şerit var mı yok mu kontrol
        switch (serit_array[k][0]) {
          case 1:
            if (serit_array[k][1] >= serit_array[k][3]) { // uzunluk turundan fazlaysa 
              if (serit_array[k][2] == 2) {  // 2 YEŞİL
                leds1[serit_array[k][3] - 1].setRGB(0, 255, 0);
              } else if (serit_array[k][2] == 1) {  // 1 KIRMIZI
                leds1[serit_array[k][3] - 1].setRGB(255, 0, 0);
              }
              serit_array[k][3] += 1;
            } else {
              int altdeger1 = serit_array[k][3] - serit_array[k][1];
              int ustdeger1 = serit_array[k][3] - 1;
              leds1[altdeger1 - 1].setRGB(0, 0, 0);
              for (int i = 0; i < 10; i++) {
                if ((i >= altdeger1) && (i <= ustdeger1)){
                    if (serit_array[k][2] == 2) {  // 2 YEŞİL
                      leds1[i].setRGB(0, 255, 0);
                    } else if (serit_array[k][2] == 1) {  // 1 KIRMIZI
                      leds1[i].setRGB(255, 0, 0);
                    }
                }
              }
              serit_array[k][3] += 1;              
            }
            break;
          case 2:
            if (serit_array[k][1] >= serit_array[k][3]) {
              if (serit_array[k][2] == 2) {  // 2 YEŞİL
                leds2[serit_array[k][3] - 1].setRGB(0, 255, 0);
              } else if (serit_array[k][2] == 1) {  // 1 KIRMIZI
                leds2[serit_array[k][3] - 1].setRGB(255, 0, 0);
              }
              serit_array[k][3] += 1;
            } else {
              int altdeger2 = serit_array[k][3] - serit_array[k][1];
              int ustdeger2 = serit_array[k][3] - 1;
              leds2[altdeger2 - 1].setRGB(0, 0, 0);
            
              for (int i = 0; i < 10; i++) {
                if ((i >= altdeger2) && (i <=ustdeger2)){
                    if (serit_array[k][2] == 2) {  // 2 YEŞİL
                      leds2[i].setRGB(0, 255, 0);
                    } else if (serit_array[k][2] == 1) {  // 1 KIRMIZI
                      leds2[i].setRGB(255, 0, 0);
                    }
                }  
              }
              serit_array[k][3] += 1;
            }              
            break;
          case 3:
            if (serit_array[k][1] >= serit_array[k][3]) {
              if (serit_array[k][2] == 2) {  // 2 YEŞİL
                leds3[serit_array[k][3] - 1].setRGB(0, 255, 0);
              } else if (serit_array[k][2] == 1) {  // 1 KIRMIZI
                leds3[serit_array[k][3] - 1].setRGB(255, 0, 0);
              }
              serit_array[k][3] += 1;
            } else {
              int altdeger3 = serit_array[k][3] - serit_array[k][1];
              int ustdeger3 = serit_array[k][3] - 1;
              leds3[altdeger3 - 1].setRGB(0, 0, 0);
              for (int i = 0; i < 10; i++) {
                if ((i >= altdeger3) && (i <=ustdeger3)){
                    if (serit_array[k][2] == 2) {  // 2 YEŞİL
                      leds3[i].setRGB(0, 255, 0);
                    } else if (serit_array[k][2] == 1) {  // 1 KIRMIZI
                      leds3[i].setRGB(255, 0, 0);
                    }
                }
              }
              serit_array[k][3] += 1;              
            }
            break;
          case 4:
            if (serit_array[k][1] >= serit_array[k][3]) {
              if (serit_array[k][2] == 2) {  // 2 YEŞİL
                leds4[serit_array[k][3] - 1].setRGB(0, 255, 0);
              } else if (serit_array[k][2] == 1) {  // 1 KIRMIZI
                leds4[serit_array[k][3] - 1].setRGB(255, 0, 0);
              }
              serit_array[k][3] += 1;
            } else {
              int altdeger4 = serit_array[k][3] - serit_array[k][1];
              int ustdeger4 = serit_array[k][3] - 1;
              leds4[altdeger4 - 1].setRGB(0, 0, 0);
              for (int i = 0; i < 10; i++) {
                if ((i >= altdeger4) && (i <=ustdeger4)){
                    if (serit_array[k][2] == 2) {  // 2 YEŞİL
                      leds4[i].setRGB(0, 255, 0);
                    } else if (serit_array[k][2] == 1) {  // 1 KIRMIZI
                      leds4[i].setRGB(255, 0, 0);
                    }
                }
              }
              serit_array[k][3] += 1;              
            }
            break;
          case 5:
            if (serit_array[k][1] >= serit_array[k][3]) {
              if (serit_array[k][2] == 2) {  // 2 YEŞİL
                leds5[serit_array[k][3] - 1].setRGB(0, 255, 0);
              } else if (serit_array[k][2] == 1) {  // 1 KIRMIZI
                leds5[serit_array[k][3] - 1].setRGB(255, 0, 0);
              }
              serit_array[k][3] += 1;
            } else {
              int altdeger5 = serit_array[k][3] - serit_array[k][1];
              int ustdeger5 = serit_array[k][3] - 1;
              leds5[altdeger5 - 1].setRGB(0, 0, 0);
              for (int i = 0; i < 10; i++) {
                if ((i >= altdeger5) && (i <=ustdeger5)){
                    if (serit_array[k][2] == 2) {  // 2 YEŞİL
                      leds5[i].setRGB(0, 255, 0);
                    } else if (serit_array[k][2] == 1) {  // 1 KIRMIZI
                      leds5[i].setRGB(255, 0, 0);
                    }
                }
              }
              serit_array[k][3] += 1;              
            }
            break;
          default:
            break;
        }
      }
    }

  FastLED.show();
  delay(1000);
  counter++;
}
