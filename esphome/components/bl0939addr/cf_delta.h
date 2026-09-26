#pragma once
#include <stdint.h>
#include <stdlib.h>

namespace esphome {
namespace bl0939 {

// BL0939 CFA_CNT/CFB_CNT are 24-bit unsigned pulse counters that count
// algebraically (positive power adds, negative power subtracts) and wrap at 2^24.
// Returns the signed pulse delta between two consecutive readings.
// A |delta| above max_delta cannot happen in one interval, so it means the chip
// reset its counter (brownout): it restarted from 0 and `now` itself is the delta.
// ponytail: reset vs wrap told apart by plausibility only; ambiguous when prev is
// within max_delta of 2^24, error bounded by max_delta pulses.
inline int32_t cf_delta(uint32_t prev, uint32_t now, int32_t max_delta) {
  int32_t d = (int32_t) ((now - prev) << 8) >> 8;  // sign-extend 24-bit difference
  if (abs(d) > max_delta)
    d = (int32_t) (now << 8) >> 8;
  return d;
}

}  // namespace bl0939
}  // namespace esphome
