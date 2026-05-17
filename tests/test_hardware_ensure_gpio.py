"""Regression: _ensure_gpio_setup must not drive the first GPIO pin (valve1) as a health check."""
import unittest
from unittest import mock

import hardware_control.hardware as hc

_GPIO_BACKUP = object()


def _inject_gpio_mock():
    """On non-Pi, RPi.GPIO is missing so the module has no GPIO name; tests simulate Pi."""
    m = mock.MagicMock()
    m.OUT = 0
    m.IN = 1
    m.HIGH = True
    m.LOW = False
    hc.GPIO = m
    return m


class TestEnsureGpio(unittest.TestCase):
    def setUp(self):
        self._gpio_backup = getattr(hc, "GPIO", _GPIO_BACKUP)

    def tearDown(self):
        if self._gpio_backup is _GPIO_BACKUP:
            hc.__dict__.pop("GPIO", None)
        else:
            hc.GPIO = self._gpio_backup

    @mock.patch.object(hc, "ON_RASPBERRY_PI", True)
    def test_ensure_gpio_uses_gpio_function_not_output(self):
        mock_gpio = _inject_gpio_mock()
        mock_gpio.gpio_function.return_value = mock_gpio.OUT
        ctrl = hc.HardwareController({"s_valve1": 21, "s_valve2": 20})
        ctrl.is_initialized = True
        ctrl._ensure_gpio_setup()
        mock_gpio.output.assert_not_called()
        mock_gpio.gpio_function.assert_called_once_with(21)

    @mock.patch.object(hc, "ON_RASPBERRY_PI", True)
    def test_control_valve2_only_outputs_valve2_pin(self):
        mock_gpio = _inject_gpio_mock()
        mock_gpio.gpio_function.return_value = mock_gpio.OUT
        ctrl = hc.HardwareController({"s_valve1": 21, "s_valve2": 20})
        ctrl.is_initialized = True
        ctrl.control_device("s_valve2", True)
        for call in mock_gpio.output.call_args_list:
            pin, level = call[0]
            self.assertEqual(pin, 20)
            self.assertEqual(level, mock_gpio.HIGH)


if __name__ == "__main__":
    unittest.main()
