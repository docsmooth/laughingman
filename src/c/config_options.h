#ifndef CONFIG_OPTIONS_H
#define CONFIG_OPTIONS_H

#include <pebble.h>
#include "../../resources/generated_config.h"

// These keys are used to communicate with Javascript.  They are
// assigned by the SDK from the messageKeys list in package.json.in.
#define CK_battery_gauge MESSAGE_KEY_battery_gauge
#define CK_bluetooth_indicator MESSAGE_KEY_bluetooth_indicator
#define CK_second_hand MESSAGE_KEY_second_hand
#define CK_hour_buzzer MESSAGE_KEY_hour_buzzer
#define CK_draw_mode MESSAGE_KEY_draw_mode
#define CK_chrono_dial MESSAGE_KEY_chrono_dial
#define CK_sweep_seconds MESSAGE_KEY_sweep_seconds
#define CK_display_lang MESSAGE_KEY_display_lang
#define CK_face_index MESSAGE_KEY_face_index
#define CK_date_window_a MESSAGE_KEY_date_window_a
#define CK_date_window_b MESSAGE_KEY_date_window_b
#define CK_date_window_c MESSAGE_KEY_date_window_c
#define CK_date_window_d MESSAGE_KEY_date_window_d
#define CK_bluetooth_buzzer MESSAGE_KEY_bluetooth_buzzer
#define CK_lunar_background MESSAGE_KEY_lunar_background
#define CK_lunar_direction MESSAGE_KEY_lunar_direction

typedef enum {
  IM_off = 0,
  IM_when_needed = 1,
  IM_always = 2,
  IM_digital = 3,
} IndicatorMode;

typedef enum {
  CDM_off = 0,
  CDM_tenths = 1,
  CDM_hours = 2,
  CDM_dual = 3,
} ChronoDialMode;

typedef enum {
  DWM_off = 0,

  // Uses date_numeric_font.
  DWM_identify = 1,
  DWM_date = 2,
  DWM_year = 3,

  // Uses date_lang_font.
  DWM_weekday = 4,
  DWM_month = 5,
  DWM_ampm = 6,
  
  // Special case.
  DWM_moon = 7,
} DateWindowMode;

typedef struct {
  IndicatorMode battery_gauge;
  IndicatorMode bluetooth_indicator;
  bool second_hand;
  bool hour_buzzer;
  bool bluetooth_buzzer;
  unsigned char draw_mode;
  ChronoDialMode chrono_dial;
  bool sweep_seconds;
  unsigned char display_lang;
  unsigned char face_index;
  DateWindowMode date_windows[NUM_DATE_WINDOWS];
  bool lunar_background;   // true for always-black background.
  bool lunar_direction;    // true for southern hemisphere (left-to-right).
} __attribute__((__packed__)) ConfigOptions;

extern ConfigOptions config;

void init_default_options();
void save_config();
void load_config();

void dropped_config_handler(AppMessageResult reason, void *context);
void receive_config_handler(DictionaryIterator *received, void *context);

void apply_config();  // implemented in the main program

#endif  // CONFIG_OPTIONS_H
