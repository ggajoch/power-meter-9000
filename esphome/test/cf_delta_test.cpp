// Host-side check of the BL0939 CF_CNT delta logic (wrap, export, chip reset).
// Run from esphome/:  g++ -std=c++11 -Icomponents/bl0939addr test/cf_delta_test.cpp -o /tmp/cf_delta_test && /tmp/cf_delta_test
#include "cf_delta.h"
#include <cassert>
#include <cstdio>

using esphome::bl0939::cf_delta;

int main() {
  const int32_t MAX = 300;                              // max plausible pulses per interval
  assert(cf_delta(100, 150, MAX) == 50);                // consumption
  assert(cf_delta(150, 100, MAX) == -50);               // export (PV): counter goes backwards
  assert(cf_delta(100, 400, MAX) == 300);               // exactly max is still plausible
  assert(cf_delta(0xFFFFF0, 0x000010, MAX) == 32);      // wrap through 2^24 upwards
  assert(cf_delta(0x000010, 0xFFFFF0, MAX) == -32);     // wrap through 2^24 downwards
  assert(cf_delta(0x7FFFF0, 0x800010, MAX) == 32);      // crossing 2^23 (the old signed-read bug) is nothing special
  assert(cf_delta(500000, 20, MAX) == 20);              // chip reset: counter restarted from 0
  assert(cf_delta(500000, 0xFFFFFB, MAX) == -5);        // chip reset while exporting
  assert(cf_delta(123456, 123456, MAX) == 0);           // first packet after boot: baseline, no energy yet
  printf("cf_delta OK\n");
  return 0;
}
