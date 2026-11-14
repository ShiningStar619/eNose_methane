(function () {
  "use strict";

  const model = globalThis.EnoseModel;
  const session = model.createSession();
  const CHIP_COLORS = {
    heating: "#fff59d",
    baseline: "#81d4fa",
    vacuum: "#b39ddb",
    mix_air: "#a5d6a7",
    measure: "#ffcc80",
    vacuum_return: "#f48fb1",
    recovery: "#80cbc4",
  };
  const SENSOR_KEYS = ["s1", "s2", "s3", "s4"];
  const SENSOR_COLORS = ["#e67e22", "#2980b9", "#27ae60", "#8e44ad"];

  const devicesEl = document.getElementById("devices");
  const chipsEl = document.getElementById("op-chips");
  const durationEl = document.getElementById("duration-fields");
  const liveSensors = document.getElementById("live-sensors");
  const liveEnv = document.getElementById("live-env");

  model.DEVICES.forEach(function (device) {
    const button = document.createElement("button");
    button.type = "button";
    button.dataset.device = device.key;
    button.textContent = device.label;
    button.addEventListener("click", function () {
      session.toggleDevice(device.key);
      render(session.snapshot());
    });
    devicesEl.appendChild(button);
  });

  model.STEPS.forEach(function (step) {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.dataset.op = step.opKey;
    chip.textContent = step.title.replace("Op", "");
    chip.disabled = true;
    chip.style.background = CHIP_COLORS[step.opKey];
    chipsEl.appendChild(chip);
  });

  const durationLabels = {
    heating: "Heating (s)",
    baseline: "Baseline (s)",
    vacuum: "Vacuum (s)",
    mix_air: "Mix Air (s)",
    measure: "Measure (s)",
    vacuum_return: "Vacuum Return (s)",
    recovery: "Recovery (s)",
    break_time: "Break (s)",
  };

  Object.keys(model.DEFAULT_DURATIONS).forEach(function (key) {
    const label = document.createElement("label");
    label.textContent = durationLabels[key] || key;
    const input = document.createElement("input");
    input.id = "dur-" + key;
    input.type = "number";
    input.min = "0";
    input.max = "90";
    input.step = "1";
    input.value = String(model.DEFAULT_DURATIONS[key]);
    label.appendChild(input);
    durationEl.appendChild(label);
  });

  ["sensor_1", "sensor_2", "sensor_3", "sensor_4"].forEach(function (name, index) {
    const box = document.createElement("div");
    const title = document.createElement("span");
    title.textContent = name;
    const value = document.createElement("strong");
    value.id = "live-" + SENSOR_KEYS[index];
    value.textContent = "—";
    box.appendChild(title);
    box.appendChild(value);
    liveSensors.appendChild(box);
  });

  [
    ["temp", "อุณหภูมิ °C"],
    ["rh", "ความชื้น %"],
    ["pressure", "ความดัน hPa"],
  ].forEach(function (pair) {
    const box = document.createElement("div");
    const title = document.createElement("span");
    title.textContent = pair[1];
    const value = document.createElement("strong");
    value.id = "live-" + pair[0];
    value.textContent = "—";
    box.appendChild(title);
    box.appendChild(value);
    liveEnv.appendChild(box);
  });

  function clampInt(raw, min, max, fallback) {
    const n = Number.parseInt(String(raw), 10);
    if (!Number.isFinite(n)) {
      return fallback;
    }
    return Math.min(max, Math.max(min, n));
  }

  function readDurations() {
    const durations = {};
    Object.keys(model.DEFAULT_DURATIONS).forEach(function (key) {
      const input = document.getElementById("dur-" + key);
      const value = clampInt(input.value, 0, 90, model.DEFAULT_DURATIONS[key]);
      input.value = String(value);
      durations[key] = value;
    });
    return durations;
  }

  function readSample() {
    const allowed = { 0: true, 5: true, 12: true, 25: true };
    const value = Number(document.getElementById("sample-ppm").value);
    return allowed[value] ? value : 12;
  }

  function readLoop() {
    const input = document.getElementById("loop-count");
    const value = clampInt(input.value, 1, 3, 1);
    input.value = String(value);
    return value;
  }

  function readManualSeconds() {
    const input = document.getElementById("manual-seconds");
    const value = clampInt(input.value, 1, 30, 8);
    input.value = String(value);
    return value;
  }

  function showPage(page) {
    ["control", "display", "settings"].forEach(function (name) {
      const section = document.getElementById("page-" + name);
      const tab = document.getElementById("tab-" + name);
      const on = name === page;
      section.hidden = !on;
      tab.setAttribute("aria-selected", on ? "true" : "false");
    });
    if (page === "display") {
      window.requestAnimationFrame(function () {
        drawChart(session.snapshot().samples);
      });
    }
  }

  document.querySelectorAll(".nav button").forEach(function (button) {
    button.addEventListener("click", function () {
      showPage(button.dataset.page);
    });
  });

  document.getElementById("mode-manual").addEventListener("click", function () {
    session.setMode("manual");
    render(session.snapshot());
  });
  document.getElementById("mode-auto").addEventListener("click", function () {
    session.setMode("auto");
    render(session.snapshot());
  });

  document.getElementById("start-btn").addEventListener("click", function () {
    const sample = readSample();
    const snap = session.snapshot();
    if (snap.mode === "manual") {
      session.startManual({ samplePpm: sample, seconds: readManualSeconds() });
    } else {
      session.startAuto({
        samplePpm: sample,
        durations: readDurations(),
        loopCount: readLoop(),
      });
    }
    render(session.snapshot());
  });

  document.getElementById("stop-btn").addEventListener("click", function () {
    session.stop();
    render(session.snapshot());
  });

  document.getElementById("sample-ppm").addEventListener("change", function () {
    session.setIdleSample(readSample());
  });

  function formatClock(seconds) {
    const whole = Math.max(0, Math.ceil(seconds));
    const mins = Math.floor(whole / 60);
    const secs = whole % 60;
    const pad = secs < 10 ? "0" : "";
    return String(mins).padStart(2, "0") + ":" + pad + String(secs);
  }

  function render(snap) {
    document.getElementById("mode-manual").setAttribute("aria-pressed", snap.mode === "manual" ? "true" : "false");
    document.getElementById("mode-auto").setAttribute("aria-pressed", snap.mode === "auto" ? "true" : "false");
    document.getElementById("mode-hint").textContent =
      snap.mode === "manual"
        ? "กดปุ่มเพื่อควบคุมอุปกรณ์จำลองโดยตรง"
        : "ตั้งค่าเวลาแล้วกด Start เพื่อรันลำดับอัตโนมัติ";
    document.getElementById("manual-timer-row").hidden = snap.mode !== "manual";
    document.getElementById("start-btn").textContent =
      snap.mode === "manual" ? "Start Collection" : "Start Auto Sequence";
    document.getElementById("start-btn").disabled = snap.running;
    document.getElementById("sample-ppm").disabled = snap.running;
    document.getElementById("loop-count").disabled = snap.running;
    document.querySelectorAll("#duration-fields input").forEach(function (input) {
      input.disabled = snap.running;
    });
    document.getElementById("manual-seconds").disabled = snap.running;
    document.getElementById("progress").textContent = snap.progress;
    document.getElementById("timer").textContent = snap.running || snap.timer > 0 ? formatClock(snap.timer) : "--:--";
    document.getElementById("cycle").textContent = "Current Cycle: " + String(snap.cycle);
    const status = document.getElementById("status");
    status.textContent = snap.status;
    status.style.color = snap.statusColor;
    document.getElementById("ppm").textContent = snap.ppmText;
    document.getElementById("display-ppm").textContent = snap.ppmText;
    document.getElementById("ppm-note").textContent =
      snap.ppm == null
        ? "รอรอบ Auto ที่มี Baseline และ Measure"
        : "ค่าประมาณจากส่วนต่างแรงดัน Baseline กับ Measure";
    document.getElementById("chart-title").textContent = snap.chartTitle;

    document.querySelectorAll("#devices button").forEach(function (button) {
      const on = Boolean(snap.devices[button.dataset.device]);
      button.setAttribute("aria-pressed", on ? "true" : "false");
      button.disabled = snap.running && snap.runKind === "auto";
    });

    document.querySelectorAll("#op-chips button").forEach(function (chip) {
      const op = chip.dataset.op;
      if (snap.activeOp === op) {
        chip.style.outline = "3px solid #f39c12";
      } else {
        chip.style.outline = "none";
      }
      if (snap.done[op]) {
        chip.style.background = "#81c784";
      } else if (snap.bypassed[op]) {
        chip.style.background = "#bdbdbd";
      } else {
        chip.style.background = CHIP_COLORS[op];
      }
    });

    const live = snap.live;
    SENSOR_KEYS.forEach(function (key) {
      document.getElementById("live-" + key).textContent = live[key].toFixed(3) + " V";
    });
    document.getElementById("live-temp").textContent = live.temp.toFixed(1);
    document.getElementById("live-rh").textContent = live.rh.toFixed(1);
    document.getElementById("live-pressure").textContent = live.pressure.toFixed(1);

    if (!document.getElementById("page-display").hidden) {
      drawChart(snap.samples);
    }
  }

  function drawChart(samples) {
    const canvas = document.getElementById("chart");
    const rect = canvas.getBoundingClientRect();
    const width = Math.max(320, rect.width || 640);
    const height = 320;
    const dpr = window.devicePixelRatio || 1;
    canvas.width = Math.floor(width * dpr);
    canvas.height = Math.floor(height * dpr);
    const ctx = canvas.getContext("2d");
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = "#ffffff";
    ctx.fillRect(0, 0, width, height);
    if (!samples.length) {
      ctx.fillStyle = "#7f8c8d";
      ctx.font = "15px sans-serif";
      ctx.textAlign = "center";
      ctx.fillText("ยังไม่มีข้อมูลรอบวัด เริ่ม Auto Sequence ที่หน้า Control", width / 2, height / 2);
      return;
    }
    const pad = { l: 52, r: 16, t: 16, b: 36 };
    let ymin = Infinity;
    let ymax = -Infinity;
    let xmax = 0;
    samples.forEach(function (row) {
      xmax = Math.max(xmax, row.t);
      SENSOR_KEYS.forEach(function (key) {
        ymin = Math.min(ymin, row[key]);
        ymax = Math.max(ymax, row[key]);
      });
    });
    const span = Math.max(0.05, ymax - ymin);
    ymin -= span * 0.12;
    ymax += span * 0.12;
    const plotW = width - pad.l - pad.r;
    const plotH = height - pad.t - pad.b;
    ctx.strokeStyle = "#ecf0f1";
    ctx.lineWidth = 1;
    ctx.fillStyle = "#7f8c8d";
    ctx.font = "12px sans-serif";
    ctx.textAlign = "right";
    for (let g = 0; g <= 4; g += 1) {
      const y = pad.t + (plotH * g) / 4;
      ctx.beginPath();
      ctx.moveTo(pad.l, y);
      ctx.lineTo(width - pad.r, y);
      ctx.stroke();
      const voltage = ymax - ((ymax - ymin) * g) / 4;
      ctx.fillText(voltage.toFixed(2), pad.l - 6, y + 4);
    }
    ctx.textAlign = "center";
    ctx.fillText("Time (s)", pad.l + plotW / 2, height - 8);
    ctx.save();
    ctx.translate(14, pad.t + plotH / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.fillText("Voltage (V)", 0, 0);
    ctx.restore();

    function xOf(t) {
      return pad.l + (xmax <= 0 ? 0 : (t / xmax) * plotW);
    }
    function yOf(v) {
      return pad.t + ((ymax - v) / (ymax - ymin)) * plotH;
    }

    SENSOR_KEYS.forEach(function (key, index) {
      ctx.beginPath();
      ctx.strokeStyle = SENSOR_COLORS[index];
      ctx.lineWidth = 2;
      samples.forEach(function (row, rowIndex) {
        const x = xOf(row.t);
        const y = yOf(row[key]);
        if (rowIndex === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
      });
      ctx.stroke();
    });
  }

  window.addEventListener("resize", function () {
    if (!document.getElementById("page-display").hidden) {
      drawChart(session.snapshot().samples);
    }
  });

  session.setMode("auto");
  session.setIdleSample(readSample());
  render(session.snapshot());
  window.setInterval(function () {
    if (!session.snapshot().running) {
      session.setIdleSample(readSample());
    }
    session.tick(0.1);
    render(session.snapshot());
  }, 100);
})();
