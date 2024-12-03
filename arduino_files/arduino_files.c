#include "driver/i2s.h"
#include "driver/adc.h"

#define PLAYBACK_PIN 15
#define SKIP_PIN 16
#define TEMPO_PIN 11
#define AUDIOIN_PIN 32
#define AUDIOOUT_PIN 33
#define SWOUT_PIN 34
#define SWIN_PIN 35
#define INPUT_WAVE 35
#define OUTPUT_WAVE 38

#define DEBOUNCE_TIME 250

#define PROCESS 0
#define HOLD 1
#define SKIP 2

#define ADC_PIN 34
#define DAC_PIN 25
#define SAMPLE_RATE 44100
#define I2S_DMA_BUF_COUNT 8
#define I2S_DMA_BUF_LEN  1024

#define BUFFER_SIZE 512

volatile int skipPressed = 0;
volatile int playbackPressed = 0;

unsigned long playbackPressTime = 0;
unsigned long skipPressTime = 0;

volatile int STATE = PROCESS;
volatile int nextSTATE = PROCESS;

int16_t audioBuffer[BUFFER_SIZE];
bool bufCleared = false;

void IRAM_ATTR handlePlaybackPress() {
  int pressTime = millis();
  if(pressTime - playbackPressTime > DEBOUNCE_TIME){
    playbackPressTime = pressTime;
    playbackPressed += 1;
    switch(STATE){
      case PROCESS:
        nextSTATE = HOLD;
        break;
      case HOLD:
        nextSTATE = PROCESS;
        break;
    }
  }
}

void IRAM_ATTR handleSkipPress() {
  int pressTime = millis();
  if(pressTime - skipPressTime > DEBOUNCE_TIME){
    skipPressTime = pressTime;
    skipPressed += 1;
    nextSTATE = SKIP;
  }
}

//void setupI2S() {
//  i2s_config_t i2s_config = {
//      .mode = I2S_MODE_MASTER | I2S_MODE_RX,
//      .sample_rate = SAMPLE_RATE,
//      .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
//      .channel_format = I2S_CHANNEL_FMT_ONLY_RIGHT,
//      .communication_format = I2S_COMM_FORMAT_I2S_MSB,
//      .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
//      .dma_buf_count = I2S_DMA_BUF_COUNT,
//      .dma_buf_len = I2S_DMA_BUF_LEN,
//  };
//
//  i2s_pin_config_t pin_config = {
//      .bck_io_num = 26,  // bit-clock line, need dedicated GPIO pin for this
//      .ws_io_num = 25,   // word-select, left or right audio channels
//      .data_out_num = -1, //OUTPUT pin -- leave null for testing at the moment
//      .data_in_num = AUDIOIN_PIN //INPUT pin
//  };
//
//  i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
//  i2s_set_pin(I2S_NUM_0, &pin_config);
// }

void setup() {
    pinMode(PLAYBACK_PIN, INPUT_PULLUP);
    pinMode(SKIP_PIN, INPUT_PULLUP);
    pinMode(INPUT_WAVE, INPUT);
    pinMode(OUTPUT_WAVE, OUTPUT);
    attachInterrupt(digitalPinToInterrupt(PLAYBACK_PIN), handlePlaybackPress, FALLING);
    attachInterrupt(digitalPinToInterrupt(SKIP_PIN), handleSkipPress, FALLING);
//    setupI2S();
    Serial.begin(115200);
}
 
void loop() {
//    analogWrite(OUTPUT_WAVE, analogRead(INPUT_WAVE);
  int inputValue = analogRead(INPUT_WAVE);  // Read the value between 0-1023
 
  // Map the input value to PWM range (0-255)
  // This assumes your AC signal is biased to be within 0-5V.
//  int pwmValue = map(inputVxalue, 0, 1023, 0, 255);  // Map to 8-bit range for PWM
 
  // Output the PWM signal on pin 8
  analogWrite(OUTPUT_WAVE, inputValue);
//  STATE = nextSTATE;
//  int tempoPot = (int32_t(analogRead(TEMPO_PIN)) >> 2) - 3;
//  Serial.print("Playback " + String((int)playbackPressed)+ "\n");
//  Serial.print("Skip " + String((int)skipPressed)+ "\n");
//  Serial.print("State: " + String((int)STATE)+ "\n");
//  Serial.print("Tempo " + String((int)tempoPot)+ "\n");
//  switch(STATE){
//    case PROCESS:
//      //process audio input and forward over I2S
//      //receive audio data from SPI and send to audio out
//      bufCleared = false;
//      break;
//    
//    case HOLD:
//      //do nothing
//      break;
//
//    case SKIP:
//      //clear buffer
//      bufCleared = true;
//      nextSTATE = PROCESS;
//      break;
//  }
//  
//  delay(1000);
}
