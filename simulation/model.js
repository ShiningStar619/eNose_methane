/**
 * Browser-side physics for the eNose auto sequence.
 * Relay map matches program/gui.py AUTO_OPERATION_STEPS.
 * Works in the browser (global EnoseModel) and in Node (module.exports).
 */
(function (root, factory) {
  "use strict";
  const api = factory();
  if (typeof module === "object" && module.exports) {
    module.exports = api;
  }
  root.EnoseModel = api;
})(typeof globalThis !== "undefined" ? globalThis : this, function () {
  "use strict";

  const DEVICES = [
    { key: "s_valve1", label: "Valve 1" },
    { key: "s_valve2", label: "Valve 2" },
    { key: "s_valve3", label: "Valve 3" },
    { key: "s_valve4", label: "Valve 4" },
    { key: "pump", label: "Pump" },
    { key: "fan", label: "Fan" },
    { key: "heater", label: "Heater" },
  ];

  const STEPS = [
    {
      opKey: "heating",
      title: "Op1: Heating",
      durationKey: "heating",
      on: ["heater"],
      off: ["s_valve1", "s_valve2", "s_valve3", "s_valve4", "pump", "fan"],
    },
    {
      opKey: "baseline",
      title: "Op2: Baseline",
      durationKey: "baseline",
      on: ["s_valve2", "s_valve3", "pump"],
      off: ["s_valve1", "s_valve4"],
      startCollection: true,
    },
    {
      opKey: "vacuum",
      title: "Op3: Vacuum",
      durationKey: "vacuum",
      on: ["s_valve3", "pump"],
      off: ["s_valve1", "s_valve2", "s_valve4"],
    },
    {
      opKey: "mix_air",
      title: "Op4: Mix Air",
      durationKey: "mix_air",
      on: ["fan"],
      off: ["s_valve1", "s_valve2", "s_valve3", "s_valve4", "pump"],
    },
    {
      opKey: "measure",
      title: "Op5: Measure",
      durationKey: "measure",
      on: ["s_valve1", "s_valve4", "pump"],
      off: ["fan", "s_valve2", "s_valve3"],
    },
    {
      opKey: "vacuum_return",
      title: "Op6: Vacuum Return",
      durationKey: "vacuum_return",
      on: ["s_valve4", "pump"],
      off: ["s_valve1", "s_valve2", "s_valve3"],
    },
    {
      opKey: "recovery",
      title: "Op7: Recovery",
      durationKey: "recovery",
      on: ["s_valve2", "s_valve3"],
      off: ["s_valve1", "s_valve4"],
    },
  ];

  const RECORDING_OPS = {
    baseline: true,
    vacuum: true,
    mix_air: true,
    measure: true,
    vacuum_return: true,
    recovery: true,
  };

  const DEFAULT_DURATIONS = {
    heating: 2,
    baseline: 2,
    vacuum: 1,
    mix_air: 1,
    measure: 3,
    vacuum_return: 1,
    recovery: 2,
    break_time: 1,
  };

  const SENSOR_BASE = [1.62, 1.4, 1.85, 1.51];
  const SENSOR_GAINS = [0.0035, 0.0025, 0.011, 0.009];
  const RESPONSE_TAU = 0.28;
  const MAX_SAMPLES = 4000;

  function deviceMap(value) {
    const devices = {};
    for (let i = 0; i < DEVICES.length; i += 1) {
      devices[DEVICES[i].key] = value;
    }
    return devices;
  }

  function samplePathOpen(devices) {
    return Boolean(
      devices.s_valve1 &&
        devices.s_valve4 &&
        devices.pump &&
        !devices.s_valve2 &&
        !devices.s_valve3 &&
        !devices.fan
    );
  }

  function channelNoise(clock, index) {
    return (
      Math.sin(clock * 7.1 + index * 1.3) * 0.003 +
      Math.sin(clock * 12.7 + index * 0.7) * 0.0015
    );
  }

  function createSimulator() {
    const sim = {
      devices: deviceMap(false),
      response: 0,
      heaterSeconds: 0,
      samplePpm: 12,
      clock: 0,
      recordClock: 0,
      recording: false,
      op: null,
      samples: [],
      live: null,
    };

    function sense(dt) {
      if (sim.devices.heater) {
        sim.heaterSeconds += dt;
      } else {
        sim.heaterSeconds = Math.max(0, sim.heaterSeconds - dt * 2);
      }
      const target = samplePathOpen(sim.devices) ? 1 : 0;
      const alpha = 1 - Math.exp(-dt / RESPONSE_TAU);
      sim.response += (target - sim.response) * alpha;
      const drift = Math.min(sim.heaterSeconds, 30) * 0.0002;
      const volts = SENSOR_BASE.map(function (base, index) {
        return (
          base +
          SENSOR_GAINS[index] * sim.samplePpm * sim.response +
          drift +
          channelNoise(sim.clock, index)
        );
      });
      const temp =
        27.4 +
        Math.min(sim.heaterSeconds, 40) * 0.12 +
        Math.sin(sim.clock) * 0.05;
      const rh =
        63 -
        Math.min(sim.heaterSeconds, 40) * 0.08 +
        Math.sin(sim.clock * 0.7) * 0.1;
      const pressure =
        1012.8 +
        (sim.devices.pump ? -0.35 : 0) +
        Math.sin(sim.clock * 0.5) * 0.05;
      sim.live = {
        s1: volts[0],
        s2: volts[1],
        s3: volts[2],
        s4: volts[3],
        temp: temp,
        rh: rh,
        pressure: pressure,
      };
      return sim.live;
    }

    function tick(dt) {
      sim.clock += dt;
      const live = sense(dt);
      if (sim.recording) {
        sim.recordClock += dt;
        sim.samples.push({
          t: sim.recordClock,
          op: sim.op,
          s1: live.s1,
          s2: live.s2,
          s3: live.s3,
          s4: live.s4,
          temp: live.temp,
          rh: live.rh,
          pressure: live.pressure,
        });
        if (sim.samples.length > MAX_SAMPLES) {
          sim.samples.splice(0, sim.samples.length - MAX_SAMPLES);
        }
      }
      return live;
    }

    function applyStep(step) {
      const off = step.off || [];
      const on = step.on || [];
      for (let i = 0; i < off.length; i += 1) {
        if (Object.prototype.hasOwnProperty.call(sim.devices, off[i])) {
          sim.devices[off[i]] = false;
        }
      }
      for (let j = 0; j < on.length; j += 1) {
        if (Object.prototype.hasOwnProperty.call(sim.devices, on[j])) {
          sim.devices[on[j]] = true;
        }
      }
    }

    function preserveHeaterOnly() {
      const keep = sim.devices.heater;
      sim.devices = deviceMap(false);
      sim.devices.heater = keep;
    }

    function toggle(key) {
      if (!Object.prototype.hasOwnProperty.call(sim.devices, key)) {
        return false;
      }
      sim.devices[key] = !sim.devices[key];
      return sim.devices[key];
    }

    function startRecording(op) {
      sim.samples = [];
      sim.recordClock = 0;
      sim.recording = true;
      sim.op = op;
    }

    function stopRecording() {
      sim.recording = false;
    }

    function setOp(op) {
      sim.op = op;
    }

    function setSamplePpm(ppm) {
      sim.samplePpm = ppm;
    }

    function resetDynamics() {
      sim.response = 0;
      sim.heaterSeconds = 0;
      sim.clock = 0;
    }

    function estimate() {
      return estimatePpm(sim.samples);
    }

    sense(0);

    return {
      tick: tick,
      applyStep: applyStep,
      preserveHeaterOnly: preserveHeaterOnly,
      toggle: toggle,
      startRecording: startRecording,
      stopRecording: stopRecording,
      setOp: setOp,
      setSamplePpm: setSamplePpm,
      resetDynamics: resetDynamics,
      estimate: estimate,
      deviceCopy: function () {
        const copy = {};
        for (let i = 0; i < DEVICES.length; i += 1) {
          const key = DEVICES[i].key;
          copy[key] = sim.devices[key];
        }
        return copy;
      },
      liveReading: function () {
        return sim.live;
      },
      sampleList: function () {
        return sim.samples;
      },
    };
  }

  function average(rows, key) {
    let sum = 0;
    for (let i = 0; i < rows.length; i += 1) {
      sum += rows[i][key];
    }
    return sum / rows.length;
  }

  function secondHalf(rows) {
    if (rows.length < 2) {
      return rows;
    }
    return rows.slice(Math.floor(rows.length / 2));
  }

  function estimatePpm(samples) {
    const baseline = secondHalf(
      samples.filter(function (row) {
        return row.op === "baseline";
      })
    );
    const measure = secondHalf(
      samples.filter(function (row) {
        return row.op === "measure";
      })
    );
    if (!baseline.length || !measure.length) {
      return null;
    }
    const d3 = average(measure, "s3") - average(baseline, "s3");
    const d4 = average(measure, "s4") - average(baseline, "s4");
    const ppm = (d3 / SENSOR_GAINS[2] + d4 / SENSOR_GAINS[3]) / 2;
    if (!Number.isFinite(ppm)) {
      return null;
    }
    return Math.max(0, ppm);
  }

  function createSession() {
    const sim = createSimulator();
    const state = {
      mode: "auto",
      running: false,
      runKind: null,
      queue: [],
      phase: null,
      cycle: 0,
      progress: "Ready to start",
      status: "Status: Ready",
      statusColor: "#27ae60",
      timer: 0,
      ppm: null,
      activeOp: null,
      done: {},
      bypassed: {},
      chartTitle: "ยังไม่มีข้อมูลรอบวัด",
    };

    function clearMarks() {
      state.done = {};
      state.bypassed = {};
      state.activeOp = null;
    }

    function shouldRecord(step, durations, started) {
      if (started) {
        return false;
      }
      if ((durations[step.durationKey] || 0) <= 0) {
        return false;
      }
      if (step.startCollection) {
        return true;
      }
      if ((durations.baseline || 0) <= 0 && RECORDING_OPS[step.opKey]) {
        return true;
      }
      return false;
    }

    function buildQueue(durations, loopCount) {
      const queue = [];
      let recordingStarted = false;
      for (let cycle = 1; cycle <= loopCount; cycle += 1) {
        for (let i = 0; i < STEPS.length; i += 1) {
          const step = STEPS[i];
          const duration = durations[step.durationKey] || 0;
          const startCollection = shouldRecord(step, durations, recordingStarted);
          if (startCollection && duration > 0) {
            recordingStarted = true;
          }
          queue.push({
            kind: "step",
            step: step,
            duration: duration,
            cycle: cycle,
            startCollection: startCollection,
          });
        }
        queue.push({ kind: "finish-cycle", cycle: cycle });
        if (cycle < loopCount && (durations.break_time || 0) > 0) {
          queue.push({
            kind: "break",
            duration: durations.break_time,
            cycle: cycle,
          });
        }
        recordingStarted = false;
      }
      return queue;
    }

    function beginPhase(item) {
      if (item.kind === "step") {
        if (item.duration <= 0) {
          state.bypassed[item.step.opKey] = true;
          state.progress = item.step.title + " bypassed";
          return null;
        }
        state.cycle = item.cycle;
        sim.applyStep(item.step);
        if (item.startCollection) {
          sim.startRecording(item.step.opKey);
          state.chartTitle = "ADC Process Data — cycle " + item.cycle + " (simulated)";
        } else if (sim.sampleList() && state.runKind === "auto") {
          sim.setOp(item.step.opKey);
        }
        state.activeOp = item.step.opKey;
        state.progress = item.step.title;
        state.status =
          "Cycle " + item.cycle + " | " + item.step.title + " - " + Math.ceil(item.duration) + "s remaining";
        state.statusColor = "#f39c12";
        return {
          kind: "step",
          opKey: item.step.opKey,
          remaining: item.duration,
          cycle: item.cycle,
          title: item.step.title,
        };
      }
      if (item.kind === "break") {
        sim.stopRecording();
        sim.preserveHeaterOnly();
        state.activeOp = "break_time";
        state.progress = "Break";
        state.status = "Break Time - Next cycle in " + Math.ceil(item.duration) + "s";
        state.statusColor = "#e74c3c";
        return {
          kind: "break",
          opKey: "break_time",
          remaining: item.duration,
          cycle: item.cycle,
          title: "Break",
        };
      }
      finishCycle(item.cycle);
      return null;
    }

    function finishCycle(cycle) {
      sim.stopRecording();
      const ppm = sim.estimate();
      state.ppm = ppm;
      sim.preserveHeaterOnly();
      state.activeOp = null;
      state.cycle = cycle;
      state.chartTitle = "ADC Process Data — cycle " + cycle + " (simulated)";
      state.progress = "Sequence Complete!";
      state.status = "Cycle " + cycle + " | Data processed!";
      state.statusColor = "#27ae60";
      state.timer = 0;
    }

    function finishRun() {
      state.running = false;
      state.runKind = null;
      state.phase = null;
      state.queue = [];
      state.activeOp = null;
      state.timer = 0;
      state.progress = "Sequence Complete!";
      state.status = "Status: All operations completed!";
      state.statusColor = "#27ae60";
    }

    function startAuto(options) {
      if (state.running) {
        return false;
      }
      const durations = options.durations;
      const loopCount = options.loopCount;
      sim.setSamplePpm(options.samplePpm);
      sim.resetDynamics();
      sim.stopRecording();
      clearMarks();
      state.ppm = null;
      state.cycle = 0;
      state.mode = "auto";
      state.running = true;
      state.runKind = "auto";
      state.queue = buildQueue(durations, loopCount);
      state.phase = null;
      state.progress = "Starting";
      state.status = "Status: Running";
      state.statusColor = "#3498db";
      state.chartTitle = "กำลังเก็บสัญญาณจำลอง";
      return true;
    }

    function startManual(options) {
      if (state.running) {
        return false;
      }
      const seconds = options.seconds;
      sim.setSamplePpm(options.samplePpm);
      sim.startRecording("manual");
      clearMarks();
      state.ppm = null;
      state.mode = "manual";
      state.running = true;
      state.runKind = "manual";
      state.queue = [];
      state.cycle = 1;
      state.phase = {
        kind: "manual",
        opKey: "manual",
        remaining: seconds,
        cycle: 1,
        title: "Manual collection",
      };
      state.progress = "Manual collection";
      state.status = "Status: Recording " + Math.ceil(seconds) + "s";
      state.statusColor = "#3498db";
      state.chartTitle = "Manual collection (simulated)";
      state.timer = seconds;
      return true;
    }

    function stop() {
      const wasRunning = state.running;
      state.running = false;
      state.runKind = null;
      state.phase = null;
      state.queue = [];
      state.activeOp = null;
      sim.stopRecording();
      sim.preserveHeaterOnly();
      state.progress = "Stopped";
      state.status = wasRunning ? "Status: Stopped" : "Status: Stopped";
      state.statusColor = "#e74c3c";
      state.timer = 0;
    }

    function setMode(mode) {
      if (mode !== "manual" && mode !== "auto") {
        return false;
      }
      if (state.running) {
        state.status = "Status: กรุณาหยุดการทำงานก่อนเปลี่ยนโหมด";
        state.statusColor = "#f39c12";
        return false;
      }
      state.mode = mode;
      state.progress = "Ready to start";
      state.status =
        mode === "manual"
          ? "Status: Manual — กดปุ่มอุปกรณ์ แล้วกด Start Collection"
          : "Status: Auto — กด Start เพื่อรันลำดับ 7 ขั้น";
      state.statusColor = "#27ae60";
      return true;
    }

    function toggleDevice(key) {
      if (state.running && state.runKind === "auto") {
        state.status = "Status: ไม่สามารถสั่ง Manual ระหว่าง Auto Sequence";
        state.statusColor = "#f39c12";
        return false;
      }
      const on = sim.toggle(key);
      if (!state.running) {
        const label = deviceLabel(key);
        state.status = "Status: " + label + (on ? " ON" : " OFF");
        state.statusColor = on ? "#27ae60" : "#7f8c8d";
      }
      return true;
    }

    function deviceLabel(key) {
      for (let i = 0; i < DEVICES.length; i += 1) {
        if (DEVICES[i].key === key) {
          return DEVICES[i].label;
        }
      }
      return key;
    }

    function completePhase(phase) {
      if (phase.kind === "step" && phase.opKey) {
        state.done[phase.opKey] = true;
      }
      if (phase.kind === "manual") {
        sim.stopRecording();
        state.running = false;
        state.runKind = null;
        state.phase = null;
        state.progress = "Collection complete";
        state.status = "Status: บันทึกสัญญาณมือแล้ว";
        state.statusColor = "#27ae60";
        state.timer = 0;
        state.chartTitle = "Manual collection (simulated)";
        return;
      }
      state.phase = null;
    }

    function tick(dt) {
      if (!state.running) {
        sim.tick(dt);
        return snapshot();
      }
      let left = dt;
      while (state.running && left > 0) {
        if (!state.phase) {
          const next = state.queue.shift();
          if (!next) {
            finishRun();
            break;
          }
          if (next.kind === "finish-cycle") {
            const more = state.queue.length > 0;
            finishCycle(next.cycle);
            if (!more) {
              finishRun();
            }
            continue;
          }
          const phase = beginPhase(next);
          if (!phase) {
            continue;
          }
          state.phase = phase;
        }
        const use = Math.min(left, state.phase.remaining);
        if (state.phase.kind === "step") {
          sim.setOp(state.phase.opKey);
        }
        sim.tick(use);
        state.phase.remaining -= use;
        left -= use;
        state.timer = Math.max(0, state.phase.remaining);
        const remain = Math.ceil(state.phase.remaining);
        if (state.phase.kind === "break") {
          state.status = "Break Time - Next cycle in " + remain + "s";
        } else if (state.phase.kind === "manual") {
          state.status = "Status: Recording " + remain + "s";
        } else {
          state.status =
            "Cycle " +
            state.phase.cycle +
            " | " +
            state.phase.title +
            " - " +
            remain +
            "s remaining";
        }
        if (state.phase.remaining <= 1e-6) {
          completePhase(state.phase);
        }
      }
      if (!state.running) {
        sim.tick(0);
      }
      return snapshot();
    }

    function snapshot() {
      const live = sim.liveReading();
      return {
        mode: state.mode,
        running: state.running,
        runKind: state.runKind,
        cycle: state.cycle,
        progress: state.progress,
        status: state.status,
        statusColor: state.statusColor,
        timer: state.timer,
        ppm: state.ppm,
        ppmText: state.ppm == null ? "----" : state.ppm.toFixed(1),
        activeOp: state.activeOp,
        done: state.done,
        bypassed: state.bypassed,
        chartTitle: state.chartTitle,
        devices: sim.deviceCopy(),
        live: live,
        samples: sim.sampleList(),
      };
    }

    sim.tick(0);

    return {
      tick: tick,
      snapshot: snapshot,
      startAuto: startAuto,
      startManual: startManual,
      stop: stop,
      setMode: setMode,
      toggleDevice: toggleDevice,
      setIdleSample: function (ppm) {
        if (!state.running) {
          sim.setSamplePpm(ppm);
        }
      },
    };
  }

  function runVirtualCycle(samplePpm, durations) {
    const session = createSession();
    session.startAuto({
      samplePpm: samplePpm,
      durations: durations || DEFAULT_DURATIONS,
      loopCount: 1,
    });
    let guard = 0;
    while (session.snapshot().running && guard < 100000) {
      session.tick(0.1);
      guard += 1;
    }
    return session.snapshot();
  }

  return {
    DEVICES: DEVICES,
    STEPS: STEPS,
    DEFAULT_DURATIONS: DEFAULT_DURATIONS,
    createSimulator: createSimulator,
    createSession: createSession,
    estimatePpm: estimatePpm,
    runVirtualCycle: runVirtualCycle,
    samplePathOpen: samplePathOpen,
  };
});
