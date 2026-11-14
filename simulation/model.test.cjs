"use strict";

const assert = require("assert");
const {
  DEFAULT_DURATIONS,
  createSession,
  runVirtualCycle,
} = require("./model.js");

function near(actual, expected, tolerance, label) {
  assert.ok(
    Math.abs(actual - expected) <= tolerance,
    label + " expected " + expected + " ± " + tolerance + ", got " + actual
  );
}

const air = runVirtualCycle(0, DEFAULT_DURATIONS);
assert.strictEqual(typeof air.ppm, "number");
near(air.ppm, 0, 0.6, "clean air");

const mid = runVirtualCycle(12, DEFAULT_DURATIONS);
near(mid.ppm, 12, 1.5, "12 ppm");
assert.ok(mid.samples.some((row) => row.op === "baseline"));
assert.ok(mid.samples.some((row) => row.op === "measure"));

const high = runVirtualCycle(25, DEFAULT_DURATIONS);
near(high.ppm, 25, 2, "25 ppm");

const session = createSession();
session.startAuto({
  samplePpm: 12,
  durations: DEFAULT_DURATIONS,
  loopCount: 1,
});
let elapsed = 0;
while (elapsed < 6.3) {
  session.tick(0.1);
  elapsed += 0.1;
}
const duringMeasure = session.snapshot();
assert.strictEqual(duringMeasure.devices.heater, true);
assert.strictEqual(duringMeasure.devices.s_valve1, true);
assert.strictEqual(duringMeasure.devices.s_valve4, true);
assert.strictEqual(duringMeasure.devices.pump, true);
assert.strictEqual(duringMeasure.devices.fan, false);
session.stop();
const stopped = session.snapshot();
assert.strictEqual(stopped.running, false);
assert.strictEqual(stopped.devices.heater, true);
assert.strictEqual(stopped.devices.pump, false);
assert.strictEqual(stopped.devices.s_valve1, false);

const blocked = createSession();
blocked.startAuto({
  samplePpm: 5,
  durations: DEFAULT_DURATIONS,
  loopCount: 1,
});
assert.strictEqual(blocked.setMode("manual"), false);
assert.strictEqual(blocked.toggleDevice("fan"), false);
blocked.stop();

console.log(
  "model ok",
  "air=" + air.ppm.toFixed(2),
  "mid=" + mid.ppm.toFixed(2),
  "high=" + high.ppm.toFixed(2)
);
